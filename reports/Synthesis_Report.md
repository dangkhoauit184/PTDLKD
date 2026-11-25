# BÁO CÁO TỔNG HỢP TOÀN BỘ DỰ ÁN (SYNTHESIS REPORT)
**Môn học:** Phân tích Dữ liệu Kinh doanh (IS403)  
**Đề tài:** Tái lập và Phân tích Thực nghiệm Bộ Dữ liệu Bán lẻ Đồ Tươi Sống FreshRetailNet-50K  
**Phương pháp trọng tâm:** Khung 2 Giai đoạn: TimesNet Khôi phục Nhu cầu Tiềm ẩn + SSA Dự báo Kháng Hết hàng  

---

## 1. Tổng Quan Đề Tài và Mục Tiêu Của Nhóm

Trong ngành bán lẻ thực phẩm tươi sống với mô hình kho vệ tinh giao hàng nhanh (Frontier Warehouse / Dark Store), tình trạng **hết hàng (stockout)** diễn ra thường xuyên do sản phẩm có hạn sử dụng ngắn, không gian kho hạn chế và nhu cầu biến động mạnh. Hiện tượng này dẫn tới **sự che khuất nhu cầu (Demand Censoring)**: doanh số ghi nhận bằng $0$ khi hết hàng dù khách hàng vẫn có nhu cầu mua.

Dự án này thực hiện tái lập quy trình nghiên cứu khoa học của bài báo *FreshRetailNet-50K: A Stockout-Annotated Censored Demand Dataset for Latent Demand Recovery and Forecasting in Fresh Retail* (arXiv:2505.16319v5, công bố bởi Dingdong Ltd.). Mục tiêu của nhóm là:
1. Đánh giá chất lượng dữ liệu và kiểm chứng tính logic nghiệp vụ của $50.000$ chuỗi thời gian ($4.850.000$ bản ghi).
2. Tái lập khung giải pháp 2 giai đoạn: sử dụng mô hình học sâu **TimesNet** để khôi phục nhu cầu ẩn trong các giờ hết hàng, sau đó áp dụng thuật toán thống kê **Similar Scenario Average (SSA)** để dự báo doanh số cho $7$ ngày tương lai.
3. So sánh hiệu năng giữa Pipeline truyền thống (Raw Sales) và Pipeline có khôi phục nhu cầu (Imputation-Augmented), kiểm tra việc khôi phục có làm giảm WAPE và độ lệch dự báo hay không.

---

## 2. Tiến độ Hoàn Thành Task 1–13

| STT | Mã Task | Tên Nhiệm Vụ | Người Thực Hiện | Trọng Tâm Bàn Giao |
| :---: | :---: | :--- | :---: | :--- |
| **1** | **Task 1** | **Đọc bài báo và chốt phạm vi** | Thành viên nhóm | Tài liệu phân tích bài toán MNAR, đối chiếu Bảng 2 & Bảng 3 bài báo. |
| **2** | **Task 2** | **Lập kế hoạch thực nghiệm** | Thành viên nhóm | Bản đặc tả 15 cấu hình dự báo, bộ siêu tham số của 7 mô hình khôi phục. |
| **3** | **Task 3** | **Chuẩn bị môi trường & Pipeline** | Thành viên nhóm | Thiết lập Google Colab GPU, giải quyết tương thích PyPOTS, tối ưu hóa I/O Parquet. |
| **4** | **Task 4** | **Kiểm tra dữ liệu (Validation)** | **Phạm Đăng Khoa** | **Notebook đối soát 48 quy tắc trên 4.85M dòng, bảng profile 19 cột, phát hiện 34 dòng discount bất thường.** |
| **5** | **Task 5** | **Khám phá dữ liệu (EDA)** | Thành viên nhóm | 2 Notebook thống kê phân phối lệch phải, phân tích đường chữ U của hết hàng, 20% SKU chiếm 87% doanh số, 8 biểu đồ. |
| **6** | **Task 6** | **Xác nhận dữ liệu đầu vào** | **Phạm Đăng Khoa** | [Notebook và biên bản đối chiếu CSV–Parquet](../Task06_Data_Preparation/). |
| **7** | **Task 7** | **Chạy thử khép kín (Smoke Test)** | **Dương Trọng Toàn** | [Báo cáo và kiểm chứng pipeline 100 cặp](Task07_Report.md). |
| **8** | **Task 8** | **SSA trên doanh số gốc** | **Sinhvienvuitinh** | [Báo cáo và kết quả baseline](Task08_Report.md). |
| **9** | **Task 9** | **TimesNet với thiếu nhân tạo (MNAR)** | **Khanh** | [Báo cáo và kết quả WAPE/WPE Bảng 2](Task09_Report.md). |
| **10** | **Task 10** | **TimesNet khôi phục giờ hết hàng thực tế** | **Minh Nguyễn** | [Báo cáo, Decoupling Score Bảng 2 và `demand_timesnet.parquet`](Task10_Report.md). |
| **11** | **Task 11** | **SSA trên nhu cầu TimesNet** | **Sinhvienvuitinh** | [Báo cáo `SSA_TimesNet` và đối chiếu trực tiếp với Task 8](Task11_Report.md). |
| **12** | **Task 12** | **DLinear khôi phục nhu cầu (Bảng 2)** | **Khanh** | [Báo cáo MNAR & Decoupling của DLinear, xuất `demand_dlinear.parquet`](Task12_Report.md). |
| **13** | **Task 13** | **SSA trên nhu cầu DLinear & Tổng hợp SSA** | **Phạm Đăng Khoa** | [Báo cáo `SSA_DLinear` và bảng tổng hợp 3 cấu hình cột SSA](Task13_Report.md). |

