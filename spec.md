# AI SPEC — Priority Digest · Nhóm T009 · Zone E403
Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [x] Tối ưu tính năng có sẵn (thay con bot nhắc lịch của BTC)  [ ] Tính năng mới

> **Trạng thái: ĐÃ CHỐT CP4 · đang bổ sung validation R6 (CP5).** Quality bar (§7) đã khóa cứng lúc nộp CP4, không sửa sau. Chỗ `⟨…⟩` còn lại là phần điền nốt ở CP5.

## §1. User & Job
- **Job executor + workflow:** học viên khoá 4 (Build Phase), đầu ngày mở Discord thấy nhiều kênh quá tải (~1.092 tin/3 ngày ở 4 kênh; `channel_10` một mình 654 tin).
- **Core JTBD:** "Đầu ngày, cho tôi biết hôm nay tôi có việc/deadline gì và ở đâu, trong 1 phút, không phải đọc hết mọi kênh."
- **Problem statement (không chữ AI):** deadline & task nằm rải rác nhiều kênh, lẫn trong hàng trăm tin tán gẫu; con bot nhắc lịch hiện tại **trả sai** vì lệ thuộc Lab Coach cập nhật tay → bị cũ.
- **Evidence:**
  - Số liệu mining (nguồn `data/discord-pack/`): 1.092 tin/3 ngày; 779 tin người, 313 tin bot; 202 tác giả; `channel_10` một mình 654 tin.
  - **Tín hiệu deadline thưa & lẫn nhiễu** (đo trên mẫu golden set rút từ log): trong 26 tin thật, **chỉ 2 tin mang mốc deadline hành-động-được** (M01982, M13092); phần còn lại là câu hỏi / tán gẫu / vận hành → đúng nỗi đau "đãi cát tìm vàng", tự đọc tay không kịp mỗi sáng.
  - Baseline lỗi thật: bản tin bot BTC (`k4_daily_reports.md`) bịa/hỏng chữ ("nguồn tham chiếu" chèn loạn) và để lửng ca deadline mâu thuẫn ("chưa xác nhận đã xử lý").
  - **≥5 quote nguyên văn** (từ `golden/golden-set.csv`):
    1. **M01982** (`channel_10`): *"Gate 1 — Chốt đề tài active +100 XP / member · Deadline 23:59:00 20/9/2026"* → deadline rõ, trễ mất 100 XP.
    2. **M78917** (`channel_10`): *"Khung giờ daily standup để được cộng XP: 0h-10h sáng…"* → luật lặp, không mốc hạn.
    3. **M19124** (`channel_02`): *"a ơi sao deadline ghép đội tự do end sớm vậy a?"* ↔ **M50841** (`channel_11`): *"Các bạn chờ BTC ghép đội nhé, hiện tại cửa sổ lập đội tự do đã đóng"* → **mâu thuẫn liên kênh**.
    4. **M13092** (`channel_10`): *"Mốc quan trọng: 22:00 13/9 công khai ngân hàng đề tài; 23:59 20/9 hạn cuối đăng ký đề tài + hoàn thiện Gate 1."* → 2 mốc, phải chọn đúng mốc còn hiệu lực.
    5. **M56777** (`channel_10`): *"hạn thành lập team là ngày nào? team không đủ 4 người có bị giải tán không"* → **câu hỏi** về hạn, KHÔNG phải tuyên bố deadline.

## §2. Impact & quyết định chọn
- **Bảng impact ≥3 ứng viên:**

  | Ứng viên | Bao nhiêu người | Tần suất | Tốn gì mỗi lần (không có nó) | Khả thi trong hackathon |
  |---|---|---|---|---|
  | **(a) Priority Digest** — gom task/deadline nhiều kênh theo ưu tiên | Cả khoá (202 tác giả/3 ngày; ai cũng phải theo ≥4 kênh) | **Hằng ngày**, đầu ngày | Đọc tay hàng trăm tin để lọc ra 2–3 mốc → mất 5–10' hoặc **bỏ sót deadline → mất XP** | **Cao** — AI classify batch, có **baseline bot BTC** để đo hơn-kém bằng số |
  | (b) Bot Q&A FAQ — trả lời câu hỏi lặp | Người hỏi lại (một phần khoá) | Rải rác | Coach trả lặp; học viên chờ | Trung bình — cần grounding kiến thức, **dễ bịa**; **trùng đúng thứ bot BTC đang làm** → khó chứng minh khác biệt |
  | (c) Cảnh báo deadline tự động (ping) | Cả khoá | Theo mỗi deadline | Quên deadline | Thấp cho MVP — **nguồn deadline chưa đáng tin (rải rác + mâu thuẫn) → ping tự động dễ ping SAI**; cost-of-error cao |

