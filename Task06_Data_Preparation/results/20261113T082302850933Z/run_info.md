# Task 6 — Kết quả xác nhận đầu vào

**Kết luận: dùng lại hai file Parquet hiện có.** Đã đối chiếu đầy đủ 4.850.000 bản ghi × 19 cột với CSV, bao gồm từng phần tử trong hai danh sách 24 giờ. Không có khác biệt sau khi đọc và chuyển kiểu theo schema Parquet.

| Tập | Số dòng | Số cặp | Khoảng ngày | Khóa trùng | Cặp thiếu ngày | Mảng sai độ dài | Discount ngoài [0, 1] |
|---|---:|---:|---|---:|---:|---:|---:|
| train | 4.500.000 | 50.000 | 2024-03-28 đến 2024-06-25 | 0 | 0 | 0 | 34 |
| eval | 350.000 | 50.000 | 2024-06-26 đến 2024-07-02 | 0 | 0 | 0 | 0 |

Hai tập có cùng danh sách cặp và các khoảng ngày không giao nhau. Giữ nguyên tất cả giá trị discount đã được đánh dấu REVIEW.

- Mẫu TimesNet: (6, 480, 6), 6 đoạn 30 ngày từ 2 cặp; 586 giờ được đánh dấu NaN ở kênh doanh số.
- Mẫu SSA: (2, 97, 3), mỗi cặp gồm 90 ngày train và 7 ngày eval.
- Sắp xếp khóa trong bộ nhớ trước khi tạo mảng theo quy trình repo. Không ghi đè, chuyển đổi lại hoặc sao chép dữ liệu gốc.
- Task 6 dừng ở kiểm tra dữ liệu và kích thước; chưa huấn luyện hay dự báo.

## Nguồn và cách chạy lại

- Lượt kiểm tra (UTC): 2026-11-13T08:23:02.850933+00:00. Python 3.12.14, NumPy 2.3.5, PyArrow 26.0.1.
- Repo nhóm đối chiếu: da2e3ccd7e64bfc944c7b28d9c4c77e975e4fe05. Mã tác giả đối chiếu: 8af694a09a5a427d1d50648d348c022565a781f2.
- Mở 06_prepare_data.ipynb, chỉnh đường dẫn nếu cần, rồi chạy tất cả các ô. Đối soát theo lô; thứ tự dòng CSV và Parquet được kiểm tra qua từng khóa và giá trị.
- Metadata Task 4: Task04_Data_Validation/results/run_info.json. Kích thước và mtime đối chiếu ở dưới; mtime có thể đổi khi sao chép file giữa các môi trường.
- Bảng Task 4: Task04_Data_Validation/results/validation_summary.csv. Số dòng discount REVIEW khớp ở cả hai tập.

### train

- CSV: `train.csv` (1.212.821.860 byte).
  SHA-256: `cfdf8cdb1287d09fce4a63bedd0f66a951339f65acd2f985e7909c3a6958bea3`.
- PARQUET: `train.parquet` (61.075.680 byte).
  SHA-256: `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96`.
- CSV so với metadata Task 4: khớp dung lượng = True; khớp mtime = True.

### eval

- CSV: `eval.csv` (94.341.043 byte).
  SHA-256: `e2ef67662e450610d80a0b22f667ad8346f0bcb943649d64b279f49af2541288`.
- PARQUET: `eval.parquet` (5.451.872 byte).
  SHA-256: `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`.
- CSV so với metadata Task 4: khớp dung lượng = True; khớp mtime = True.

Các đường dẫn trong biên bản này tương đối với thư mục gốc dự án. Nếu dùng Drive, chọn hai bản có SHA-256 tương ứng hoặc chạy lại đối soát với dữ liệu trên Drive.