---

## 3. Tóm Tắt Phương Pháp Thực Hiện Từng Task

### Task 1 — Cơ Sở Lý Thuyết & Chốt Phạm Vi
* Xác định bản chất dữ liệu khuyết **MNAR (Missing Not At Random)**: xác suất hết hàng phụ thuộc vào chính nhu cầu tiêu dùng.
* Phân tích vòng lặp sai lệch: $\text{Hết hàng} \to \text{Doanh số thấp} \to \text{Dự báo thiếu} \to \text{Nhập ít} \to \text{Tiếp tục hết hàng}$.
* Chốt mục tiêu tái lập: Bảng 2 (Khôi phục MNAR) và Bảng 3 (Dự báo 7 ngày trên nhóm Overall, High-sale, Low-sale).

### Task 2 — Kế Hoạch Thực Nghiệm & Siêu Tham Số
* Thiết lập ma trận $3 \times 5 = 15$ cấu hình thử nghiệm dự báo (3 mô hình SSA, TFT, DLinear $\times$ 5 nguồn dữ liệu Raw Sales, TimesNet, ImputeFormer, iTransformer, DLinear).
* Chuẩn hóa cấu hình TimesNet: `n_steps=480` ($30 \text{ ngày} \times 16 \text{ giờ}$), `n_features=6`, `top_k=7`, `n_kernels=5`, `batch_size=128`, optimizer Adam (`lr=0.001`).
* Thiết lập quy ước đánh giá Ground Truth: Chỉ đánh giá trên các ngày trong Eval có `stock_hour6_22_cnt == 0`.

### Task 3 — Môi Trường Điện Toán & Quy Trình Dữ Liệu
* Xây dựng notebook đồng bộ trên Google Colab GPU (T4/L4/V100).
* Chuyển đổi toàn bộ dữ liệu CSV sang Apache Parquet giúp tăng tốc độ đọc từ đĩa lên gấp $14$ lần và tiết kiệm $95\%$ dung lượng.
* Đóng gói quy trình cài đặt các phiên bản thư viện chuyên biệt: PyTorch 2.0.1, PyPOTS 0.1.2, PyTorch-Forecasting 1.0.0.

### Task 4 — Kiểm Định Toàn Vẹn Dữ Liệu (Data Validation)
* Thực thi 48 quy tắc kiểm định trên toàn bộ $4.500.000$ dòng train và $350.000$ dòng eval bằng kỹ thuật batch reading $20.000$ dòng/lô.
* Xác nhận tính toàn vẹn đạt **$100\%$**: $0$ giá trị thiếu, $0$ khóa trùng lặp, $100\%$ mảng giờ khớp doanh số ngày, $100\%$ số giờ hết hàng khớp nhãn kho trong khung $06:00 - 22:00$.
* Có 96 hạng mục OK và một hạng mục REVIEW: 34 dòng train có `discount > 1.0`. Lượt tái lập chính giữ nguyên các giá trị này.

