# CP3 · Việc CẦN NGƯỜI LÀM (Human-in-the-loop)

> **Hạn: 16:00 · 17/9** — phải nộp **video 30s AI chạy thật** + **bảng số đo % (đúng N/25 tin)**.
> Code đã dựng sẵn (`src/*.py`), chỉ chờ các việc dưới đây — **AI không làm hộ được**.
> Chạy **2 nhánh song song** để kịp giờ. Đánh dấu `[x]` khi xong.

---

## 🔴 Chặn đầu tiên — làm trước, mở khóa mọi thứ

- [ ] **Lấy API key OpenAI** → tạo file `src/.env` từ `src/.env.example`, điền `OPENAI_API_KEY=...`
  *(không có key thì AI không chạy được lần nào → hỏng cả 2 deliverable)*

---

## 📊 NHÁNH A — Đo số (người phụ trách: C + D + E)

### A1. Gán nhãn mù 25 tin — **C + D làm ĐỘC LẬP, 2 bản**
> ⚠️ Phải gán **TRƯỚC khi chạy AI** và **không nhìn nhau** — nếu không, số đo mất giá trị.
> Đọc `golden/labeling-guide.md` trước. File cần điền: `golden/golden-set.csv`.

- [ ] C điền 4 cột trống cho cả 25 dòng: `gt_bucket` · `gt_deadline` · `gt_source_channel` · `gt_needs_confirm`
- [ ] D điền độc lập một bản riêng (copy file, vd `golden-set-D.csv`)
- [ ] C + D **đối chiếu 2 bản**, chốt bản thống nhất → lưu đè `golden/golden-set.csv`
- [ ] `git commit` bản nhãn đã chốt để **đóng băng** (không sửa sau khi thấy AI trả gì)

### A2. Chạy AI + chấm điểm — **E làm** (sau khi A1 xong)
```bash
cd K4-3A-E403-T009
python -m venv .venv && source .venv/bin/activate
pip install -r src/requirements.txt
mkdir -p out
python src/classify.py golden/golden-set.csv > out/predictions.csv   # gọi AI thật
python src/evaluate.py golden/golden-set.csv out/predictions.csv     # in bảng %
```
- [ ] Chạy xong, có `out/predictions.csv`
- [ ] Có **bảng "đúng N/25 · X%"** → chép vào `spec.md §7` (dòng Lượt 1)
- [ ] Viết **4 dòng phân tích "vì sao mấy ca kia sai"** *(số xấu vẫn được điểm nếu thật + có phân tích)*

---

## 🎬 NHÁNH B — Bot live & video (người phụ trách: A + B)

### B1. Dựng Discord — **A làm**
- [ ] Discord Developer Portal → **New Application** → **Bot** → **Reset Token** → điền vào `src/.env`
- [ ] Bật **MESSAGE CONTENT INTENT** (bắt buộc, không bật bot không đọc được tin)
- [ ] Tạo **server test riêng** (bạn là admin) → mời bot (OAuth scope `bot` + `applications.commands`)
- [ ] Tạo role **"Lab Coach"** → lấy Role ID → điền `LAB_COACH_ROLE_ID` vào `src/.env`

### B2. Nạp data + quay — **B làm**
- [ ] Post ~25 tin từ `golden/golden-set.csv` (hoặc `k4_messages.csv`) vào vài kênh test
- [ ] Gán role "Lab Coach" cho 1 tài khoản test (để demo authority)
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
