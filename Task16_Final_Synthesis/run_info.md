# Thông tin chạy thực nghiệm — Task 16 (Kiểm định Thống kê IS403 & Đóng gói Cuối kỳ)

- **Nhiệm vụ:** Task 16 — Kiểm định giả thuyết thống kê Chương 2 IS403, giải mã cơ chế nghiệp vụ `SSA` vs `DLinear` vs `TFT`, xuất bộ biểu đồ tổng hợp, Báo cáo Word `.docx` và Slide thuyết trình cuối kỳ
- **Nhánh Git:** `feature/task16-final-synthesis`
- **Môi trường thực thi:** Python `3.12.10` | NumPy `2.2.5` | Pandas `2.2.3` | SciPy `1.15.2` | PyArrow `26.0.0` | Matplotlib `3.10.1` | python-docx `1.2.0`
- **Thời gian thực thi tính toán & xuất biểu đồ:** `16,29` giây — log chi tiết: [task16_statistical_synthesis.log](results/full/task16_statistical_synthesis.log)

## Danh mục Dữ liệu Parquet & Hiện vật Google Drive Dùng Chung (Đã kiểm chứng SHA-256)

1. **`train.parquet`** (có sẵn trong repo tại [Task06_Data_Preparation/train.parquet](../Task06_Data_Preparation/train.parquet) | [biên bản Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md)):
   - Kích thước: `4.500.000` dòng × `19` cột (`58,25 MiB`)
   - SHA-256: `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96`
2. **`eval.parquet`** (có sẵn trong repo tại [Task06_Data_Preparation/eval.parquet](../Task06_Data_Preparation/eval.parquet) | [biên bản Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md)):
   - Kích thước: `350.000` dòng × `19` cột (`5,20 MiB`), gồm `206.562` quan sát không hết hàng hợp lệ (`153.208` Low Sale + `53.354` High Sale)
   - SHA-256: `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`
3. **`demand_timesnet.parquet`** ([biên bản Task 10](../Task10_TimesNet_Recovery/run_info.md)):
   - Link tải Google Drive: https://drive.google.com/file/d/1f9db-U9f9C9OFS-V2EcmQv4FIU3bguR3/view?usp=sharing
   - Kích thước: `4.500.000` dòng × `20` cột (`77,78 MiB`)
   - SHA-256: `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`
4. **`demand_dlinear.parquet`** ([biên bản Task 12](../Task12_DLinear_Recovery/run_info.md)):
   - Link tải Google Drive: https://drive.google.com/file/d/1MDcD7cOyzcnoBu48I6eGUkSfwx8b3hkh/view?usp=drive_link
   - Kích thước: `4.500.000` dòng × `20` cột (`77,75 MiB`)
   - SHA-256: `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b`
5. **Checkpoint mô hình SOTA `TFT` (`lightning_logs/`)** ([biên bản Task 15](../Task15_TFT_Forecasting/run_info.md)):
   - Link thư mục Google Drive (`HTTP 200 OK`): https://drive.google.com/drive/folders/1gPexk9JqLJFH-MUPFE-7d69g9pQa7xD2

## Sản phẩm đã kiểm chứng
- Notebook tổng hợp đã chạy và lưu đầy đủ output: [16_final_synthesis.ipynb](notebooks/16_final_synthesis.ipynb)
- Bảng kiểm định thống kê Chương 2 IS403 (`21` phép kiểm định): [statistical_tests_is403.csv](results/statistical_tests_is403.csv)
- Bảng cơ chế khôi phục nhu cầu theo phân khúc SKU: [recovery_regime_mechanism.csv](results/recovery_regime_mechanism.csv)
- Bộ 6 biểu đồ tổng hợp `300 DPI`: `results/figures/01_*.png` → `06_*.png`
- Quyển Báo cáo tổng kết cuối kỳ (Word): [Bao_Cao_Cuoi_Ky_IS403_FreshRetailNet50K.docx](deliverables/Bao_Cao_Cuoi_Ky_IS403_FreshRetailNet50K.docx)
- Bộ Slide thuyết trình cuối kỳ (Markdown Marp & HTML tương tác 16:9): [Slide_Thuyet_Trinh_IS403_FreshRetailNet50K.md](deliverables/Slide_Thuyet_Trinh_IS403_FreshRetailNet50K.md) và [Slide_Thuyet_Trinh_IS403_FreshRetailNet50K.html](deliverables/Slide_Thuyet_Trinh_IS403_FreshRetailNet50K.html)