- **Ứng viên ĐÃ LOẠI + vì sao:**
  - **(b)** loại: trùng phạm vi bot "Trợ lý" của BTC + factuality rủi ro cao, **không có baseline để đo mình hơn ở đâu**.
  - **(c)** loại: chính là **hệ quả** của (a) — muốn nhắc đúng thì trước hết phải **đọc đúng + flag được mâu thuẫn**; ping khi nguồn chưa sạch sẽ gây hại hơn. Đặt vào non-goal, để sau.
- **Ứng viên CHỌN:** **(a) Priority Digest** — nỗi đau "quá tải kênh" xảy ra **hằng ngày**, là **tiền đề** của (c), và là ứng viên **duy nhất có baseline (bot BTC) để đo hơn-kém bằng số**.

## §3. Giải pháp tương tự
- **Bot "Trợ lý" của BTC:** flow = tóm tắt ngày "học viên đang hỏi gì". **Đáng học** = định dạng bản tin ngày gọn, gom theo kênh. **Đáng né** = lệ thuộc người cập nhật tay → cũ/sai, và **bịa "nguồn tham chiếu"** (thấy trong `k4_daily_reports.md`). **Mình khác** = đọc thẳng tin gốc, mỗi mục **dẫn link tin nguồn**, ca mâu thuẫn **flag ⚪ thay vì chốt liều**.
- **Discord Catch Up / Summaries (tính năng ngay trên Discord):** flow = tóm tắt kênh/luồng chưa đọc, gợi ý luồng đáng xem. **Đáng học** = ở đúng nơi học viên đã chat, cho bấm nhảy về tin gốc. **Đáng né** = recap dạng văn xuôi "đang bàn gì", **không tách được "đây là deadline phải làm"** khỏi tán gẫu, và không cảnh báo khi hai tin **mâu thuẫn**. **Mình khác** = output **có cấu trúc theo ưu tiên hành động** (🔴 làm ngay / 🟡 sắp đến / ⚪ cần xác nhận), gắn mốc + kênh nguồn, flag ca mâu thuẫn.

## §4. Thiết kế
- **Lát cắt MỘT CÂU:** học viên gõ `/digest` → AI phân loại tin nhiều kênh → trả embed gom task/deadline theo ưu tiên (🔴/🟡/⚪), mỗi mục có deadline + kênh nguồn + link tin gốc.
- **Non-goals (≥3):** (1) không tự nhắc/ping tự động; (2) không maintain danh sách deadline nhập tay; (3) không trả lời Q&A tổng quát; (4) không chạy trên server BTC (chạy server test riêng); (5) **chưa gom "thay đổi lịch/phòng học"** — khảo sát cho thấy 60% muốn gom lịch, 55% muốn gom phòng, nhưng đây là **hướng mở rộng đã cân nhắc và chủ động cắt** để kịp scope CP3; lõi ưu tiên **task + deadline** (task 85–90%, deadline 60–70% muốn) mới là nỗi đau số 1.
- **Mức prototype:** [ ] Sketch [x] Mock+Working — UI/action row là mock (đã có ở CP2); **lõi phân loại là AI thật** (`src/classify.py`, OpenAI gpt-4o-mini).
- **Automation:** [ ] augment [x] conditional [ ] automate — **conditional**: khi tin mâu thuẫn/mơ hồ, AI KHÔNG tự chốt mà đẩy ⚪ "cần xác nhận" (cost-of-error cao: chốt sai deadline gây hại hơn là hỏi lại).
- **§4b. Nguyên tắc (HAX/PAIR):**
  | Nguyên tắc | Áp vào đâu |
  |---|---|
  | Make clear what the system can do | Embed ghi rõ "gom từ nhiều kênh theo ưu tiên" |
  | Show contextually relevant info | Mỗi mục kèm deadline + #kênh + **link xem nguồn ngay trên dòng (1-click, nhảy tin gốc)** |
  | Support efficient correction | Nút ✅ đánh dấu xong / 🙈 ẩn / ↩️ hoàn tác |
  | Convey uncertainty (⑤ scope) | Ca mâu thuẫn → ⚪ "cần xác nhận" thay vì đoán |

