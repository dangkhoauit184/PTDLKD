# Phân công Task 11–15 — Tái lập & Mở rộng Thực nghiệm FreshRetailNet-50K

Tài liệu này quy định phân công công việc, sản phẩm bàn giao và toàn bộ lưu ý kỹ thuật bắt buộc cho **giai đoạn Task 11–15**, nối tiếp sau khi nhóm đã hoàn thành và merge trọn vẹn **Task 1–10** trên nhánh `main` (`bfff86f`). Bản mã tác giả đối chiếu: [frn-50k-baseline, commit 8af694a](https://github.com/Dingdong-Inc/frn-50k-baseline/tree/8af694a09a5a427d1d50648d348c022565a781f2). Nguồn tham chiếu số liệu bài báo: [Bảng 2 và Bảng 3 (arXiv:2505.16319v5)](https://arxiv.org/html/2505.16319v5#S5) và [replicated_tables_target.md](../Task01_Paper_Review/docs/replicated_tables_target.md).

---

## 1. Bảng tổng quan phân công 5 thành viên (Task 11 → Task 15)

Khi hoàn tất 5 task dưới đây, nhóm tự chạy thực nghiệm được **2/7 mô hình khôi phục ở Bảng 2** (`TimesNet` tốt nhất vs `DLinear` baseline tuyến tính) và **8/15 cấu hình dự báo ở Bảng 3** trải đều trên cả **3 họ mô hình dự báo của bài báo (`SSA`, `DLinear`, `TFT`)**:

| Thành viên | Task trước đã làm | Task mới & Thư mục trên Git | Nội dung trọng tâm | Trạng thái |
|---|---|---|---|---|
| **Sinhvienvuitinh** | Task 8 (`SSA_RawSales`) | **Task 11** — `Task11_SSA_TimesNet/` | Dự báo **`SSA_TimesNet`** từ `demand_timesnet.parquet` (Task 10) và đối chiếu trực tiếp với Task 8 | **Đã hoàn thành** ([Báo cáo Task 11](../reports/Task11_Report.md)) |
| **Khanh** | Task 9 (`TimesNet` MNAR) | **Task 12** — `Task12_DLinear_Recovery/` | Khôi phục nhu cầu bằng **`DLinear`** cho cả chế độ MNAR (`0.3`) lẫn thực tế (`0.0`), xuất `demand_dlinear.parquet` | **Đã hoàn thành** ([Báo cáo Task 12](../reports/Task12_Report.md)) |
| **Phạm Đăng Khoa** | Task 4 & Task 6 | **Task 13** — `Task13_SSA_DLinear/` | Dự báo **`SSA_DLinear`** từ `demand_dlinear.parquet` (Task 12) và tổng hợp trọn bộ 3 cấu hình cột SSA | **Đã hoàn thành** ([Báo cáo Task 13](../reports/Task13_Report.md)) |
| **Dương Trọng Toàn** | Task 7 (`Smoke Test`) | **Task 14** — `Task14_DLinear_Forecasting/` | Dự báo 7 ngày bằng mạng học sâu **`DLinear`**: `DLinear_RawSales`, `DLinear_TimesNet`, `DLinear_DLinear` | **Đã hoàn thành** ([Báo cáo Task 14](../reports/Task14_Report.md)) |
| **Minh Nguyễn** | Task 10 (`TimesNet` Recovery) | **Task 15** — `Task15_TFT_Forecasting/` | Dự báo 7 ngày bằng mô hình SOTA **`TFT`**: `TFT_RawSales` và `TFT_TimesNet` trên GPU L4 High-RAM | **Đã hoàn thành** ([Báo cáo Task 15](../reports/Task15_Report.md)) |

---

## 2. Quy ước bắt buộc áp dụng chung cho cả 5 thành viên

1. **Nhánh Git & Bảo vệ dữ liệu lớn:**
   - Luôn `git checkout main && git pull origin main` trước khi tách nhánh riêng theo mẫu `feature/task<số>-<tên>` quy định tại [Contribution_Guide.md](Contribution_Guide.md).
   - **Tuyệt đối không commit** các tệp nhị phân lớn (`.parquet`, `.npy`, `.ckpt`, `.pth`, `.pypots`, thư mục `checkpoints/`, `demand/`, `lightning_logs/`) lên GitHub. Chỉ đẩy notebook `.ipynb` (đã lưu đầy đủ output thực chạy), CSV chỉ số nhỏ, log `.log`, `run_metadata.json`, `run_info.md`, `README.md`, `code_changes.diff` (nếu có vá mã tác giả) và báo cáo `reports/Task<số>_Report.md`. File [`.gitignore`](../.gitignore) ở thư mục gốc đã mở sẵn whitelist CSV và `.log` cho toàn bộ `Task11` → `Task15`.

2. **Chuẩn dữ liệu đầu vào dùng chung (xác minh đúng SHA-256 trước khi chạy):**
   - **`train.parquet`** (có sẵn trực tiếp trong repo tại `Task06_Data_Preparation/train.parquet` | [biên bản Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md)): `4.500.000` dòng × `19` cột (`61.075.680` bytes) — SHA-256: `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96`.
   - **`eval.parquet`** (có sẵn trực tiếp trong repo tại `Task06_Data_Preparation/eval.parquet` | [biên bản Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md)): `350.000` dòng × `19` cột (`5.451.872` bytes) — SHA-256: `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`.
   - **`demand_timesnet.parquet`** ([biên bản Task 10](../Task10_TimesNet_Recovery/run_info.md) | [Link tải Google Drive](https://drive.google.com/file/d/1f9db-U9f9C9OFS-V2EcmQv4FIU3bguR3/view?usp=sharing)): `4.500.000` dòng × `20` cột (`81.562.029` bytes) — SHA-256: `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`.
   - **`demand_dlinear.parquet`** ([biên bản Task 12](../Task12_DLinear_Recovery/run_info.md) | [Link tải Google Drive](https://drive.google.com/file/d/1MDcD7cOyzcnoBu48I6eGUkSfwx8b3hkh/view?usp=drive_link)): `4.500.000` dòng × `20` cột (`81.531.473` bytes) — SHA-256: `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b`.
   - Giữ nguyên toàn bộ dữ liệu gốc trong các lượt tái lập chính (kể cả 34 dòng `discount > 1` gắn cờ `REVIEW` ở [Task 4](../reports/Task04_Report.md)).

3. **Quy tắc bất di bất dịch cho mọi Task dự báo Bảng 3 (Task 11, 13, 14, 15):**
   - Biến phân nhóm **`psd` BẮT BUỘC luôn tính bằng trung bình `sale_amount` GỐC trong tập `train` (`dt <= '2024-06-25'`)** theo từng cặp `(store_id, product_id)` (`Overall: psd >= 0`, `Low Sale: psd < 1`, `High Sale: psd >= 1`). **Tuyệt đối không tính `psd` từ `sale_amount_pred`**, nhằm đảm bảo danh sách cặp thuộc `Low Sale` và `High Sale` trùng khớp 100% giữa mọi mô hình và mọi nguồn dữ liệu khôi phục.
   - Chỉ đánh giá trên các dòng `eval` không hết hàng trong khung giờ kinh doanh `06:00–22:00` (`stock_hour6_22_cnt == 0`, tổng cộng đúng **`206.562` dòng** trên 7 ngày `2024-06-26` → `2024-07-02`). Với `DLinear` và `TFT`, chặn dưới dự báo âm về `0` (`np.maximum(pred, 0)`) theo đúng mã tác giả. Tính WAPE, WPE, MAE theo từng ngày rồi lấy trung bình cộng qua 7 ngày.
   - Mọi file CSV chỉ số dự báo đối chiếu Bảng 3 dùng chung đúng **10 cột chuẩn** (đồng bộ với [ssa_raw_sales_metrics.csv](../Task08_SSA_Raw_Sales/results/ssa_raw_sales_metrics.csv)):
     ```text
     config_id,group,wape_pct,wpe_pct,mae,paper_wape_pct,paper_wpe_pct,delta_wape_pp,delta_wpe_pp,status
     ```
     Trong đó `delta = số nhóm tự chạy − số bài báo` (đơn vị điểm phần trăm `pp`). **Nếu một nhóm con không được bài báo in số tham chiếu** (cụ thể là `Low Sale` và `High Sale` của các cấu hình dùng nhu cầu khôi phục `DLinear`), ghi đầy đủ `wape_pct, wpe_pct, mae` tự chạy nhưng **để trống** 4 cột `paper_wape_pct, paper_wpe_pct, delta_wape_pp, delta_wpe_pp` — **tuyệt đối không điền `0`**.

---

## 3. Chi tiết công việc, bàn giao & lưu ý kỹ thuật từng Task

### 3.1. Sinhvienvuitinh — Task 11: Dự báo `SSA_TimesNet` và so sánh với Task 8

- **Nhánh Git:** `feature/task11-ssa-timesnet` | **Thư mục:** `Task11_SSA_TimesNet/` | **Mã cấu hình:** `SSA_TimesNet`
- **Mục tiêu:** Chạy SSA trên lịch sử nhu cầu đã khôi phục bằng TimesNet (`sale_amount_pred` từ Task 10) và lập bảng đối chiếu trực tiếp với `SSA_RawSales` (Task 8) cùng cột SSA của Bảng 3 bài báo.
- **Các bước thực hiện:**
  1. Tải `demand_timesnet.parquet` từ link Google Drive trong [Task10_TimesNet_Recovery/run_info.md](../Task10_TimesNet_Recovery/run_info.md) và dùng cùng `eval.parquet` của Task 6; in kiểm tra khớp cả hai mã SHA-256 trước khi chạy.
  2. Kế thừa khung chạy tối ưu bộ nhớ từ [08_ssa_raw_sales.ipynb](../Task08_SSA_Raw_Sales/notebooks/08_ssa_raw_sales.ipynb) (bám sát [ssa_forecasting.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/SSA/ssa_forecasting.py)): nạp thêm cột `sale_amount_pred` từ `demand_timesnet.parquet` và gán `eval_df['sale_amount_pred'] = np.nan` trước khi ghép nối 90 ngày train + 7 ngày eval.
  3. Đưa `sale_amount_pred` vào cột thứ 3 của mảng đặc trưng liên tục `x_cont = all_data[['time_idx', 'discount', 'sale_amount_pred']].values.reshape(-1, 97, 3)` để thuật toán SSA lấy trung bình kịch bản tương tự trên chuỗi nhu cầu đã khôi phục.
  4. Tính `psd` từ `sale_amount` gốc của `train`, đánh giá dự báo đối chiếu `sale_amount` thật của `eval` trên `206.562` dòng `stock_hour6_22_cnt == 0`. Đối chiếu số tham chiếu Bảng 3:
     - `Overall`: WAPE `29.79%`, WPE `+1.39%`
     - `Low Sale`: WAPE `37.87%`, WPE `+4.89%`
     - `High Sale`: WAPE `23.98%`, WPE `-1.12%`
  5. Đọc kết quả từ [ssa_raw_sales_metrics.csv](../Task08_SSA_Raw_Sales/results/ssa_raw_sales_metrics.csv) để xuất thêm bảng đặt song song hai cấu hình `SSA_RawSales` và `SSA_TimesNet` trên cả 3 nhóm sản phẩm.
- **Sản phẩm bàn giao trên Git:**
  - `Task11_SSA_TimesNet/notebooks/11_ssa_timesnet.ipynb` (đã lưu output thực chạy)
  - `Task11_SSA_TimesNet/results/ssa_timesnet_metrics.csv` (3 dòng chuẩn 10 cột, `config_id=SSA_TimesNet`)
  - `Task11_SSA_TimesNet/results/ssa_raw_vs_timesnet_comparison.csv` (6 dòng đặt song song `SSA_RawSales` và `SSA_TimesNet`)
  - `Task11_SSA_TimesNet/results/full/ssa_timesnet.log`, `Task11_SSA_TimesNet/results/run_metadata.json`
  - `Task11_SSA_TimesNet/run_info.md`, `Task11_SSA_TimesNet/README.md` và `reports/Task11_Report.md`
- **Tiêu chí xác nhận hoàn thành:** `eligible_eval_rows == 206562`; số lượng bản ghi của hai nhóm con `Low Sale` và `High Sale` trùng khớp 100% với Task 8; chỉ số trong CSV khớp hoàn toàn với `.log`.
- **⚠️ Lưu ý kỹ thuật bắt buộc:**
  - Tuyệt đối không ghi đè cột `sale_amount` bằng `sale_amount_pred` trước khi tính `psd` hoặc trên tập `eval` (`subdf['sale_amount']` trong `eval` là doanh số quan sát thật ở ngày không hết hàng, dùng làm Ground Truth để tính WAPE/WPE/MAE).

---

### 3.2. Khanh — Task 12: Khôi phục nhu cầu bằng `DLinear` (Bảng 2 & Xuất Parquet)

- **Nhánh Git:** `feature/task12-dlinear-recovery` | **Thư mục:** `Task12_DLinear_Recovery/`
- **Mục tiêu:** Tự chạy mô hình khôi phục thứ hai là **`DLinear`** ở cả hai chế độ (`missing_rate=0.3` và `missing_rate=0.0`) để đối chứng trực tiếp với `TimesNet` trên **Bảng 2**, đồng thời xuất tệp `demand_dlinear.parquet` chuyển giao cho **Phạm Đăng Khoa** (Task 13) và **Dương Trọng Toàn** (Task 14).
- **Các bước thực hiện:**
  1. Nạp `train.parquet` chuẩn của Task 6 (`SHA-256: b7e01c71...`). Kế thừa trực tiếp kiến trúc nạp dữ liệu chống tràn RAM từ [09_timesnet_mnar.ipynb](../Task09_TimesNet_MNAR/notebooks/09_timesnet_mnar.ipynb) và [10_timesnet_recovery.ipynb](../Task10_TimesNet_Recovery/notebooks/10_timesnet_recovery.ipynb). Theo mã gốc [latent_demand_recovery/exp/model/models.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/latent_demand_recovery/exp/model/models.py) và [pypots/imputation/dlinear/model.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/latent_demand_recovery/pypots/imputation/dlinear/model.py), `DLinear` dùng chung `DatasetForSAITS` và nhân `imputed_data * inputs['norm_val']` giống hệt `TimesNet`, nên kỹ thuật cấp phát `float32` + `norm_val` thu gọn `(n, 1, 6)` chạy ổn định 100% trên Colab T4 12,7 GB RAM.
  2. **Lượt 1 — Chế độ MNAR (`--model DLinear --missing_rate 0.3`):** Giữ đúng siêu tham số mặc định trong `models.py`: `n_steps=480`, `n_features=6`, `moving_avg_window_size=17` (`patch_len // 2 * 2 + 1` với `patch_len=16`), `individual=False`, `d_model=64`, `epochs=5`, `batch_size=128`, `lr=0.001`, `seed=1024`. Kiểm chứng `equivalence_ok=True` trên 200 cặp trước, sau đó chạy toàn bộ 50.000 cặp (`150.000` mẫu); ghi WAPE/WPE trên `783.078` ngày hợp lệ để đối chiếu Bảng 2 (`DLinear`: WAPE `29.99%`, WPE `-1.28%`).
  3. **Lượt 2 — Chế độ Khôi phục thực tế (`--model DLinear --missing_rate 0`):** Giữ `epochs=5`, `batch_size=128`, `lr=0.001` (ghi rõ `seed=1024` hoặc `2024` thực tế sử dụng). Xuất tệp `demand_dlinear.parquet` lên Google Drive (bật quyền chia sẻ *Anyone with the link*), chạy đối soát toàn vẹn giống Cell 7 của Task 10 và tính `evaluation_decoupling` đối chiếu Bảng 2 (Raw Sales `-0.57`, `DLinear` `-0.16`).
- **Sản phẩm bàn giao trên Git & Google Drive:**
  - **Trên Google Drive (gửi link ngay cho Phạm Đăng Khoa & Dương Trọng Toàn):** `demand_dlinear.parquet` (`4.500.000` dòng × `20` cột; tính và ghi rõ kích thước byte + SHA-256 vào `run_info.md`) cùng thư mục checkpoint `.pypots`.
  - **Trên Git:**
    - `Task12_DLinear_Recovery/notebooks/12_dlinear_recovery.ipynb` (lưu đầy đủ output cả lượt MNAR và lượt Recovery)
    - `Task12_DLinear_Recovery/results/dlinear_mnar_metrics.csv` — đúng 1 dòng `DLinear` theo mẫu cột:
      `model,missing_rate,seed,epochs,batch_size,n_artificially_masked_hours,wape_pct,wpe_pct,status,log_path`
    - `Task12_DLinear_Recovery/results/dlinear_decoupling_metrics.csv` — đúng 2 dòng (`Raw Sales`, `DLinear`) theo mẫu cột:
      `method,decoupling_score,log_path`
    - `Task12_DLinear_Recovery/results/demand_file_check.csv` — `4.500.000` dòng × `20` cột, toàn bộ cột đếm lỗi = `0`, theo mẫu cột:
      `file_path,n_rows,n_cols,n_duplicate_keys,n_missing_keys_vs_train,n_extra_keys_vs_train,n_pred_missing,n_pred_non_finite,n_pred_negative`
    - `Task12_DLinear_Recovery/results/full/dlinear_mnar.log`, `Task12_DLinear_Recovery/results/full/dlinear_recovery.log`, `Task12_DLinear_Recovery/results/smoke/dlinear_smoke.log`, `Task12_DLinear_Recovery/results/run_metadata.json`
    - `Task12_DLinear_Recovery/run_info.md`, `Task12_DLinear_Recovery/README.md` và `reports/Task12_Report.md`
- **Tiêu chí xác nhận hoàn thành:** Với `seed=1024` trên cùng `train.parquet`, lượt MNAR che đúng `9.163.425` điểm giờ (`783.078` ngày đánh giá) như Task 9; tệp `demand_dlinear.parquet` đạt `0` lỗi đối soát và mở tải được ở trình duyệt ẩn danh.
- **⚠️ Lưu ý kỹ thuật bắt buộc:**
  - Trong hàm `_demand_recovery`, bắt buộc chặn âm `np.where(imputation > 0, imputation, 0)`, chỉ thay thế lát giờ kinh doanh `hours_sale_origin[..., 6:22]` tại đúng các vị trí hết hàng, **giữ nguyên 8 giờ ban đêm (`[0:6]` và `[22:24]`)**, rồi cộng đủ 24 giờ thành `sale_amount_pred`. Giữ nguyên cột `hours_sale` và `sale_amount` gốc trong tệp Parquet xuất ra.
  - Tuyệt đối không gửi nhầm tệp `demand.parquet` của lượt smoke 200 cặp làm tệp bàn giao full.

---

### 3.3. Phạm Đăng Khoa — Task 13: Dự báo `SSA_DLinear` và Tổng hợp cột SSA

- **Nhánh Git:** `feature/task13-ssa-dlinear` | **Thư mục:** `Task13_SSA_DLinear/` | **Mã cấu hình:** `SSA_DLinear`
- **Mục tiêu:** Chạy SSA trên tệp nhu cầu khôi phục bằng `DLinear` (`demand_dlinear.parquet` từ Task 12) và lập bảng tổng hợp trọn vẹn cả 3 cấu hình thuộc cột SSA của Bảng 3 (`SSA_RawSales` vs `SSA_DLinear` vs `SSA_TimesNet`).
- **Các bước thực hiện:**
  1. Chuẩn bị sẵn notebook kế thừa từ [08_ssa_raw_sales.ipynb](../Task08_SSA_Raw_Sales/notebooks/08_ssa_raw_sales.ipynb); ngay khi nhận link `demand_dlinear.parquet` từ **Khanh**, kiểm tra khớp mã SHA-256 ghi trong `Task12_DLinear_Recovery/run_info.md` và `eval.parquet` của Task 6 (`SHA-256: 61cfd3cb...`).
  2. Chạy `SSA` với lịch sử 90 ngày lấy từ cột `sale_amount_pred` của `demand_dlinear.parquet`, `psd` tính từ `sale_amount` gốc của `train`, đánh giá trên đúng `206.562` dòng `eval` hợp lệ (`stock_hour6_22_cnt == 0`).
  3. Xuất chỉ số WAPE, WPE, MAE cho cả 3 nhóm (`Overall`, `Low Sale`, `High Sale`). Đối chiếu nhóm `Overall` với số bài báo Bảng 3 (`WAPE = 30.00%`, `WPE = -1.49%`).
  4. Tổng hợp bảng 9 dòng so sánh 3 cấu hình cột SSA (`SSA_RawSales` từ Task 8, `SSA_TimesNet` từ Task 11, `SSA_DLinear` từ Task 13) để chứng minh tác động của chất lượng khôi phục (Bảng 2) lên độ chính xác dự báo (Bảng 3).
- **Sản phẩm bàn giao trên Git:**
  - `Task13_SSA_DLinear/notebooks/13_ssa_dlinear.ipynb` (đã lưu output thực chạy)
  - `Task13_SSA_DLinear/results/ssa_dlinear_metrics.csv` (3 dòng chuẩn 10 cột, `config_id=SSA_DLinear`)
  - `Task13_SSA_DLinear/results/ssa_all_3configs_summary.csv` (bảng tổng hợp 3 cấu hình SSA)
  - `Task13_SSA_DLinear/results/full/ssa_dlinear.log`, `Task13_SSA_DLinear/results/run_metadata.json`
  - `Task13_SSA_DLinear/run_info.md`, `Task13_SSA_DLinear/README.md` và `reports/Task13_Report.md`
- **Tiêu chí xác nhận hoàn thành:** `eligible_eval_rows == 206562`; số dòng từng nhóm con khớp Task 8 & Task 11; chỉ số CSV khớp log.
- **⚠️ Lưu ý kỹ thuật bắt buộc:**
  - Trong Bảng 3 của bài báo gốc, tác giả **chỉ công bố số của `SSA_DLinear` cho nhóm `Overall`** (`30.00%` / `-1.49%`), **không in số cho `Low Sale` và `High Sale`**. Vì vậy ở 2 dòng `Low Sale` và `High Sale` trong `ssa_dlinear_metrics.csv`, bắt buộc ghi đầy đủ `wape_pct, wpe_pct, mae` nhóm tự chạy nhưng **để trống** 4 cột `paper_wape_pct, paper_wpe_pct, delta_wape_pp, delta_wpe_pp` (không điền `0`).

---

### 3.4. Dương Trọng Toàn — Task 14: Dự báo 7 ngày bằng Mạng học sâu `DLinear`

- **Nhánh Git:** `feature/task14-dlinear-forecasting` | **Thư mục:** `Task14_DLinear_Forecasting/`
- **Mục tiêu:** Tái lập cột **DLinear** của Bảng 3 cho 3 cấu hình: **`DLinear_RawSales`**, **`DLinear_TimesNet`** *(chạy ngay)* và **`DLinear_DLinear`** *(chạy bổ sung khi nhận `demand_dlinear.parquet` từ Task 12)*.
- **Các bước thực hiện:**
  1. Clone `frn-50k-baseline` tại commit `8af694a`, làm việc với thư mục [`demand_forecasting/DLinear/`](https://github.com/Dingdong-Inc/frn-50k-baseline/tree/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/DLinear) trên Google Colab GPU T4.
  2. Chạy thử smoke trên 200 cặp trước để kiểm tra pipeline đầu–cuối, sau đó chạy full 50.000 cặp cho từng cấu hình theo đúng bộ cờ trong [train_predict.sh](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/DLinear/train_predict.sh) và [train_predict_on_recovered.sh](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/DLinear/train_predict_on_recovered.sh):
     - Tham số chung: `fix_seed=2025`, `--is_training 1 --train_only True --model DLinear --scale True --loss mae --features MS --revin False --total_seq_len 90 --seq_len 62 --pred_len 7 --moving_avg 28 --enc_in 7 --do_predict --itr 1 --batch_size 1024 --train_epochs 6 --learning_rate 0.001 --num_workers 2`.
     - **Cấu hình 1 (`DLinear_RawSales`):** `--data censored_dataset --data_path <train.parquet Task 6> --target sale_amount --des raw_l1`.
     - **Cấu hình 2 (`DLinear_TimesNet`):** `--data recovered_dataset --data_path <demand_timesnet.parquet Task 10> --target sale_amount_pred --des timesnet_l1`.
     - **Cấu hình 3 (`DLinear_DLinear`):** `--data recovered_dataset --data_path <demand_dlinear.parquet Task 12> --target sale_amount_pred --des dlinear_l1`.
  3. Trích xuất kết quả từ hàm `cal_metrics` trong [exp/exp_main.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/DLinear/exp/exp_main.py) và đối chiếu cột `DLinear` của Bảng 3:
     - `DLinear_RawSales`: `Overall` `31.56% / -4.89%`, `Low Sale` `39.78% / -1.03%`, `High Sale` `25.68% / -7.63%`.
     - `DLinear_TimesNet`: `Overall` `30.73% / +6.88%`, `Low Sale` `40.73% / +12.37%`, `High Sale` `23.58% / +2.98%`.
     - `DLinear_DLinear`: `Overall` `30.60% / +4.02%` (`Low Sale` & `High Sale` để trống cột `paper_*` và `delta_*`).
- **Sản phẩm bàn giao trên Git:**
  - `Task14_DLinear_Forecasting/notebooks/14_dlinear_forecasting.ipynb` (đã lưu output thực chạy), `Task14_DLinear_Forecasting/code_changes.diff`
  - `Task14_DLinear_Forecasting/results/dlinear_forecasting_metrics.csv` (9 dòng = 3 cấu hình × 3 nhóm, chuẩn 10 cột)
  - `Task14_DLinear_Forecasting/results/full/dlinear_raw_sales.log`, `dlinear_timesnet.log`, `dlinear_dlinear.log`, `Task14_DLinear_Forecasting/results/smoke/dlinear_smoke.log`, `Task14_DLinear_Forecasting/results/run_metadata.json`
  - `Task14_DLinear_Forecasting/run_info.md`, `Task14_DLinear_Forecasting/README.md` và `reports/Task14_Report.md` *(các tệp `.pth` và `real_prediction.npy` lưu trên Drive, không commit lên Git)*.
- **Tiêu chí xác nhận hoàn thành:** Cả 3 cấu hình kết thúc `exit_code == 0`, tổng mẫu đánh giá hợp lệ trên nhóm `psd >= 0` tại `cal_metrics` đạt đúng `206.562` dòng, đủ 9 dòng chỉ số hữu hạn khớp log.
- **⚠️ 4 Lưu ý kỹ thuật bắt buộc (phát hiện trực tiếp từ mã gốc `DLinear`):**
  1. **KHÔNG sửa `type=bool` và KHÔNG bỏ cờ `--revin False` / `--train_only True` trong [main.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/DLinear/main.py):** Dòng 32 của `main.py` khai báo `parser.add_argument('--revin', type=bool, default=False)`. Trong Python, truyền `--revin False` trên dòng lệnh làm `bool("False")` trả về `True` — nghĩa là lượt chạy trong bài báo thực tế **có bật chuẩn hóa `RevIN`**! Phải giữ nguyên cách truyền cờ của `.sh` gốc để tái lập đúng hành vi tác giả.
  2. **Sửa `Exp_Main.data_organization` trong `exp/exp_main.py` (dòng 347–353):** Mặc định hàm này gọi `load_dataset("Dingdong-Inc/FreshRetailNet-50K")` mỗi lần đánh giá. Hãy đổi sang đọc trực tiếp `train.parquet` (để tính `psd` gốc chuẩn xác cho mọi cấu hình) và `eval.parquet` của Task 6 từ Google Drive; ghi lại thay đổi vào `code_changes.diff`.
  3. **Luôn truyền tường minh `--data_path` cho cả `DLinear_RawSales`:** Trong `train_predict.sh` gốc không truyền `--data_path`, khiến `Dataset_Custom` tải Hugging Face còn `Dataset_Pred` ([data_loader.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/DLinear/data_provider/data_loader.py) dòng 121) lại tìm `'./train.parquet'` ở thư mục hiện hành và báo `FileNotFoundError`.
  4. **Hạ `--num_workers` từ `16` xuống `2`** để tránh nghẽn tiến trình con trên Colab, đồng thời đặt `--des` khác nhau (`raw_l1`, `timesnet_l1`, `dlinear_l1`) để thư mục checkpoint và `results/` của 3 cấu hình không ghi đè lên nhau.

---

### 3.5. Minh Nguyễn — Task 15: Dự báo SOTA bằng `TFT` (`Temporal Fusion Transformer`)

- **Nhánh Git:** `feature/task15-tft-forecasting` | **Thư mục:** `Task15_TFT_Forecasting/`
- **Mục tiêu:** Tái lập cột **TFT** (mô hình đạt độ chính xác cao nhất toàn bài báo) cho 2 cấu hình trọng tâm: **`TFT_RawSales`** và **`TFT_TimesNet`** trên Google Colab GPU NVIDIA L4 (High-RAM).
- **Các bước thực hiện:**
  1. Dùng lại bộ 3 tệp chuẩn đã có trên Google Drive từ Task 10: `train.parquet` (`b7e01c71...`), `eval.parquet` (`61cfd3cb...`) và `demand_timesnet.parquet` (`c34f4eafe087...`).
  2. Khởi tạo môi trường **Python `3.10`** độc lập bằng `micromamba` / `condacolab` trên phiên Colab GPU L4 để cài đúng bộ thư viện tương thích mã gốc [`demand_forecasting/TFT/`](https://github.com/Dingdong-Inc/frn-50k-baseline/tree/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/TFT): `torch==2.0.1+cu118`, `pytorch-lightning==1.9.4`, `pytorch-forecasting==1.0.0`, `pyarrow`, `pandas<2.2`, `numpy<2.0`, `datasets`.
  3. Chạy kiểm tra smoke trên 200 cặp trước; sau đó chạy full lần lượt [trainTFT.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/TFT/trainTFT.py) rồi [predictTFT.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/TFT/predictTFT.py) (giữ đúng cấu hình tại [configs/tft_config.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/TFT/configs/tft_config.py): `seed=2025`, `max_encoder_length=70`, `max_prediction_length=7`, `batch_size=1024`, `hidden_size=128`, `attention_head_size=8`, `lstm_layers=2`, `lr=0.01`, `max_epochs=5`):
     - **Cấu hình 1 (`TFT_RawSales`):** chạy mặc định không bật `--demand` (`data_type='censored'`).
     - **Cấu hình 2 (`TFT_TimesNet`):** chạy với `--demand --demand_path <demand_timesnet.parquet>` (`data_type='recovered'`).
  4. Đối chiếu kết quả với cột `TFT` của Bảng 3:
     - `TFT_RawSales`: `Overall` `31.75% / -7.37%`, `Low Sale` `37.04% / -1.72%`, `High Sale` `27.95% / -11.46%`.
     - `TFT_TimesNet` *(SOTA bài báo)*: `Overall` `29.02% / +2.58%`, `Low Sale` `37.33% / +7.78%`, `High Sale` `23.03% / +0.87%`.
- **Sản phẩm bàn giao trên Git:**
  - `Task15_TFT_Forecasting/notebooks/15_tft_forecasting.ipynb` (đã lưu output thực chạy), `Task15_TFT_Forecasting/code_changes.diff`
  - `Task15_TFT_Forecasting/results/tft_forecasting_metrics.csv` (6 dòng = 2 cấu hình × 3 nhóm, chuẩn 10 cột)
  - `Task15_TFT_Forecasting/results/full/tft_raw_sales.log`, `tft_timesnet.log`, `Task15_TFT_Forecasting/results/smoke/tft_smoke.log`, `Task15_TFT_Forecasting/results/run_metadata.json`
  - `Task15_TFT_Forecasting/run_info.md`, `Task15_TFT_Forecasting/README.md` và `reports/Task15_Report.md` *(checkpoint `.ckpt` trong `lightning_logs/` lưu trên Google Drive, không commit lên Git)*.
- **Tiêu chí xác nhận hoàn thành:** Cả hai lượt (`censored` và `recovered`) hoàn tất 5 epoch huấn luyện, `predictTFT.py` lọc đúng `206.562` dòng `eval` hợp lệ và xuất đủ 6 dòng chỉ số hữu hạn khớp log.
- **⚠️ 4 Lưu ý kỹ thuật sống còn (phát hiện trực tiếp từ mã gốc `TFT`):**
  1. **Bắt buộc chạy trên Python `3.10` + `pytorch-lightning==1.9.4`:** Trong [trainer/model.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/TFT/trainer/model.py) dòng 55 gọi `pl.Trainer(..., gpus=1)` và `models/base_model.py` dùng các hook vòng đời của Lightning 1.x. Nếu chạy trực tiếp trên Python 3.12/3.13 + Lightning 2.x mặc định của Colab sẽ gãy ngay với `TypeError: unexpected keyword argument 'gpus'`. Tạo môi trường Python 3.10 bằng `micromamba` giúp giữ nguyên 100% logic huấn luyện của tác giả.
  2. **Giữ đúng thứ tự tính `psd` trong `predictTFT.py` (dòng 25–34):** Khi sửa hàm `loadDataset` để nạp Parquet từ Google Drive thay vì Hugging Face, **bắt buộc tính `df_train_psd` từ `train.parquet` gốc và `merge` vào `df_eval` TRƯỚC KHI** nạp `demand_timesnet.parquet` và gán `df_train['sale_amount'] = df_train['sale_amount_pred']`. Đảo ngược thứ tự này sẽ làm lệch hoàn toàn hai nhóm `Low Sale` và `High Sale`.
  3. **Hạ `config.num_workers` từ `32` xuống `2` hoặc `4`** ở cả `trainTFT.py` (dòng 53) và `predictTFT.py` (dòng 17) để không bị tràn bộ nhớ chia sẻ (`/dev/shm`) gây crash DataLoader trên Colab; đồng thời trỏ thư mục lưu checkpoint `./lightning_logs/` sang Google Drive để bảo toàn trọng số sau mỗi epoch.
  4. **Bật chế độ High-RAM (~25 GB+ RAM trên runtime GPU L4):** Khởi tạo `TimeSeriesDataSet` cho 4,5 triệu dòng tốn nhiều RAM hệ thống. Có thể thay phép lặp `df['dt'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').weekday())` trong `trainTFT.py` / `predictTFT.py` bằng `pd.to_datetime(df['dt']).dt.weekday` (giá trị số nguyên `0..6` trùng khớp 100% nhưng giảm thời gian tiền xử lý mỗi tập từ ~20 giây xuống `0.2` giây).

---

## 4. Mẫu tin nhắn bàn giao khi tạo Pull Request

Mỗi thành viên sau khi tự kiểm tra đủ checklist ở mục tương ứng thì push nhánh `feature/task<số>-<tên>`, mở Pull Request về `main` và gửi thông tin theo mẫu:

```text
Task / Người thực hiện:
Nhánh GitHub / Link PR:
Link thư mục kết quả & checkpoint trên Google Drive (đã bật quyền xem):
SHA-256 đầu vào đã kiểm tra (train / eval / demand_*):
Số dòng hợp lệ đánh giá (ví dụ 206.562 dòng eval hoặc 783.078 ngày MNAR):
Tóm tắt kết quả chính (tự chạy vs bài báo):
Các thay đổi so với mã gốc tác giả (nếu có):
```
