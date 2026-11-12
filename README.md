# IS403 - Phân Tích Dữ Liệu Kinh Doanh | Đồ Án Nhóm
## Tái Lập và Đánh Giá Thực Nghiệm Bộ Dữ Liệu Bán Lẻ Đồ Tươi Sống FreshRetailNet-50K

[![Python 3.8+](https://img.shields.io/badge/python-3.8%20%7C%203.10%20%7C%203.12-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0.1-EE4C2C.svg)](https://pytorch.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Repository](https://img.shields.io/badge/GitHub-PTDLKD-green.svg)](https://github.com/dangkhoauit184/PTDLKD)

> **Đề tài:** Khôi phục Nhu cầu Tiềm ẩn bằng TimesNet và Dự báo Doanh số Kháng Hết hàng bằng SSA trên Bộ dữ liệu FreshRetailNet-50K.  
> **Bài báo tham chiếu:** *FreshRetailNet-50K: A Stockout-Annotated Censored Demand Dataset for Latent Demand Recovery and Forecasting in Fresh Retail* (arXiv: [2505.16319v5](https://arxiv.org/abs/2505.16319), Dingdong Ltd.).

---

## 📖 1. Giới Thiệu Đề Tài

Trong ngành bán lẻ thực phẩm tươi sống với mô hình kho vệ tinh giao hàng nhanh 30 phút, tình trạng **hết hàng (stockout)** diễn ra liên tục do hạn sử dụng ngắn và nhu cầu biến động mạnh. Khi hết hàng, doanh số ghi nhận trên hệ thống rơi về $0$ dù nhu cầu thực tế của khách hàng vẫn tồn tại — hiện tượng này gọi là **Demand Censoring** (Nhu cầu bị che khuất).

Mô hình dự báo truyền thống nếu học trực tiếp từ doanh số bị che khuất sẽ rơi vào **vòng lặp sai lệch dự báo thấp (Under-forecasting Bias Loop)**. Đồ án này triển khai khung nghiên cứu **2 giai đoạn (Two-Stage Framework)**:
1. **Giai đoạn 1 (Latent Demand Recovery):** Dùng mô hình học sâu chuỗi thời gian đa chu kỳ **TimesNet** để khôi phục lượng bán bị che trong các giờ hết hàng.
2. **Giai đoạn 2 (Demand Forecasting):** Tích lũy nhu cầu đã khôi phục lên cấp độ ngày và áp dụng thuật toán **Similar Scenario Average (SSA)** để dự báo 7 ngày tương lai.

```
[Dữ liệu 50K chuỗi: Giờ bán + Nhãn hết hàng]
           │
           ▼
┌────────────────────────────────────────────────────────┐
│ Giai đoạn 1: TimesNet Latent Demand Recovery          │
│ • Imputation chuỗi thời gian với mặt nạ stockout       │
│ • Đầu ra: demand.parquet (Nhu cầu giờ đã khôi phục)    │
└────────────────────────────────────────────────────────┘
           │
           ▼ (Tích lũy 24h thành ngày)
┌────────────────────────────────────────────────────────┐
│ Giai đoạn 2: Censoring-Robust Demand Forecasting (SSA) │
│ • Dự báo 7 ngày trên nhóm Overall, High-sale, Low-sale│
│ • Đối chứng: Raw Sales Pipeline vs TimesNet Pipeline  │
└────────────────────────────────────────────────────────┘
```

---

## 👥 2. Thành Viên Nhóm & Phân Công Nhiệm Vụ

Dự án được phân chia thành 5 Task chuyên biệt với sự phối hợp chặt chẽ giữa các thành viên:

| Task | Nhiệm vụ chính | Người phụ trách | Trạng thái |
| :---: | :--- | :---: | :---: |
| **Task 1** | **Đọc bài báo & Chốt phạm vi nghiên cứu:** Phân tích cơ chế MNAR, vòng lặp bias, chốt Bảng 2 & Bảng 3. | Thành viên nhóm | ✅ Hoàn thành |
| **Task 2** | **Lập kế hoạch thực nghiệm:** Thiết lập 15 cấu hình dự báo, bóc tách siêu tham số 7 mô hình PyPOTS. | Thành viên nhóm | ✅ Hoàn thành |
| **Task 3** | **Chuẩn bị môi trường & Pipeline:** Cấu hình Colab GPU, giải quyết xung đột thư viện, tối ưu hóa I/O Parquet. | Thành viên nhóm | ✅ Hoàn thành |
| **Task 4** | **Kiểm tra và đối soát dữ liệu (Validation):** Xây dựng notebook kiểm định 48 quy tắc trên 4.85M dòng, phát hiện 34 dòng discount bất thường. | **Đăng Khoa** | ✅ Hoàn thành |
| **Task 5** | **Khám phá thống kê mô tả (EDA):** Tối ưu RAM, phân tích phân phối lệch phải, quy luật chữ U của hết hàng, nguyên lý Pareto 20-87. | Thành viên nhóm | ✅ Hoàn thành |

---

## 📂 3. Cấu Trúc Repository

```text
PTDLKD/
│
├── .gitignore                          # Loại trừ các file dataset nặng (>1.2GB) và checkpoint
├── README.md                           # Tài liệu tổng quan dự án (file này)
├── requirements.txt                    # Danh sách thư viện và phiên bản chính xác
│
├── docs/                               # Tài liệu hướng dẫn và tổng quan
│   ├── Project_Overview.md             # Phân tích sâu bài toán kinh doanh và cơ chế MNAR
│   └── Contribution_Guide.md           # Quy định Git Workflow (Branch, PR, Merge) cho nhóm
│
├── reports/                            # Báo cáo chuẩn hóa 8 phần theo chuẩn học thuật
│   ├── Task01_Report.md                # Báo cáo Task 1: Nghiên cứu bài báo
│   ├── Task02_Report.md                # Báo cáo Task 2: Kế hoạch thực nghiệm
│   ├── Task03_Report.md                # Báo cáo Task 3: Môi trường & Pipeline
│   ├── Task04_Report.md                # Báo cáo Task 4: Đối soát chất lượng dữ liệu
│   ├── Task05_Report.md                # Báo cáo Task 5: Thống kê mô tả (EDA)
│   └── Synthesis_Report.md             # Báo cáo tổng hợp toàn bộ 5 Task của dự án
│
├── Task01_Paper_Review/                # Thư mục làm việc Task 1
│   ├── README.md
│   └── docs/
│       ├── paper_summary.md
│       └── replicated_tables_target.md
│
├── Task02_Experiment_Plan/             # Thư mục làm việc Task 2
│   ├── README.md
│   └── docs/
│       ├── 15_forecasting_configurations.md
│       └── model_hyperparameters.md
│
├── Task03_Environment_Setup/           # Thư mục làm việc Task 3
│   ├── README.md
│   ├── requirements.txt
│   └── scripts/
│       ├── setup_colab.sh              # Cài đặt tự động trên Google Colab
│       └── download_data.py            # Tải dữ liệu HuggingFace xuất Parquet
│
├── Task04_Data_Validation/             # Thư mục làm việc Task 4 (Đăng Khoa)
│   ├── README.md
│   ├── notebooks/
│   │   └── 04_data_validation_colab.ipynb  # Notebook kiểm định 48 quy tắc
│   └── results/                        # Kết quả đối soát dữ liệu (CSV & JSON)
│       ├── validation_summary.csv
│       ├── column_profile.csv
│       ├── issue_examples.csv
│       └── run_info.json
│
└── Task05_EDA/                         # Thư mục làm việc Task 5
    ├── README.md
    ├── notebooks/
    │   ├── Task5_EDA_01_tai_du_lieu.ipynb  # Tải dữ liệu & Tiền xử lý RAM
    │   └── Task5_EDA_02_thong_ke_mo_ta.ipynb # Thống kê chi tiết & Vẽ biểu đồ
    └── results/
        └── summary_statistics.json     # Tóm tắt chỉ số thống kê
```

---

## 📊 4. Tóm Tắt Kết Quả Nổi Bật Của Các Task

### Task 4 (Kiểm định Dữ liệu)
* Đã kiểm định toàn bộ $4.500.000$ dòng train và $350.000$ dòng eval qua $48$ quy tắc nghiêm ngặt:
  * **$100\%$ toàn vẹn:** $0$ giá trị null, $0$ khóa trùng lặp, $100\%$ các cặp có đủ $90$ ngày train và $7$ ngày eval.
  * **$100\%$ nhất quán:** Tổng doanh số giờ khớp hoàn toàn doanh số ngày; số giờ hết hàng khớp với số bit $1$ trong khung giờ $6..21$.
  * **Phát hiện dị thường:** Tìm thấy duy nhất $34$ bản ghi có `discount > 1.0` (max 1.088) trong tập train và đã đề xuất xử lý clip về $1.0$.

### Task 5 (Thống kê Mô tả & EDA)
* **Phân phối doanh số:** Lệch phải mạnh (`mean = 0.999`, `median = 0.700`, `skewness = 8.47`).
* **Độ thưa thớt theo giờ:** Chỉ $4.46\%$ số ngày có doanh số $= 0$, nhưng có tới $69.06\%$ số giờ trong khung $6..21$ bằng $0$.
* **Hiện tượng hết hàng:** Chiếm $19.88\%$ số giờ kinh doanh, có dạng **chữ U** đạt đỉnh $41.9\%$ vào lúc 22h đêm.
* **Nguyên tắc Pareto:** $20\%$ sản phẩm chiếm tới $87.0\%$ tổng doanh số bán ra toàn mạng lưới.

### Đối chiếu Hiệu năng Dự báo (Bảng 3 Tái lập)
| Nhóm Đánh Giá | SSA trên Doanh số Gốc | SSA trên Nhu cầu TimesNet | Mức Độ Cải Thiện |
| :--- | :---: | :---: | :--- |
| **Overall (Toàn bộ)** | WAPE $31.97\%$ \| WPE $-10.50\%$ | **WAPE $29.79\%$ \| WPE $+1.39\%$** | **WAPE giảm $2.18\%$, xóa bỏ bias âm** |
| **High Sale (Bán chạy)** | WAPE $27.40\%$ \| WPE $-12.26\%$ | **WAPE $23.98\%$ \| WPE $-1.12\%$** | **WAPE giảm $3.42\%$, bias chỉ còn $-1.1\%$** |
| **Low Sale (Bán chậm)** | WAPE $38.33\%$ \| WPE $-8.03\%$ | WAPE $37.87\%$ \| WPE $+4.89\%$ | Giảm sai số tuyệt đối, xuất hiện bias dương nhẹ |

---

## 🚀 5. Hướng Dẫn Cài Đặt và Chạy

### Cách 1: Chạy trên Google Colab (Khuyến nghị cho huấn luyện GPU)
1. Mở notebook cần chạy trong thư mục `Task04_Data_Validation/notebooks/` hoặc `Task05_EDA/notebooks/` bằng Google Colab.
2. Đổi môi trường thực thi: **Runtime** $\rightarrow$ **Change runtime type** $\rightarrow$ Chọn **T4 GPU** hoặc **L4 GPU**.
3. Chạy ô đầu tiên để kết nối Google Drive và cài đặt thư viện tự động.

### Cách 2: Chạy trên Máy Cá Nhân (Local)
```bash
# 1. Clone repository
git clone https://github.com/dangkhoauit184/PTDLKD.git
cd PTDLKD

# 2. Tạo môi trường ảo Python 3.8 hoặc 3.10
conda create -n frn_env python=3.8 -y
conda activate frn_env

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 4. Tải dữ liệu gốc từ HuggingFace sang Parquet
python Task03_Environment_Setup/scripts/download_data.py
```

---

## 🤝 6. Quy Định Đóng Góp (Git Workflow)
Xem chi tiết tài liệu hướng dẫn cộng tác tại: [docs/Contribution_Guide.md](docs/Contribution_Guide.md).
* **Quy tắc vàng:** Không push trực tiếp lên `main`. Tạo branch dạng `feature/task<số>-<tên>`, commit rõ ràng và mở Pull Request để nhóm cùng review trước khi merge.
