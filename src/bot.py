"""
bot.py — Bot Discord THẬT (chạy trong SERVER TEST CỦA BẠN, không phải server BTC).

Đây là bề mặt để quay video 30s: gõ /digest → bot quét tin gần đây trong kênh →
gọi classify.py (OpenAI thật) → trả embed gom task/deadline theo ưu tiên.

Action row dưới embed (component Discord thật, như mock CP2):
  ✅ Đánh dấu đã xong  → gạch ngang ~~text~~ (vẫn hiện) + ↩️ Hoàn tác
  🙈 Ẩn khỏi digest    → ẩn ngay + ↩️ Hoàn tác + 🚫 Luôn bỏ qua (phiên bot)
  🔍 Xem nguồn/ngữ cảnh → ephemeral kèm LINK nhảy tới tin gốc (jump-to-message)
  🔄 Làm mới           → quét & phân loại lại

⚠️ PHẦN NÀY CẦN BẠN TỰ LÀM (tôi không làm hộ được):
  1. Vào https://discord.com/developers → New Application → tab Bot → Reset Token
     → dán vào .env (DISCORD_BOT_TOKEN). Bật MESSAGE CONTENT INTENT.
  2. Tạo server Discord của riêng bạn (bạn là admin) → mời bot vào bằng OAuth
     (scope: bot + applications.commands).
  3. Nạp dữ liệu: paste tay vài tin (xem CP3-seed-messages.md) vào kênh test
     bằng TÀI KHOẢN NGƯỜI (bot bỏ qua tin do bot đăng) để có gì mà /digest.

Chạy: python src/bot.py
"""
import os
from datetime import date
# Bot live coi "hôm nay" = NGÀY THẬT → digest tính gần/xa hạn đúng thực tế.
# (Phải set TRƯỚC khi import classify vì classify đọc REFERENCE_NOW lúc nạp module.)
os.environ.setdefault("REFERENCE_NOW", date.today().isoformat())

import discord
from discord import app_commands
from dotenv import load_dotenv
from classify import classify_batch  # tái dùng đúng lời gọi AI ở classify.py

load_dotenv()
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
GUILD_ID = os.getenv("GUILD_ID", "").strip()  # có → /digest hiện NGAY ở server đó; không → sync global (chậm ~1h)

intents = discord.Intents.default()
intents.message_content = True   # cần MESSAGE CONTENT INTENT (bật ở Developer Portal)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

EMOJI = {"do_now": "🔴", "soon": "🟡", "confirm": "⚪"}
TITLE = {"do_now": "Cần làm ngay", "soon": "Sắp đến hạn", "confirm": "Cần người xác nhận"}
ORDER = {"do_now": 0, "soon": 1, "confirm": 2}

# Trạng thái nhớ theo phiên (mất khi restart bot; muốn bền hơn thì ghi ra file JSON):
IGNORED = {}   # guild_id -> set(msg_id) bị luật "🚫 luôn bỏ qua"
DONE = {}      # guild_id -> set(msg_id) đã "✅ đánh dấu xong" → lần /digest sau vẫn gạch ngang


def _short(s, n=95):
    s = " ".join((s or "").split())
    return (s[:n - 1] + "…") if len(s) > n else s


@client.event
async def on_ready():
    # In ID mọi server bot đang ở → copy vào GUILD_ID (khỏi cần bật Developer Mode)
    for g in client.guilds:
        print(f"[GUILD] {g.name}  →  GUILD_ID={g.id}")

    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        tree.copy_global_to(guild=guild)        # copy lệnh sang server test
        await tree.sync(guild=guild)            # → hiện NGAY LẬP TỨC (không chờ ~1h)
        print(f"Bot sẵn sàng: {client.user} · /digest đã sync cho guild {GUILD_ID}")
    else:
        await tree.sync()                        # sync global — có thể chậm tới ~1h
        print(f"Bot sẵn sàng: {client.user} · sync GLOBAL (có thể chờ tới 1h). "
              f"Muốn hiện ngay: điền GUILD_ID vào .env")


