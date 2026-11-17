"""Gộp 6 notebook EDA (E0.1 -> E0.6) thành 1 notebook tổng hợp chạy từ trên xuống dưới.

Cách dùng (đứng ở thư mục gốc repo):
    python notebooks/eda/gop_eda.py
Kết quả: notebooks/eda/00_EDA_tong_hop_C2_Han.ipynb (chưa có output) -> mở và Run All.

Quy tắc: 6 notebook E0.x là nguồn gốc. Khi sửa code EDA thì sửa trong notebook E0.x
tương ứng, rồi chạy lại script này để notebook tổng hợp luôn khớp với 6 notebook con.
Script chỉ chép ô, bỏ các ô lặp lại (ô log, thông tin, cài đặt, đọc dữ liệu, chuẩn bị chung,
W&B, nhật ký riêng) và không sửa nội dung ô phân tích nào.

Tạo 14/11/2026 – Cao Ngọc Hân (theo cách đã làm ở C1).
"""
import copy
import datetime
import json
from pathlib import Path

THU_MUC = Path(__file__).resolve().parent
NGUON = [
    ("E0.1", "01_E0.1_thong_ke_mo_ta_Han.ipynb"),
    ("E0.2", "01_E0.2_xep_hang_dac_trung_Han.ipynb"),
    ("E0.3", "01_E0.3_ngoai_lai_da_cong_tuyen_Han.ipynb"),
    ("E0.4", "01_E0.4_so_dac_trung_toi_uu_Han.ipynb"),
    ("E0.5", "01_E0.5_nghe_si_va_the_loai_Han.ipynb"),
    ("E0.6", "01_E0.6_tach_lop_pca_tsne_Han.ipynb"),
]
TEN_RA = "00_EDA_tong_hop_C2_Han"

# Ô code bắt đầu bằng các dòng này là phần chuẩn bị lặp lại ở mỗi notebook con -> chỉ giữ ở notebook đầu
BO_QUA_SAU_NB_DAU = ("import os, warnings", "train = pd.read_csv(", "# Chuẩn bị chung", "# Đọc xếp hạng")
BO_QUA_MOI_NB = ("## Log lên W&B", "if USE_WANDB", "## Nhật ký")


def src(c):
    return "".join(c["source"])


def o_md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def o_code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.splitlines(keepends=True)}


def lam_sach(c):
    c = copy.deepcopy(c)
    c["metadata"] = {}
    c.pop("id", None)
    if c["cell_type"] == "code":
        c["execution_count"], c["outputs"] = None, []
    return c


nbs = [(ma, ten, json.loads((THU_MUC / ten).read_text(encoding="utf-8"))) for ma, ten in NGUON]
o_moi, da_co = [], set()

# 1. Ô ghi log (lấy của E0.1, đổi tên notebook)
o_log = lam_sach(nbs[0][2]["cells"][0])
o_log["source"] = src(o_log).replace(f'"{Path(NGUON[0][1]).stem}"', f'"{TEN_RA}"').splitlines(keepends=True)
o_moi.append(o_log)

# 2. Thông tin notebook tổng hợp
muc_luc = "\n".join(f"| {ma} | `{ten}` |" for ma, ten in NGUON)
o_moi.append(o_md(f"""# EDA tổng hợp E0.1 → E0.6 (C2 – Music Genre)

| | |
|---|---|
| **Tác giả** | Cao Ngọc Hân – Nhóm 11 |
| **Ngày tạo** | {datetime.date.today():%d/%m/%Y} – sinh tự động bằng `notebooks/eda/gop_eda.py` từ 6 notebook con |
| **Câu hỏi nghiên cứu** | RQ0: Đặc trưng âm thanh nào phân biệt các thể loại tốt nhất? (E0.5 liên quan RQ1, E0.6 liên quan RQ4) |
| **Đọc vào** | `data/raw/train.csv`, `test.csv` |
| **Ghi ra** | `figures/eda/c2_E0.1_*` … `c2_E0.6_*` (giống 6 notebook con), `c2_E0_tong_hop_tom_tat.txt` |

Đây là **bản chính thức đọc từ trên xuống dưới** của toàn bộ phần EDA. Nội dung từng phần được chép
nguyên từ notebook con, chỉ bỏ các ô chuẩn bị bị lặp lại:

| Phần | Notebook con (nguồn gốc) |
|---|---|
{muc_luc}

**Sửa code:** sửa trong notebook con, rồi chạy `python notebooks/eda/gop_eda.py` để sinh lại file này.
**Cách chạy:** Run All. File log nằm ở `logs/eda_log/`. W&B tắt (các run E0.1–E0.6 đã log ngày 08/11)."""))

# 3. Chép ô từ 6 notebook con
for so, (ma, ten, nb) in enumerate(nbs):
    o_moi.append(o_md(f"---\n# Phần {ma}\n> Nguồn: `notebooks/eda/{ten}`"))
    for i, c in enumerate(nb["cells"]):
        s = src(c).strip()
        if i <= 1:                                   # ô log + ô thông tin của notebook con
            continue
        if s.startswith(BO_QUA_MOI_NB):
            continue
        if so > 0 and c["cell_type"] == "code" and s.startswith(BO_QUA_SAU_NB_DAU):
            continue
        if c["cell_type"] == "code" and s in da_co:  # ô giống hệt ô đã có
            continue
        c = lam_sach(c)
        if s.startswith("import os, warnings"):      # ô cài đặt: không log W&B trong bản tổng hợp
            c["source"] = src(c).replace('LOG = {"E0.1": True}', "LOG = {}").splitlines(keepends=True)
        if c["cell_type"] == "code":
            da_co.add(s)
        o_moi.append(c)

# 4. Tóm tắt chung + nhật ký
o_moi.append(o_md("---\n# Tóm tắt toàn bộ EDA"))
o_moi.append(o_code('''tom_tat = "\\n".join((FIG / f"c2_{ma}_tom_tat.txt").read_text(encoding="utf-8")
                    for ma in ["E0.1", "E0.2", "E0.3", "E0.4", "E0.5", "E0.6"])
(FIG / "c2_E0_tong_hop_tom_tat.txt").write_text(tom_tat, encoding="utf-8")
log.info("Tóm tắt EDA tổng hợp:\\n" + tom_tat)'''))
o_moi.append(o_md(f"""## Nhật ký

- {datetime.date.today():%d/%m/%Y} – Gộp 6 notebook EDA con (E0.1 → E0.6) thành bản hoàn chỉnh `{TEN_RA}.ipynb` bằng script `gop_eda.py`. Commit `...`."""))

ra = {"cells": o_moi, "metadata": nbs[0][2]["metadata"], "nbformat": 4, "nbformat_minor": 4}
(THU_MUC / f"{TEN_RA}.ipynb").write_text(json.dumps(ra, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"Đã tạo {TEN_RA}.ipynb: {len(o_moi)} ô (gộp từ {len(nbs)} notebook)")
