"""
bot.py — Bot Discord THẬT (chạy trong SERVER TEST CỦA BẠN, không phải server BTC).

Đây là bề mặt để quay video 30s: gõ /digest → bot quét tin gần đây trong kênh →
gọi classify.py (OpenAI thật) → trả embed gom task/deadline theo ưu tiên.

⚠️ PHẦN NÀY CẦN BẠN TỰ LÀM (tôi không làm hộ được):
  1. Vào https://discord.com/developers → New Application → tab Bot → Reset Token
     → dán vào .env (DISCORD_BOT_TOKEN). Bật MESSAGE CONTENT INTENT.
  2. Tạo server Discord của riêng bạn (bạn là admin) → mời bot vào bằng OAuth
     (scope: bot + applications.commands).
  3. (Demo authority) Tạo role tên "Lab Coach", lấy Role ID điền vào .env.
  4. Nạp dữ liệu: chạy 1 script post các tin trong k4_messages.csv vào kênh test
     (hoặc paste tay vài tin) để có gì mà /digest.

Chạy: python src/bot.py
"""
import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from classify import classify_batch  # tái dùng đúng lời gọi AI ở classify.py

load_dotenv()
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
COACH_ROLE_ID = int(os.getenv("LAB_COACH_ROLE_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True   # cần MESSAGE CONTENT INTENT (bật ở Developer Portal)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

EMOJI = {"do_now": "🔴", "soon": "🟡", "confirm": "⚪"}
TITLE = {"do_now": "Cần làm ngay", "soon": "Sắp đến hạn", "confirm": "Cần người xác nhận"}


@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot sẵn sàng: {client.user}")


@tree.command(name="digest", description="Gom task & deadline từ các kênh theo ưu tiên")
async def digest(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    # 1) Quét tin gần đây ở mọi kênh text bot đọc được
    msgs = []
    for ch in interaction.guild.text_channels:
        try:
            async for m in ch.history(limit=50):
                if m.author.bot:
                    continue
                # DEMO AUTHORITY (role-only, không vào thước đo golden — xem grill):
                is_coach = any(r.id == COACH_ROLE_ID for r in getattr(m.author, "roles", []))
                msgs.append({"msg_id": str(m.id), "channel": ch.name,
                             "created_at": str(m.created_at)[:16],
                             "content": m.content[:200], "is_coach": is_coach})
        except discord.Forbidden:
            continue

    if not msgs:
        await interaction.followup.send("Không có tin nào để tổng hợp.")
        return

    # 2) LỜI GỌI AI THẬT — phân loại (dùng chung hàm với classify.py)
    preds = classify_batch(msgs)

    # 3) Gom theo nhóm ưu tiên, bỏ 'skip'
    groups = {"do_now": [], "soon": [], "confirm": []}
    for p in preds:
        if p["bucket"] in groups:
            groups[p["bucket"]].append(p)

    embed = discord.Embed(title="📋 Priority Digest",
                          description="Task & deadline gom từ nhiều kênh, xếp theo ưu tiên.")
    for b in ("do_now", "soon", "confirm"):
        if not groups[b]:
            continue
        lines = []
        for p in groups[b]:
            dl = f" · ⏰ {p['deadline']}" if p["deadline"] else ""
            lines.append(f"{EMOJI[b]} {p['reason'][:80]}{dl} · #{p['source_channel']}")
        embed.add_field(name=f"{EMOJI[b]} {TITLE[b]}",
                        value="\n".join(lines)[:1000], inline=False)

    await interaction.followup.send(embed=embed)


if __name__ == "__main__":
    client.run(TOKEN)
