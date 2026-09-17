# Nhật ký quyết định — Prompt phân loại (`src/classify.py`)

> **Người phụ trách mảng `prompt` (spec.md §8):** Nguyễn Sơn Giang · `songiangvn` · 2A202602747
> File này ghi lại **vì sao prompt có hình dạng như hiện tại** — mỗi luật trong prompt ra đời từ một ca sai cụ thể đo được trên golden set.
> Phục vụ **luật vibe-coding (CP6):** người mang tên phải giải thích được phần của mình.
> File tài liệu — **không ảnh hưởng luồng chạy**. Số đo & kết luận chính thức: [`spec.md`](spec.md) §7.

---

## 1. Prompt này phải giải quyết bài toán gì

Model nhận **cả lô tin** (~25 tin/lần gọi) và phải trả về, cho từng tin: `bucket` · `deadline` · `source_channel` · `needs_confirm`.

Ràng buộc chi phối mọi lựa chọn bên dưới: **cost-of-error bất đối xứng**.

| Kiểu sai | Hậu quả với học viên |
|---|---|
| Bỏ sót 1 deadline thật | trễ hạn, mất XP |
| **Chốt liều 1 deadline sai** | học viên tin nhầm → làm sai hạn — **nặng hơn** |
| Đẩy nhầm 1 tin sang ⚪ | người đọc mất ~5 giây tự xác nhận — **rẻ nhất** |

→ Nguyên tắc xuyên suốt: **khi lăn tăn thì hỏi lại, không đoán liều.** Đây chính là automation *conditional* ở §4 spec, và nó là lý do tồn tại của luật cuối trong prompt: *"Khi không chắc, ưu tiên 'confirm' + needs_confirm=true thay vì đoán liều."*

---

## 2. Ba luật trong prompt — mỗi luật sinh ra từ một ca sai thật

### Luật 1 · Ngưỡng ≤ 2 ngày (tách 🔴 do_now / 🟡 soon)

**Ca sai làm lộ vấn đề (lượt 1):** M01982 & M13092 đều có hạn 20/9. Mốc "hôm nay" là 14/9 → còn 6 ngày → đúng ra là `soon`. AI xếp cả hai vào `do_now`.

**Chẩn đoán:** AI **thiên "khẩn cấp"** — thấy chữ "Deadline"/"hạn cuối" là gán gấp, không thực sự trừ ngày.

**Sửa:** không chỉ nêu ngưỡng, mà **ép model tính trước rồi mới chọn**, kèm một ví dụ số cụ thể:

> `BẮT BUỘC tính số ngày trước khi chọn. Ví dụ: HÔM NAY 14/9, hạn 20/9 = còn 6 ngày > 2 → 'soon' (KHÔNG phải 'do_now'). Chỉ 'do_now' khi hạn ≤ 16/9 hoặc đã qua.`

Viết sẵn ngày biên (`≤ 16/9`) vào prompt để model khỏi phải tự suy ra — đây là chỗ nó hay trượt nhất.

**Kết quả:** `do_now` 2/3 → 3/3, `soon` 3/5 → 4/5 (lượt 1b → lượt 2).

**Ca còn sai đến giờ:** SYN03 hạn 16/9 = **đúng 2 ngày**, nằm ngay trên biên. Đây là ca biên giới đã biết, còn nằm trong 4 ca sai của lượt chốt — không giấu.

---

### Luật 2 · Đối chiếu cả lô để flag ⚪ (bài học đắt nhất)

**Bối cảnh:** ⚪ là **ngôi sao sản phẩm** — thứ bot BTC không có. Ca kinh điển: `M19124` (`channel_02`) *"a ơi sao deadline ghép đội tự do end sớm vậy a?"* ↔ `M50841` (`channel_11`) *"cửa sổ lập đội tự do đã đóng"*.

**Sự cố (lượt 2):** để chữa bệnh "over-eager" ở Luật 1, prompt siết luật `skip` mạnh tay. Tổng điểm lên 88% — **nhưng `confirm` gãy 2/2 → 0/2**. Tin M19124 bị đọc là "câu hỏi vu vơ" → skip; M50841 bị đọc là "thông báo bình thường" → skip.

**Đây là lượt duy nhất TRƯỢT quality bar** dù điểm tổng đẹp: bar yêu cầu *100% ca mâu thuẫn phải flag ⚪*. Xét theo giá trị sản phẩm, lượt 2 **tệ hơn** lượt 1b ở đúng chỗ khác biệt nhất.

**Nguyên nhân gốc:** phát hiện mâu thuẫn **không thể làm khi xử từng tin độc lập** — phải so 2 tin cùng chủ đề với nhau. Việc lượt 1 tình cờ được 2/2 chỉ là may.

**Sửa (lượt 3):** thêm luật đối chiếu phạm vi cả lô, và chặn thẳng đường thoát sang `skip`:

> `ĐỐI CHIẾU CẢ LÔ: nếu ≥2 tin nói KHÁC NHAU về cùng một mốc/việc, HOẶC một tin CHẤT VẤN/thắc mắc về một deadline trong khi tin khác nói mốc đó đã thay đổi/đóng → CẢ HAI tin = confirm. TUYỆT ĐỐI KHÔNG skip các tin này.`

Kèm một luật phân biệt tinh hơn: câu hỏi về deadline → `skip`, **trừ khi** nó chất vấn một deadline đang mâu thuẫn → `confirm`.

**Kết quả:** `confirm` hồi 2/2 và **giữ được 2/2 ở lượt chốt**. Đánh đổi: `skip` 21 → 20 — chấp nhận, vì flag mâu thuẫn là giá trị khác biệt số 1.