## §5. Kiểu lỗi — 4 lớp + kịch bản (≥8)

**4 lớp cụ thể hoá cho Priority Digest** (taxonomy guide §2.5 ①②③④):
- ① **Nguồn sự thật** — AI bịa deadline/task khi tin không nêu mốc.
- ② **Mơ hồ / thiếu thông tin** — mốc mơ hồ, biên giới ngưỡng, hay câu hỏi bị nhầm thành tuyên bố.
- ③ **Ngoài phạm vi / thẩm quyền** — user đòi digest làm việc nó không được phép (Q&A chung, tự chốt việc phải người quyết).
- ④ **Đặc thù domain** — sai là học viên **trễ deadline / mất XP / mất niềm tin** ngay.

| # | Tình huống cụ thể (case) | Lớp | Hành vi mong muốn | Nguyên tắc áp |
|---|---|---|---|---|
| 1 | M07416 *"Hạn nộp Lab02"* — nhắc hạn nhưng KHÔNG có mốc thời gian | ① | **Không bịa** mốc; không đưa vào 🔴/🟡 → bỏ (skip) | Factuality; PAIR *Errors* |
| 2 | M13092 — thông báo 2 mốc (13/9 đã qua + 20/9) | ① | Chỉ lấy **mốc còn hiệu lực** 20/9, bỏ mốc đã qua; không gộp bừa | Show contextually relevant info |
| 3 | M63574 *"workshop chủ nhật ngày mai"* — mốc mơ hồ | ② | **Không đoán ngày cứng**; hạ xuống ⚪ / bỏ, không gắn 🔴/🟡 liều | Convey uncertainty |
| 4 | M56777 *"hạn thành lập team là ngày nào?"* — câu HỎI | ② | Không coi câu hỏi là tuyên bố deadline → skip | Convey uncertainty; Mental Models |
| 5 | SYN03 hạn 16/9 (đúng 2 ngày) — **biên giới** do_now/soon | ② | Áp đúng ngưỡng ≤2 ngày → `do_now`, nhất quán mọi lần chạy | Định nghĩa kiểm chứng được (§7) |
| 6 | M77476 *"xem bảng xếp hạng XP kiểu gì"* / M03059 *"hỗ trợ giấy tờ"* — Q&A chung | ③ | Ngoài phạm vi digest → không trả lời, bỏ khỏi danh sách task | Make clear what the system can do |
| 7 | User muốn bot **tự chốt** deadline khi tin mâu thuẫn | ③ | Bot **không có thẩm quyền chốt** → đẩy ⚪ "cần người xác nhận" | Convey uncertainty; automation *conditional* |
| 8 | **M19124 ↔ M50841** — mâu thuẫn deadline ghép đội, 2 kênh | ④ | **Flag ⚪**, link cả 2 tin gốc, **KHÔNG chốt liều** (ngôi sao sản phẩm) | Support efficient correction; Explainability |
| 9 | M01982 — Gate 1 deadline 23:59 20/9 (trễ mất 100 XP) | ④ | Trích **đúng mốc + đúng kênh**, phân đúng bucket | Show contextually relevant info |
| 10 | Bug live: tin tán gẫu ("oke nhé") bị gán hạn = `sent_at` (giờ gửi) | ④ | Phân biệt `sent_at` ≠ deadline; tán gẫu/link/tag → skip | Errors + Graceful Failure |

**Case đáng sợ nhất khi demo:** #8 — nếu bot chốt liều một phía của ca mâu thuẫn, học viên làm sai deadline thật. Đây là lý do quality bar (§7) đặt **cổng cứng 100% ca mâu thuẫn phải flag ⚪**. Mỗi lớp ①②③④ đều có ≥2 case tương ứng trong golden set.

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
- **Quality bar (🔒 ĐÃ CHỐT 17/9, không sửa sau):** *"Đạt khi ≥ **85%** golden set đúng theo tiêu chí khắt khe (bucket + deadline + kênh; ca mâu thuẫn = flag ⚪), **VÀ 100% ca mâu thuẫn được flag ⚪** (không chốt liều)."*
  > Căn cứ đặt bar: số ổn định lượt 4 = **88%** (còn biên) · baseline "đoán skip hết" = 22/32 = **69%** (bar phải cao hơn hẳn mới có ý nghĩa) · cổng cứng 100% flag ⚪ là điểm khác biệt an toàn không nhân nhượng.
  > **Kết quả hiện tại so bar:** 88% ≥ 85% ✅ · confirm 2/2 = 100% ✅ → **ĐẠT** (theo cấu hình lượt 4).
