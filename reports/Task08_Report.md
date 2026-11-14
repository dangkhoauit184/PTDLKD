# Báo cáo Task 08: Dự báo nhu cầu bằng SSA trên dữ liệu doanh số gốc (`SSA_RawSales`)

## 1. Tóm tắt thiết lập thực nghiệm
- **Mô hình:** Similar Scenario Average (SSA) — phương pháp thống kê dựa trên trọng số khoảng cách thời gian, khuyến mãi, thứ trong tuần, ngày lễ và lượng mưa.
- **Dữ liệu đầu vào:** 90 ngày lịch sử từ tập `train.parquet` (4.500.000 dòng) và 7 ngày kiểm thử từ `eval.parquet` (350.000 dòng) cho 50.000 cặp cửa hàng–sản phẩm.
- **Tiêu chuẩn đánh giá:** Lọc 206.562 dòng không hết hàng từ 06:00 đến trước 22:00 (`stock_hour6_22_cnt == 0`). Tính chỉ số riêng cho từng ngày, sau đó lấy trung bình qua 7 ngày.

## 2. Kết quả định lượng và Đối chiếu Bảng 3
| Phân nhóm | Điều kiện `psd` | WAPE thực chạy | WPE thực chạy | MAE | WAPE bài báo | WPE bài báo | Chênh lệch |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | `psd >= 0` | 31.97% | -10.50% | 0.3982 | 31.97% | -10.50% | 0.00 pp |
| **Low Sale** | `psd < 1` | 38.33% | -8.03% | 0.2691 | 38.33% | -8.03% | 0.00 pp |
| **High Sale** | `psd >= 1` | 27.40% | -12.26% | 0.7761 | 27.40% | -12.26% | 0.00 pp |

## 3. Nhận xét
- WAPE và WPE của cả ba nhóm khớp Bảng 3 ở độ chính xác công bố, với chênh lệch 0,00 điểm phần trăm. MAE là chỉ số bổ sung do notebook tính.
- WPE âm ở cả ba nhóm cho thấy dự báo thấp hơn doanh số quan sát xét trên các dòng eval đủ điều kiện; nhóm High Sale có độ lệch âm lớn nhất (−12,26%). Riêng kết quả Task 8 chưa xác định nguyên nhân của độ lệch. Task 11 sẽ đối chiếu thêm SSA dùng đầu vào TimesNet theo cùng tập eval và cách tính chỉ số.

## 4. Bàn giao

[Notebook đã chạy](../Task08_SSA_Raw_Sales/notebooks/08_ssa_raw_sales.ipynb), [CSV ba nhóm](../Task08_SSA_Raw_Sales/results/ssa_raw_sales_metrics.csv), [log](../Task08_SSA_Raw_Sales/results/full/ssa_raw_sales.log) và [hướng dẫn tái lập](../Task08_SSA_Raw_Sales/run_info.md). Lượt chạy lại kiểm tra SHA-256 của cả hai Parquet theo Task 6 và khớp toàn bộ chỉ số với log đã merge.