async def scan_and_classify(guild):
    """Quét kênh → gọi AI → trả list item (đã bỏ 'skip' và các tin bị luật 'luôn bỏ qua')."""
    ignore = IGNORED.get(guild.id, set())
    msgs, msg_objs = [], {}
    for ch in guild.text_channels:
        try:
            async for m in ch.history(limit=50):
                if m.author.bot:
                    continue
                mid = str(m.id)
                if mid in ignore:
                    continue
                msgs.append({"msg_id": mid, "channel": ch.name,
                             "created_at": str(m.created_at)[:16], "content": m.content[:200]})
                msg_objs[mid] = m
        except discord.Forbidden:
            continue
    if not msgs:
        return []

    preds = classify_batch(msgs)   # LỜI GỌI AI THẬT (dùng chung hàm với classify.py)
    done_set = DONE.get(guild.id, set())   # nhớ mục đã đánh dấu xong từ lần trước
    items = []
    for p in preds:
        if p["bucket"] not in ("do_now", "soon", "confirm"):
            continue
        m = msg_objs.get(p["msg_id"])
        task = _short(m.content if m else p.get("reason", "")) or "(không có nội dung)"
        items.append({
            "bucket": p["bucket"], "task": task, "deadline": p.get("deadline", ""),
            "channel": p.get("source_channel") or (m.channel.name if m else ""),
            "jump_url": m.jump_url if m else "", "msg_id": p["msg_id"],
            "done": p["msg_id"] in done_set, "hidden": False,
        })
    items.sort(key=lambda it: ORDER[it["bucket"]])
    return items


class DigestView(discord.ui.View):
    """Embed digest + action row: ✅ đánh dấu xong · 🙈 ẩn · 🔍 xem nguồn · 🔄 làm mới."""

    def __init__(self, items, guild_id):
        super().__init__(timeout=900)
        self.items = items
        self.guild_id = guild_id
        self.refresh_components()

    def _visible(self):
        return [(i, it) for i, it in enumerate(self.items) if not it["hidden"]]

    def build_embed(self):
        embed = discord.Embed(title="📋 Priority Digest",
                              description="Task & deadline gom từ nhiều kênh, xếp theo ưu tiên.")
        shown = False
        for b in ("do_now", "soon", "confirm"):
            lines = []
            for _, it in self._visible():
                if it["bucket"] != b:
                    continue
                task = f"~~{it['task']}~~" if it["done"] else f"**{it['task']}**"
                prefix = "✅" if it["done"] else EMOJI[b]
                dl = f" · ⏰ {it['deadline']}" if it["deadline"] else ""
                lines.append(f"{prefix} {task}{dl} · #{it['channel']}")
            if lines:
                shown = True
                embed.add_field(name=f"{EMOJI[b]} {TITLE[b]}",
                                value="\n".join(lines)[:1000], inline=False)
        if not shown:
            embed.add_field(name="🎉 Xong hết việc hôm nay!", value="Không còn mục nào trong digest.", inline=False)
        pending = sum(1 for _, it in self._visible()
                      if it["bucket"] in ("do_now", "soon") and not it["done"])
        conf = sum(1 for _, it in self._visible() if it["bucket"] == "confirm")
        embed.set_footer(text=f"{pending} việc có hạn · {conf} cần xác nhận")
        return embed

    def _opts(self, idx_items):
        out = []
        for i, it in idx_items:
            desc = (f"⏰ {it['deadline']} · " if it["deadline"] else "") + f"#{it['channel']}"
            out.append(discord.SelectOption(label=_short(it["task"], 95), value=str(i),
                                            description=_short(desc, 95)))
        return out[:25]

    def refresh_components(self):
        self.clear_items()
        vis = self._visible()
        done_src = [(i, it) for i, it in vis
                    if it["bucket"] in ("do_now", "soon") and not it["done"]]
        if done_src:
            self.add_item(ActionSelect("done", "✅ Đánh dấu đã xong…", self._opts(done_src)))
        if vis:
            self.add_item(ActionSelect("hide", "🙈 Ẩn khỏi digest…", self._opts(vis)))
            self.add_item(ActionSelect("source", "🔍 Xem nguồn / ngữ cảnh…", self._opts(vis), single=True))
        self.add_item(RefreshButton())

    # --- xử lý các thao tác ---
    async def mark_done(self, interaction, idxs):
        done_set = DONE.setdefault(self.guild_id, set())
        for i in idxs:
            self.items[i]["done"] = True
            done_set.add(self.items[i]["msg_id"])   # NHỚ để /digest lần sau vẫn gạch ngang
        self.refresh_components()
        await interaction.response.edit_message(embed=self.build_embed(), view=self)   # sửa message tại chỗ
        await interaction.followup.send(
            f"✅ Đã đánh dấu **{len(idxs)} mục** xong → ~~gạch ngang~~ (vẫn hiển thị). Digest mai sẽ bỏ.",
            ephemeral=True, view=UndoView(self, interaction.message, idxs, "done"))

    async def hide_items(self, interaction, idxs):
        for i in idxs:
            self.items[i]["hidden"] = True
        self.refresh_components()
        await interaction.response.edit_message(embed=self.build_embed(), view=self)
        names = ", ".join(self.items[i]["task"][:30] for i in idxs)
        await interaction.followup.send(
            f"🙈 Đã ẩn **{len(idxs)} mục** khỏi digest: {names}.",
            ephemeral=True, view=UndoView(self, interaction.message, idxs, "hide"))

    async def show_source(self, interaction, idx):
        it = self.items[idx]
        if it["jump_url"]:
            link = f"[→ Nhảy tới tin gốc ở #{it['channel']}]({it['jump_url']})"
        else:
            link = "(không có link — tin đã bị xoá?)"
        extra = ("\n⚪ *Đây là ca cần xác nhận: có tin khác nói khác về cùng deadline này. "
                 "Bot KHÔNG tự chốt — bạn kiểm 2 nguồn rồi quyết.*") if it["bucket"] == "confirm" else ""
        await interaction.response.send_message(
            f"📌 Nguồn của **{_short(it['task'], 80)}**\n#{it['channel']} · {link}{extra}",
            ephemeral=True)


