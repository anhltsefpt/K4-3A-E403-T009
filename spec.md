# AI SPEC — Priority Digest · Nhóm T009 · Zone E403
Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [x] Tối ưu tính năng có sẵn (thay con bot nhắc lịch của BTC)  [ ] Tính năng mới

> **Trạng thái: BẢN NHÁP CP3 — chốt tại CP4 (21:00 17/9).** Chỗ `⟨…⟩` là phần nhóm phải điền. Quality bar (§7) chốt cứng lúc nộp CP4, sau đó không sửa.

## §1. User & Job
- **Job executor + workflow:** học viên khoá 4 (Build Phase), đầu ngày mở Discord thấy nhiều kênh quá tải (~1.092 tin/3 ngày ở 4 kênh; `channel_10` một mình 654 tin).
- **Core JTBD:** "Đầu ngày, cho tôi biết hôm nay tôi có việc/deadline gì và ở đâu, trong 1 phút, không phải đọc hết mọi kênh."
- **Problem statement (không chữ AI):** deadline & task nằm rải rác nhiều kênh, lẫn trong hàng trăm tin tán gẫu; con bot nhắc lịch hiện tại **trả sai** vì lệ thuộc Lab Coach cập nhật tay → bị cũ.
- **Evidence:**
  - Số liệu mining: 1.092 tin/3 ngày; 779 tin người, 313 tin bot; 202 tác giả (nguồn `data/discord-pack/`). ⟨bổ sung: đếm bao nhiêu tin chứa deadline, bao nhiêu bị hỏi lặp⟩
  - Baseline lỗi thật: bản tin bot BTC (`k4_daily_reports.md`) bịa/hỏng chữ ("nguồn tham chiếu" chèn loạn) và để lửng ca deadline mâu thuẫn ("chưa xác nhận đã xử lý").
  - ≥5 quote nguyên văn: M01982 (Gate 1 deadline 23:59 20/9), M78917 (khung giờ standup), M19124↔M50841 (mâu thuẫn deadline ghép đội), ⟨thêm 2⟩.

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên: ⟨điền: (a) Priority Digest, (b) bot Q&A FAQ, (c) cảnh báo deadline sắp tới — mỗi cái: bao nhiêu người · tần suất · tốn gì · khả thi⟩
- Ứng viên đã loại + vì sao: ⟨…⟩
- **Ứng viên CHỌN:** Priority Digest — chạm đúng nỗi đau "quá tải kênh" hằng ngày, và có baseline (bot BTC) để đo hơn-kém bằng số.

## §3. Giải pháp tương tự
- **Bot "Trợ lý" của BTC:** flow = tóm tắt ngày; **đáng né** = lệ thuộc người cập nhật → cũ/sai; **mình khác** = đọc thẳng tin gốc, có dẫn nguồn, flag mâu thuẫn.
- ⟨Sản phẩm 2: vd Slack "catch up up" / Reader digest⟩

## §4. Thiết kế
- **Lát cắt MỘT CÂU:** học viên gõ `/digest` → AI phân loại tin nhiều kênh → trả embed gom task/deadline theo ưu tiên (🔴/🟡/⚪), mỗi mục có deadline + kênh nguồn + link tin gốc.
- **Non-goals (≥3):** (1) không tự nhắc/ping tự động; (2) không maintain danh sách deadline nhập tay; (3) không trả lời Q&A tổng quát; (4) không chạy trên server BTC (chạy server test riêng); (5) **chưa gom "thay đổi lịch/phòng học"** — khảo sát cho thấy 60% muốn gom lịch, 55% muốn gom phòng, nhưng đây là **hướng mở rộng đã cân nhắc và chủ động cắt** để kịp scope CP3; lõi ưu tiên **task + deadline** (task 85–90%, deadline 60–70% muốn) mới là nỗi đau số 1.
- **Mức prototype:** [ ] Sketch [x] Mock+Working — UI/action row là mock (đã có ở CP2); **lõi phân loại là AI thật** (`src/classify.py`, OpenAI gpt-4o-mini).
- **Automation:** [ ] augment [x] conditional [ ] automate — **conditional**: khi tin mâu thuẫn/mơ hồ, AI KHÔNG tự chốt mà đẩy ⚪ "cần xác nhận" (cost-of-error cao: chốt sai deadline gây hại hơn là hỏi lại).
- **§4b. Nguyên tắc (HAX/PAIR):**
  | Nguyên tắc | Áp vào đâu |
  |---|---|
  | Make clear what the system can do | Embed ghi rõ "gom từ nhiều kênh theo ưu tiên" |
  | Show contextually relevant info | Mỗi mục kèm deadline + #kênh + link tin gốc |
  | Support efficient correction | Nút ✅ đánh dấu xong / 🙈 ẩn / ↩️ hoàn tác |
  | Convey uncertainty (⑤ scope) | Ca mâu thuẫn → ⚪ "cần xác nhận" thay vì đoán |

