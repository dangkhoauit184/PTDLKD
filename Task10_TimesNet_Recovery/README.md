# Task 10 — Khôi phục nhu cầu tiềm ẩn bằng TimesNet trên giờ hết hàng thực tế

## 1. Mục tiêu
Huấn luyện mô hình **TimesNet** (`--missing_rate 0`) trên toàn bộ tập `train` (`4.500.000` dòng, `50.000` cặp cửa hàng–sản phẩm × `90` ngày) để:
1. Khôi phục nhu cầu tại các giờ hết hàng thực tế trong khung `06:00–22:00`, tích lũy thành nhu cầu ngày `sale_amount_pred` và xuất tệp `demand_timesnet.parquet` làm đầu vào cho **Task 11 (`SSA_TimesNet`)**.
2. Tính chỉ số **Decoupling Score ($\rho_{DS}$)** cho doanh số gốc (`Raw Sales`) và nhu cầu khôi phục (`TimesNet`) để đối chiếu với **Bảng 2** của bài báo *FreshRetailNet-50K*.

## 2. Kết quả Decoupling Score ($\rho_{DS}$) và đối chiếu Bảng 2
| Phương pháp | Cột đánh giá | Thực chạy (log gốc) | Thực chạy (2 chữ số) | Bài báo (Bảng 2) | Chênh lệch |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Raw Sales** | `sale_amount` | `-0.566447` | **-0.57** | -0.57 | **0.00** |
| **TimesNet** | `sale_amount_pred` | `0.069918` | **+0.07** | +0.07 | **0.00** |

## 3. Kiểm định tệp đầu ra `demand_timesnet.parquet` (bàn giao cho Task 11)
- **Quy mô & cấu trúc:** `4.500.000` dòng × `20` cột (`19` cột gốc giữ nguyên + `sale_amount_pred`), dung lượng `81.562.029` bytes, SHA-256: `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`.
- **Toàn vẹn khóa & giá trị ([results/demand_file_check.csv](results/demand_file_check.csv)):** `0` khóa trùng, `0` khóa thiếu/thừa so với `train.parquet` của Task 6 (`SHA-256: b7e01c71...`), `0` giá trị thiếu/vô cực/âm ở `sale_amount_pred`; cột `sale_amount` và `hours_sale` gốc được bảo toàn tuyệt đối (`max_diff = 0.0`).
- **Liên kết Google Drive cho Task 11:** xem mục liên kết trong [run_info.md](run_info.md).

## 4. Cấu trúc thư mục
- [Notebook đã chạy](notebooks/10_timesnet_recovery.ipynb): xác minh SHA-256 đầu vào, huấn luyện 5 epoch trên GPU NVIDIA L4 (`84,66` phút), xuất Parquet, đối soát toàn vẹn và trích xuất chỉ số.
- [Bản ghi thay đổi mã nguồn](code_changes.diff): đồng bộ đọc `train.parquet` local, sắp xếp ổn định theo khóa `['store_id', 'product_id', 'dt']` và cố định `seed = 2024` theo kế hoạch Task 2.
- [Bảng điểm Decoupling](results/decoupling_metrics.csv) và [bảng kiểm định tệp nhu cầu](results/demand_file_check.csv).
- [Log huấn luyện & đánh giá đầy đủ](results/full/timesnet_recovery.log), [metadata JSON](results/run_metadata.json) và [biên bản chạy](run_info.md).
- [Báo cáo Task 10](../reports/Task10_Report.md).