### Task 5 — Khám Phá Thống Kê & Đặc Trưng Nghiệp Vụ (EDA)
* Phát hiện phân phối doanh số lệch phải mạnh (`skewness = 8.47`, `mean = 0.999`, `median = 0.700`).
* Làm rõ nghịch lý độ thưa dữ liệu: Doanh số ngày chỉ có $4.46\%$ bằng $0$, nhưng dữ liệu theo giờ có tới $69.06\%$ số giờ bằng $0$ (khung 6..21) và $77.78\%$ trên 24 giờ.
* Xác nhận hiện tượng hết hàng diễn ra trên $19.88\%$ số giờ kinh doanh và tuân theo **quy luật chữ U**: thấp nhất lúc 7h sáng ($5.0\%$) và cao nhất lúc 22h đêm ($41.9\%$).
* Khẳng định tính tập trung cao độ: $20\%$ mặt hàng chiếm tới $87\%$ tổng doanh số bán ra.

![Phân phối số giờ hết hàng và quy luật chữ U theo giờ](../Task05_EDA/results/figures/03_hourly_stockout_ushape.png)

### Task 6 — Xác nhận dữ liệu đầu vào
* Hai bản Parquet hiện có khớp đầy đủ với CSV trên 4.850.000 dòng × 19 cột, kể cả từng phần tử của các mảng giờ.
* Train và eval cùng 50.000 cặp, đủ 90 và 7 ngày/cặp, không trùng khóa ngày. Kiểm tra mẫu cho TimesNet và SSA đạt kích thước kỳ vọng.
* Xem [báo cáo Task 6](Task06_Report.md) và [file kết quả](../Task06_Data_Preparation/).

### Task 7 — Kiểm thử Khép kín Đường ống trên Tập con (`Smoke Test`)
* Kiểm chứng luồng đầu–cuối (`SSA_RawSales` → `TimesNet --missing_rate 0` → `SSA_TimesNet`) trên mẫu 100 cặp (`9.000` dòng `train`, `700` dòng `eval`), đảm bảo cách nối khóa và truyền tệp riêng biệt không gây rò rỉ dữ liệu hay đọc nhầm tập đầy đủ ([báo cáo Task 7](Task07_Report.md)).

### Task 8 — Dự báo Baseline SSA trên Doanh số Gốc (`SSA_RawSales`)
* Thực thi SSA trên toàn bộ $50.000$ chuỗi (90 ngày lịch sử `train`, dự báo 7 ngày `eval`), đánh giá trên $206.562$ dòng `eval` không hết hàng trong khung `06:00–22:00` (`stock_hour6_22_cnt == 0`).
* Tái lập khớp hoàn toàn (`0.00 pp`) số công bố của Bảng 3 trên cả ba nhóm: `Overall` (WAPE $31.97\%$, WPE $-10.50\%$), `Low Sale` (WAPE $38.33\%$, WPE $-8.03\%$), và `High Sale` (WAPE $27.40\%$, WPE $-12.26\%$). Xác nhận rõ độ lệch âm nặng nhất nằm ở nhóm hàng bán chạy (`High Sale`).

### Task 9 — Đánh giá Khôi phục Nhu cầu MNAR bằng TimesNet
* Huấn luyện và đánh giá TimesNet (`5` epoch, `batch_size=128`, `seed=1024`) với cơ chế tạo thiếu nhân tạo `mimic_missing` (`missing_rate=0.3`, che thêm thực tế $9.163.425$ điểm giờ $= 15.88\%$ số giờ còn hàng trong khung `6..21`) trên $783.078$ ngày hợp lệ.
* Đạt WAPE **$27.81\%$** và WPE **$+2.04\%$** (bám sát mức $27.62\%$ và $+1.43\%$ của Bảng 2 bài báo), đồng thời giải quyết bài toán giới hạn $12.7\text{ GB}$ RAM trên Colab miễn phí thông qua cấp phát `float32` và `norm_val` thu gọn đã kiểm chứng tương đương $100\%$ (`equivalence_ok=True`).

