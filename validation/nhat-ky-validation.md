# Nhật ký người ngoài dùng thử — Priority Digest (R6 · 8 điểm)

> Cần **5 người ngoài nhóm**, trong đó **≥2 người đã khai Willing users từ CP1**.
> **Ẩn danh — KHÔNG ghi tên thật trong repo** (yêu cầu bảo mật): mỗi người chỉ ghi **vai/nghề** + mã `P-00x`. Bảng ánh xạ mã↔người giữ riêng ngoài repo.
> Người chê vẫn tính đủ điểm — miễn bằng chứng thật. Quote phải **nguyên văn** (giữ cả lỗi chính tả).
> Kịch bản đầy đủ: xem [`kich-ban-test.md`](kich-ban-test.md).

## 3 task giao cho người thử (giải nghĩa T1 / T2 / T3)

| Mã | Task giao (đọc cho người thử) | Kiểm tính năng nào | Đáp án đúng trong data mẫu |
|---|---|---|---|
| **T1** 🔴 | *"Hôm nay bạn **phải nộp gì gấp nhất**, nó nằm **kênh nào**? Mở tin gốc ra xem."* | Nhóm 🔴 **Cần làm ngay** + nút **🔍 Xem nguồn** (nhảy về tin gốc) | "hạn nộp Lab03 · 23:59 hôm nay 14/9" ở `#channel_10` |
| **T2** ⚪ | *"Có deadline nào **hai người nói khác nhau** không? Bạn **tin cái nào**?"* | Nhóm ⚪ **Cần xác nhận** — bot KHÔNG tự chốt khi 2 tin mâu thuẫn (ngôi sao sản phẩm) | ghép đội tự do: `#channel_02` "sao end sớm?" ↔ `#channel_11` "cửa sổ đã đóng" |
| **T3** ✅ | *"Giả sử bạn **vừa làm xong** 1 việc, **đánh dấu** nó lại."* | Nút **✅ Đánh dấu đã xong** (gạch ngang, vẫn hiện + nút ↩️ hoàn tác) | mục bất kỳ → bị ~~gạch ngang~~ |

Trong các bảng bên dưới: **"T1 🔴 xong?"** = tự tìm được việc gấp + mở nguồn · **"T2 ⚪ hiểu?"** = hiểu ⚪ là "bot nhường người quyết" · **"T3 ✅ xong?"** = tự đánh dấu xong được.

## Thông tin buổi test
- **Ngày test:** ⟨…⟩
- **Người điều phối (ngồi xem):** ⟨…⟩
- **Người ghi chép:** ⟨…⟩
- **Môi trường:** server test Discord của nhóm (tin mẫu theo `CP3-seed-messages.md`)

---

## Bảng tổng hợp 5 người

| # | Vai / nghề (ẩn danh) | Willing từ CP1? | T1 🔴 xong? | T2 ⚪ hiểu? | T3 ✅ xong? | Kẹt chính |
|---|---|---|---|---|---|---|
| P-001 | ⟨vai/nghề⟩ | ⟨Có/Không⟩ | ✅ | (không ghi nhận) | ✅ | Không — dùng mượt, không confuse |
| P-002 | ⟨vai/nghề⟩ | ⟨Có/Không⟩ | (không ghi nhận) | (không ghi nhận) | (không ghi nhận) | Hiển thị rối · tóm tắt chữ nhỏ dễ bỏ sót · các mục sát nhau |
| P-003 | ⟨vai/nghề⟩ | ⟨Có/Không⟩ | ⚠️ | (không ghi nhận) | (không ghi nhận) | Khó tìm đúng task ở ô search của menu 🔍 xem nguồn/ngữ cảnh |
| 4 | ⟨…⟩ | ⟨Không⟩ | ⟨…⟩ | ⟨…⟩ | ⟨…⟩ | ⟨…⟩ |
| 5 | ⟨…⟩ | ⟨Không⟩ | ⟨…⟩ | ⟨…⟩ | ⟨…⟩ | ⟨…⟩ |

Ký hiệu: ✅ tự làm được · ⚠️ làm được nhưng lúng túng · ❌ không làm được / hiểu sai.

---

## Nhật ký chi tiết từng người

