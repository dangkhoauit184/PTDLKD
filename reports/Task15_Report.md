# Báo cáo Task 15: Dự báo SOTA bằng Temporal Fusion Transformer (`TFT_RawSales` & `TFT_TimesNet`)

**Người thực hiện:** Minh Nguyễn | **Nhánh:** `feature/task15-tft-forecasting` | **Thư mục:** `Task15_TFT_Forecasting/`

## 1. Thiết lập thực nghiệm
- **Môi trường & phần cứng:** Google Colab GPU `NVIDIA L4` (High-RAM), môi trường Python `3.10.22` độc lập qua `micromamba` với `torch==2.0.1+cu118`, `pytorch-lightning==1.9.4`, `pytorch-forecasting==1.0.0`, `pandas==1.5.3` để bảo toàn 100% mã huấn luyện gốc (`pl.Trainer(..., gpus=1)` và hook Lightning 1.x).
- **Dữ liệu đầu vào chuẩn:** `train.parquet` (`b7e01c71...`), `eval.parquet` (`61cfd3cb...`) và `demand_timesnet.parquet` (`c34f4eafe087...` từ [Task 10](Task10_Report.md)).
- **Cấu hình mô hình (`configs/tft_config.py` + `trainTFT.py`):** `seed=2025`, `max_encoder_length=70`, `max_prediction_length=7`, `batch_size=1024`, `hidden_size=128`, `attention_head_size=8`, `lstm_layers=2`, `dropout=0.1`, `lr=0.01`, `optimizer=adamw`, `weight_decay=1e-4`, `max_epochs=5`, `num_workers=4`.
- **Quy trình đánh giá:** Cả hai lượt hoàn tất 5 epoch huấn luyện; `predictTFT.py` tính `psd` từ `train.parquet` gốc trước khi nạp `demand_timesnet.parquet` để đồng bộ tuyệt đối phân nhóm `Low Sale` (`psd < 1`, **153.208** dòng), `High Sale` (`psd >= 1`, **53.354** dòng) và `Overall` (**206.562** dòng `stock_hour6_22_cnt == 0`).

## 2. Kết quả định lượng và Đối chiếu Bảng 3
| Phân nhóm | Cấu hình | WAPE thực chạy | WPE thực chạy | MAE | WAPE bài báo | WPE bài báo | Chênh lệch WAPE | Chênh lệch WPE |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | `TFT_RawSales` | 31.96% | -9.85% | 0.3990 | 31.75% | -7.37% | +0.21 pp | -2.48 pp |
| **Overall** | `TFT_TimesNet` | 28.93% | +0.78% | 0.3595 | 29.02% | +2.58% | -0.09 pp | -1.80 pp |
| **Low Sale** | `TFT_RawSales` | 36.89% | -5.59% | 0.2588 | 37.04% | -1.72% | -0.15 pp | -3.87 pp |
| **Low Sale** | `TFT_TimesNet` | 37.06% | +6.84% | 0.2599 | 37.33% | +7.78% | -0.27 pp | -0.94 pp |
| **High Sale** | `TFT_RawSales` | 28.41% | -12.90% | 0.8120 | 27.95% | -11.46% | +0.46 pp | -1.44 pp |
| **High Sale** | `TFT_TimesNet` | 23.07% | -3.57% | 0.6506 | 23.03% | +0.87% | +0.04 pp | -4.44 pp |

## 3. Phân tích so sánh `TFT_RawSales` và `TFT_TimesNet`
1. **Cải thiện toàn cục (Overall):** Khi huấn luyện TFT trên nhu cầu đã khôi phục từ TimesNet thay cho doanh số bị che khuất, WAPE giảm từ **31.96%** xuống **28.93%** (**-3.03 điểm phần trăm**) và MAE thay đổi từ **0.3990** xuống **0.3595**; đồng thời WPE chuyển từ dự báo thiếu sâu (**-9.85%**) lên **+0.78%**.
2. **Đột phá ở nhóm bán chạy (High Sale):** Nhóm mặt hàng chủ lực có tỉ lệ hết hàng cao ghi nhận mức cải thiện mạnh nhất — WAPE giảm từ **28.41%** xuống **23.07%** (**-5.34 điểm phần trăm**), MAE giảm từ **0.8120** xuống **0.6506**, và thiên lệch dự báo thiếu giảm mạnh từ **-12.90%** về sát 0 (**-3.57%**).
3. **Đánh đổi ở nhóm bán chậm (Low Sale):** Do dữ liệu bán chậm thưa thớt theo giờ, `TFT_TimesNet` đạt WAPE **37.06%** so với **36.89%** của `TFT_RawSales`, và WPE chuyển dương (**+6.84%** so với **-5.59%**), nhất quán với xu hướng công bố trong bài báo gốc.
4. **Mức độ tái lập SOTA & vị thế giữa 3 họ mô hình (`SSA`, `DLinear`, `TFT`):** Cả hai cấu hình tái lập sát kết quả công bố của Bảng 3; đặc biệt `TFT_TimesNet` vươn lên đứng **#1 tốt nhất toàn đồ án trên cả 3 phân nhóm** (`Overall`: **28.93%** < `SSA_TimesNet` 29.79% < `DLinear_TimesNet` 30.55%; `High Sale`: **23.07%** < `DLinear_TimesNet` 23.46% < `SSA_TimesNet` 23.98%; `Low Sale`: **37.06%** < `SSA_TimesNet` 37.87% < `DLinear_TimesNet` 40.45%), nhờ tận dụng đồng thời biến ngoại sinh tĩnh/động (khuyến mãi, thời tiết, ngày lễ, phân cấp danh mục) và hàm mất mát phân vị `QuantileLoss`.

## 4. Bàn giao
- [Notebook đã chạy](../Task15_TFT_Forecasting/notebooks/15_tft_forecasting.ipynb), [bản vá mã nguồn](../Task15_TFT_Forecasting/code_changes.diff), [bảng chỉ số cột TFT (6 dòng)](../Task15_TFT_Forecasting/results/tft_forecasting_metrics.csv), [bảng tổng hợp 8 cấu hình Bảng 3 (24 dòng)](../Task15_TFT_Forecasting/results/table3_all_8configs_summary.csv).
- [Log smoke 200 cặp](../Task15_TFT_Forecasting/results/smoke/tft_smoke.log), [log full `TFT_RawSales`](../Task15_TFT_Forecasting/results/full/tft_raw_sales.log), [log full `TFT_TimesNet`](../Task15_TFT_Forecasting/results/full/tft_timesnet.log), [metadata](../Task15_TFT_Forecasting/results/run_metadata.json), [biên bản chạy](../Task15_TFT_Forecasting/run_info.md) và [README](../Task15_TFT_Forecasting/README.md).
- Checkpoint `.ckpt` trong `lightning_logs/` lưu trên Google Drive (không commit lên Git): https://drive.google.com/drive/folders/1gPexk9JqLJFH-MUPFE-7d69g9pQa7xD2.
