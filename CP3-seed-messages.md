# CP3 · Tin mẫu để nạp vào server test (cho video B2)

> Mục tiêu: dán ~8 tin vào **3 kênh** để `/digest` gom ra đủ 🔴 / 🟡 / ⚪ + cặp mâu thuẫn.
> **QUAN TRỌNG:** dán bằng **tài khoản NGƯỜI thật** (không để bot post) — vì `/digest` bỏ qua mọi tin do bot đăng.
> Tạo 3 kênh text tên đúng như dưới (để digest ghi đúng #kênh nguồn). Dán lần lượt, mỗi dòng một tin.

---

## Kênh `#channel_10` (nhiều deadline)

```
Gate 1 — Chốt đề tài · Deadline 23:59:00 20/9/2026 · nộp Brief + PRD + Wireframe + GitHub repo
```
```
Nhắc: hạn nộp Lab03 là 23:59 hôm nay 14/9, trễ không tính +XP
```
```
check xem t đã nộp bài codelab chưa
```
```
xem bảng xếp hạng điểm XP kiểu gì
```

## Kênh `#channel_02`

```
a ơi sao deadline ghép đội tự do end sớm vậy a?
```
```
Em đang cần hỗ trợ về vấn đề giấy tờ gấp thì em liên lạc đến bộ phận nào
```

## Kênh `#channel_11`

```
Các bạn chờ BTC ghép đội nhé, hiện tại cửa sổ lập đội tự do đã đóng
```
```
Workshop 2 (bắt buộc) lúc 14:00 ngày 21/9 tại E403
```

---

## Kết quả `/digest` kỳ vọng (để kiểm khi quay)

| Nhóm | Tin | Vì sao |
|---|---|---|
| 🔴 **Cần làm ngay** | "hạn nộp Lab03 23:59 hôm nay 14/9" (#channel_10) | hạn = hôm nay (mốc 14/9) |
| 🟡 **Sắp đến hạn** | "Gate 1 · 20/9" (#channel_10) · "Workshop 2 · 21/9" (#channel_11) | còn > 2 ngày |
| ⚪ **Cần người xác nhận** | "sao ghép đội end sớm?" (#channel_02) ↔ "cửa sổ đã đóng" (#channel_11) | 2 tin 2 kênh nói khác nhau → bot KHÔNG chốt liều |
| *(ẩn)* skip | "check đã nộp chưa", "xem bảng xếp hạng", "hỗ trợ giấy tờ" | nhiễu, không phải task/deadline |

> Điểm nhấn quay (20–30s): chỉ vào nhóm ⚪ — đây là chỗ bot BTC gục còn sản phẩm mình flag "cần xác nhận".

---

## Lưu ý mốc thời gian
`src/classify.py` chốt cứng **HÔM NAY = 14/9/2026** (`REFERENCE_NOW`). Nên dù quay ngày nào, AI vẫn tính hạn so với 14/9 — tin "hạn hôm nay 14/9" luôn ra 🔴, "20/9" ra 🟡. Nhất quán với golden set.