### P-001 — ⟨vai/nghề⟩  ·  Willing CP1: ⟨Có/Không⟩
| Task giao | Họ làm gì (thao tác thật) | Kẹt ở đâu | Quote nguyên văn | Quyết định của nhóm |
|---|---|---|---|---|
| T1 · Việc gấp nhất + kênh nào | Dùng được **🔍 xem nguồn tin nhắn**, mở đúng tin gốc | Không | *"Dùng mượt, không bị confuse khi sử dụng"* · *"sử dụng được tính năng đánh dấu, xem nguồn tin nhắn"* | Giữ nguyên — luồng xem nguồn đi đúng hướng |
| T2 · Deadline mâu thuẫn tin ai | (không hỏi/không ghi nhận riêng trong buổi này) | — | — | Bổ sung ở buổi test sau để phủ ca ⚪ |
| T3 · Đánh dấu đã xong | Dùng được **✅ đánh dấu đã xong** | Không | *"sử dụng được tính năng đánh dấu…"* | Giữ nguyên |
| Câu mở: "tiếc điều gì nhất?" | — | — | *(chưa hỏi)* | — |

> **Tổng P-001:** tín hiệu tích cực — người dùng non-onboarding vẫn thao tác trơn, tự dùng được 🔍 và ✅ mà không cần hướng dẫn. Không phát hiện điểm kẹt.

### P-002 — ⟨vai/nghề⟩  ·  Willing CP1: ⟨Có/Không⟩
| Task giao | Họ làm gì | Kẹt ở đâu | Quote nguyên văn | Quyết định |
|---|---|---|---|---|
| T1 · Việc gấp nhất + kênh nào | Dùng được, nhưng vướng ở **cách trình bày digest** | 3 nhóm 🔴🟡⚪ nhìn dồn vào nhau, khó tách bằng mắt | *"Cách hiển thị hơi rối, tách 3 sections ra cho nó thoáng"* | **SỬA:** tăng khoảng cách / phân tách rõ 3 nhóm 🔴🟡⚪ (blank line / divider giữa các nhóm) |
| — · Đọc phần tóm tắt | Dễ bỏ sót dòng tóm tắt/bộ đếm | Cỡ chữ tóm tắt nhỏ, không thu hút chú ý | *"Cái tóm tắt nhìn hơi nhỏ, ko để ý được"* | **SỬA:** làm nổi tóm tắt (in đậm / heading / emoji đầu dòng) |
| — · Đọc từng mục | Các mục việc sát nhau, khó phân biệt từng task | Thiếu khoảng cách giữa 2 mục | *"Tách ra khoảng cách giữa 2 tasks"* | **SỬA:** thêm khoảng trắng giữa các mục trong cùng nhóm |
| Cần thêm tính năng? | — | — | *"Cần biết chính xác nguồn — và đã có rồi"* | Không yêu cầu tính năng mới; nhu cầu "biết chính xác nguồn" đã được 🔍 xem nguồn đáp ứng |
| Câu mở | — | — | *(chưa hỏi)* | — |

> **Tổng P-002:** không vướng về chức năng — 3 góp ý đều về **trình bày (layout/spacing/typography)** của embed digest. Đây là nhóm sửa nhanh, rẻ, và ăn điểm R6 vì có "chỗ cụ thể để nói".

### P-003 — ⟨vai/nghề⟩  ·  Willing CP1: ⟨Có/Không⟩
| Task giao | Họ làm gì | Kẹt ở đâu | Quote nguyên văn | Quyết định |
|---|---|---|---|---|
| T1 · Việc gấp nhất + kênh nào | Mở được menu **🔍 Xem nguồn / ngữ cảnh** nhưng mất thời gian dò đúng mục | Ô search trong menu khó lọc — gõ không ra đúng task cần xem nguồn | *"phần tìm context lại hơi khó dùng, vì việc tìm task ở ô search khso"* | **ĐÃ SỬA (`bot.py`):** gắn link **[🔍 xem nguồn]** thẳng lên mỗi dòng (1 click, khỏi dò) → **bỏ hẳn menu 🔍**; ca ⚪ thêm dòng nhắc ⚠️ "bot không tự chốt" ngay trong embed |
| T2 · Deadline mâu thuẫn tin ai | (không hỏi/không ghi nhận riêng) | — | — | Bổ sung ở buổi sau để phủ ca ⚪ |
| T3 · Đánh dấu đã xong | (không hỏi/không ghi nhận riêng) | — | — | Bổ sung ở buổi sau |
| Câu mở | — | — | *(chưa hỏi)* | — |

