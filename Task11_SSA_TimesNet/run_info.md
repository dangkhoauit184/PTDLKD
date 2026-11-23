# Thông tin chạy Task 11 — SSA_TimesNet

**Cách tái lập kết quả trong repo:** mở [notebook](notebooks/11_ssa_timesnet.ipynb), đặt đường dẫn tới `demand_timesnet.parquet` của [Task 10](../Task10_TimesNet_Recovery/run_info.md) và `eval.parquet` của [Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md) (trên Google Colab notebook tự tải `demand_timesnet.parquet` qua Google Drive ID `1f9db-U9f9C9OFS-V2EcmQv4FIU3bguR3`), rồi chạy lần lượt các ô. `python ssa_forecasting.py --demand --demand_path demand_timesnet.parquet` là lệnh tham chiếu trong [mã gốc tác giả](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/SSA/ssa_forecasting.py).

## Đầu vào và thiết lập

| Tập | File | Số dòng | Kích thước (bytes) | SHA-256 đối chiếu |
|---|---|---:|---:|---|
| Train (khôi phục TimesNet — Task 10) | `demand_timesnet.parquet` | 4.500.000 | 81.562.029 | `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694` |
| Eval (Task 6) | `eval.parquet` | 350.000 | 5.451.872 | `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872` |

- **Người thực hiện:** Sinhvienvuitinh (`TRILE1603`).
- **Repo nhóm đối chiếu:** nhánh `feature/task11-ssa-timesnet` tách từ commit nền `bfff86f` trên `main`.
- **Mã tác giả đối chiếu (`frn-50k-baseline`):** commit `8af694a09a5a427d1d50648d348c022565a781f2`.
- **Môi trường kiểm chứng đã lưu:** Windows CPU, Python `3.12.10`, NumPy `2.2.5`, pandas `2.2.3`, PyArrow `26.0.0` (khớp 100% từng dòng log và chỉ số với lượt chạy trên Google Colab Python `3.13` của thành viên phụ trách).
- **Lịch sử đưa vào SSA:** cột `sale_amount_pred` (90 ngày `train`), gán `NaN` cho 7 ngày `eval` trước khi ghép nối.
- **Phân nhóm sản phẩm (`psd`):** tính bằng trung bình `sale_amount` **gốc** trong tập `train` (`dt <= '2024-06-25'`) theo từng cặp `(store_id, product_id)` (`Overall: psd >= 0`, `Low Sale: psd < 1`, `High Sale: psd >= 1`), trùng khớp 100% danh sách cặp với [Task 8](../Task08_SSA_Raw_Sales/run_info.md).
- **Đánh giá Ground Truth:** đối chiếu với `sale_amount` thật trên đúng **206.562** dòng `eval` có `stock_hour6_22_cnt == 0` (`Low Sale = 153.208` dòng, `High Sale = 53.354` dòng); tính WAPE, WPE, MAE theo từng ngày rồi lấy trung bình qua 7 ngày (`2024-06-26` → `2024-07-02`). SSA là thuật toán tất định, không dùng seed hay checkpoint huấn luyện.

## File kết quả bàn giao

- [CSV ba nhóm `SSA_TimesNet`](results/ssa_timesnet_metrics.csv): chuẩn 10 cột (`config_id=SSA_TimesNet`).
- [CSV đối chiếu song song Task 8 vs Task 11](results/ssa_raw_vs_timesnet_comparison.csv): 6 dòng đặt cạnh nhau `SSA_RawSales` (đọc trực tiếp từ CSV Task 8) và `SSA_TimesNet`.
- [Log gốc](results/full/ssa_timesnet.log): WAPE và WPE ở dạng tỷ lệ thập phân; MAE giữ đơn vị doanh số chuẩn hóa.
- [Metadata lượt chạy](results/run_metadata.json) và [Báo cáo phân tích Task 11](../reports/Task11_Report.md).
