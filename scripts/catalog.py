#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
catalog.py — Đọc catalog pattern trong patterns/*.yml.

Đây là nơi duy nhất đọc file YAML. Cả kiem_tra.py, validate-patterns.py và
run-benchmark.py đều lấy luật từ đây, nên mỗi luật chỉ được định nghĩa một lần.

Chỉ dùng thư viện chuẩn. Catalog viết theo một khuôn cố định:

    - id: VA-L1-02
      name: ...
      che_do: [hoc-thuat, ky-thuat]
      signals:
        regex:
          - "..."
        phrases:
          - "..."
      bad_examples:
        - "..."
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERNS_DIR = ROOT / "patterns"

TRUONG_DON = [
    "name", "lop", "category", "finding_type", "scope", "aggregation",
    "min_occurrences", "false_positive_risk", "description", "explanation",
]
TRUONG_DANH_SACH = ["che_do", "exceptions", "bad_examples", "good_examples"]
TRUONG_SIGNAL = ["regex", "phrases", "exclude_phrases"]


def giai_ma_scalar(raw):
    """Trả về giá trị thật của một scalar YAML nằm gọn trên một dòng.

    YAML nháy kép hiểu hai dấu backslash là một, còn nháy đơn giữ nguyên chữ.
    Bỏ bước này thì mọi regex trong catalog bị lệch một lớp escape và không
    bao giờ khớp với văn bản thật.
    """
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        return raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(raw) >= 2 and raw[0] == "'" and raw[-1] == "'":
        return raw[1:-1].replace("''", "'")
    return raw


def _danh_sach_dong(raw):
    """Đọc danh sách viết gọn trên một dòng: [a, b, c]."""
    raw = raw.strip()
    if not (raw.startswith("[") and raw.endswith("]")):
        return None
    ben_trong = raw[1:-1].strip()
    if not ben_trong:
        return []
    return [giai_ma_scalar(x) for x in ben_trong.split(",") if x.strip()]


def doc_patterns(text):
    """Tách một file YAML thành danh sách pattern."""
    patterns = []
    hien_tai = None
    khoa_2, khoa_4 = None, None

    for dong in text.split("\n"):
        if not dong.strip() or dong.lstrip().startswith("#"):
            continue

        m = re.match(r"^- id:\s*(.*)$", dong)
        if m:
            hien_tai = {"id": giai_ma_scalar(m.group(1)), "signals": {}}
            for t in TRUONG_DANH_SACH + TRUONG_SIGNAL:
                hien_tai.setdefault(t, [])
            patterns.append(hien_tai)
            khoa_2, khoa_4 = None, None
            continue

        if hien_tai is None:
            continue

        m = re.match(r"^  (\w+):\s*(.*)$", dong)
        if m:
            khoa, gia_tri = m.group(1), m.group(2)
            khoa_2, khoa_4 = khoa, None
            if khoa in TRUONG_DON and gia_tri.strip():
                v = giai_ma_scalar(gia_tri)
                if khoa in ("lop", "min_occurrences") and v.isdigit():
                    v = int(v)
                hien_tai[khoa] = v
            elif khoa in TRUONG_DANH_SACH:
                inline = _danh_sach_dong(gia_tri)
                if inline is not None:
                    hien_tai[khoa] = inline
            continue

        m = re.match(r"^    (\w+):\s*(.*)$", dong)
        if m and khoa_2 == "signals":
            khoa_4 = m.group(1)
            continue

        m = re.match(r"^(\s+)- (.*)$", dong)
        if m:
            gia_tri = giai_ma_scalar(m.group(2))
            if khoa_2 == "signals" and khoa_4 in TRUONG_SIGNAL:
                hien_tai["signals"].setdefault(khoa_4, []).append(gia_tri)
                hien_tai[khoa_4] = hien_tai["signals"][khoa_4]
            elif khoa_2 in TRUONG_DANH_SACH:
                hien_tai[khoa_2].append(gia_tri)

    return patterns


def nap_catalog(thu_muc=None):
    """Đọc toàn bộ patterns/*.yml thành {ma_pattern: pattern}."""
    thu_muc = Path(thu_muc) if thu_muc else PATTERNS_DIR
    files = sorted(thu_muc.glob("*.yml")) + sorted(thu_muc.glob("*.yaml"))
    if not files:
        raise SystemExit(f"Không tìm thấy file pattern nào trong {thu_muc}")
    catalog = {}
    for f in files:
        for p in doc_patterns(f.read_text(encoding="utf-8")):
            p["nguon"] = f.name
            catalog[p["id"]] = p
    return catalog


# ------------------------------------------------------------ tiện ích cho linter

def bien_dich(catalog, ma, co=re.I):
    """Biên dịch signal regex của một pattern thành một regex duy nhất."""
    p = catalog.get(ma)
    if not p or not p.get("regex"):
        raise SystemExit(f"Pattern '{ma}' không có signals.regex trong catalog")
    return re.compile("|".join(f"(?:{r})" for r in p["regex"]), co)


def bien_dich_cum_tu(catalog, ma, co=re.I):
    """Biên dịch signals.phrases thành regex bắt nguyên cụm, khoảng trắng co giãn."""
    p = catalog.get(ma)
    if not p or not p.get("phrases"):
        raise SystemExit(f"Pattern '{ma}' không có signals.phrases trong catalog")
    cum = sorted(p["phrases"], key=len, reverse=True)
    than = "|".join(re.escape(c).replace(r"\ ", r"\s+") for c in cum)
    return re.compile(r"(?<!\w)(" + than + r")(?!\w)", co)


def ap_dung_cho(catalog, ma, che_do):
    """Pattern này có áp dụng cho chế độ đang chạy không?"""
    p = catalog.get(ma)
    if not p:
        return True
    ds = p.get("che_do") or []
    return che_do in ds if ds else True
