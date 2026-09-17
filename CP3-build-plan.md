# CP3 → CP6 · Kế hoạch build (chốt sau phiên grill)

> **Hạn CP3: 16:00 · 17/9** — nộp **video 30s AI chạy thật** + **golden set ≥20 + bảng kết quả lượt 1 có %**.
> Track B · lát cắt "Priority Digest" (nối tiếp [CP1-canvas.md](CP1-canvas.md) · [CP2-flow.md](CP2-flow.md)).

---

## 0. Các quyết định đã chốt (đừng mở lại)

| # | Quyết định | Chốt |
|---|---|---|
| Bề mặt chạy AI | Bot Discord thật, trong **server test của chính nhóm** (không phải server BTC — member không mời được bot; self-bot vi phạm ToS) | A |
| Nguồn dữ liệu | Import `k4_messages.csv` (BTC, đã ẩn danh) vào server test | A |
| Model | **gpt-4o-mini** (OpenAI), structured output (json_schema strict), gọi batch ~25 tin | A |
| Đơn vị golden set | **Mỗi tin nhắn** (không phải mỗi lần /digest) | A |
| Tiêu chí "đúng" | **Khắt khe**: bucket + deadline + kênh; ca mâu thuẫn = flag ⚪; nhiễu = bỏ | B |
| Gán nhãn | **Mù, trước khi chạy AI**, lý tưởng 2 người độc lập | A |
| Role "Lab Coach" | Chỉ là **tính năng demo live**, KHÔNG vào thước đo golden (CSV không có role) | A |
| Xử lý mâu thuẫn | **Lai**: chốt khi rõ (1 nguồn, mốc cụ thể); flag ⚪ khi mâu thuẫn/mơ hồ | C |

**Định vị lõi (viết vào spec):** khác con bot nhắc-lịch của BTC (sai vì lệ thuộc Lab Coach cập nhật tay) — sản phẩm này **đọc thẳng luồng tin (source of truth)** nên không cũ, và **flag "cần xác nhận"** thay vì chốt liều. Con bot BTC là **baseline để so** (BTC nói vậy trong `data/discord-pack/k4_daily_reports.md`).

---

## 1. Cây phụ thuộc — làm theo thứ tự này

```
[Bạn]  Tạo Discord app + bot token  ─┐
[Bạn]  Tạo server test + role Coach  ─┼─→ [Bạn] Nạp data vào kênh ─→ [Bạn] Quay video 30s
[AI đã dựng] classify.py / bot.py ────┘
[2 người] Gán nhãn mù golden-set.csv ─→ [chạy] classify.py ─→ [chạy] evaluate.py ─→ Bảng % lượt 1
```

Hai nhánh **song song được**: (a) gán nhãn + chạy số đo; (b) dựng bot live + quay video. Chia 2 người/2 nhánh cho kịp 16:00.

---

## 2. Việc CHỈ nhóm làm được (tôi không làm hộ)

1. **Discord Developer Portal** → New Application → Bot → Reset Token → điền `.env`. Bật **MESSAGE CONTENT INTENT**.
2. **Tạo server test** (bạn là admin) → mời bot (OAuth scope `bot` + `applications.commands`).
3. **Tạo role "Lab Coach"** → lấy Role ID → `.env` (`LAB_COACH_ROLE_ID`).
4. **Nạp data**: post một ít tin từ `k4_messages.csv` vào kênh test (hoặc paste tay ~25 tin golden). Gán role Coach cho 1 tài khoản test để demo authority.
5. **Gán nhãn mù** golden set — phán đoán con người (xem `golden/labeling-guide.md`).
6. **Quay video 30s** — bấm `/digest`, thấy embed AI trả thật.
7. **Nộp form** bằng mã học viên đội trưởng.

> ⚠️ **Vibe-coding rule**: mỗi người phải giải thích được phần code mang tên mình, nếu không phần đó **0 điểm**. Sáng dậy **đọc kỹ** `src/*.py` trước — code có chú thích tiếng Việt để dễ nắm. Chia rõ ai chịu trách nhiệm file nào.

---

## 3. Việc tôi ĐÃ dựng sẵn (chạy được, chỉ thiếu API key/token)

