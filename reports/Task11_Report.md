# Báo cáo Task 11: Dự báo nhu cầu bằng SSA trên dữ liệu khôi phục TimesNet (`SSA_TimesNet`)

**Người thực hiện:** Sinhvienvuitinh (`TRILE1603`) | **Nhánh:** `feature/task11-ssa-timesnet` | **Thư mục:** `Task11_SSA_TimesNet/`

## 1. Thiết lập thực nghiệm
- **Đầu vào lịch sử (90 ngày `train`):** Sử dụng cột nhu cầu ngày đã khôi phục `sale_amount_pred` từ tệp `demand_timesnet.parquet` của [Task 10](Task10_Report.md) (`4.500.000` dòng × `20` cột, SHA-256: `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`).
- **Đầu vào đối chiếu (7 ngày `eval`):** Sử dụng doanh số quan sát thực tế `sale_amount` trên tập `eval.parquet` chuẩn của [Task 6](Task06_Report.md) (`350.000` dòng × `19` cột, SHA-256: `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`), lọc đúng **206.562** dòng không hết hàng trong khung giờ kinh doanh (`stock_hour6_22_cnt == 0`) làm Ground Truth.
- **Phân nhóm sản phẩm đồng bộ 100% với Task 8:** Tính `psd` từ doanh số gốc `sale_amount` của tập `train` (`dt <= '2024-06-25'`), bảo đảm tập mẫu của `Low Sale` (`psd < 1`, **153.208** dòng) và `High Sale` (`psd >= 1`, **53.354** dòng) trùng khớp tuyệt đối với [Task 8](Task08_Report.md).

## 2. Kết quả định lượng và Đối chiếu Bảng 3
| Phân nhóm | Cấu hình | WAPE thực chạy | WPE thực chạy | MAE | WAPE bài báo | WPE bài báo | Chênh lệch WAPE | Chênh lệch WPE |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | `SSA_RawSales` (Task 8) | 31.97% | -10.50% | 0.3982 | 31.97% | -10.50% | 0.00 pp | 0.00 pp |
| **Overall** | `SSA_TimesNet` (Task 11) | **29.79%** | **+1.40%** | **0.3709** | 29.79% | +1.39% | **0.00 pp** | **+0.01 pp** |
| **Low Sale** | `SSA_RawSales` (Task 8) | 38.33% | -8.03% | 0.2691 | 38.33% | -8.03% | 0.00 pp | 0.00 pp |
| **Low Sale** | `SSA_TimesNet` (Task 11) | **37.87%** | **+4.96%** | **0.2656** | 37.87% | +4.89% | **0.00 pp** | **+0.07 pp** |
| **High Sale** | `SSA_RawSales` (Task 8) | 27.40% | -12.26% | 0.7761 | 27.40% | -12.26% | 0.00 pp | 0.00 pp |
| **High Sale** | `SSA_TimesNet` (Task 11) | **23.98%** | **-1.15%** | **0.6790** | 23.98% | -1.12% | **0.00 pp** | **-0.03 pp** |

## 3. Phân tích so sánh với Task 8 (`SSA_RawSales`)
1. **Độ chính xác tái lập so với Bảng 3:** WAPE thực chạy của `SSA_TimesNet` khớp tuyệt đối số công bố của bài báo (`0.00 pp`) trên cả ba nhóm (`29.79%`, `37.87%`, `23.98%`); WPE chỉ lệch `0.01–0.07 pp` do tính không tất định nhỏ trên GPU ở giai đoạn huấn luyện TimesNet (Task 10).
2. **Cải thiện độ chính xác dự báo (giảm WAPE và MAE):** Trên toàn bộ tập đánh giá (`Overall`), thay doanh số bị che khuất bằng nhu cầu khôi phục TimesNet giúp giảm WAPE từ **31.97%** xuống **29.79%** (**−2.18 điểm phần trăm**) và giảm MAE từ **0.3982** xuống **0.3709**. Mức cải thiện mạnh nhất diễn ra ở nhóm mặt hàng chủ lực **High Sale**: WAPE giảm từ **27.40%** xuống **23.98%** (**−3.42 điểm phần trăm**) và MAE giảm từ **0.7761** xuống **0.6790**.
3. **Triệt tiêu thiên lệch dự báo thiếu (Under-forecasting Bias):** Khi dự báo trực tiếp trên doanh số thô ở Task 8, WPE âm sâu ở mọi phân nhóm (`-10.50%` Overall, `-12.26%` High Sale) do thuật toán học nhầm các giờ hết hàng là nhu cầu bằng `0`. Sau khi khôi phục nhu cầu bằng TimesNet, WPE được kéo sát ngưỡng cân bằng `0` (`+1.40%` Overall và `-1.15%` High Sale), phá vỡ vòng lặp *hết hàng → dự báo thấp → nhập thiếu hàng*.

## 4. Bàn giao
- [Notebook đã chạy](../Task11_SSA_TimesNet/notebooks/11_ssa_timesnet.ipynb), [bảng chỉ số `SSA_TimesNet`](../Task11_SSA_TimesNet/results/ssa_timesnet_metrics.csv), [bảng đối chiếu song song Task 8 vs Task 11](../Task11_SSA_TimesNet/results/ssa_raw_vs_timesnet_comparison.csv), [log gốc](../Task11_SSA_TimesNet/results/full/ssa_timesnet.log), [metadata](../Task11_SSA_TimesNet/results/run_metadata.json) và [biên bản chạy](../Task11_SSA_TimesNet/run_info.md).