## §5. Kiểu lỗi — 4 lớp + kịch bản (≥8)
⟨điền bảng theo guide §2.5. Gợi ý các case đã có trong golden set:⟩
1. Tin có deadline rõ → phải trích đúng mốc + kênh (M01982).
2. Câu HỎI về deadline → không được coi là tuyên bố deadline (M56777).
3. Hai tin mâu thuẫn → phải flag ⚪, không chốt (M19124↔M50841).
4. Tin nhiễu/cá nhân → phải bỏ (M73161, M03059).
5. Mốc mơ hồ "chủ nhật ngày mai" → xử lý sao (M63574). 6–8: ⟨…⟩

## §6. Bốn đường đi của trải nghiệm
- **Happy path:** tin deadline rõ → 🔴/🟡 đúng nhóm + đúng mốc + đúng kênh.
- **Low-confidence (②):** mốc mơ hồ → hạ xuống ⚪ cần xác nhận.
- **Failure/không căn cứ (①):** không bịa deadline khi tin không nêu mốc → để trống.
- **Correction:** user bấm ✅/🙈 sửa digest tại chỗ.
- **Đòi ngoài phạm vi (③):** hỏi Q&A chung → ngoài phạm vi digest.
- **Case domain (④):** mâu thuẫn liên kênh → link cả 2 tin.

## §7. Kiểm thử
- **Chiều chất lượng:** "phân loại đúng + trích đúng deadline/kênh + flag đúng ca mâu thuẫn".
- **Golden set:** 32 case ở `golden/golden-set.csv` (26 tin thật + 6 tin synthetic `SYN*` đánh dấu rõ, để phủ ca do_now/soon mà data thật thiếu). Phân bố: do_now 3 · soon 5 · confirm 2 · skip 22. Gán nhãn mù trước khi chạy (`golden/labeling-guide.md`).
- **Mốc "hôm nay" (chốt):** phân biệt `do_now`/`soon` theo ngày giả định **14/9/2026** (ngày cuối của data). `do_now` = quá hạn hoặc còn **≤ 2 ngày**; `soon` = còn **> 2 ngày**. Mốc này nhét vào cả prompt AI (`REFERENCE_NOW` ở `src/classify.py`) lẫn nhãn người → cùng một đồng hồ, chấm điểm mới công bằng.
- **Quality bar (CHỐT tại CP4, giữ nguyên sau đó):** *"Đạt khi ≥ ⟨__⟩% golden set đúng theo tiêu chí khắt khe (bucket + deadline + kênh; ca mâu thuẫn = flag ⚪), VÀ 100% ca mâu thuẫn được flag ⚪ (không chốt liều)."*
  > Điền % sau khi chạy lượt 1 để đặt bar thực tế, NHƯNG phải chốt trước 21:00 17/9 và không sửa sau đó.
- **Kết quả các lượt chạy:**
  | Lượt | Ngày | Model | Đúng/Tổng | % | Ghi chú |
  |---|---|---|---|---|---|
  | 1 | 17/9 | gpt-4o-mini | 21/32 | 66% | lượt đầu, prompt gốc · matcher so chuỗi (dính artifact định dạng) |
  | 1b | 17/9 | gpt-4o-mini | 26/32 | 81% | **chỉ đổi cách chấm**: so deadline theo NGÀY (bỏ artifact format) — cùng output lượt 1 |
  | 2 | 17/9 | gpt-4o-mini | 28/32 | 88% | prompt nhấn ngưỡng ≤2 ngày + luật skip · ⚠️ **confirm gãy 2/2 → 0/2** |
  | 3 | 17/9 | gpt-4o-mini | **29/32** | **91%** | **+luật đối chiếu mâu thuẫn** → confirm hồi 2/2 · **cấu hình chốt** |

  **So sánh theo bucket:**
  | bucket | Lượt 1b | Lượt 2 | Lượt 3 (chốt) |
  |---|---|---|---|
  | do_now | 2/3 | **3/3** ✅ | **3/3** ✅ |
  | soon | 3/5 | **4/5** ✅ | **4/5** ✅ |
  | skip | 19/22 | 21/22 | 20/22 |
  | confirm ⚪ | 2/2 ✅ | **0/2** ❌ | **2/2** ✅ |
  | **Tổng** | 81% | 88% | **91%** |

- **Phân tích lượt 1 (vì sao 11 ca "sai"):** con số 66% bị kéo xuống bởi **lỗi định dạng**, không phải AI hiểu sai.
  - **Bóc tách theo nhóm giá trị:** bucket đúng **26/32 = 81%** · **trích deadline đúng NGÀY 8/8 = 100%** · **flag mâu thuẫn ⚪ 2/2 = 100%** (ngôi sao sản phẩm chạy đúng) · lọc nhiễu skip 19/22.
  - **7/11 ca "sai" là SAI ĐỊNH DẠNG, không sai nghĩa:** AI trích đúng ngày nhưng viết `23:59 14/9` còn nhãn ghi `23:59 14/09/2026`; matcher `deadline_match` so chuỗi "chứa nhau" nên trượt. → sản phẩm hiển thị vẫn đúng cho người dùng.
  - **4 ca sai THẬT (đáng học):** (1) M01982 & M13092 hạn 20/9 (còn 6 ngày) → AI xếp `do_now` thay vì `soon` — **AI thiên "khẩn cấp", chưa tôn trọng ngưỡng ≤2 ngày**; (2) SYN03 hạn 16/9 (đúng 2 ngày) → biên giới do_now/soon; (3) M22827/M07416/M41884 → AI thấy có ngày/chữ "hạn" là gắn task, trong khi người coi là skip (**AI over-eager**).