| File | Vai trò |
|---|---|
| `src/classify.py` | **Lời gọi AI trung tâm** — phân loại tin (gpt-4o-mini, structured output, batch). Đây là "AI chạy thật" của CP3. |
| `src/evaluate.py` | Chấm output so golden set → in **bảng kết quả lượt 1 có %** + danh sách ca sai để phân tích. |
| `src/bot.py` | Bot Discord thật: `/digest` → gọi `classify` → trả embed. Bề mặt để quay video. Có sẵn khung demo "authority theo role". |
| `golden/golden-set.csv` | 25 tin ứng viên đã lấy sẵn (deadline rõ · cặp mâu thuẫn M19124↔M50841 · nhiễu). **Cột nhãn để trống** cho nhóm gán mù. |
| `golden/labeling-guide.md` | Quy ước gán nhãn + tiêu chí chấm. |
| `spec.md` | Bản nháp AI Spec (deliverable trung tâm CP4). |
| `src/.env.example` | Mẫu biến môi trường. |

---

## 4. Chạy số đo CP3 (sau khi gán nhãn xong)

```bash
cd K4-3A-E403-T009
python -m venv .venv && source .venv/bin/activate
pip install -r src/requirements.txt
cp src/.env.example src/.env      # rồi điền OPENAI_API_KEY

# 1) Gán nhãn mù golden-set.csv (2 người) → commit đóng băng
# 2) Chạy AI trên golden set:
mkdir -p out
python src/classify.py golden/golden-set.csv > out/predictions.csv
# 3) Chấm:
python src/evaluate.py golden/golden-set.csv out/predictions.csv
```

Output của bước 3 chính là **"Thử 25 tin, đúng N tin"** để nộp CP3. **Số xấu vẫn đủ điểm nếu thật** — kèm phân tích "vì sao 12 ca kia sai" ăn điểm cao hơn "chạy tốt" không bằng chứng.

Muốn số đo trên tải thật cả 1 ngày (đối chiếu baseline bot BTC): `python src/classify.py --from-messages 2026-09-13 > out/day.csv`.

---

## 5. Video 30s (CP3) — kịch bản quay

Quay thô, không lồng tiếng. Thấy được **≥1 lời gọi AI thật**:
1. (0–8s) Discord server test, vài kênh có tin (build-phase / channel_10 / 02 / 11).
2. (8–20s) Gõ `/digest` → bot "thinking" → trả **embed** 3 nhóm 🔴🟡⚪, mỗi mục có deadline + #kênh.
3. (20–30s) Chỉ vào **ca ⚪ cần xác nhận** (M19124↔M50841): bot KHÔNG chốt liều — đúng chỗ bot BTC gục.

> Video CP3 ≠ video CP5. CP3 chỉ chứng minh chạy thật (thô cũng được).

---

## 6. Roadmap CP4 → CP6 (nhẹ, làm sau khi CP3 xong)

- **CP4 · chốt `spec.md`** (21:00 17/9): hoàn thiện `spec.md` (đã có nháp) — chốt "thế nào là đạt" (chính là tiêu chí B ở trên) TRƯỚC khi biết kết quả. Tự khai phần chưa xong (khai thiếu không bị trừ, giấu mới bị). Sau 21:00 không sửa chuẩn "đạt".
- **CP5 · slide + video dự phòng** (13:00 18/9): slide 6 trang xuất **PDF** (theo `02-guide.md §5.1`); **video demo dự phòng** quay đúng phần định demo sân khấu; thư mục `validation/`; cần **≥2 willing user** đã khai từ CP1.
- **CP6 · thuyết trình** (17:30 18/9): không nộp gì. Phòng **E403** — mỗi nhóm **6 phút**. Mọi thành viên phải trả lời được câu hỏi về phần mang tên mình.

> Nhắc: cả 5 mốc nộp bằng **cùng một mã học viên đội trưởng**, nếu không BTC ghép nhầm → mất điểm mốc lệch.

---

## 7. Chia việc gợi ý (đội T009)

| Người | CP3 |
|---|---|
| A (đội trưởng) | Discord Portal + bot token + server test + mời bot; nộp form |
| B | Nạp data vào kênh; quay video 30s |
| C + D | Gán nhãn mù golden set (độc lập, 2 bản) rồi đối chiếu |
| E | Chạy classify+evaluate, lập bảng %, viết 4 dòng phân tích "vì sao sai" |

(Đọc code trước khi demo — vibe-coding rule.)
