# Task 7 — Thông tin lượt chạy smoke

- Thời điểm ghi: `2026-11-17T21:53:39.688255+00:00`
- Repo baseline: `19483da785f171cb28699e3cba2ae16d6512089a`
- Mã tác giả FreshRetailNet-50K: `8af694a09a5a427d1d50648d348c022565a781f2` ([repo](https://github.com/Dingdong-Inc/frn-50k-baseline/tree/8af694a09a5a427d1d50648d348c022565a781f2)).
- Dataset dự phòng chính thức: `Dingdong-Inc/FreshRetailNet-50K`.
- Seed chọn cặp: `2024`.
- TimesNet: `--model TimesNet --missing_rate 0 --epochs 1 --batch_size 128 --seed 1024`.
- Eval chỉ dùng để chọn/đánh giá cặp; không dùng để huấn luyện.

## Nguồn dữ liệu

- Nguồn: Task 6 train.parquet/eval.parquet không có ở repo root; Hugging Face `Dingdong-Inc/FreshRetailNet-50K` là fallback nhưng chưa được nạp
- SHA-256 train tham chiếu Task 6: `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96`
- SHA-256 eval tham chiếu Task 6: `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`
- Chỉ ghi hash thực tế ở các dòng dưới sau khi dữ liệu được đọc và xác minh.
- SHA-256 train: chưa kiểm tra
- SHA-256 eval: chưa kiểm tra
- Khi chọn cặp thành công, train/eval thử được ghi thành Parquet riêng và truyền đường dẫn tường minh cho TimesNet lẫn SSA.

## Môi trường

- Python: 3.15.2
- Interpreter: `C:\Users\trong\AppData\Roaming\uv\python\cpython-3.15.2-windows-x86_64-none\python.exe`
- NumPy: chưa import được
- pandas: chưa import được
- PyArrow: chưa import được
- PyTorch/CUDA: chưa import được

## Kiểm tra dữ liệu

- Cặp đã chọn: 0 / 100
- Train đã kiểm tra: 0 / 9.000 dòng; 0 khóa duy nhất
- Eval đã kiểm tra: 0 / 700 dòng; 0 khóa duy nhất
- Eval hợp lệ (`stock_hour6_22_cnt == 0`): 0 dòng
- Đầu ra nhu cầu: `demand_timesnet_smoke.parquet` chưa được tạo.

## Trạng thái

- `SSA_RawSales`: **not_run**
- `TimesNet`: **not_run**
- `SSA_TimesNet`: **not_run**

## Lệnh chạy

- Tái chạy pipeline: `python Task07_Smoke_Test/smoke_pipeline.py` (hoặc chạy tất cả cell trong `07_smoke_test.ipynb`).
- TimesNet dự kiến: `python app.py --model TimesNet --missing_rate 0 --train_path <train_smoke.parquet> --demand_path <Task07_Smoke_Test/demand_timesnet_smoke.parquet> --epochs 1 --batch_size 128 --seed 1024`.
- SSA raw dự kiến: `python ssa_forecasting_smoke.py --train_path <train_smoke.parquet> --eval_path <eval_smoke.parquet> --metrics_path <raw_metrics.csv>`.
- SSA TimesNet dự kiến: `python ssa_forecasting_smoke.py --demand --demand_path <Task07_Smoke_Test/demand_timesnet_smoke.parquet> --eval_path <eval_smoke.parquet> --metrics_path <timesnet_metrics.csv>`.
- Các lệnh dự kiến chưa được chạy nếu chưa xuất hiện trong phần `Đã chạy`.

## Lỗi / giới hạn

- Data/preflight: RuntimeError: Required imports failed: numpy: ModuleNotFoundError: No module named 'numpy'; pandas: ModuleNotFoundError: No module named 'pandas'; pyarrow: ModuleNotFoundError: No module named 'pyarrow'; torch: ModuleNotFoundError: No module named 'torch'

Các CSV, Parquet và log thuộc dữ liệu/kết quả của lượt chạy; giữ ngoài Git theo `docs/Contribution_Guide.md`. Không chép kết quả smoke vào Bảng 3.