### Task 10 — Khôi phục Nhu cầu Thực tế bằng TimesNet & Xuất `demand_timesnet.parquet`
* Huấn luyện TimesNet ở chế độ `--missing_rate 0` (`5` epoch, `batch_size=128`, `seed=2024` trên GPU NVIDIA L4 trong $84.66$ phút) trên toàn bộ tập `train.parquet` chuẩn của Task 6 ($4.500.000$ dòng).
* Tái lập chỉ số tách rời **Decoupling Score ($\rho_{DS}$)** khớp tuyệt đối Bảng 2 bài báo ở độ chính xác công bố: doanh số gốc đạt **$-0.5664$** ($-0.57$), nhu cầu khôi phục bằng TimesNet đạt **$+0.0699$** ($+0.07$). Tệp đầu ra `demand_timesnet.parquet` ($4.500.000$ dòng × $20$ cột) đạt $0$ lỗi đối soát toàn vẹn ([báo cáo Task 10](Task10_Report.md)).

### Task 11 — Dự báo `SSA_TimesNet` và Đối chiếu Trực tiếp với Task 8
* Thực thi SSA trên lịch sử nhu cầu khôi phục `sale_amount_pred` từ `demand_timesnet.parquet`, phân nhóm theo `psd` gốc và đánh giá trên cùng $206.562$ dòng `eval` hợp lệ (`Low Sale = 153.208`, `High Sale = 53.354`).
* Tái lập khớp tuyệt đối `0.00 pp` WAPE của Bảng 3 trên cả ba nhóm: `Overall` (**$29.79\%$** / **$+1.40\%$**), `Low Sale` (**$37.87\%$** / **$+4.96\%$**) và `High Sale` (**$23.98\%$** / **$-1.15\%$**), giảm $3.42\text{ pp}$ WAPE ở mặt hàng bán chạy và triệt tiêu thiên lệch dự báo thiếu ([báo cáo Task 11](Task11_Report.md)).

### Task 12 — Khôi phục Nhu cầu bằng `DLinear` (Bảng 2) & Xuất `demand_dlinear.parquet`
* Thực thi mô hình khôi phục tuyến tính `DLinear` ở cả hai chế độ trên Colab GPU T4: lượt MNAR (`missing_rate=0.3`, `seed=1024`) đạt WAPE **$30.32\%$** (bài báo $29.99\%$), WPE **$-14.38\%$** trên đúng $783.078$ ngày như Task 9; lượt khôi phục thực tế (`missing_rate=0`, `seed=2024`) đạt Decoupling Score **$-0.1512$** ($-0.15$, bài báo $-0.16$) và xuất `demand_dlinear.parquet` đạt $0$ lỗi đối soát ([báo cáo Task 12](Task12_Report.md)).

### Task 13 — Dự báo `SSA_DLinear` & Hoàn thiện Cột SSA Bảng 3
* Thực thi SSA trên `demand_dlinear.parquet` của Task 12, đạt WAPE **$30.12\%$**, WPE **$-0.58\%$**, MAE **$0.3749$** trên `Overall` (khớp sát Bảng 3 bài báo $30.00\%$ / $-1.49\%$, chênh $+0.12\text{ pp}$ WAPE).
* Tổng hợp 9 dòng cho cả 3 cấu hình cột SSA (`SSA_RawSales` → `SSA_DLinear` → `SSA_TimesNet`), xác nhận quy luật cải thiện đơn điệu trên mọi phân nhóm (`Overall`: $31.97\% \to 30.12\% \to 29.79\%$; `High Sale`: $27.40\% \to 24.46\% \to 23.98\%$; xem [báo cáo Task 13](Task13_Report.md)).

---

## 4. Kết quả nhóm đã tự chạy và số tham chiếu bài báo

### 4.1. Kết quả nhóm đã tự chạy (Task 8–13)
- **Bảng 2 — Khôi phục nhu cầu tiềm ẩn:**
  - `TimesNet` ([Task 9](Task09_Report.md) & [Task 10](Task10_Report.md)): WAPE MNAR **27,81%** (bài báo 27,62%), WPE MNAR **+2,04%** (bài báo +1,43%); Decoupling Score **+0,0699** (+0,07, bài báo +0,07; Raw Sales **−0,5664** ≈ −0,57).
  - `DLinear` ([Task 12](Task12_Report.md)): WAPE MNAR **30,32%** (bài báo 29,99%), WPE MNAR **−14,38%** (bài báo −1,28%); Decoupling Score **−0,1512** (−0,15, bài báo −0,16).