> **Bài học mang đi:** tối ưu điểm tổng có thể **giết đúng tính năng khác biệt nhất**. Phải đọc bảng theo từng bucket, không chỉ nhìn con số %.

---

### Luật 3 · `sent_at` ≠ deadline (bug bắt được khi chạy live)

**Ca sai:** lỗi này **không lộ ra trên golden set** — chỉ xuất hiện khi chạy bot thật trên server test. Tin tán gẫu như *"oke nhé"*, *"chia gì cơ"* bị nhét vào 🟡 với deadline = **giờ gửi tin**.

**Chẩn đoán:** input đưa cho model có trường `time=`, model hiểu nhầm đó là mốc hạn.

**Sửa hai tầng:**
1. **Đổi nhãn input** `time=` → `sent_at=` — làm rõ ngữ nghĩa ngay tại dữ liệu, không bắt prompt gánh hết.
2. **Luật cứng trong prompt:** *"'sent_at' là GIỜ GỬI tin, KHÔNG phải deadline. TUYỆT ĐỐI không dùng sent_at làm deadline. Chỉ trích deadline từ NỘI DUNG ('content')."* + liệt kê thẳng ví dụ phải skip (`"oke nhé"`, `"có"`, link, tag người).

**Kết quả:** `skip` đạt **21/22 — tốt nhất trong 4 lượt**, và bot live hết gán hạn bừa.

---

## 3. Hai quyết định về cách đo (không phải luật prompt, nhưng chi phối mọi con số)

### `temperature=0` — chọn số thật thay vì số đẹp

Trước lượt 4, `temperature` không được set → kết quả **nhảy 88–91% giữa các lần chạy cùng input**. Con số 91% ở lượt 3 là **một lần may, không tái lập được**.

Sau khi cố định `temperature=0`: ổn định **88%**, cùng input cho cùng điểm.

**Nhóm chốt lấy 88% để nộp, bỏ 91%.** Số thấp hơn nhưng tái lập được — nếu BGK bảo chạy lại tại chỗ thì ra đúng con số đó.

### `REFERENCE_NOW` — một đồng hồ chung cho AI và người

Việc tách `do_now`/`soon` phụ thuộc hoàn toàn vào "hôm nay là ngày nào". Nếu AI dùng ngày hệ thống còn người gán nhãn dùng ngày khác thì mọi phép so đều vô nghĩa.

| Ngữ cảnh | Giá trị | Vì sao |
|---|---|---|
| Chấm golden set | cố định `2026-09-14` (ngày cuối của data) | tái lập được — chạy lại tháng sau vẫn ra đúng số |
| Bot live | ngày thật, truyền qua env | digest không bị lệch ngày khi demo |

Cùng một mốc này được nhét vào **cả prompt AI lẫn hướng dẫn gán nhãn người** (`golden/labeling-guide.md`).

---

## 4. Bảng truy vết: luật → ca sai → kết quả

| Luật trong prompt | Sinh ra từ ca | Lượt | Bucket cải thiện |
|---|---|---|---|
| Ngưỡng ≤2 ngày + ví dụ tính ngày | M01982, M13092 xếp nhầm `do_now` | 2 | do_now 2/3→3/3 · soon 3/5→4/5 |
| Đối chiếu cả lô → `confirm` | M19124 ↔ M50841 bị skip mất | 3 | confirm 0/2→**2/2** |
| `sent_at` ≠ deadline + list skip | tin tán gẫu bị gán hạn = giờ gửi (bug live) | 4 | skip 20/22→**21/22** |
| `temperature=0` | điểm nhảy 88–91% không tái lập | 4 | ổn định tại **88%** |

---

## 5. Bốn ca còn sai ở lượt chốt — và vì sao chấp nhận được

Lượt 4: **28/32 = 88%**, `confirm` ⚪ 2/2.

| Ca | Sai thế nào | Đánh giá |
|---|---|---|
| M01982 (hạn 20/9) | ranh giới do_now/soon | sai **xếp nhóm**, không sai deadline — người dùng vẫn thấy đúng việc, đúng mốc |
| SYN03 (hạn 16/9) | đúng 2 ngày = ngay trên biên ngưỡng | ca biên đã biết, ngưỡng nào cũng có biên |
| M07416 (*"Hạn nộp Lab02"*, không mốc) | AI đẩy sang `confirm` thay vì `skip` | **over-confirm — sai về phía an toàn**: hỏi lại thay vì bịa mốc |
| (ca thứ 4) | spec §7 không nêu đích danh — cần đối chiếu `out/predictions.csv` của lượt 4 trước demo | **cần xác minh**, không đoán |

**Trong 3 ca đã truy được, không ca nào là "chốt sai một deadline"** — kiểu sai nguy hiểm nhất mà §5 spec gọi là *case đáng sợ nhất khi demo*. Hai ca còn lại nghiêng về phía thận trọng (over-confirm), đúng tinh thần *conditional*.

---

## 6. Nếu có thêm thời gian

- **Ngưỡng biên:** SYN03 cho thấy ca "đúng 2 ngày" mong manh. Cách chắc hơn: bắt model xuất `days_left` dạng số rồi để code so ngưỡng — chuyển việc quyết định biên từ prompt sang code.
- **Gom cụm chủ đề trước khi đối chiếu:** hiện luật ⚪ dựa vào việc cả 2 tin mâu thuẫn cùng nằm trong một lô 25 tin. Lô lớn hơn hoặc 2 tin cách xa nhau thì có thể sót.
- **Tách prompt khỏi code:** đưa `SYSTEM` ra file riêng để đổi luật mà không đụng logic.
