# Báo cáo Task 11: Dự báo nhu cầu bằng SSA trên dữ liệu khôi phục TimesNet (`SSA_TimesNet`)

## 1. Thiết lập thực nghiệm
- **Đầu vào:** Sử dụng cột nhu cầu khôi phục `sale_amount_pred` từ `demand_timesnet.parquet` (Task 10, SHA-256: `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`) cho 90 ngày lịch sử và giữ nguyên doanh số thực tế `sale_amount` trên tập `eval.parquet` (SHA-256: `678caca15afed20239f2ea79208856fe18dad17fd444472c7d7e930edfa685bd`, 206.562 dòng không hết hàng `stock_hour6_22_cnt == 0`) làm Ground Truth đánh giá.
- **Phân nhóm sản phẩm:** Tính `psd` từ doanh số gốc của tập train nhằm đảm bảo tập mẫu của hai nhóm `Low Sale` (`psd < 1`, 153.208 dòng) và `High Sale` (`psd >= 1`, 53.354 dòng) trùng khớp 100% với Task 8.

## 2. Kết quả định lượng và Đối chiếu Bảng 3
| Phân nhóm | Cấu hình | WAPE thực chạy | WPE thực chạy | MAE | WAPE bài báo | WPE bài báo | Chênh lệch WAPE | Chênh lệch WPE |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | `SSA_RawSales` (Task 8) | 31.97% | -10.50% | 0.3982 | 31.97% | -10.50% | 0.00 pp | 0.00 pp |
| **Overall** | `SSA_TimesNet` (Task 11) | 29.79% | +1.40% | 0.3709 | 29.79% | +1.39% | 0.00 pp | +0.01 pp |
| **Low Sale** | `SSA_RawSales` (Task 8) | 38.33% | -8.03% | 0.2691 | 38.33% | -8.03% | 0.00 pp | 0.00 pp |
| **Low Sale** | `SSA_TimesNet` (Task 11) | 37.87% | +4.96% | 0.2656 | 37.87% | +4.89% | 0.00 pp | +0.07 pp |
| **High Sale** | `SSA_RawSales` (Task 8) | 27.40% | -12.26% | 0.7761 | 27.40% | -12.26% | 0.00 pp | 0.00 pp |
| **High Sale** | `SSA_TimesNet` (Task 11) | 23.98% | -1.15% | 0.6790 | 23.98% | -1.12% | 0.00 pp | -0.03 pp |

## 3. Phân tích so sánh với Task 8 (`SSA_RawSales`)
1. **Cải thiện độ chính xác (giảm WAPE và MAE):** Trên toàn bộ tập dữ liệu (`Overall`), việc sử dụng dữ liệu khôi phục từ TimesNet giúp giảm sai số WAPE từ **31.97%** xuống còn **29.79%** (-2.18 điểm phần trăm) và MAE từ **0.3982** xuống **0.3709**. Mức cải thiện rõ rệt nhất nằm ở nhóm **High Sale** (WAPE giảm từ **27.40%** xuống **23.98%**, tương đương -3.42 điểm phần trăm; MAE giảm từ **0.7761** xuống **0.6790**) — nhóm sản phẩm bán chạy chịu ảnh hưởng nặng nề nhất bởi tình trạng hết hàng cục bộ.
2. **Triệt tiêu thiên lệch dự báo thấp (WPE):** Khi dùng doanh số thô ở Task 8, chỉ số WPE âm sâu ở mọi phân nhóm (`-10.50%` Overall, `-12.26%` High Sale) do mô hình học nhầm các giờ hết hàng là nhu cầu bằng 0. Sau khi khôi phục nhu cầu bằng TimesNet, WPE được kéo về sát ngưỡng cân bằng 0 (`+1.40%` Overall và `-1.15%` High Sale), giải quyết triệt để hiện tượng dự báo thiếu hụt hàng hóa.