> **Tổng P-003:** dùng được luồng xem nguồn nhưng vướng ở **thao tác chọn mục** — ô search của menu 🔍 khó lọc đúng task. Điểm kẹt về UX chọn mục, không phải về chức năng. → sửa tận gốc: **bỏ menu 🔍, đưa link xem nguồn lên thẳng mỗi dòng** (1 click).

### Người 4 — ⟨vai/nghề⟩  ·  Willing CP1: Không
| Task giao | Họ làm gì | Kẹt ở đâu | Quote nguyên văn | Quyết định |
|---|---|---|---|---|
| T1 | ⟨…⟩ | ⟨…⟩ | *"⟨…⟩"* | ⟨…⟩ |
| T2 | ⟨…⟩ | ⟨…⟩ | *"⟨…⟩"* | ⟨…⟩ |
| T3 | ⟨…⟩ | ⟨…⟩ | *"⟨…⟩"* | ⟨…⟩ |
| Câu mở | — | — | *"⟨…⟩"* | ⟨…⟩ |

### Người 5 — ⟨vai/nghề⟩  ·  Willing CP1: Không
| Task giao | Họ làm gì | Kẹt ở đâu | Quote nguyên văn | Quyết định |
|---|---|---|---|---|
| T1 | ⟨…⟩ | ⟨…⟩ | *"⟨…⟩"* | ⟨…⟩ |
| T2 | ⟨…⟩ | ⟨…⟩ | *"⟨…⟩"* | ⟨…⟩ |
| T3 | ⟨…⟩ | ⟨…⟩ | *"⟨…⟩"* | ⟨…⟩ |
| Câu mở | — | — | *"⟨…⟩"* | ⟨…⟩ |

---

## Kết luận (4 dòng bắt buộc — R6)
> **Tiến độ: đã test 3/5 người (P-001, P-002, P-003).** Cần thêm 2 người (trong đó đủ 2 Willing user đã khai CP1) trước khi chốt phần này ở CP5.

1. **Chủ đề lặp nhiều nhất (tạm tính 3/5):** vướng ở **trình bày / thao tác chọn**, không phải chức năng — P-002 nêu 3 điểm layout digest (3 nhóm dồn nhau, tóm tắt chữ nhỏ, các mục sát nhau); P-003 nêu ô search menu 🔍 khó lọc đúng task; P-001 không vướng gì. → cả 3 đều dùng được chức năng, tín hiệu kẹt tập trung ở UX bề mặt.
2. **Đã sửa (`bot.py`):** (a) layout embed digest — tách rõ 3 nhóm 🔴🟡⚪ (vạch ngăn ━━), đưa tóm tắt lên đầu in đậm, giãn cách giữa các mục (P-002); (b) gắn link **[🔍 xem nguồn]** thẳng lên mỗi dòng (1 click) → **bỏ hẳn menu 🔍**, ca ⚪ thêm dòng nhắc ⚠️ trong embed (P-003). → đã ghi vào `spec.md` §9 Changelog.
3. **Giữ nguyên gì & vì sao:** luồng 🔍 xem nguồn + ✅ đánh dấu đã xong — cả 2 người dùng được, P-001 thao tác trơn không cần hướng dẫn; nhu cầu "biết chính xác nguồn" đã được đáp ứng.
4. **Để dành sau:** kiểm chứng ca ⚪ "cần xác nhận" (ngôi sao sản phẩm) — 2 buổi này chưa phủ, ưu tiên hỏi ở các người test tiếp theo.

> **Nhắc:** R6 yêu cầu **ít nhất 1 thay đổi** ghi vào `spec.md` §9. Nếu quyết định giữ nguyên toàn bộ thì phải nêu rõ lý do có bằng chứng (như nhóm VLearn Recall kỳ trước — vẫn đủ điểm).
