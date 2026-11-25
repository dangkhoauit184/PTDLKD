# Đồ án IS403 — Tái lập & Mở rộng Thực nghiệm FreshRetailNet-50K

Đồ án phân tích bộ dữ liệu bán lẻ đồ tươi sống FreshRetailNet-50K và tái lập thực nghiệm quy trình nghiên cứu trong bài báo [FreshRetailNet-50K: A Stockout-Annotated Censored Demand Dataset for Latent Demand Recovery and Forecasting in Fresh Retail](https://arxiv.org/abs/2505.16319).

## Đồ án cần làm gì?

Khi một mặt hàng hết hàng, doanh số ghi nhận có thể bằng 0 dù khách vẫn muốn mua. Đây là hiện tượng **nhu cầu bị che khuất** (*demand censoring*, bản chất dữ liệu khuyết MNAR). Đồ án kiểm chứng quy trình hai giai đoạn của bài báo từ cơ sở cốt lõi đến mở rộng đa mô hình:

1. **Giai đoạn 1 — Khôi phục nhu cầu tiềm ẩn (Bảng 2):** Dùng **TimesNet** (mô hình chu kỳ 2D tốt nhất bài báo) và **DLinear** (baseline tuyến tính) khôi phục nhu cầu ở những giờ có nhãn hết hàng, đánh giá qua WAPE/WPE trên điểm thiếu nhân tạo (MNAR) và chỉ số tách rời **Decoupling Score ($\rho_{DS}$)** trên giờ hết hàng thực tế.
2. **Giai đoạn 2 — Dự báo nhu cầu 7 ngày kháng hết hàng (Bảng 3):** Cộng nhu cầu theo giờ thành nhu cầu ngày, sau đó huấn luyện và đánh giá cả **3 họ mô hình dự báo** của bài báo gồm **SSA** (thống kê kịch bản tương tự), **DLinear** (mạng học sâu tuyến tính phân rã chuỗi) và **TFT** (*Temporal Fusion Transformer* — SOTA của bài báo).
3. **Đối chứng thực nghiệm (8 cấu hình Bảng 3):** So sánh trực tiếp dự báo từ doanh số gốc (*Raw Sales*) với dự báo từ nhu cầu đã khôi phục (*TimesNet*, *DLinear*) trên cùng tập đánh giá **206.562** dòng không hết hàng (`stock_hour6_22_cnt == 0`) cho ba nhóm `Overall`, `Low Sale` và `High Sale`.
4. **Minh bạch học thuật:** Các số trong bài báo chỉ là số tham chiếu; một chỉ số chỉ được ghi nhận là kết quả của nhóm khi có lượt chạy thực tế, tệp log và bảng kết quả tương ứng.

## Tiến độ và phân công thực hiện (Task 1–15)

| Task | Phụ trách | Nội dung | Trạng thái | Sản phẩm / ghi chú |
|---|---|---|---|---|
| **1** | Nhóm chung | Đọc bài báo, giải thích vấn đề MNAR và chốt phạm vi tái lập | **Đã hoàn thành** | [Báo cáo Task 1](reports/Task01_Report.md), [tóm tắt bài báo](Task01_Paper_Review/docs/paper_summary.md), [bảng mục tiêu](Task01_Paper_Review/docs/replicated_tables_target.md) |
| **2** | Nhóm chung | Lập kế hoạch thực nghiệm, quy tắc đánh giá và cấu hình mô hình | **Đã hoàn thành** | [Báo cáo Task 2](reports/Task02_Report.md), [15 cấu hình dự báo](Task02_Experiment_Plan/docs/15_forecasting_configurations.md), [siêu tham số](Task02_Experiment_Plan/docs/model_hyperparameters.md) |
| **3** | Nhóm chung | Chuẩn bị môi trường và cách tải/chuyển dữ liệu sang Parquet | **Đã hoàn thành** | [Hướng dẫn Task 3](Task03_Environment_Setup/README.md), [script xuất Parquet](Task03_Environment_Setup/scripts/download_data.py), [báo cáo Task 3](reports/Task03_Report.md) |
| **4** | **Phạm Đăng Khoa** | Kiểm định chất lượng và logic dữ liệu train/eval | **Đã hoàn thành** | [Notebook kiểm định](Task04_Data_Validation/notebooks/04_data_validation_colab.ipynb), [báo cáo Task 4](reports/Task04_Report.md). Có 34 dòng train `REVIEW` do `discount > 1`; giữ nguyên dữ liệu gốc. |
| **5** | Nhóm chung | EDA và thống kê mô tả dữ liệu | **Đã hoàn thành** | Hai notebook trong [Task05_EDA/notebooks](Task05_EDA/notebooks/), [báo cáo Task 5](reports/Task05_Report.md), 8 biểu đồ tại `Task05_EDA/results/figures/`. |
| **6** | **Phạm Đăng Khoa** | Đối chiếu CSV–Parquet và xác nhận dữ liệu sẵn sàng cho thực nghiệm | **Đã hoàn thành** | [Notebook Task 6](Task06_Data_Preparation/notebooks/06_prepare_data.ipynb), [báo cáo](reports/Task06_Report.md), [biên bản và SHA-256](Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md). Xác nhận 4.500.000 dòng train và 350.000 dòng eval. |
| **7** | **Dương Trọng Toàn** | Chạy thử khép kín TimesNet → SSA trên tập nhỏ | **Đã hoàn thành** | [Notebook](Task07_Smoke_Test/07_smoke_test.ipynb), [chỉ số smoke](Task07_Smoke_Test/smoke_metrics.csv), [báo cáo](reports/Task07_Report.md), [biên bản](Task07_Smoke_Test/run_info.md) (100 cặp). |
| **8** | **Sinhvienvuitinh** | SSA trên doanh số gốc (`SSA_RawSales`) | **Đã hoàn thành** | [Notebook](Task08_SSA_Raw_Sales/notebooks/08_ssa_raw_sales.ipynb), [bảng kết quả](Task08_SSA_Raw_Sales/results/ssa_raw_sales_metrics.csv), [báo cáo](reports/Task08_Report.md). Khớp tuyệt đối Bảng 3 (`0,00 pp`). |
| **9** | **Khanh** | Đánh giá TimesNet với các điểm thiếu nhân tạo (MNAR) | **Đã hoàn thành** | [Notebook](Task09_TimesNet_MNAR/notebooks/09_timesnet_mnar.ipynb), [bảng kết quả](Task09_TimesNet_MNAR/results/mnar_metrics.csv), [báo cáo](reports/Task09_Report.md), [biên bản](Task09_TimesNet_MNAR/run_info.md). |
| **10** | **Minh Nguyễn** | Chạy TimesNet trên giờ hết hàng thực tế để khôi phục nhu cầu | **Đã hoàn thành** | [Notebook](Task10_TimesNet_Recovery/notebooks/10_timesnet_recovery.ipynb), [bảng Decoupling](Task10_TimesNet_Recovery/results/decoupling_metrics.csv), [báo cáo](reports/Task10_Report.md), [biên bản & link Drive](Task10_TimesNet_Recovery/run_info.md). Xuất `demand_timesnet.parquet`. |
| **11** | **Sinhvienvuitinh** | Chạy SSA trên nhu cầu TimesNet (`SSA_TimesNet`) và so sánh với Task 8 | **Đã hoàn thành** | [Notebook](Task11_SSA_TimesNet/notebooks/11_ssa_timesnet.ipynb), [chỉ số `SSA_TimesNet`](Task11_SSA_TimesNet/results/ssa_timesnet_metrics.csv), [bảng đối chiếu](Task11_SSA_TimesNet/results/ssa_raw_vs_timesnet_comparison.csv), [báo cáo](reports/Task11_Report.md). WAPE khớp Bảng 3 `0,00 pp` trên cả 3 nhóm. |
| **12** | **Khanh** | Khôi phục nhu cầu bằng `DLinear` (MNAR & thực tế) và xuất Parquet | **Đã hoàn thành** | [Notebook](Task12_DLinear_Recovery/notebooks/12_dlinear_recovery.ipynb), [MNAR CSV](Task12_DLinear_Recovery/results/dlinear_mnar_metrics.csv), [Decoupling CSV](Task12_DLinear_Recovery/results/dlinear_decoupling_metrics.csv), [báo cáo](reports/Task12_Report.md), [biên bản & link Drive](Task12_DLinear_Recovery/run_info.md). Xuất `demand_dlinear.parquet`. |
| **13** | **Phạm Đăng Khoa** | Chạy SSA trên nhu cầu DLinear (`SSA_DLinear`) và tổng hợp cột SSA | **Đã hoàn thành** | [Notebook](Task13_SSA_DLinear/notebooks/13_ssa_dlinear.ipynb), [chỉ số `SSA_DLinear`](Task13_SSA_DLinear/results/ssa_dlinear_metrics.csv), [tổng hợp 3 cấu hình SSA](Task13_SSA_DLinear/results/ssa_all_3configs_summary.csv), [báo cáo](reports/Task13_Report.md), [biên bản](Task13_SSA_DLinear/run_info.md). |
| **14** | **Dương Trọng Toàn** | Dự báo 7 ngày bằng mạng học sâu `DLinear` (3 cấu hình Bảng 3) | **Đang triển khai (đã đủ cả 3 tệp Parquet)** | Tạo `Task14_DLinear_Forecasting/`, chạy `DLinear_RawSales`, `DLinear_TimesNet` và `DLinear_DLinear` trên GPU T4; bàn giao `dlinear_forecasting_metrics.csv` (9 dòng), `code_changes.diff`, log và `reports/Task14_Report.md`. |
| **15** | **Minh Nguyễn** | Dự báo 7 ngày bằng mô hình SOTA `TFT` (2 cấu hình Bảng 3) | **Đang triển khai (đã đủ các tệp Parquet)** | Tạo `Task15_TFT_Forecasting/`, chạy `TFT_RawSales` và `TFT_TimesNet` trên GPU L4 High-RAM; bàn giao `tft_forecasting_metrics.csv` (6 dòng), `code_changes.diff`, log và `reports/Task15_Report.md`. |

Chi tiết phân công và lưu ý kỹ thuật nằm tại [docs/Task11-15_Phan_cong_chi_tiet.md](docs/Task11-15_Phan_cong_chi_tiet.md) và [docs/Task06-10_Phan_cong_chi_tiet.md](docs/Task06-10_Phan_cong_chi_tiet.md). Báo cáo tổng hợp tại [reports/Synthesis_Report.md](reports/Synthesis_Report.md).

## Kết quả nhóm đã tự chạy (Task 1–13)

### 1. Khôi phục nhu cầu tiềm ẩn — Đối chiếu Bảng 2 (Task 9, Task 10, Task 12)

| Hạng mục (Bảng 2) | Nhóm tự chạy | Tham chiếu bài báo | Chênh lệch |
|---|---:|---:|---:|
| **TimesNet** — WAPE / WPE (MNAR, Task 9) | 27,81% / +2,04% | 27,62% / +1,43% | +0,19 pp / +0,61 pp |
| **DLinear** — WAPE / WPE (MNAR, Task 12) | 30,32% / −14,38% | 29,99% / −1,28% | +0,33 pp / −13,10 pp |
| **Raw Sales** — Decoupling Score $\rho_{DS}$ (Task 10 & 12) | −0,5664 (−0,57) | −0,57 | 0,00 |
| **DLinear** — Decoupling Score $\rho_{DS}$ (Task 12) | −0,1512 (−0,15) | −0,16 | +0,01 |
| **TimesNet** — Decoupling Score $\rho_{DS}$ (Task 10) | +0,0699 (+0,07) | +0,07 | 0,00 |

### 2. Dự báo 7 ngày — Trọn bộ 3 cấu hình cột SSA Bảng 3 (Task 8, Task 13, Task 11)

Đánh giá đồng nhất trên **206.562** dòng `eval` không hết hàng (`stock_hour6_22_cnt == 0`, chia nhóm theo `psd` gốc: `Low Sale = 153.208` dòng, `High Sale = 53.354` dòng):

| Phân nhóm | Cấu hình | WAPE tự chạy | WPE tự chạy | MAE | WAPE bài báo | WPE bài báo | Lệch WAPE / WPE |
|---|---|---:|---:|---:|---:|---:|---:|
| **Overall** | `SSA_RawSales` (Task 8) | 31,97% | −10,50% | 0,3982 | 31,97% | −10,50% | 0,00 / 0,00 pp |
| **Overall** | `SSA_DLinear` (Task 13) | 30,12% | −0,58% | 0,3749 | 30,00% | −1,49% | +0,12 / +0,91 pp |
| **Overall** | `SSA_TimesNet` (Task 11) | **29,79%** | **+1,40%** | **0,3709** | 29,79% | +1,39% | 0,00 / +0,01 pp |
| **Low Sale** | `SSA_RawSales` (Task 8) | 38,33% | −8,03% | 0,2691 | 38,33% | −8,03% | 0,00 / 0,00 pp |
| **Low Sale** | `SSA_DLinear` (Task 13) | 38,00% | +3,69% | 0,2664 | – | – | – |
| **Low Sale** | `SSA_TimesNet` (Task 11) | **37,87%** | **+4,96%** | **0,2656** | 37,87% | +4,89% | 0,00 / +0,07 pp |
| **High Sale** | `SSA_RawSales` (Task 8) | 27,40% | −12,26% | 0,7761 | 27,40% | −12,26% | 0,00 / 0,00 pp |
| **High Sale** | `SSA_DLinear` (Task 13) | 24,46% | −3,64% | 0,6925 | – | – | – |
| **High Sale** | `SSA_TimesNet` (Task 11) | **23,98%** | **−1,15%** | **0,6790** | 23,98% | −1,12% | 0,00 / −0,03 pp |

Các cấu hình dự báo học sâu còn lại thuộc **Task 14 (`DLinear_*`)** và **Task 15 (`TFT_*`)** vẫn là mục tiêu tham chiếu từ bài báo cho tới khi hai lượt chạy hoàn tất.

## Dữ liệu và cách lấy các file Parquet chuẩn

Hai tệp gốc đã được đưa trực tiếp vào thư mục `Task06_Data_Preparation/` trong repo (chỉ cần `git pull` là có sẵn trên máy); riêng các tệp nhu cầu khôi phục đầu ra lưu trên Google Drive và đối soát bằng mã SHA-256:

- `Task06_Data_Preparation/train.parquet` (`4.500.000` dòng × `19` cột, có sẵn trong repo): SHA-256 `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96` ([biên bản Task 6](Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md)).
- `Task06_Data_Preparation/eval.parquet` (`350.000` dòng × `19` cột, có sẵn trong repo): SHA-256 `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872` ([biên bản Task 6](Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md)).
- `demand_timesnet.parquet` (`4.500.000` dòng × `20` cột, tải qua Google Drive): SHA-256 `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694` ([biên bản & link Google Drive Task 10](Task10_TimesNet_Recovery/run_info.md)).
- `demand_dlinear.parquet` (`4.500.000` dòng × `20` cột, tải qua Google Drive): SHA-256 `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b` ([biên bản & link Google Drive Task 12](Task12_DLinear_Recovery/run_info.md)).

Để tạo lại hai tệp gốc từ nguồn Hugging Face:

```bash
pip install datasets
python Task03_Environment_Setup/scripts/download_data.py
```

## Việc cần làm tiếp theo

1. **Dương Trọng Toàn (Task 14 — `Task14_DLinear_Forecasting/`):** Chạy đủ 3 cấu hình `DLinear_RawSales`, `DLinear_TimesNet` và `DLinear_DLinear` trên GPU T4 theo hướng dẫn tại [docs/Task11-15_Phan_cong_chi_tiet.md](docs/Task11-15_Phan_cong_chi_tiet.md).
2. **Minh Nguyễn (Task 15 — `Task15_TFT_Forecasting/`):** Chạy 2 cấu hình SOTA `TFT_RawSales` và `TFT_TimesNet` trên GPU L4 High-RAM.
3. **Tổng kết đồ án:** Hợp nhất đủ 8 cấu hình Bảng 3 vào [reports/Synthesis_Report.md](reports/Synthesis_Report.md) và hoàn thiện slide trình bày cuối kỳ.

## Quy ước báo cáo và tái lập

- Giữ nguyên dữ liệu gốc trong các lượt tái lập chính; ghi riêng mọi thay đổi hoặc lượt thử.
- Không đẩy các tệp nhị phân lớn (`.parquet`, `.npy`, `.ckpt`, `.pth`, `.pypots`) lên GitHub; lưu trên Google Drive và dẫn link kèm SHA-256 trong `run_info.md`.
- Với mọi lượt dự báo Bảng 3, biến phân nhóm `psd` bắt buộc tính từ `sale_amount` gốc trong `train` (`dt <= '2024-06-25'`) và chỉ đánh giá trên đúng `206.562` dòng `eval` có `stock_hour6_22_cnt == 0`.
- Tách kết quả `smoke` khỏi kết quả `full`. Lượt lỗi, chưa chạy hoặc ô bài báo không công bố số tham chiếu thì để trống tương ứng, tuyệt đối không điền số `0` thay cho giá trị thiếu.

## Liên kết nhanh

- [Phân công & lưu ý kỹ thuật chi tiết Task 11–15](docs/Task11-15_Phan_cong_chi_tiet.md)
- [Phân công chi tiết Task 6–10](docs/Task06-10_Phan_cong_chi_tiet.md)
- [Tổng quan dự án](docs/Project_Overview.md)
- [Hướng dẫn đóng góp Git](docs/Contribution_Guide.md)
- [Báo cáo tổng hợp](reports/Synthesis_Report.md)
- [Task 7 — Smoke Test](Task07_Smoke_Test/README.md)
- [Task 8 — `SSA_RawSales`](Task08_SSA_Raw_Sales/README.md)
- [Task 9 — `TimesNet` MNAR](Task09_TimesNet_MNAR/README.md)
- [Task 10 — `TimesNet` Recovery](Task10_TimesNet_Recovery/README.md)
- [Task 11 — `SSA_TimesNet`](Task11_SSA_TimesNet/README.md)
- [Task 12 — `DLinear` Recovery](Task12_DLinear_Recovery/README.md)
- [Task 13 — `SSA_DLinear` & Tổng hợp SSA](Task13_SSA_DLinear/README.md)
