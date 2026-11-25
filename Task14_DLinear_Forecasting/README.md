# Task 14 - DLinear Forecasting

Task này tái lập ba cấu hình DLinear của Bảng 3.

## Trạng thái

- `DLinear_RawSales`: hoàn tất.
- `DLinear_TimesNet`: hoàn tất.
- `DLinear_DLinear`: hoàn tất.

## Cấu hình chung

- Commit mã gốc: `8af694a09a5a427d1d50648d348c022565a781f2`
- Seed: `2025`
- `train_only=True`, `loss=mae`, `features=MS`
- `total_seq_len=90`, `seq_len=62`, `pred_len=7`
- `moving_avg=28`, `enc_in=7`, `itr=1`
- `batch_size=1024`, `train_epochs=6`, `learning_rate=0.001`
- `num_workers=0` trên Windows; giữ `num_workers=2` trên Colab/Linux theo kế hoạch.

## Sản phẩm

- [Chỉ số hoàn tất](results/dlinear_forecasting_metrics.csv)
- [Log RawSales](results/full/dlinear_raw_sales.log)
- [Log TimesNet](results/full/dlinear_timesnet.log)
- [Log smoke](results/smoke/dlinear_smoke.log)
- [Thay đổi mã nguồn](code_changes.diff)
- [Báo cáo](../reports/Task14_Report.md)

