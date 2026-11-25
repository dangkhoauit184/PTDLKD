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
    ├── table3_all_8configs_summary.csv
    ├── run_metadata.json
    ├── smoke/tft_smoke.log
    └── full/
        ├── tft_raw_sales.log
        └── tft_timesnet.log
```

## Tài liệu & Báo cáo liên quan
- Biên bản chạy & link checkpoint Google Drive: [run_info.md](run_info.md)
- Báo cáo phân tích chi tiết Task 15: [Task15_Report.md](../reports/Task15_Report.md)
- Bảng tổng hợp 8 cấu hình Bảng 3 (`SSA`, `DLinear`, `TFT` — 24 dòng): [table3_all_8configs_summary.csv](results/table3_all_8configs_summary.csv)

## Cách chạy lại
1. Mở [notebooks/15_tft_forecasting.ipynb](notebooks/15_tft_forecasting.ipynb) trên Google Colab với runtime **NVIDIA L4 GPU (High-RAM)**.
2. Kiểm tra/cập nhật 4 đường dẫn Google Drive ở **Bước 2** (tự động đối soát SHA-256 của `train.parquet`, `eval.parquet`, `demand_timesnet.parquet`).
3. Chạy tuần tự từ **Bước 1 → Bước 12** (môi trường Python 3.10 + `pytorch-lightning==1.9.4` + `pandas==1.5.3` được khởi tạo tự động bằng `micromamba`).
