from datasets import load_dataset
import duckdb

print("1. Đang lấy lại dữ liệu gốc từ bộ nhớ đệm...")
dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")

# Tạo lại 2 file parquet
dataset["eval"].to_parquet("eval.parquet")
dataset["train"].to_parquet("train.parquet")
print("-> Đã tạo lại xong eval.parquet và train.parquet!")

print("2. Đang xuất sang eval.csv...")
duckdb.sql("COPY (SELECT * FROM 'eval.parquet') TO 'eval.csv' (HEADER, DELIMITER ',')")
print("-> Đã xong eval.csv!")

print("3. Đang xuất sang train.csv (chờ khoảng 15 - 30 giây)...")
duckdb.sql("COPY (SELECT * FROM 'train.parquet') TO 'train.csv' (HEADER, DELIMITER ',')")
print("-> HOÀN TẤT TOÀN BỘ!")