- **Kết quả các lượt chạy:**
  | Lượt | Ngày | Model | Đúng/Tổng | % | Ghi chú |
  |---|---|---|---|---|---|
  | 1 | 17/9 | gpt-4o-mini | 21/32 | 66% | lượt đầu, prompt gốc · matcher so chuỗi (dính artifact định dạng) |
  | 1b | 17/9 | gpt-4o-mini | 26/32 | 81% | **chỉ đổi cách chấm**: so deadline theo NGÀY (bỏ artifact format) — cùng output lượt 1 |
  | 2 | 17/9 | gpt-4o-mini | 28/32 | 88% | prompt nhấn ngưỡng ≤2 ngày + luật skip · ⚠️ **confirm gãy 2/2 → 0/2** |
  | 3 | 17/9 | gpt-4o-mini | 29/32 | 91% | +luật đối chiếu mâu thuẫn → confirm hồi 2/2 (một lần chạy, chưa cố định temperature) |
  | 4 | 17/9 | gpt-4o-mini | 28/32 | **88%** | **CHỐT** · +luật "sent_at≠deadline" & bỏ tán gẫu (sửa bug live) · `temperature=0` → **tái lập được** |

  **So sánh theo bucket:**
  | bucket | Lượt 1b | Lượt 2 | Lượt 3 | Lượt 4 (chốt) |
  |---|---|---|---|---|
  | do_now | 2/3 | 3/3 | 3/3 | 2/3 |
  | soon | 3/5 | 4/5 | 4/5 | 3/5 |
  | skip | 19/22 | 21/22 | 20/22 | **21/22** |
  | confirm ⚪ | 2/2 ✅ | 0/2 ❌ | 2/2 ✅ | **2/2** ✅ |
  | **Tổng** | 81% | 88% | 91%* | **88%** |

  *91% (lượt 3) là **một lần chạy may** khi chưa set temperature → không tái lập. Sau khi cố định `temperature=0`, số ỔN ĐỊNH là **88%** — đây là con số trung thực để nộp.

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
- **Phân tích lượt 4 (CHỐT — 88%, tái lập được):** phát hiện khi chạy bot LIVE trên server thật: AI nhầm `sent_at` (giờ gửi tin) thành deadline → gán cả tin tán gẫu ("oke nhé", "chia gì cơ") vào 🟡 với hạn = giờ gửi. Sửa:
  - **Prompt cứng thêm:** (a) *"sent_at là giờ gửi, KHÔNG phải deadline; chỉ trích hạn từ content"*; (b) liệt kê tán gẫu/link/tag → skip. Đổi nhãn input `time=` → `sent_at=` cho rõ.
  - **`temperature=0`:** trước đó không set → kết quả nhảy 88–91% giữa các lần (91% ở lượt 3 là **một lần may, không tái lập**). Sau khi cố định → **ổn định 88%**, cùng input cho cùng điểm.
  - **Kết quả chốt:** 28/32 = **88%** · **confirm ⚪ 2/2** (giữ ngôi sao, thoả điều kiện lõi quality bar) · skip **21/22** (tốt nhất) · 4 ca sai còn lại đều ở ranh giới do_now/soon (M01982, SYN03) hoặc over-confirm an toàn (M07416) — không phải chốt sai deadline.
  - **Kết luận:** dùng **cấu hình lượt 4** làm bản demo/nộp. Số nộp CP3 = **28/32 (88%)** — thấp hơn 91% nhưng **trung thực + tái lập được + bot live chạy đúng**. Đây là lựa chọn kỹ thuật đúng, không chạy theo con số đẹp một lần.

