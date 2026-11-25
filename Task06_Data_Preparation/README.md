# Task 6 — Xác nhận dữ liệu đầu vào thực nghiệm

**Kết quả:** Dùng lại `train.parquet` và `eval.parquet` ở thư mục gốc. Toàn bộ 4.850.000 dòng và 19 cột khớp với hai CSV đã kiểm tra ở Task 4, sau khi đọc CSV theo kiểu dữ liệu tương ứng. Đối chiếu bao gồm từng phần tử trong cả hai mảng 24 giờ.

| Tập | Số dòng | Cặp cửa hàng–sản phẩm | Số ngày mỗi cặp |
|---|---:|---:|---:|
| Train | 4.500.000 | 50.000 | 90 |
| Eval | 350.000 | 50.000 | 7 |

Hai tập có cùng danh sách cặp, không trùng khóa ngày. Giữ nguyên 34 dòng `discount` được gắn `REVIEW` ở Task 4. Mẫu từ hai cặp tạo được mảng TimesNet `(6, 480, 6)` và mảng đặc trưng số SSA `(2, 97, 3)`.

## Bàn giao

- **`train.parquet`** (`61.075.680` bytes, SHA-256 `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96`) và **`eval.parquet`** (`5.451.872` bytes, SHA-256 `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`) nằm trực tiếp ngay trong thư mục `Task06_Data_Preparation/` để toàn bộ thành viên dùng chung (chỉ cần `git pull` là có sẵn trên máy, không cần tải từ Google Drive).
- [Notebook đã chạy và có output](notebooks/06_prepare_data.ipynb).
- [Biên bản đối soát và SHA-256 của bốn file nguồn](results/20261113T082302850933Z/run_info.md).
- [Bảng đối soát input_check.csv](results/20261113T082302850933Z/input_check.csv) có một dòng `PASS` cho mỗi tập.

## Chạy lại trên Colab

1. Mở notebook và chạy ô kết nối Drive. Chỉnh `WORKSPACE`, `DATA_DIR` và `TASK4_DIR` trong ô cấu hình theo tên thư mục thực tế. `DATA_DIR` chứa cả hai CSV và hai Parquet cần đối soát; hai file kết quả Task 4 dùng để đối chiếu nguồn nếu có.
2. Chạy các ô còn lại bằng CPU. Đợi cả hai tập báo `PASS` và xem output kiểm tra kích thước mẫu.
3. Lấy bảng đối soát từ đường dẫn `Đã lưu kết quả` ở ô cuối. Mỗi lượt có một thư mục kết quả riêng.

Task 6 kiểm tra đầu vào và kích thước mẫu. Việc huấn luyện và dự báo bắt đầu ở các task tiếp theo.
