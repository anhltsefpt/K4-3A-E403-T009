"""
classify.py — LỜI GỌI AI TRUNG TÂM của sản phẩm (CP3).

Đọc tin nhắn Discord → gọi OpenAI (gpt-4o-mini) phân loại từng tin thành:
  - bucket: do_now (🔴) / soon (🟡) / confirm (⚪) / skip
  - deadline: mốc thời gian trích được (chuỗi, "" nếu không có)
  - source_channel: kênh nguồn
  - needs_confirm: True nếu tin mâu thuẫn/mơ hồ, AI KHÔNG tự chốt

Đây là "≥1 lời gọi AI chạy thật" mà CP3 bắt buộc — KHÔNG hardcode kết quả.
Dùng structured output (response_format json_schema, strict) để model trả JSON đúng schema.
Gọi theo batch ~25 tin/lần để né rate-limit và tiết kiệm.

Chạy:
    python src/classify.py golden/golden-set.csv > out/predictions.csv
hoặc chấm cả 1 ngày data:
    python src/classify.py --from-messages 2026-09-13 > out/day.csv
"""
import csv, json, os, sys, argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()  # đọc OPENAI_API_KEY từ .env

MODEL = "gpt-4o-mini"               # rẻ, đủ cho phân loại; đổi model OpenAI khác ở đây
DATA = "data/discord-pack/k4_messages.csv"  # (repo BTC — chỉ đọc, không commit)

# Ngày giả định học viên bấm /digest. NGƯỜI gán nhãn & AI PHẢI dùng CHUNG mốc này,
# nếu không do_now/soon sẽ lệch nhau và chấm điểm bất công. Đổi ở đây nếu chọn ngày khác.
REFERENCE_NOW = "2026-09-14"        # = ngày cuối của data; ngưỡng do_now = ≤ 2 ngày

# Prompt hệ thống: mô tả LUẬT phân loại. Sửa ở đây khi tinh chỉnh.
SYSTEM = f"""Bạn là bộ lọc digest cho cộng đồng Discord của một khoá học.
HÔM NAY là {REFERENCE_NOW}. Tính gần/xa hạn so với ngày này.
Với MỖI tin nhắn, phân loại theo luật sau:
- do_now: việc/deadline có mốc thời gian, ĐÃ QUÁ HẠN hoặc còn ≤ 2 ngày (tính từ HÔM NAY).
- soon: việc/deadline có mốc thời gian, còn > 2 ngày.
  BẮT BUỘC tính số ngày trước khi chọn. Ví dụ: HÔM NAY 14/9, hạn 20/9 = còn 6 ngày
  > 2 → 'soon' (KHÔNG phải 'do_now'). Chỉ 'do_now' khi hạn ≤ 16/9 hoặc đã qua.
- confirm: liên quan deadline NHƯNG thông tin mâu thuẫn / mơ hồ / nhiều nguồn
  nói khác nhau. KHÔNG được tự chốt — đặt needs_confirm=true.
- skip: không phải task/deadline (hỏi vu vơ, hỗ trợ kỹ thuật, xã giao, cá nhân).

QUY TẮC QUAN TRỌNG:
- ĐỐI CHIẾU CẢ LÔ: nếu ≥2 tin nói KHÁC NHAU về cùng một mốc/việc, HOẶC một tin
  CHẤT VẤN / thắc mắc về một deadline (vd "sao deadline ghép đội end sớm vậy?")
  trong khi tin khác nói mốc đó đã thay đổi/đóng → CẢ HAI tin = confirm,
  needs_confirm=true. TUYỆT ĐỐI KHÔNG skip các tin này — đây là ca cần người xác nhận.
- Một CÂU HỎI về deadline ("hạn lập team là ngày nào?") KHÔNG phải tuyên bố
  deadline → skip, TRỪ KHI nó chất vấn một deadline đang mâu thuẫn (→ confirm ở trên).
- Tin chỉ THÔNG BÁO một ngày/sự kiện mà KHÔNG yêu cầu người đọc phải LÀM gì, VÀ
  không mâu thuẫn với tin nào → skip (vd "ngày bắt đầu ghi nhận XP là 14/9").
- Chỉ trích 'deadline' khi tin THỰC SỰ nêu mốc thời gian cụ thể; nếu không, để "".
  Xuất 'deadline' theo định dạng "DD/MM/YYYY HH:MM", LUÔN kèm năm 2026.
- Khi không chắc, ưu tiên 'confirm' + needs_confirm=true thay vì đoán liều.
- 'source_channel' = kênh của tin đang xét (trừ khi tin dẫn chiếu kênh khác)."""

# Schema structured output — ép model trả đúng cấu trúc, không cần parse tay.
SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "msg_id": {"type": "string"},
                    "bucket": {"type": "string",
                               "enum": ["do_now", "soon", "confirm", "skip"]},
                    "deadline": {"type": "string"},
                    "source_channel": {"type": "string"},
                    "needs_confirm": {"type": "boolean"},
                    "reason": {"type": "string"},
                },
                "required": ["msg_id", "bucket", "deadline",
                             "source_channel", "needs_confirm", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
    "additionalProperties": False,
}


def classify_batch(msgs):
    """Gọi OpenAI một lần cho cả lô tin. Trả list dict theo SCHEMA."""
    lines = [f"- msg_id={m['msg_id']} | channel={m['channel']} | "
             f"time={m['created_at']} | content={m['content']}" for m in msgs]
    user = "Phân loại các tin sau. Trả về đúng một kết quả cho mỗi msg_id:\n" \
           + "\n".join(lines)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": user}],
        response_format={"type": "json_schema", "json_schema": {
            "name": "digest_results", "strict": True, "schema": SCHEMA}},
    )
    text = resp.choices[0].message.content
    return json.loads(text)["results"]


def load_golden(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    return [{"msg_id": r["msg_id"], "channel": r["channel"],
             "created_at": r["created_at"], "content": r["excerpt"]} for r in rows]


def load_from_messages(day):
    """Lấy tin của 1 ngày từ CSV data BTC (bỏ tin bot)."""
    out = []
    for r in csv.DictReader(open(DATA, encoding="utf-8")):
        if r["is_bot"] == "True":
            continue
        if r["created_at_vn"].startswith(day):
            out.append({"msg_id": r["msg_id"], "channel": r["channel"],
                        "created_at": r["created_at_vn"],
                        "content": " ".join(r["content"].split())[:200]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("golden", nargs="?", help="đường dẫn golden-set.csv")
    ap.add_argument("--from-messages", metavar="YYYY-MM-DD",
                    help="chạy trên toàn bộ tin của 1 ngày trong data BTC")
    ap.add_argument("--batch", type=int, default=25)
    args = ap.parse_args()

    msgs = (load_from_messages(args.from_messages) if args.from_messages
            else load_golden(args.golden))

    preds = []
    for i in range(0, len(msgs), args.batch):
        preds += classify_batch(msgs[i:i + args.batch])

    w = csv.DictWriter(sys.stdout,
                       fieldnames=["msg_id", "bucket", "deadline",
                                   "source_channel", "needs_confirm", "reason"])
    w.writeheader()
    for p in preds:
        w.writerow(p)


if __name__ == "__main__":
    main()
