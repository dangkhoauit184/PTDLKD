"""
Script tải dữ liệu FreshRetailNet-50K từ HuggingFace và xuất ra định dạng Parquet.
"""
from datasets import load_dataset
import os

def download_and_export():
    print("1. Đang kết nối HuggingFace Datasets: Dingdong-Inc/FreshRetailNet-50K...")
    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")
    
    print("2. Đang xuất tập eval sang eval.parquet...")
    dataset["eval"].to_parquet("eval.parquet")
    print("-> Xong eval.parquet!")
    
    print("3. Đang xuất tập train sang train.parquet...")
    dataset["train"].to_parquet("train.parquet")
    print("-> Xong train.parquet!")
    
    print("=== HOÀN TẤT XUẤT DỮ LIỆU SẠCH! ===")

if __name__ == '__main__':
    download_and_export()