class ActionSelect(discord.ui.Select):
    def __init__(self, mode, placeholder, options, single=False):
        super().__init__(placeholder=placeholder, min_values=1,
                         max_values=1 if single else len(options), options=options)
        self.mode = mode

    async def callback(self, interaction):
        view: DigestView = self.view
        idxs = [int(v) for v in self.values]
        if self.mode == "source":
            await view.show_source(interaction, idxs[0])
        elif self.mode == "done":
            await view.mark_done(interaction, idxs)
        else:
            await view.hide_items(interaction, idxs)


class UndoView(discord.ui.View):
    """Nút ↩️ Hoàn tác (và 🚫 Luôn bỏ qua khi ẩn) trong ephemeral — sửa lại chính message digest."""

    def __init__(self, dview, message, idxs, mode):
        super().__init__(timeout=180)
        self.dview, self.message, self.idxs, self.mode = dview, message, idxs, mode
        if mode == "hide":
            btn = discord.ui.Button(label="🚫 Luôn bỏ qua (phiên này)", style=discord.ButtonStyle.danger)
            btn.callback = self.always_ignore
            self.add_item(btn)

    @discord.ui.button(label="↩️ Hoàn tác", style=discord.ButtonStyle.secondary)
    async def undo(self, interaction, button):
        key = "done" if self.mode == "done" else "hidden"
        for i in self.idxs:
            self.dview.items[i][key] = False
            if self.mode == "done":   # bỏ khỏi bộ nhớ "đã xong" để không còn gạch ngang
                DONE.get(self.dview.guild_id, set()).discard(self.dview.items[i]["msg_id"])
        self.dview.refresh_components()
        await self.message.edit(embed=self.dview.build_embed(), view=self.dview)
        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(content="↩️ Đã hoàn tác — các mục trở lại digest.", view=self)

    async def always_ignore(self, interaction):
        s = IGNORED.setdefault(self.dview.guild_id, set())
        for i in self.idxs:
            s.add(self.dview.items[i]["msg_id"])
        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(
            content="🚫 Đã bật luật: các tin này sẽ bị bỏ qua ở lần /digest sau (trong phiên bot).", view=self)


class RefreshButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🔄 Làm mới", style=discord.ButtonStyle.primary, row=4)

    async def callback(self, interaction):
        await interaction.response.defer()
        items = await scan_and_classify(interaction.guild)
        if not items:
            await interaction.edit_original_response(
                content="Không có task/deadline nào để tổng hợp.", embed=None, view=None)
            return
        view = DigestView(items, interaction.guild.id)
        await interaction.edit_original_response(embed=view.build_embed(), view=view)


@tree.command(name="digest", description="Gom task & deadline từ các kênh theo ưu tiên")
async def digest(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    items = await scan_and_classify(interaction.guild)
    if not items:
        await interaction.followup.send("Không có task/deadline nào để tổng hợp.")
        return
    view = DigestView(items, interaction.guild.id)
    await interaction.followup.send(embed=view.build_embed(), view=view)


if __name__ == "__main__":
    client.run(TOKEN)