- **Phân tích lượt 2 (đánh đổi, KHÔNG phải thắng sạch):**
  - **Sửa cách chấm (lượt 1b) đóng góp lớn nhất:** 66% → 81% chỉ nhờ so deadline theo NGÀY. Đây là **sửa thước đo**, không phải AI giỏi lên — 7 ca trước bị trừ oan vì format.
  - **Prompt mới (lượt 2) lời phần này, lỗ phần kia:** fix được do_now (2/3→3/3), soon (3/5→4/5), skip (19→21) — AI hết "over-eager". NHƯNG luật skip mạnh tay khiến **cặp mâu thuẫn M19124/M50841 bị đẩy sang `skip`** (câu hỏi chất vấn deadline + tin "cửa sổ đã đóng" bị coi là thông báo) → **confirm 2/2 → 0/2**.
  - **⚠️ Hệ quả với Quality bar:** bar yêu cầu *"100% ca mâu thuẫn flag ⚪"*. Lượt 2 tuy 88% nhưng **TRƯỢT điều kiện lõi này** → xét theo giá trị sản phẩm, lượt 2 **tệ hơn** lượt 1b ở đúng chỗ khác biệt nhất.
  - **Nguyên nhân gốc:** phát hiện mâu thuẫn cần model **đối chiếu 2 tin cùng chủ đề**; prompt hiện xử từng tin nên "confirm" ở lượt 1 mang tính may rủi. Luật skip mới vô tình dập nó.
- **Phân tích lượt 3 (CHỐT — 91%):** thêm luật đối chiếu mâu thuẫn vào prompt (giữ matcher-theo-ngày + phần tốt của lượt 2).
  - **Đạt cả hai mục tiêu:** tổng **91%** (cao nhất) VÀ **confirm 2/2** → thoả điều kiện lõi của Quality bar *"100% ca mâu thuẫn flag ⚪"*. do_now 3/3, soon 4/5.
  - **3 ca sai còn lại đều "over-confirm" — sai về phía AN TOÀN:** M56777 (câu hỏi "hạn lập team là ngày nào?") và M07416 ("Hạn nộp Lab02" không mốc) và M13092 (thông báo 2 mốc 13/9+20/9) → AI đẩy sang `confirm` thay vì skip/soon. Tức khi lăn tăn, AI **hỏi lại thay vì đoán liều** — đúng tinh thần automation *conditional* (§4). Đây là kiểu sai **chấp nhận được** hơn nhiều so với chốt sai một deadline.
  - **Đánh đổi nhỏ:** skip 21→20 (đổi lấy confirm 0→2) — rất đáng, vì flag mâu thuẫn là giá trị khác biệt số 1.
  - **Kết luận:** dùng **cấu hình lượt 3** làm bản demo/nộp. Số nộp CP3 = **29/32 (91%)** theo tiêu chí khắt khe, deadline-theo-ngày.

## §8. Phân công & kế hoạch
- **Phân công có tên:** spec = ⟨⟩ · evidence = ⟨⟩ · prompt = ⟨⟩ · code = ⟨⟩ · demo = ⟨⟩
- **Willing users (≥2):** ⟨tên 1⟩, ⟨tên 2⟩ — khai từ CP1, cần cho khối R6 ở CP5.
- **Multi-prototype (nếu làm):** so gpt-4o-mini vs gpt-4o trên cùng golden set → 2 dòng số.

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| CP3 · 17/9 | Khởi tạo spec + golden set 25 case + lõi classify gpt-4o-mini | Chốt luồng sau grill |
| CP3 · 17/9 | Mở rộng golden set 25→32 (thêm 6 tin synthetic phủ do_now/soon) + chốt mốc "hôm nay"=14/9, ngưỡng ≤2 ngày | Data thật thiếu ca do_now & chỉ 1 deadline |
| CP3 · 17/9 | Chạy lượt 1: 21/32 (66%) · bucket 81% · deadline-ngày 8/8 · confirm 2/2 | Số đo thật để đặt quality bar ở CP4 |
| CP3 · 17/9 | Lượt 2: matcher so deadline theo ngày + prompt nhấn ngưỡng/skip → 28/32 (88%) NHƯNG confirm gãy 2/2→0/2 | Tinh chỉnh; lộ đánh đổi giữa "bớt over-eager" và "giữ flag mâu thuẫn" |
| CP3 · 17/9 | Lượt 3: +luật đối chiếu mâu thuẫn → 29/32 (91%), confirm hồi 2/2 · **chốt cấu hình này** | Đạt cả % cao lẫn 100% flag mâu thuẫn — thoả điều kiện lõi quality bar |
