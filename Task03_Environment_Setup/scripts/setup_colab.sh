#!/bin/bash
echo "=== BẮT ĐẦU THIẾT LẬP MÔI TRƯỜNG COLAB CHO FRN-50K ==="

# 1. Kiểm tra GPU
nvidia-smi

# 2. Cài đặt các thư viện xử lý dữ liệu và nền tảng
pip install -q datasets duckdb pyarrow pygrinder tsdb einops sympy

# 3. Cài đặt PyTorch tương thích CUDA 11.8
pip install -q torch==2.0.1+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 4. Cài đặt PyTorch Lightning và PyTorch Forecasting
pip install -q pytorch-lightning==1.9.4 pytorch-forecasting==1.0.0

echo "=== THIẾT LẬP HOÀN TẤT THÀNH CÔNG! ==="
