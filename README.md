# Đồ án IS403 — Tái lập FreshRetailNet-50K

Đồ án phân tích bộ dữ liệu bán lẻ đồ tươi sống FreshRetailNet-50K và tái lập một phần các thực nghiệm trong bài báo [FreshRetailNet-50K: A Stockout-Annotated Censored Demand Dataset for Latent Demand Recovery and Forecasting in Fresh Retail](https://arxiv.org/abs/2505.16319).

## Đồ án cần làm gì?

Khi một mặt hàng hết hàng, doanh số ghi nhận có thể bằng 0 dù khách vẫn muốn mua. Đây là hiện tượng **nhu cầu bị che khuất** (*demand censoring*). Đồ án kiểm tra quy trình hai giai đoạn trong bài báo:

1. Dùng **TimesNet** khôi phục nhu cầu ở những giờ có nhãn hết hàng.
2. Cộng nhu cầu theo giờ thành nhu cầu ngày, rồi dùng **SSA (Similar Scenario Average)** dự báo 7 ngày.
3. So sánh SSA dùng doanh số gốc với SSA dùng nhu cầu đã khôi phục bằng TimesNet trên cùng tập đánh giá.
4. Đối chiếu kết quả tự chạy với các bảng trong bài báo, ghi rõ thiết lập, sai khác và giới hạn tái lập.

Phạm vi trọng tâm của nhóm là hai cấu hình **`SSA_RawSales`** và **`SSA_TimesNet`**. Các số trong bài báo chỉ là số tham chiếu; chỉ số được gọi là kết quả của nhóm khi có lượt chạy, log và tệp kết quả tương ứng.

## Tiến độ và sản phẩm hiện có

Trạng thái dưới đây được tổng hợp từ các thư mục, notebook, báo cáo và kết quả hiện có trong repository.

| Task | Nội dung | Trạng thái | Sản phẩm / ghi chú |
|---|---|---|---|
| **1** | Đọc bài báo, giải thích vấn đề MNAR và chốt phạm vi tái lập | **Đã hoàn thành** | [Báo cáo Task 1](reports/Task01_Report.md), [tóm tắt bài báo](Task01_Paper_Review/docs/paper_summary.md), [bảng mục tiêu cần tái lập](Task01_Paper_Review/docs/replicated_tables_target.md) |
| **2** | Lập kế hoạch thực nghiệm, quy tắc đánh giá và cấu hình mô hình | **Đã hoàn thành** | [Báo cáo Task 2](reports/Task02_Report.md), [15 cấu hình dự báo](Task02_Experiment_Plan/docs/15_forecasting_configurations.md), [siêu tham số](Task02_Experiment_Plan/docs/model_hyperparameters.md) |
| **3** | Chuẩn bị môi trường và cách tải/chuyển dữ liệu sang Parquet | **Đã có hướng dẫn và script** | [Hướng dẫn Task 3](Task03_Environment_Setup/README.md), [script tải dữ liệu và xuất Parquet](Task03_Environment_Setup/scripts/download_data.py), [báo cáo Task 3](reports/Task03_Report.md). Hai file dữ liệu lớn không được lưu trong GitHub. |
| **4** | Kiểm định chất lượng và logic dữ liệu train/eval | **Đã hoàn thành** | [Notebook kiểm định](Task04_Data_Validation/notebooks/04_data_validation_colab.ipynb), [báo cáo Task 4](reports/Task04_Report.md), thư mục `Task04_Data_Validation/results/`. Có 34 dòng train mang trạng thái `REVIEW` do `discount > 1`; lượt tái lập chính giữ nguyên dữ liệu. |
| **5** | EDA và thống kê mô tả dữ liệu | **Đã hoàn thành** | Hai notebook trong [Task05_EDA/notebooks](Task05_EDA/notebooks/), [báo cáo Task 5](reports/Task05_Report.md). |
| **6** | Đối chiếu CSV–Parquet và xác nhận dữ liệu sẵn sàng cho thực nghiệm | **Đã hoàn thành** | [Notebook Task 6](Task06_Data_Preparation/notebooks/06_prepare_data.ipynb), [báo cáo](reports/Task06_Report.md), [biên bản và SHA-256](Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md). Đã xác nhận 4.500.000 dòng train và 350.000 dòng eval. |
| **7** | Chạy thử khép kín TimesNet → SSA trên tập nhỏ | **Chưa thấy sản phẩm trong repo** | Cần tạo `Task07_Smoke_Test/`, thử cùng một tập nhỏ cho hai nhánh, lưu log và chỉ số thử. Đây là bước kiểm tra pipeline, không dùng số thử làm kết quả chính thức. |
| **8** | SSA trên doanh số gốc (`SSA_RawSales`) | **Đã hoàn thành** | [Notebook](Task08_SSA_Raw_Sales/notebooks/08_ssa_raw_sales.ipynb), [bảng kết quả](Task08_SSA_Raw_Sales/results/ssa_raw_sales_metrics.csv), [báo cáo](reports/Task08_Report.md). WAPE/WPE của ba nhóm khớp số công bố ở độ chính xác báo cáo. |
| **9** | Đánh giá TimesNet với các điểm thiếu nhân tạo (MNAR) | **Đã hoàn thành** | [Notebook](Task09_TimesNet_MNAR/notebooks/09_timesnet_mnar.ipynb), [bảng kết quả](Task09_TimesNet_MNAR/results/mnar_metrics.csv), [báo cáo](reports/Task09_Report.md), [biên bản](Task09_TimesNet_MNAR/run_info.md). Chạy `--missing_rate 0.3` (seed 1024, 5 epoch) để đối chiếu Bảng 2; không tạo đầu vào cho SSA. |
| **10** | Chạy TimesNet trên giờ hết hàng thực tế để khôi phục nhu cầu | **Chưa thấy sản phẩm trong repo** | Cần tạo `Task10_TimesNet_Recovery/` và xuất `demand_timesnet.parquet` đầy đủ, kiểm tra khóa/giá trị, lưu decoupling score và log. File này là đầu vào của Task 11. |
| **11** | Chạy SSA trên nhu cầu TimesNet và so sánh với Task 8 | **Chưa hoàn thành; phụ thuộc Task 10** | Tạo `Task11_SSA_TimesNet/`, dùng cùng eval và cách chia nhóm như Task 8; báo cáo song song `SSA_RawSales` và `SSA_TimesNet` cho Overall, Low Sale, High Sale. |

Chi tiết phân công Task 6–10 nằm trong [docs/Task06-10_Phan_cong_chi_tiet.md](docs/Task06-10_Phan_cong_chi_tiet.md). Báo cáo tổng hợp hiện có ở [reports/Synthesis_Report.md](reports/Synthesis_Report.md); cần cập nhật báo cáo này khi các task còn lại hoàn tất.

## Kết quả nhóm đã tự chạy

Task 8 đã chạy SSA trên dữ liệu đầy đủ. Kết quả WAPE/WPE tự chạy khớp số bài báo ở độ chính xác công bố:

| Nhóm | WAPE | WPE | MAE |
|---|---:|---:|---:|
| Overall | 31,97% | −10,50% | 0,3982 |
| Low Sale | 38,33% | −8,03% | 0,2691 |
| High Sale | 27,40% | −12,26% | 0,7761 |

Đây là kết quả **SSA trên doanh số gốc**. Số SSA trên nhu cầu TimesNet vẫn là mục tiêu tham chiếu từ bài báo cho tới khi Task 10 và Task 11 chạy xong; không được trình bày các số tham chiếu ấy như kết quả của nhóm.

Task 9 đã chạy đánh giá TimesNet với thiếu nhân tạo (`--missing_rate 0.3` theo ví dụ README tác giả, tỷ lệ che thực tế 15,88% = 9.163.425 giờ quan sát khung 6..21; seed 1024, 5 epoch) trên 783.078 ngày hợp lệ để đối chiếu Bảng 2:

| Mô hình | Nhóm tự chạy (WAPE / WPE) | Tham chiếu bài báo (WAPE / WPE) | Chênh lệch |
|---|---:|---:|---:|
| TimesNet (MNAR) | 27,81% / +2,04% | 27,62% / +1,43% | +0,19 pp / +0,61 pp |

## Dữ liệu và cách lấy hai file Parquet

Các tệp `train.parquet` và `eval.parquet` được tạo/tải trong bước Task 3, rồi được Task 6 kiểm tra. Trong bản làm việc local, chúng nằm ở thư mục gốc dự án cạnh `README.md`. Chúng bị loại khỏi Git bởi `.gitignore` vì đây là dữ liệu lớn, nên người clone GitHub cần tự tải hoặc dùng bản nhóm lưu trên Drive.

Để tạo lại từ nguồn Hugging Face, cài thư viện `datasets` và chạy script từ thư mục dự án:

```bash
pip install datasets
python Task03_Environment_Setup/scripts/download_data.py
```

Script ghi `train.parquet` và `eval.parquet` vào thư mục đang chạy lệnh. Khi dùng Google Drive/Colab, lưu hai file vào thư mục dữ liệu dùng chung của nhóm và cập nhật đường dẫn trong notebook. Dùng [biên bản Task 6](Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md) để nhận diện bản dữ liệu đã được xác nhận qua SHA-256.

## Việc cần làm tiếp theo

1. Hoàn thành Task 7 trên một tập con để kiểm tra việc nạp dữ liệu, chạy TimesNet, tạo Parquet nhu cầu và chạy SSA ở cả hai nhánh (hiện nhánh `feature/task07-smoke-test` mới có mã nguồn, trạng thái `not_run` do thiếu thư viện).
2. Chạy Task 10 trên train đầy đủ để tạo và đối soát `demand_timesnet.parquet`.
3. Sau khi Task 10 bàn giao file, chạy Task 11 trên cùng eval như Task 8 và so sánh chỉ số hai cấu hình SSA.
4. Cập nhật báo cáo tổng hợp, kết luận và slide bằng kết quả thực chạy; ghi rõ các khác biệt so với bài báo.

Task 11 cần đầu ra đầy đủ của Task 10. Theo dõi yêu cầu chi tiết, tham số, log và sản phẩm bàn giao trong [tài liệu phân công Task 6–10](docs/Task06-10_Phan_cong_chi_tiet.md).

## Quy ước báo cáo và tái lập

- Giữ nguyên dữ liệu gốc trong các lượt tái lập chính; ghi riêng mọi thay đổi hoặc lượt thử.
- Lưu notebook/mã nguồn và hướng dẫn trong repository; lưu dataset, checkpoint, log lớn và kết quả không được Git theo hướng dẫn của nhóm.
- Với mỗi lượt chạy, ghi nguồn/đường dẫn dữ liệu, commit mã, phiên bản môi trường, cấu hình, seed, lệnh chạy, trạng thái và đường dẫn đầu ra trong `run_info.md`.
- Tách kết quả `smoke` khỏi kết quả `full`. Lượt lỗi hoặc chưa chạy ghi trạng thái tương ứng, không điền số 0 thay cho kết quả thiếu.
- Chỉ công bố số là kết quả của nhóm nếu có bằng chứng lượt chạy tương ứng; khi đối chiếu bài báo, ghi cả số tự chạy, số tham chiếu và độ lệch.

## Liên kết nhanh

- [Tổng quan dự án](docs/Project_Overview.md)
- [Hướng dẫn đóng góp Git](docs/Contribution_Guide.md)
- [Báo cáo tổng hợp](reports/Synthesis_Report.md)
- [Notebook và báo cáo Task 8](Task08_SSA_Raw_Sales/README.md)
- [Notebook và báo cáo Task 9](Task09_TimesNet_MNAR/README.md)
