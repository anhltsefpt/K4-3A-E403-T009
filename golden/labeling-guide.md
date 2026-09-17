# Hướng dẫn gán nhãn mù — golden set CP3

> **Nguyên tắc số 1 (đã chốt): gán nhãn TRƯỚC khi chạy AI.** Không được xem output AI rồi mới điền đáp án — như vậy con số ảo và giám khảo không tin. Điền xong thì **đóng băng file `golden-set.csv`** (commit lại), sau đó mới chạy `src/classify.py`.

## Ai làm
Lý tưởng: **2 người gán độc lập** (mỗi người 1 bản copy), rồi đối chiếu. Ô nào 2 người lệch nhau → ghi vào `note`, đó thường chính là ca khó/mâu thuẫn (đáng phân tích ở phần "vì sao sai" khi pitch). Người gán **không nên** là người viết prompt cho AI.

## ⚠️ Minh bạch: golden set có tin BỊA (synthetic)
Data thật của BTC gần như không có ca `do_now` và chỉ có **một** deadline (20/9), nên golden set được bổ sung **6 tin bịa** (`msg_id` bắt đầu bằng `SYN`) để test đủ 4 bucket với deadline **khác ngày**. Các tin này **đánh dấu rõ trong cột `note`** ("BỊA — không có trong data BTC"). Khi pitch phải nói thẳng: *"N/32 tin lấy từ data thật; 6 tin synthetic để phủ ca do_now/soon mà data thật thiếu."* — KHÔNG được lờ đi.

## Đọc gì
Mỗi dòng có cột `excerpt` (trích ngắn) + `msg_id`. Đọc **toàn văn** tin theo `msg_id` trong `data/discord-pack/k4_messages.csv` (KHÔNG copy toàn văn vào repo nộp bài — theo quy định data BTC; chỉ giữ excerpt ≤2 câu như CP2 đã làm).

## Điền 4 cột ground-truth

| Cột | Điền gì |
|---|---|
| `gt_bucket` | Một trong: `do_now` (🔴 cần làm ngay/quá hạn) · `soon` (🟡 sắp đến hạn) · `confirm` (⚪ cần người xác nhận) · `skip` (không phải task/deadline → bỏ). **Phân biệt do_now/soon theo mốc "hôm nay" cố định — xem ô bên dưới.** |
| `gt_deadline` | Mốc thời gian cụ thể nếu tin **tuyên bố** một hạn (vd `23:59 20/9`). Để trống nếu không có mốc rõ. |
| `gt_source_channel` | Kênh nguồn của deadline (thường = cột `channel`, trừ ca mâu thuẫn liên kênh). |
| `gt_needs_confirm` | `TRUE` nếu đây là ca AI **không được tự chốt** (tin mâu thuẫn / mơ hồ / nhiều nguồn khác nhau). Ngược lại `FALSE`. |

## Mốc "hôm nay" để phân biệt do_now / soon (CHỐT — bắt buộc dùng chung)
`do_now` và `soon` là **tương đối theo ngày chạy digest**, nên phải cố định một mốc "hôm nay":
- **HÔM NAY = 14/9/2026** (giả định học viên bấm `/digest` sáng ngày cuối của data).
- `do_now` 🔴 = deadline **đã quá hạn** HOẶC **còn ≤ 2 ngày** (tính từ 14/9, tức hạn ≤ 16/9).
- `soon` 🟡 = deadline **còn > 2 ngày** (hạn từ 17/9 trở đi).
- Ví dụ: **M01982** hạn 20/9 → còn 6 ngày → **`soon`**.

> Mốc & ngưỡng này cũng được nhét vào prompt AI (`REFERENCE_NOW` trong `src/classify.py`) để **người và AI dùng chung một cái đồng hồ** — nếu lệch, chấm điểm sẽ bất công.

## Quy ước phân định (thống nhất trước khi gán)
- **Câu HỎI về deadline** ("hạn lập team là ngày nào?") ≠ **tuyên bố deadline**. Câu hỏi thường là `skip` hoặc `confirm`, không phải `do_now/soon`. Nhóm tự chốt quy ước và ghi vào `spec.md`.
- **Tin có mốc thời gian rõ + là việc phải làm** → `do_now`/`soon` tuỳ hạn gần/xa.
- **Hai tin nói khác nhau về cùng một hạn** (M19124 ↔ M50841) → cả hai `confirm`, `gt_needs_confirm=TRUE`.
- **Tin cá nhân/hỗ trợ kỹ thuật/xã giao** → `skip`.

## Tiêu chí "đúng" khi chấm (đã chốt — phương án B, khắt khe)
Một tin tính **ĐÚNG** khi:
- `bucket` khớp, **VÀ**
- nếu `do_now`/`soon`: `deadline` khớp **VÀ** `source_channel` khớp;
- nếu `confirm`: AI đặt `needs_confirm=TRUE`;
- nếu `skip`: AI cũng trả `skip`.

Sai một trong các điều kiện trên → tính **SAI** (và ghi lý do sai để phân tích — số xấu vẫn đủ điểm nếu trung thực).
