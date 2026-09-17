# Kịch bản cho người ngoài dùng thử — Priority Digest (R6)

> **Nguyên tắc số 1:** giao task rồi **NGỒI IM xem họ làm**. Không mách nút, không hỏi "sản phẩm hay không".
> Quote ăn điểm là lời họ nói **lúc đang vật lộn với task**, không phải lời khen xã giao.
> Ghi mọi thứ vào [`nhat-ky-validation.md`](nhat-ky-validation.md).

## Chuẩn bị (làm 1 lần trước buổi test)
1. Server test đã nạp đủ tin mẫu theo [`../CP3-seed-messages.md`](../CP3-seed-messages.md) — 3 kênh `#channel_10 · #channel_02 · #channel_11`, dán bằng **tài khoản người thật** (bot post sẽ bị `/digest` bỏ qua).
2. Tạo **Invite link** của server test, gửi cho người thử — HỌ vào server của bạn, bạn **không** đụng Discord của họ. Ai ngại join thì cho ngồi máy bạn đã login sẵn.
3. Mốc thời gian bot chốt cứng **HÔM NAY = 14/9/2026** → "Lab03 hạn hôm nay 14/9" luôn ra 🔴, "Gate 1 · 20/9" ra 🟡. Nhất quán dù test ngày nào.

## Lời dẫn (đọc y nguyên, KHÔNG giải thích cách bấm)
> *"Sáng nay bạn vừa mở Discord. Có 4 kênh đang quá tải, khoảng 1.000 tin trong 3 ngày. Bạn có 1 phút. Tôi sẽ nhờ bạn làm 3 việc — cứ tự mò, tôi ngồi xem thôi. Nghĩ gì cứ nói ra thành tiếng nhé."*

---

## 3 task (mỗi task ~2–3 phút)

### Task 1 — Việc gấp nhất hôm nay + nó ở đâu  → test 🔴 + jump-to-source
**Giao:** *"Cho tôi biết hôm nay bạn **phải nộp gì gấp nhất**, và nó nằm ở **kênh nào**. Mở tin gốc ra cho tôi xem."*
- **Đáp án đúng:** "hạn nộp Lab03 · 23:59 hôm nay 14/9" ở `#channel_10` (nhóm 🔴).
- **Kỳ vọng thao tác:** gõ `/digest` → đọc nhóm 🔴 → mở select **🔍 Xem nguồn/ngữ cảnh** → bấm link nhảy về tin gốc.
- **Quan sát:** họ có tự tìm ra `/digest` không? Có hiểu 🔴 = gấp không? Có biết link nhảy sang đúng kênh không?

### Task 2 — Deadline mâu thuẫn: tin ai?  → test ⚪ confirm (NGÔI SAO sản phẩm)
**Giao:** *"Có một deadline mà **hai người nói khác nhau**. Bạn tìm xem là cái nào, và bạn sẽ **tin thông tin nào**?"*
- **Đáp án đúng:** ca "ghép đội tự do" — `#channel_02` hỏi *"sao end sớm?"* ↔ `#channel_11` *"cửa sổ đã đóng"*. Bot xếp vào ⚪ **Cần người xác nhận**, đưa 2 link 2 kênh, KHÔNG tự chốt.
- **Quan sát:** họ có hiểu ⚪ nghĩa là "bot không dám chốt, tự đi xác nhận" không? Hay tưởng bot bị lỗi/thiếu thông tin? — đây là chỗ khác biệt lớn nhất so với bot thường, nghe kỹ quote.

### Task 3 — Dọn việc đã xong  → test nút ✅ (interaction.update + hoàn tác)
**Giao:** *"Giả sử bạn **vừa làm xong** một việc trong danh sách. Đánh dấu nó lại."*
- **Đáp án đúng:** mở select **✅ Đánh dấu đã xong** → chọn mục → Áp dụng → mục bị ~~gạch ngang~~ vẫn hiển thị, có nút ↩️ Hoàn tác.
- **Quan sát:** họ có tưởng "gạch ngang = bị xoá mất" không? Có tìm thấy nút hoàn tác không? Có nhầm với 🙈 Ẩn không?

---

## Sau 3 task — 1 câu hỏi mở duy nhất
> *"Nếu mai không có bot này nữa, bạn thấy tiếc điều gì nhất?"* — câu trả lời hé lộ giá trị lõi thật sự (hoặc lộ ra là chẳng tiếc gì → tín hiệu quan trọng, vẫn ghi nhận).

## Nhắc người ghi chép
- Chép **nguyên văn** lời họ buột miệng, cả lỗi chính tả.
- Đánh dấu mọi chỗ họ **khựng lại / bấm nhầm / hỏi lại** — đó chính là "kẹt ở đâu".
- Đừng cứu họ ngay; đếm thầm 5 giây xem họ tự thoát được không.
