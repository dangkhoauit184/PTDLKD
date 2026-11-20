#!/bin/bash
set -e
echo "=== BẮT ĐẦU THIẾT LẬP MÔI TRƯỜNG COLAB CHO FRN-50K ==="

# 1. Kiểm tra GPU & Phiên bản Python
nvidia-smi
PY_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
echo "Detected Python 3.${PY_MINOR}"

# 2. Cài đặt các thư viện xử lý dữ liệu và nền tảng
pip install -q datasets duckdb pyarrow einops sympy h5py psutil scikit-learn

# 3. Cài đặt phụ thuộc Deep Learning tương thích theo phiên bản Python của Colab
if [ "$PY_MINOR" -le 11 ]; then
    pip install -q pygrinder tsdb
    pip install -q torch==2.0.1+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip install -q pytorch-lightning==1.9.4 pytorch-forecasting==1.0.0
else
    echo "Colab Python 3.${PY_MINOR}: giữ nguyên PyTorch/NumPy có sẵn, cài pygrinder & tsdb với --no-deps cho pypots đi kèm repo."
    pip install -q --no-deps pygrinder==0.4 tsdb==0.3.1
fi

echo "=== THIẾT LẬP HOÀN TẤT THÀNH CÔNG! ==="
