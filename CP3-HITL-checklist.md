# CP3 · Việc CẦN NGƯỜI LÀM (Human-in-the-loop)

> **Hạn: 16:00 · 17/9** — phải nộp **video 30s AI chạy thật** + **bảng số đo % (đúng N/25 tin)**.
> Code đã dựng sẵn (`src/*.py`), chỉ chờ các việc dưới đây — **AI không làm hộ được**.
> Chạy **2 nhánh song song** để kịp giờ. Đánh dấu `[x]` khi xong.

---

## 🔴 Chặn đầu tiên — làm trước, mở khóa mọi thứ

- [x] **Lấy API key OpenAI** → `src/.env` đã có `OPENAI_API_KEY` (đã chạy AI thật thành công)
  *(không có key thì AI không chạy được lần nào → hỏng cả 2 deliverable)*

---

## 📊 NHÁNH A — Đo số (người phụ trách: C + D + E)

### A1. Gán nhãn mù golden set — ✅ **ĐÃ XONG** (32 tin, đã đóng băng)
> ⚠️ Phải gán **TRƯỚC khi chạy AI** — đã đảm bảo: nhãn cố định rồi mới chạy classify, KHÔNG sửa nhãn theo output AI.

- [x] Điền đủ 4 cột cho **cả 32 dòng** (26 tin thật + 6 tin synthetic `SYN*` đánh dấu rõ)
- [x] Chốt bản thống nhất → `golden/golden-set.csv`
- [x] `git commit` đóng băng (`25b659f`)

> ⚠️ **Lưu ý trung thực để đội biết khi pitch:** nhãn KHÔNG gán theo quy trình lý tưởng "2 người mù độc lập" — mà do đội trưởng + AI-hỗ-trợ chốt. Nếu còn thời gian, nên nhờ 1 người thứ 2 rà lại độc lập để tăng độ tin.

### A2. Chạy AI + chấm điểm — ✅ **ĐÃ XONG** (chạy 3 lượt có tinh chỉnh)
```bash
cd K4-3A-E403-T009
python -m venv .venv && source .venv/bin/activate
pip install -r src/requirements.txt
mkdir -p out
python src/classify.py golden/golden-set.csv > out/predictions.csv   # gọi AI thật
python src/evaluate.py golden/golden-set.csv out/predictions.csv     # in bảng %
```
- [x] Chạy xong, có `out/predictions*.csv` (3 lượt: predictions / predictions2 / predictions3)
- [x] Có **bảng "đúng N/32 · %"** → đã chép vào `spec.md §7`: 66% → 81% → 88% → **91%** (chốt lượt 3)
- [x] Viết **phân tích "vì sao sai"** → đã có đầy đủ trong `spec.md §7` (từng lượt + ca sai)
- [x] Đã commit đóng băng (`25b659f`)

> Kết quả nộp: **29/32 (91%)** theo tiêu chí khắt khe · confirm ⚪ 2/2 (thoả điều kiện lõi quality bar).

---

## 🎬 NHÁNH B — Bot live & video (người phụ trách: A + B)

### B1. Dựng Discord — **A làm**
- [ ] Discord Developer Portal → **New Application** → **Bot** → **Reset Token** → điền vào `src/.env`
- [ ] Bật **MESSAGE CONTENT INTENT** (bắt buộc, không bật bot không đọc được tin)
- [ ] Tạo **server test riêng** (bạn là admin) → mời bot (OAuth scope `bot` + `applications.commands`)
- [ ] ~~Tạo role "Lab Coach"~~ → **ĐÃ BỎ** (gỡ khỏi `bot.py`, không cần role ID nữa)

### B2. Nạp data + quay — **B làm**
- [ ] Tạo 3 kênh `#channel_10` · `#channel_02` · `#channel_11` → dán tin từ **`CP3-seed-messages.md`** bằng **tài khoản NGƯỜI** (bot bỏ qua tin do bot đăng)
- [ ] Gõ `/digest` → thấy bot trả **embed 3 nhóm 🔴🟡⚪** thật
- [ ] **Quay video 30s** theo kịch bản:
  - (0–8s) server test, vài kênh có tin
  - (8–20s) gõ `/digest` → bot "thinking" → trả embed 3 nhóm, mỗi mục có deadline + #kênh
  - (20–30s) chỉ vào ca ⚪ **M19124 ↔ M50841**: bot KHÔNG chốt liều (đúng chỗ bot BTC gục)

> Video CP3 chỉ cần chứng minh **AI chạy thật** — quay thô, không cần lồng tiếng.

---

## 📤 NỘP BÀI — **A (đội trưởng) làm**

- [ ] Gom: **video 30s** + **bảng số đo %** (+ 4 dòng phân tích)
- [ ] Nộp form bằng **đúng mã học viên đội trưởng** *(2A202602952 — sai mã là BTC ghép nhầm, mất điểm)*
- [ ] Nộp **trước 16:00 · 17/9**

---

## ⚠️ Nhắc quan trọng

- **Vibe-coding rule:** mỗi người phải **giải thích được** phần code mang tên mình → đọc `src/*.py` (có chú thích tiếng Việt) trước khi demo, nếu không phần đó **0 điểm**.
- Gán nhãn **mù + đóng băng bằng commit** — đây là điểm mấu chốt để số đo đáng tin.
- Cả 5 mốc nộp bằng **cùng 1 mã học viên đội trưởng**.
