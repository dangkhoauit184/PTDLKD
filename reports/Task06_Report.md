# Báo cáo Task 6 — Xác nhận dữ liệu đầu vào thực nghiệm

**Kết luận:** Dùng lại `train.parquet` và `eval.parquet` hiện có. Cả hai khớp toàn bộ với các file CSV đã kiểm tra ở Task 4. Không cần chuyển đổi lại dữ liệu.

## Dữ liệu và cách kiểm tra

Notebook đọc theo lô và đối chiếu từng dòng cùng thứ tự khóa `store_id`, `product_id`, `dt`. Sau khi đọc CSV theo kiểu dữ liệu của Parquet, notebook so sánh đủ 19 cột, bao gồm từng phần tử trong hai mảng 24 giờ. Notebook cũng kiểm tra khóa trùng, số ngày từng cặp, tập cặp giữa train và eval, và sự chồng lặp ngày giữa hai tập.

| Tập | Số dòng | Số cặp | Ngày mỗi cặp | Khoảng ngày | Dòng khác CSV–Parquet |
|---|---:|---:|---:|---|---:|
| Train | 4.500.000 | 50.000 | 90 | 28/03–25/06/2024 | 0 |
| Eval | 350.000 | 50.000 | 7 | 26/06–02/07/2024 | 0 |

Không có khóa trùng, chuỗi thiếu ngày hoặc mảng sai độ dài. Hai tập có cùng 50.000 cặp và không chồng lặp khóa ngày. 34 dòng `discount` ở trạng thái REVIEW của Task 4 vẫn được giữ nguyên.

## Kiểm tra đầu vào mô hình

- **TimesNet:** Hai cặp mẫu tạo 6 đoạn, mỗi đoạn 480 bước và 6 đặc trưng. Mặt nạ giờ hết hàng khớp với vị trí NaN ở kênh doanh số; 586 giờ được đánh dấu trên mẫu.
- **SSA:** Hai cặp mẫu tạo mảng đặc trưng số `(2, 97, 3)`, mỗi cặp có đủ 90 ngày train và 7 ngày eval theo thứ tự.

Task 6 xác nhận tính tương đương của các file đang dùng và kiểm tra cách dựng đầu vào trên mẫu. Kết quả này chưa đánh giá hiệu năng khôi phục hoặc dự báo.

## Bàn giao

- [Notebook đã chạy](../Task06_Data_Preparation/notebooks/06_prepare_data.ipynb) và [hướng dẫn chạy lại](../Task06_Data_Preparation/README.md).
- [Bảng đối soát hai tập](../Task06_Data_Preparation/results/20261113T082302850933Z/input_check.csv).
- [Biên bản, môi trường và SHA-256](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md) và [kết quả dạng JSON](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.json).

Các file dữ liệu đầy đủ lưu riêng. Dùng SHA-256 trong biên bản để nhận diện đúng hai bản Parquet đã kiểm tra. Bước kế tiếp là chạy thử theo [phân công Task 6–10](../docs/Task06-10_Phan_cong_chi_tiet.md).
