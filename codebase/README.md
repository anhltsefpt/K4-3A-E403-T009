# Priority Digest — CP2 clickable mock

Prototype tĩnh cho checkpoint CP2 của Track B · B2. Mock chứng minh luồng trải nghiệm; chưa kết nối Discord và chưa gọi AI thật.

## Chạy mock

Cách nhanh nhất: mở trực tiếp `index.html` bằng trình duyệt.

Hoặc chạy local server:

```bash
cd codebase
python3 -m http.server 8000
```

Sau đó mở `http://localhost:8000`.

## Luồng demo chính

1. Bấm **Tạo bản tin hôm nay**.
2. Xem ba bước mô phỏng: phát hiện → kiểm tra nguồn → xếp ưu tiên.
3. Xem các mục **Cần làm ngay**, **Sắp đến hạn**, **Cần xác nhận**.
4. Bấm vào một task để xem lý do xếp hạng và tin nguồn.
5. Với deadline đã xác minh, bấm **Báo deadline sai** để thử correction flow.
6. Chuyển sang **Cần xác nhận** để xem cách hệ thống xử lý tin thiếu căn cứ.
7. Dùng thanh **Thử tình huống** ở cuối màn hình để mở case “Không có căn cứ”.

## Phạm vi mock và phần thật

| Thành phần | Trạng thái CP2 |
|---|---|
| Flow và tương tác trên giao diện | Hoạt động thật trong trình duyệt |
| Task/deadline | Fixture mô phỏng |
| Message `M07653`, `M72484` | Trích ngắn từ data pack, chỉ dùng làm tín hiệu chưa xác minh |
| Phân loại, confidence và xếp ưu tiên | Mock bằng JavaScript |
| Discord API | Chưa tích hợp |
| Lời gọi AI | Chưa tích hợp; sẽ thực hiện ở CP3 |

## Nguyên tắc thiết kế đã thể hiện

- Không trình bày câu hỏi của học viên như một deadline chính thức.
- Không chắc thì đưa vào **Cần xác nhận**, không đoán.
- Mỗi kết quả cho biết trạng thái nguồn và lý do xếp ưu tiên.
- Người dùng có thể mở nguồn hoặc báo deadline sai.
- Nội dung Discord được coi là dữ liệu, không phải chỉ thị cho hệ thống.
