# Task 3: Chuẩn Bị Môi Trường Thực Nghiệm & Thiết Kế Pipeline

## 📌 Tổng Quan
Task 3 xây dựng môi trường điện toán đám mây hỗ trợ GPU (Google Colab / Local CUDA) và chuẩn hóa pipeline đọc/ghi dữ liệu hiệu năng cao.

## 🎯 Mục Tiêu
1. Thiết lập runtime GPU (NVIDIA T4/L4/V100) trên Google Colab.
2. Tối ưu hóa I/O dữ liệu bằng định dạng Apache Parquet thay cho CSV.
3. Giải quyết tương thích giữa PyTorch 2.0.1, PyPOTS và PyTorch-Forecasting.
4. Đảm bảo khả năng lưu trữ checkpoint an toàn về Google Drive tránh timeout.

## 📁 Cấu Trúc Thư Mục
* [requirements.txt](../requirements.txt): Danh sách thư viện tương thích cho cả môi trường Conda (Python 3.8–3.10) và Colab/Local mới (Python 3.12–3.13).
* [scripts/setup_colab.sh](scripts/setup_colab.sh): Script bash cài đặt môi trường tự động trên Colab (tự thích ứng với Python 3.12+ hiện tại bằng cách giữ `torch`/`numpy` có sẵn và cài `--no-deps pygrinder==0.4 tsdb==0.3.1`).
* [scripts/download_data.py](scripts/download_data.py): Script Python nạp dữ liệu từ Hugging Face và xuất Parquet.

## ⚠️ Lưu Ý Thực Tế Trên Google Colab Hiện Tại (Python 3.12 / 3.13, RAM 12,7 GB)
* Trên Colab runtime mới (Python 3.12/3.13), không hạ cấp về `torch==2.0.1` hay `numpy<2.0`; giữ nguyên `torch`/`numpy`/`pandas` có sẵn, dùng thư mục `pypots` đi kèm `frn-50k-baseline/latent_demand_recovery` và cài `pip install --no-deps pygrinder==0.4 tsdb==0.3.1`.
* Với lượt huấn luyện/dự đoán TimesNet trên toàn bộ 50.000 chuỗi (150.000 mẫu), cần đọc mảng đầu vào ở `float32`, lưu checkpoint `.pypots` trực tiếp lên Drive và truyền `norm_val` dạng thu gọn `(n, 1, 6)` khi `predict` để tránh tràn 12,7 GB RAM (xem chi tiết đã kiểm chứng tại [Task09_TimesNet_MNAR/run_info.md](../Task09_TimesNet_MNAR/run_info.md)).

## 🔗 Liên Kết Báo Cáo
Xem báo cáo đầy đủ chuẩn học thuật tại: [Task03_Report.md](../reports/Task03_Report.md).
