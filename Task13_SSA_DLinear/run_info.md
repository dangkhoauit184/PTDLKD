# Thông tin chạy Task 13 — SSA_DLinear & Tổng hợp Cột SSA

**Cách tái lập kết quả trong repo:** mở [notebooks/13_ssa_dlinear.ipynb](notebooks/13_ssa_dlinear.ipynb), đặt đường dẫn tới `demand_dlinear.parquet` của [Task 12](../Task12_DLinear_Recovery/run_info.md) và `eval.parquet` của [Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md) (trên Google Colab notebook tự tải `demand_dlinear.parquet` qua Google Drive ID `1MDcD7cOyzcnoBu48I6eGUkSfwx8b3hkh`), rồi chạy tuần tự các ô. `python ssa_forecasting.py --demand --demand_path demand_dlinear.parquet` là lệnh tham chiếu trong [mã gốc tác giả](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/SSA/ssa_forecasting.py).

## Đầu vào và thiết lập

| Tập | File | Số dòng | Kích thước (bytes) | SHA-256 đối chiếu |
|---|---|---:|---:|---|
| Train (khôi phục DLinear — Task 12) | `demand_dlinear.parquet` | 4.500.000 | 81.531.473 | `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b` |
| Eval (Task 6) | `eval.parquet` | 350.000 | 5.451.872 | `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872` |

- **Người thực hiện:** Phạm Đăng Khoa (`dangkhoauit184`).
- **Repo nhóm đối chiếu:** nhánh `feature/task13-ssa-dlinear` tách từ commit nền `0e3806e` trên `main` (sau khi merge Task 11 & Task 12).
- **Mã tác giả đối chiếu (`frn-50k-baseline`):** commit `8af694a09a5a427d1d50648d348c022565a781f2`.
- **Môi trường chạy thực tế:** Windows CPU, Python `3.12.10`, NumPy `2.2.5`, pandas `2.2.3`, PyArrow `26.0.0`.
- **Lịch sử đưa vào SSA:** cột `sale_amount_pred` (90 ngày `train`), gán `NaN` cho 7 ngày `eval` trước khi ghép nối.
- **Phân nhóm sản phẩm (`psd`):** tính bằng trung bình `sale_amount` **gốc** trong tập `train` (`dt <= '2024-06-25'`) theo từng cặp `(store_id, product_id)` (`Overall: psd >= 0`, `Low Sale: psd < 1`, `High Sale: psd >= 1`), trùng khớp 100% danh sách cặp với [Task 8](../Task08_SSA_Raw_Sales/run_info.md) và [Task 11](../Task11_SSA_TimesNet/run_info.md).
- **Đánh giá Ground Truth:** đối chiếu với `sale_amount` thật trên đúng **206.562** dòng `eval` có `stock_hour6_22_cnt == 0` (`Low Sale = 153.208` dòng, `High Sale = 53.354` dòng); tính WAPE, WPE, MAE theo từng ngày rồi lấy trung bình qua 7 ngày (`2024-06-26` → `2024-07-02`). SSA là thuật toán tất định, không dùng seed hay checkpoint huấn luyện.
- **Quy ước số tham chiếu bài báo:** Trong Bảng 3 của bài báo gốc, tác giả chỉ công bố số của `SSA_DLinear` cho nhóm `Overall` (`WAPE = 30.00%`, `WPE = -1.49%`), không in cho `Low Sale` và `High Sale`. Theo quy ước nhóm, 4 cột `paper_wape_pct`, `paper_wpe_pct`, `delta_wape_pp`, `delta_wpe_pp` ở hai dòng `Low Sale` và `High Sale` được để trống (không điền `0`).

## File kết quả bàn giao

- [CSV ba nhóm `SSA_DLinear`](results/ssa_dlinear_metrics.csv): chuẩn 10 cột (`config_id=SSA_DLinear`).
- [CSV tổng hợp 3 cấu hình cột SSA](results/ssa_all_3configs_summary.csv): 9 dòng ghép trực tiếp `SSA_RawSales` ([Task 8](../Task08_SSA_Raw_Sales/results/ssa_raw_sales_metrics.csv)), `SSA_DLinear` (Task 13) và `SSA_TimesNet` ([Task 11](../Task11_SSA_TimesNet/results/ssa_timesnet_metrics.csv)).
- [Log gốc](results/full/ssa_dlinear.log): WAPE và WPE ở dạng tỷ lệ thập phân; MAE giữ đơn vị doanh số chuẩn hóa.
- [Metadata lượt chạy](results/run_metadata.json) và [Báo cáo phân tích Task 13](../reports/Task13_Report.md).
