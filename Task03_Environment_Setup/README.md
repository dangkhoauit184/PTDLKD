# Task 3: Chuẩn Bị Môi Trường Thực Nghiệm & Thiết Kế Pipeline

## 📌 Tổng Quan
Task 3 xây dựng môi trường điện toán đám mây hỗ trợ GPU (Google Colab / Local CUDA) và chuẩn hóa pipeline đọc/ghi dữ liệu hiệu năng cao.

## 🎯 Mục Tiêu
1. Thiết lập runtime GPU (NVIDIA T4/L4/V100) trên Google Colab.
2. Tối ưu hóa I/O dữ liệu bằng định dạng Apache Parquet thay cho CSV.
3. Giải quyết tương thích giữa PyTorch 2.0.1, PyPOTS và PyTorch-Forecasting.
4. Đảm bảo khả năng lưu trữ checkpoint an toàn về Google Drive tránh timeout.

## 📁 Cấu Trúc Thư Mục
* `requirements.txt`: Danh sách phiên bản thư viện đã kiểm thử.
* `scripts/setup_colab.sh`: Script bash cài đặt môi trường tự động trên Colab.
* `scripts/download_data.py`: Script Python nạp dữ liệu từ Hugging Face và xuất Parquet.

## 🔗 Liên Kết Báo Cáo
Xem báo cáo đầy đủ chuẩn học thuật tại: [Task03_Report.md](../../reports/Task03_Report.md).
