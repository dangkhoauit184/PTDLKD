# BÁO CÁO TASK 3: CHUẨN BỊ MÔI TRƯỜNG THỰC NGHIỆM VÀ THIẾT KẾ PIPELINE
**Môn học:** Phân tích Dữ liệu Kinh doanh (IS403)  
**Nhiệm vụ:** Thiết lập môi trường điện toán đám mây (Google Colab / Local GPU) và giải quyết tương thích thư viện  

---

## 1. Giới thiệu và Mục tiêu của Task
* **Mục tiêu:**
  1. Cấu hình môi trường thực thi hỗ trợ tăng tốc phần cứng (NVIDIA GPU CUDA) để phục vụ việc huấn luyện TimesNet và các mô hình chuỗi thời gian lớn.
  2. Giải quyết triệt để các xung đột phụ thuộc (dependency conflicts) do mã nguồn gốc của repo sử dụng các phiên bản thư viện cũ (Python 3.8, PyTorch 2.0.1, PyTorch Lightning 1.9.4).
  3. Xây dựng pipeline đọc/ghi dữ liệu hiệu năng cao giữa Google Drive và ổ đĩa cục bộ tạm thời của Colab (`/content/`).
  4. Đảm bảo tính tái lập (reproducibility) bằng cách cố định ngẫu nhiên (random seeds) và tự động hóa quy trình cài đặt.

---

## 2. Mô tả Dataset và Yêu cầu Lưu trữ / Tải dữ liệu
* Do bộ dữ liệu FreshRetailNet-50K có dung lượng tương đối lớn ($1.2\text{ GB}$ với `train.csv`, hoặc $\approx 61\text{ MB}$ với `train.parquet`), việc đọc dữ liệu từ Google Drive qua giao thức FUSE mount thông thường có thể gây nghẽn cổ chai I/O.
* **Chiến lược tối ưu hóa dữ liệu:**
  1. Sử dụng định dạng **Apache Parquet** (`train.parquet`, `eval.parquet`) thay vì CSV để giảm dung lượng đĩa từ $1.3\text{ GB}$ xuống dưới $70\text{ MB}$ (giảm hơn $90\%$).
  2. Sao chép trực tiếp file Parquet từ Google Drive vào ổ cứng SSD cục bộ của Colab (`/content/`) trước khi bắt đầu huấn luyện.
  3. Đọc cột mảng 24 giờ trực tiếp thành mảng NumPy đa chiều (`(N, 24)`), tránh việc parse chuỗi JSON lặp đi lặp lại trong vòng lặp huấn luyện.

---

## 3. Các Thư viện, Công cụ và Công nghệ Sử dụng
* **Hệ điều hành:** Linux (Ubuntu trên Google Colab) hoặc Windows 11 với môi trường Conda.
* **Tăng tốc phần cứng:** NVIDIA GPU (Tesla T4 16GB, V100 16GB hoặc L4 24GB).
* **Python Runtime:** Python 3.8 (môi trường lý tưởng cho PyPOTS ban đầu) hoặc Python 3.10/3.12 (đã cập nhật tương thích).
* **Các thư viện chính:**
  * `torch==2.0.1+cu118`
  * `pytorch-lightning==1.9.4`
  * `pytorch-forecasting==1.0.0`
  * `pypots==0.1.2` (kèm theo mã nguồn trong `frn-50k-baseline/latent_demand_recovery`)
  * `datasets==3.1.0`
  * `pyarrow>=12.0.0`, `duckdb>=0.9.0`

---

## 4. Quy trình Cài đặt Môi trường (Environment Setup Workflow)

### 4.1. Cấu hình trên Google Colab
Quy trình thiết lập tự động được cấu hình qua notebook:
1. **Kiểm tra phần cứng:**
   ```bash
   !nvidia-smi
   ```
2. **Mount Google Drive:**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
3. **Cài đặt thư viện theo thứ tự kiểm soát:**
   ```bash
   !pip install -q datasets duckdb pyarrow pygrinder tsdb einops sympy
   !pip install -q torch==2.0.1+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   !pip install -q pytorch-lightning==1.9.4 pytorch-forecasting==1.0.0
   ```
4. **Đồng bộ mã nguồn repo:**
   ```bash
   !git clone https://github.com/dangkhoauit184/PTDLKD.git
   ```

### 4.2. Cấu hình trên Máy Trạm Local (Conda)
```bash
conda create --name py38_frn python=3.8 -y
conda activate py38_frn
pip install -r requirements.txt
```

---

## 5. Phương pháp Thực hiện và Giải thích Scripts Hỗ trợ

### 5.1. Script Tự Động Tải Dữ Liệu (`download_data.py`)
Sử dụng thư viện `datasets` của Hugging Face kết hợp `duckdb` để trích xuất nhanh chóng dữ liệu gốc thành các định dạng Parquet chuẩn:
```python
from datasets import load_dataset
import duckdb

print("Đang nạp dữ liệu từ HuggingFace...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
dataset["eval"].to_parquet("eval.parquet")
dataset["train"].to_parquet("train.parquet")
print("-> Đã xuất thành công train.parquet và eval.parquet!")
```

### 5.2. Hàm Cố Định Hạt Giống Ngẫu Nhiên (Reproducibility Seed)
Trong `app.py`, hàm `set_seed` đảm bảo mọi kết quả huấn luyện mô hình sâu là hoàn toàn nhất quán giữa các lần chạy:
```python
def set_seed(seed_value=2024):
    np.random.seed(seed_value)
    random.seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)
    torch.backends.cudnn.deterministic = True
```

---

## 6. Kết quả Kiểm thử Môi trường
* Môi trường Google Colab GPU T4 / L4 khởi động thành công và nhận diện thiết bị `cuda:0`.
* Thư viện PyPOTS và mô hình `TimesNet` khởi tạo thành công với cấu hình `n_steps=480`, `n_features=6`.
* Thời gian đọc `train.parquet` vào bộ nhớ RAM đạt $\approx 3.2$ giây (so với hơn 45 giây khi đọc `train.csv`).

---

## 7. Đánh giá và Các Lưu ý Quan Trọng
1. **Quản lý phiên chạy (Session Timeout) trên Colab:**
   * Google Colab miễn phí có thể tự động ngắt kết nối sau 12 giờ hoặc khi không có tương tác.
   * **Giải pháp:** Cấu hình mã nguồn luôn lưu checkpoint sau mỗi epoch (`best_model.ckpt`) trực tiếp vào thư mục Google Drive (`/content/drive/MyDrive/...`), không lưu tại ổ đĩa tạm thời của Colab.
2. **Quản lý RAM hệ thống:**
   * Tập dữ liệu $4.500.000$ dòng khi bung đầy đủ các cột dạng đối tượng (objects) có thể chiếm hơn $10\text{ GB}$ RAM.
   * Cần loại bỏ ngay các cột không dùng sau khi xử lý và ép kiểu dữ liệu số (`int32`, `float32`).

---

## 8. Kết luận
Task 3 đã hoàn tất việc chuẩn bị hạ tầng kỹ thuật sẵn sàng cho các task tiếp theo:
* Pipeline xử lý I/O dữ liệu tối ưu với định dạng Parquet.
* Môi trường học sâu đồng bộ giữa máy tính cá nhân và Google Colab.
* Bộ script cài đặt và kiểm tra tương thích hoạt động ổn định.
