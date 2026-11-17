"""
Ngay 1 - Han: ghi thong tin du lieu goc UCI.
Chay tu thu muc goc repo:  python src/mo_ta_goc_src/00_raw_info.py
Dau vao : data/raw/household_power_consumption.txt  (giai nen tu file .zip cua UCI)
Dau ra  : data/mo_ta_goc_data/raw_data_info.md, data/mo_ta_goc_data/raw_sample_10rows.csv, data/mo_ta_goc_data/raw_describe.csv
KHONG sua file trong data/raw/.
"""
import hashlib
import os
import sys
from datetime import date

import pandas as pd

RAW_DIR = "data/raw"
TXT = os.path.join(RAW_DIR, "household_power_consumption.txt")


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


if not os.path.exists(TXT):
    sys.exit(f"Khong thay {TXT}. Hay giai nen file zip UCI vao {RAW_DIR}/ truoc.")

# Doc dung nhu file goc: phan cach ';', ky tu thieu la '?'
df = pd.read_csv(TXT, sep=";", na_values=["?"], low_memory=False)

n_rows, n_cols = df.shape
size_mb = os.path.getsize(TXT) / 1024 / 1024
missing = df.isna().sum()
missing_pct = (missing / n_rows * 100).round(3)
dup_rows = int(df.duplicated().sum())

# Ghi lai cac file trong data/raw (ca file zip neu co)
lines = []
lines.append("# Thong tin du lieu goc (raw)\n")
lines.append("## 1. Nguon")
lines.append("- Ten: Individual Household Electric Power Consumption")
lines.append("- Tac gia: Hebrail, G., & Berard, A. (2012). UCI Machine Learning Repository")
lines.append("- DOI: https://doi.org/10.24432/C58K54")
lines.append("- Giay phep: CC BY 4.0")
lines.append(f"- Ngay tai: {date.today().isoformat()}\n")
lines.append("## 2. File goc (khong chinh sua)")
lines.append("| File | Dung luong (MB) | SHA-256 |")
lines.append("|---|---|---|")
for name in sorted(os.listdir(RAW_DIR)):
    p = os.path.join(RAW_DIR, name)
    if os.path.isfile(p):
        lines.append(f"| {name} | {os.path.getsize(p)/1024/1024:.2f} | {sha256(p)} |")
lines.append("")
lines.append("## 3. Kich thuoc (tu dem bang code, khong chep tu Proposal)")
lines.append(f"- So dong du lieu: {n_rows:,}")
lines.append(f"- So cot: {n_cols}")
lines.append(f"- Dung luong file .txt: {size_mb:.2f} MB")
lines.append(f"- So dong trung lap hoan toan: {dup_rows:,}\n")
lines.append("## 4. Kieu du lieu va gia tri thieu ('?' da doc thanh NaN)")
lines.append("| Cot | Kieu doc vao | So thieu | % thieu |")
lines.append("|---|---|---|---|")
for c in df.columns:
    lines.append(f"| {c} | {df[c].dtype} | {int(missing[c]):,} | {missing_pct[c]} |")
lines.append("")
lines.append("Luu y: Date (dd/mm/yyyy) va Time (hh:mm:ss) dang la chuoi, se doi sang datetime o buoc lam sach (Ngay 2).")

os.makedirs("data/mo_ta_goc_data", exist_ok=True)
with open("data/mo_ta_goc_data/raw_data_info.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

df.head(10).to_csv("data/mo_ta_goc_data/raw_sample_10rows.csv", index=False)
df.describe().T.round(3).to_csv("data/mo_ta_goc_data/raw_describe.csv")

print(f"Xong. Dong: {n_rows:,} | Cot: {n_cols} | Trung lap: {dup_rows}")
print("Da ghi: data/mo_ta_goc_data/raw_data_info.md, data/mo_ta_goc_data/raw_sample_10rows.csv, data/mo_ta_goc_data/raw_describe.csv")