## §8. Phân công & kế hoạch
- **Phân công có tên:**
  | Mảng | Người phụ trách | Việc cụ thể |
  |---|---|---|
  | **spec** | **Lê Tuấn Anh** (đội trưởng) | Viết & chốt `spec.md` §1–§9, giữ quality bar, changelog; điều phối nhóm |
  | **evidence** | **Nguyễn Ngọc Thái An** | Mining `discord-pack`, rút 5 quote thật, dựng bảng impact §2, đối chiếu baseline bot BTC |
  | **prompt** | **Nguyễn Sơn Giang** | Thiết kế & tinh chỉnh prompt phân loại (`src/classify.py`): ngưỡng ≤2 ngày, luật flag ⚪, luật `sent_at`≠deadline |
  | **code** | **Vũ Thường Tín** | `classify.py` (gọi AI) · `evaluate.py` (bảng %) · `bot.py` (bot live) · matcher chấm điểm |
  | **demo** | **Lê Tuấn Anh** + **Nguyễn Sơn Giang** | Dựng server test Discord, nạp tin mẫu (`CP3-seed-messages.md`), quay video 30s CP3 |

  *(Vibe-coding rule CP6: mỗi người phải giải thích được phần mang tên mình.)*
- **Willing users (≥2):** người ngoài nhóm đã dùng thử, định danh **ẩn danh** là `P-001` · `P-002` · `P-003` (vai/nghề + task + quote nguyên văn ở `validation/nhat-ky-validation.md`). **Không công khai tên thật trong repo** (yêu cầu bảo mật); bảng ánh xạ mã↔người giữ riêng ngoài repo, xuất trình khi giám khảo cần. Người thật, quote nguyên văn — **không bịa**.
- **Multi-prototype (nếu làm):** so gpt-4o-mini vs gpt-4o trên cùng golden set → 2 dòng số.

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| CP3 · 17/9 | Khởi tạo spec + golden set 25 case + lõi classify gpt-4o-mini | Chốt luồng sau grill |
| CP3 · 17/9 | Mở rộng golden set 25→32 (thêm 6 tin synthetic phủ do_now/soon) + chốt mốc "hôm nay"=14/9, ngưỡng ≤2 ngày | Data thật thiếu ca do_now & chỉ 1 deadline |
| CP3 · 17/9 | Chạy lượt 1: 21/32 (66%) · bucket 81% · deadline-ngày 8/8 · confirm 2/2 | Số đo thật để đặt quality bar ở CP4 |
| CP3 · 17/9 | Lượt 2: matcher so deadline theo ngày + prompt nhấn ngưỡng/skip → 28/32 (88%) NHƯNG confirm gãy 2/2→0/2 | Tinh chỉnh; lộ đánh đổi giữa "bớt over-eager" và "giữ flag mâu thuẫn" |
| CP3 · 17/9 | Lượt 3: +luật đối chiếu mâu thuẫn → 29/32 (91%), confirm hồi 2/2 | Một lần chạy may, chưa cố định temperature |
| CP3 · 17/9 | Lượt 4 (CHỐT): sửa bug live "sent_at≠deadline" + bỏ tán gẫu + `temperature=0` → **28/32 (88%) ổn định**, confirm 2/2 | Bot live nhầm giờ gửi thành hạn; ưu tiên đúng + tái lập hơn con số đẹp một lần |
| CP3 · 17/9 | 🔒 Khóa Quality bar = **≥85% + 100% flag ⚪** | Chốt chuẩn "đạt" trước 21:00; căn theo số ổn định 88% và baseline 69% |
| CP5 · validation R6 (17/9) | Test người ngoài dùng thử 3/5 (P-001·P-002·P-003 — chi tiết `validation/`): P-001 thao tác trơn, tự dùng được xem nguồn + ✅ đánh dấu không cần hướng dẫn; P-002 góp ý **trình bày embed digest**. **ĐÃ SỬA `bot.py`:** (a) tách rõ 3 nhóm 🔴🟡⚪ (vạch ngăn ━━), (b) đưa tóm tắt lên đầu embed in đậm, (c) giãn cách giữa các mục | Feedback lặp về layout, sửa nhanh & rẻ trước demo |
| CP5 · validation R6 (17/9) | **P-003 kẹt: khó tìm đúng task ở ô search menu 🔍.** ĐÃ SỬA `bot.py`: gắn link **[🔍 xem nguồn]** thẳng lên mỗi dòng (xem context 1 click) → **bỏ hẳn menu 🔍**; ca ⚪ thêm dòng nhắc ⚠️ "bot không tự chốt" ngay trong embed | Xem nguồn qua menu bắt user dò lại task đã hiện trên embed → thừa thao tác; link inline giải quyết tận gốc |
