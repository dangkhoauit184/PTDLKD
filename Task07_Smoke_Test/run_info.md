# Task 7 — Thông tin lượt chạy smoke

## Trạng thái thực tế

**not_run** — chưa có bước chọn cặp, SSA, TimesNet hoặc SSA trên nhu cầu TimesNet nào được thực thi. `smoke_pairs.csv` chỉ chứa header; các metric để trống. Không tạo `demand_timesnet_smoke.parquet` vì không có mô hình chạy. Các log ghi lý do `not_run`, không chứa số liệu mô phỏng.

## Dữ liệu

- Ưu tiên Task 6: `train.parquet` và `eval.parquet` ở repo root.
- Task 6 tham chiếu train SHA-256 `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96` và eval SHA-256 `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`; các file không có trong workspace để kiểm tra hash.
- Hugging Face fallback chính thức: `Dingdong-Inc/FreshRetailNet-50K`. Chưa nạp hoặc tải dữ liệu vì Python runtime/package `datasets` không khả dụng.
- Số cặp, dòng train/eval, khóa đã kiểm tra: **0**. Chưa có eval nào dùng trong huấn luyện.

## Môi trường và nguyên nhân

- Repo baseline: `19483da785f171cb28699e3cba2ae16d6512089a` (`feature/task07-smoke-test`).
- Mã tác giả dự kiến: `Dingdong-Inc/frn-50k-baseline` commit `8af694a09a5a427d1d50648d348c022565a781f2`.
- `python --version` không chạy được: lệnh trỏ tới Windows App Execution Alias và báo Python không được cài. Không tìm thấy `py`, Conda, hoặc Python đã cấu hình trong VS Code.
- Vì không có Python, chưa thể import/kiểm tra thực tế PyTorch, NumPy, pandas, PyArrow, `datasets` hoặc native extensions.
- Có GPU NVIDIA GeForce RTX 4060, driver 566.26 / CUDA driver 12.7; tại lúc kiểm tra GPU đang dùng 6.159/8.188 MiB. GPU driver không cung cấp Python/PyTorch runtime. WSL không khả dụng (`REGDB_E_CLASSNOTREG`); không tìm thấy runtime Colab/kernel đã cấu hình.
- Không cài package, không đổi hệ thống và không bỏ qua bảo vệ môi trường.

## Cấu hình dự kiến — chưa chạy

- Seed chọn cặp: `2024`.
- TimesNet: `--model TimesNet --missing_rate 0 --epochs 1 --batch_size 128 --seed 1024`.
- `load_data` và `_demand_recovery` trong bản runtime tạm sẽ cùng đọc `train_smoke.parquet`; lệnh phục hồi và cả hai SSA sẽ nhận đường dẫn rõ ràng. SSA raw và SSA TimesNet sẽ dùng cùng `eval_smoke.parquet` 700 dòng.
- Baseline `EPOCHS=5`; một epoch là giảm smoke đã định trước, không phải kết quả đã chạy.

## Lệnh tái chạy

Trong kernel Python tương thích theo `Task03_Environment_Setup/` và `requirements.txt`, mở `07_smoke_test.ipynb` rồi chạy tất cả cell từ đầu. Pipeline ghi CSV/log/run_info, lấy Parquet Task 6 nếu hash đúng hoặc dùng Hugging Face chính thức. Các lệnh con được tạo bởi notebook:

```text
python Task07_Smoke_Test/smoke_pipeline.py
python app.py --model TimesNet --missing_rate 0 --train_path <train_smoke.parquet> --demand_path <Task07_Smoke_Test/demand_timesnet_smoke.parquet> --epochs 1 --batch_size 128 --seed 1024
python ssa_forecasting_smoke.py --train_path <train_smoke.parquet> --eval_path <eval_smoke.parquet> --metrics_path <raw_metrics.csv>
python ssa_forecasting_smoke.py --demand --demand_path <Task07_Smoke_Test/demand_timesnet_smoke.parquet> --eval_path <eval_smoke.parquet> --metrics_path <timesnet_metrics.csv>
```

Các lệnh SSA là bản CLI tạm được tạo từ đúng commit tác giả để thêm `--train_path`, `--eval_path` và metrics CSV; logic dự báo/đánh giá SSA được giữ nguyên. Mọi bản patch, file Parquet thử và output huấn luyện nằm trong `smoke/tmp/`, không đưa vào Git.

## Bàn giao hiện có

- `07_smoke_test.ipynb`, `smoke_pipeline.py`: quy trình có thể tái chạy, gồm kiểm tra hash, chọn cặp, đường dẫn train/eval tường minh, đối soát khóa, metric và log.
- `smoke_pairs.csv`: header-only do chưa thể chọn cặp.
- `smoke_metrics.csv`: hai hàng Overall `not_run`, metric để trống.
- `smoke/ssa_raw.log`, `smoke/timesnet.log`, `smoke/ssa_timesnet.log`: trạng thái và lỗi/điều kiện chạy.
- `demand_timesnet_smoke.parquet`: **không tồn tại**, không tạo file giả.

CSV, Parquet và log bị `.gitignore` loại khỏi Git theo `docs/Contribution_Guide.md`; chỉ notebook, pipeline và biên bản được đưa lên nhánh. Chưa có số liệu smoke để ghi vào Bảng 3.