- **Bảng 3 — Dự báo 7 ngày trên trọn bộ cột SSA (`206.562` dòng `eval` không hết hàng):**
  - `SSA_RawSales` ([Task 8](Task08_Report.md)): Overall **31,97% / −10,50%** (MAE 0,3982); Low Sale **38,33% / −8,03%** (MAE 0,2691); High Sale **27,40% / −12,26%** (MAE 0,7761).
  - `SSA_DLinear` ([Task 13](Task13_Report.md)): Overall **30,12% / −0,58%** (MAE 0,3749; bài báo 30,00% / −1,49%); Low Sale **38,00% / +3,69%** (MAE 0,2664); High Sale **24,46% / −3,64%** (MAE 0,6925).
  - `SSA_TimesNet` ([Task 11](Task11_Report.md)): Overall **29,79% / +1,40%** (MAE 0,3709; bài báo 29,79% / +1,39%); Low Sale **37,87% / +4,96%** (MAE 0,2656); High Sale **23,98% / −1,15%** (MAE 0,6790).

### 4.2. Tổng hợp Cột SSA tự chạy và Mục tiêu Tham chiếu cho Task 14–15
| Nhóm Sản Phẩm | Cấu hình Dự Báo | Nguồn số liệu | WAPE (%) | WPE (%) | Ý Nghĩa Kết Quả |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Overall** | `SSA_RawSales` (Task 8) | Nhóm tự chạy | **$31.97\%$** | **$-10.50\%$** | Thiên lệch dự báo thiếu nặng nề |
| | `SSA_DLinear` (Task 13) | Nhóm tự chạy | **$30.12\%$** | **$-0.58\%$** | Giảm 1,85 pp WAPE bằng khôi phục tuyến tính |
| | `SSA_TimesNet` (Task 11) | Nhóm tự chạy | **$29.79\%$** | **$+1.40\%$** | **Giảm 2,18 pp WAPE; triệt tiêu lệch âm** |
| | *`TFT_TimesNet` (Task 15)* | *Tham chiếu bài báo* | *$29.02\%$* | *$+2.58\%$* | *Mục tiêu SOTA đang triển khai* |
| **High Sale** | `SSA_RawSales` (Task 8) | Nhóm tự chạy | $27.40\%$ | $-12.26\%$ | Dự báo thiếu hơn $12\%$ nhu cầu thực |
| | `SSA_DLinear` (Task 13) | Nhóm tự chạy | $24.46\%$ | $-3.64\%$ | Còn lệch âm nhẹ do giới hạn tách rời DLinear |
| | `SSA_TimesNet` (Task 11) | Nhóm tự chạy | **$23.98\%$** | **$-1.15\%$** | **Giảm 3,42 pp WAPE; WPE về sát 0** |
| **Low Sale** | `SSA_RawSales` (Task 8) | Nhóm tự chạy | $38.33\%$ | $-8.03\%$ | Sai số cao do chuỗi giờ thưa |
| | `SSA_DLinear` (Task 13) | Nhóm tự chạy | $38.00\%$ | $+3.69\%$ | Cải thiện nhẹ WAPE |
| | `SSA_TimesNet` (Task 11) | Nhóm tự chạy | **$37.87\%$** | **$+4.96\%$** | Cải thiện tốt nhất trên cột SSA |

---

## 5. Việc tiếp theo (Task 15)

Nhóm đã hoàn tất **Task 1–14**, bao gồm cả hai mô hình khôi phục ở Bảng 2 (`TimesNet`, `DLinear`) và trọn bộ [3 cấu hình cột SSA ở Bảng 3](../Task13_SSA_DLinear/results/ssa_all_3configs_summary.csv). Kết quả cột DLinear gồm 3 cấu hình được tổng hợp tại [dlinear_forecasting_metrics.csv](../Task14_DLinear_Forecasting/results/dlinear_forecasting_metrics.csv), với đủ 9 dòng và `206.562` mẫu đánh giá hợp lệ.

Hạng mục còn lại đang được triển khai theo [docs/Task11-15_Phan_cong_chi_tiet.md](../docs/Task11-15_Phan_cong_chi_tiet.md):
1. **Task 15 (`TFT` Forecasting — Minh Nguyễn):** Chạy 2 cấu hình SOTA `TFT_RawSales` và `TFT_TimesNet` trên GPU L4 High-RAM.
