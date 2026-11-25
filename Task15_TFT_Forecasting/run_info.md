# Task 15 — Run Info (TFT Forecasting: `TFT_RawSales` & `TFT_TimesNet`)

- **Thời điểm hoàn tất (UTC):** 2026-11-25T11:40:57.778312+00:00
- **Người thực hiện:** Minh Nguyễn | **Nhánh:** `feature/task15-tft-forecasting`
- **Phần cứng:** Google Colab GPU `NVIDIA L4` (High-RAM)
- **Môi trường Python 3.10 độc lập (`micromamba`):** Python `3.10.22`, PyTorch `2.0.1+cu118`, PyTorch Lightning `1.9.4`, PyTorch Forecasting `1.0.0`, NumPy `1.26.4`, Pandas `1.5.3`, PyArrow `25.0.1`
- **Mã tác giả đối chiếu (`frn-50k-baseline`):** commit `8af694a09a5a427d1d50648d348c022565a781f2`
- **Bản vá áp dụng:** Xem [code_changes.diff](code_changes.diff) (nạp Parquet local giữ đúng thứ tự tính `df_train_psd` trước khi thay `sale_amount_pred`, vectorize `day_of_week`, `num_workers=4`, tách thư mục `lightning_logs` lên Drive và hỗ trợ smoke 200 cặp).

## Đầu vào đã kiểm định SHA-256
- `train.parquet` ([Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md)): `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96`
- `eval.parquet` ([Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md)): `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`
- `demand_timesnet.parquet` ([Task 10](../Task10_TimesNet_Recovery/run_info.md)): `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`

## Lệnh chạy chính thức
```bash
# Cấu hình 1: TFT_RawSales (censored)
python -u trainTFT.py
python -u predictTFT.py

# Cấu hình 2: TFT_TimesNet (recovered)
python -u trainTFT.py --demand --demand_path /content/frn_cache/demand_timesnet.parquet
python -u predictTFT.py --demand --demand_path /content/frn_cache/demand_timesnet.parquet
```

## Thời gian chạy & kiểm định
- Smoke 200 cặp (2 epoch): `0.56` phút — log: `results/smoke/tft_smoke.log`
- Full `TFT_RawSales` (5 epoch + predict): `49.12` phút — log: `results/full/tft_raw_sales.log`
- Full `TFT_TimesNet` (5 epoch + predict): `49.27` phút — log: `results/full/tft_timesnet.log`
- Số dòng eval hợp lệ (`stock_hour6_22_cnt == 0`): **206.562** (`153.208` Low Sale + `53.354` High Sale) ở cả 2 cấu hình.

## Liên kết checkpoint trên Google Drive (không commit lên Git)
- Thư mục `lightning_logs/` (gồm `censored/checkpoints/*.ckpt` và `recovered/checkpoints/*.ckpt`): https://drive.google.com/drive/folders/1gPexk9JqLJFH-MUPFE-7d69g9pQa7xD2
