#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate-patterns.py — Kiểm catalog YAML có khớp schema.json không.

Kiểm cả những trường mà bản trước bỏ qua: giá trị enum, quan hệ giữa mã pattern
và trường lop, và tính hợp lệ của từng regex sau khi đã giải mã escape.
Chỉ dùng thư viện chuẩn.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = catalog.ROOT
SCHEMA_FILE = catalog.PATTERNS_DIR / "schema.json"

TRUONG_BAT_BUOC = [
    "name", "lop", "category", "finding_type", "scope", "aggregation", "description",
]
TRUONG_ENUM = ["category", "finding_type", "scope", "aggregation", "false_positive_risk"]


def validate_patterns():
    if not SCHEMA_FILE.exists():
        print(f"Lỗi: không tìm thấy schema tại {SCHEMA_FILE}")
        return 1

    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    thuoc_tinh = schema["properties"]
    id_pattern = re.compile(thuoc_tinh["id"]["pattern"])
    enum_hop_le = {
        t: set(thuoc_tinh[t]["enum"]) for t in TRUONG_ENUM if "enum" in thuoc_tinh.get(t, {})
    }
    che_do_hop_le = set(thuoc_tinh["che_do"]["items"]["enum"])
    lop_hop_le = set(thuoc_tinh["lop"]["enum"])

    files = sorted(catalog.PATTERNS_DIR.glob("*.yml")) + sorted(catalog.PATTERNS_DIR.glob("*.yaml"))
    if not files:
        print("Lỗi: không có file YAML nào trong patterns/")
        return 1

    da_gap = set()
    tong = 0
    loi = []

    for f in files:
        patterns = catalog.doc_patterns(f.read_text(encoding="utf-8"))
        print(f"Đang kiểm {f.name} ({len(patterns)} pattern)...")

        for p in patterns:
            tong += 1
            pid = p.get("id", "")

            if not id_pattern.match(pid):
                loi.append(f"[{f.name}] Mã pattern sai khuôn: '{pid}'")
            if pid in da_gap:
                loi.append(f"[{f.name}] Mã pattern trùng: '{pid}'")
            da_gap.add(pid)

            for t in TRUONG_BAT_BUOC:
                if not p.get(t):
                    loi.append(f"[{f.name}:{pid}] Thiếu trường bắt buộc: '{t}'")

            # lop phải khớp tiền tố trong mã.
            m = re.match(r"^VA-L(\d)-", pid)
            if m:
                lop_theo_ma = int(m.group(1))
                if p.get("lop") not in lop_hop_le:
                    loi.append(f"[{f.name}:{pid}] Giá trị lop không hợp lệ: {p.get('lop')!r}")
                elif p.get("lop") != lop_theo_ma:
                    loi.append(
                        f"[{f.name}:{pid}] lop={p.get('lop')} nhưng mã pattern nói lớp {lop_theo_ma}"
                    )

            for t, hop_le in enum_hop_le.items():
                v = p.get(t)
                if v and v not in hop_le:
                    loi.append(
                        f"[{f.name}:{pid}] '{t}' = '{v}' không nằm trong schema: {sorted(hop_le)}"
                    )

            for cd in p.get("che_do") or []:
                if cd not in che_do_hop_le:
                    loi.append(f"[{f.name}:{pid}] che_do '{cd}' không nằm trong schema")

            mo = p.get("min_occurrences")
            if mo is not None and (not isinstance(mo, int) or mo < 1):
                loi.append(f"[{f.name}:{pid}] min_occurrences phải là số nguyên từ 1: {mo!r}")

            if not p.get("bad_examples"):
                loi.append(f"[{f.name}:{pid}] Thiếu bad_examples")
            if not p.get("good_examples"):
                loi.append(f"[{f.name}:{pid}] Thiếu good_examples")

            for r in p.get("regex") or []:
                try:
                    re.compile(r)
                except re.error as e:
                    loi.append(f"[{f.name}:{pid}] Regex hỏng '{r}': {e}")

            for c in p.get("phrases") or []:
                if not c.strip():
                    loi.append(f"[{f.name}:{pid}] Có cụm signal rỗng")

    print("=" * 68)
    if loi:
        print(f"Catalog KHÔNG đạt, {len(loi)} lỗi:")
        for e in loi:
            print(f"  ✗ {e}")
        return 1

    print(f"Đạt: {tong} pattern trong {len(files)} file đều hợp lệ.")
    return 0


if __name__ == "__main__":
    sys.exit(validate_patterns())
