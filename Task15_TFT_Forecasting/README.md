# Task 15 — Dự báo SOTA bằng Temporal Fusion Transformer (TFT)

Thư mục chứa notebook, bản vá, log và kết quả tái lập cột **TFT** (Bảng 3 bài báo FreshRetailNet-50K) cho 2 cấu hình trọng tâm:
- **`TFT_RawSales`** (`data_type='censored'`): huấn luyện trực tiếp trên doanh số bị che khuất `train.parquet`.
- **`TFT_TimesNet`** (`data_type='recovered'`): huấn luyện trên nhu cầu đã khôi phục `sale_amount_pred` từ `demand_timesnet.parquet` (Task 10).

## Cấu trúc thư mục
```text
Task15_TFT_Forecasting/
├── README.md
├── run_info.md
├── code_changes.diff
├── notebooks/
│   └── 15_tft_forecasting.ipynb
└── results/
    ├── tft_forecasting_metrics.csv
    ├── run_metadata.json
    ├── smoke/tft_smoke.log
    └── full/
        ├── tft_raw_sales.log
        └── tft_timesnet.log
```

## Cách chạy lại
1. Mở `notebooks/15_tft_forecasting.ipynb` trên Google Colab với runtime **NVIDIA L4 GPU (High-RAM)**.
2. Cập nhật 4 đường dẫn Google Drive ở Cell 2 (khớp SHA-256 của `train.parquet`, `eval.parquet`, `demand_timesnet.parquet`).
3. Chạy tuần tự Cell 1 → Cell 10 (môi trường Python 3.10 + `pytorch-lightning==1.9.4` + `pandas==1.5.3` được khởi tạo tự động bằng `micromamba`).
