# Task 6 — Xác nhận dữ liệu đầu vào thực nghiệm

**Kết quả:** Dùng lại `train.parquet` và `eval.parquet` ở thư mục gốc. Toàn bộ 4.850.000 dòng và 19 cột khớp với hai CSV đã kiểm tra ở Task 4, sau khi đọc CSV theo kiểu dữ liệu tương ứng. Đối chiếu bao gồm từng phần tử trong cả hai mảng 24 giờ.

| Tập | Số dòng | Cặp cửa hàng–sản phẩm | Số ngày mỗi cặp |
|---|---:|---:|---:|
| Train | 4.500.000 | 50.000 | 90 |
| Eval | 350.000 | 50.000 | 7 |

Hai tập có cùng danh sách cặp, không trùng khóa ngày. Giữ nguyên 34 dòng `discount` được gắn `REVIEW` ở Task 4. Mẫu từ hai cặp tạo được mảng TimesNet `(6, 480, 6)` và mảng đặc trưng số SSA `(2, 97, 3)`.

## Bàn giao

- [Notebook đã chạy và có output](notebooks/06_prepare_data.ipynb).
- [Biên bản đối soát và SHA-256 của bốn file nguồn](results/20261113T082302850933Z/run_info.md).
- [Bảng đối soát input_check.csv](results/20261113T082302850933Z/input_check.csv) có một dòng `PASS` cho mỗi tập. File dữ liệu đầy đủ lưu riêng; dùng mã SHA-256 trong biên bản để nhận diện đúng bản.

## Chạy lại trên Colab

1. Mở notebook và chạy ô kết nối Drive. Chỉnh `WORKSPACE`, `DATA_DIR` và `TASK4_DIR` trong ô cấu hình theo tên thư mục thực tế. `DATA_DIR` chứa cả hai CSV và hai Parquet cần đối soát; hai file kết quả Task 4 dùng để đối chiếu nguồn nếu có.
2. Chạy các ô còn lại bằng CPU. Đợi cả hai tập báo `PASS` và xem output kiểm tra kích thước mẫu.
3. Lấy bảng đối soát từ đường dẫn `Đã lưu kết quả` ở ô cuối. Mỗi lượt có một thư mục kết quả riêng.

Task 6 kiểm tra đầu vào và kích thước mẫu. Việc huấn luyện và dự báo bắt đầu ở các task tiếp theo.
