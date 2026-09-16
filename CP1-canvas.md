# CP1 · Canvas — Chốt Canvas + repo

> **Hạn nộp: 19:30 · 16/9** · Đội trưởng nộp thay cả nhóm (điểm chung của nhóm, 5 điểm).
> Đây là **bản nháp** — evidence & spec hoàn thiện dần, chốt tại 21:00 · 17/9 (CP4).
> Nội dung điền từ `spec.md` (Output A · hướng "Priority Digest").

---

## Thông tin nộp

- **Đội trưởng (họ tên):** Lê Tuấn Anh
- **Mã học viên đội trưởng:** 2A202602952
- **GitHub đội trưởng:** anhltsefpt
- **Link repo GitHub (đã để công khai):** https://github.com/anhltsefpt/K4-3A-E403-T009
---

## Canvas 7 dòng *(theo guide §1.5)*

**1. Hướng (Track + đề):**
> **Track B · B2 — Tính năng mới: "Priority Digest"** — AI tóm tắt task + deadline theo mức ưu tiên cho học viên.

**2. Job executor (người trực tiếp làm việc này — một vai cụ thể):**
> Học viên tuần onboarding, mỗi ngày mở Discord ~10–20 phút, phải lướt nhiều kênh để không bỏ sót việc cần làm.

**3. Pain một câu (ai — đang làm gì — vướng đâu — hậu quả gì):**
> Học viên mở Discord mỗi ngày để nắm việc cần làm, nhưng task/deadline **nằm lẫn trong quá nhiều tin ở nhiều kênh**, phải tự quét thủ công nên **dễ bỏ sót → trễ hạn, mất điểm, hoặc hỏi lại câu đã có đáp án**.

**4. Bằng chứng đầu tiên (khảo sát + mining):**
> _(A — khảo sát 20 người ngoài nhóm, log gốc lưu trong repo)_
> - **20/20 (100%)** phải kiểm tra nhiều kênh · **17/20 (85%)** đã từng bỏ lỡ/suýt bỏ lỡ thông tin quan trọng · **14/20 (70%)** nói **deadline** dễ bị bỏ sót nhất.
>
> _(B — mining `data/discord-pack/`, 1.092 tin 12–14/09; trích ≤2 câu, dẫn msg_id)_
> - 1 kênh đơn (`channel_10`) đã có **654 tin/3 ngày** → khối lượng khiến tin bị trôi.
> - `M72484`: "Hạn nộp Lab02" · `M07653`: "[@BOT] hạn nộp daily stand up".

**5. Lát cắt MỘT CÂU** *(1 user · 1 việc · 1 quyết định AI · 1 kết quả):*
> Một học viên mở Discord đầu ngày · AI đọc các tin gần đây và tạo bản tóm tắt **"việc cần làm hôm nay"** — chỉ gồm task + deadline, sắp theo ưu tiên (cần làm ngay / sắp đến hạn), có link tới tin gốc · học viên nắm việc trong 1 phút mà không phải quét hết các kênh.

**6. Automation dự kiến + 1 dòng lý do:**
> **Conditional** — AI tự tóm tắt các mục **chắc** là task/deadline; mục không chắc đưa vào khu "cần người xác nhận", không đoán liều. Lý do: bịa/sai một deadline → học viên tin nhầm → nộp trễ, mất điểm → luôn kèm link nguồn để tự kiểm.

**7. Willing users dự kiến (≥2 người thật, tên cụ thể):**
> _(khai NGAY từ CP1 — CP5 khối R6 yêu cầu ≥2 người đã khai ở đây)_
> - **P07**
> - **P20**

---

## Phân công (có tên)

| Việc | Người phụ trách |
|---|---|
| Mining data + evidence (đếm + ví dụ nguyên văn) | Nguyễn Sơn Giang (`songiangvn`) |
| Golden set (tin → kỳ vọng: là task/deadline hay bỏ qua) | Nguyễn Ngọc Thái An (`nnthaian`) |
| Code prototype (≥1 lời gọi AI thật) | Vũ Thường Tín (`Nituv05`) |
| Spec + demo + khảo sát willing users | **Lê Tuấn Anh (`anhltsefpt`) — đội trưởng** |

---

## Checklist tự kiểm trước khi nộp *(rubric CP1)*

- [x] Lát cắt đúng format MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả) ✅ (dòng 5)
- [x] Có evidence ban đầu (số đếm được + trích nguyên văn) ✅ (dòng 4)
- [x] Đủ tên phân công
- [x] Link repo GitHub đã công khai
- [ ] Đã khai ≥2 willing user (tên cụ thể)
- [ ] Cả 5 mốc sẽ nộp bằng **cùng mã học viên đội trưởng**
