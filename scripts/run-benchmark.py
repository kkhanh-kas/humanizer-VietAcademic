#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-benchmark.py — Chạy bộ case chuẩn của Humanizer-VietAcademic.

Hai chế độ:

  python scripts/run-benchmark.py
      Kiểm tra chính bộ case: mã pattern có thật, câu đầu vào thật sự dính lỗi
      mà case khai báo, đáp án mẫu sạch lỗi cơ học và giữ đủ trích dẫn.

  python scripts/run-benchmark.py --actual ket_qua.json
      Chấm bản viết lại thật của model. File JSON có dạng {"BENCH-VA-001": "..."}.

Không dùng thư viện ngoài.
"""

import argparse
import json
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
CASES_FILE = ROOT / "benchmarks" / "cases" / "academic-cases.json"
PATTERNS_DIR = ROOT / "patterns"

sys.path.insert(0, str(ROOT / "scripts"))
import catalog as pattern_catalog
import kiem_tra

CHE_DO_HOP_LE = {"hoc-thuat", "ky-thuat", "cong-viec", "doi-thuong"}
MODE_HOP_LE = {"clean_rewrite", "review_comment", "needs_author_decision", "no_change"}
TRUONG_BAT_BUOC = [
    "id", "che_do", "domain", "input", "citations", "constraints",
    "expected_patterns", "expected_output_mode", "expected_output",
    "must_preserve", "must_not_add", "blockers",
]


def nap_catalog():
    """Trả về {ma_pattern: [regex, ...]} lấy từ scripts/catalog.py."""
    return {
        ma: p.get("regex") or []
        for ma, p in pattern_catalog.nap_catalog(PATTERNS_DIR).items()
    }


def loi_nang(text, che_do):
    loi, _ = kiem_tra.quet(text, che_do=che_do)
    return sorted({l.ma for l in loi if l.muc == "nang"})


def kiem_bo_case(cases, catalog):
    """Kiểm tính đúng đắn của chính bộ case."""
    ket_qua = []
    for case in cases:
        cid = case.get("id", "(thiếu id)")
        loi_case = []

        for truong in TRUONG_BAT_BUOC:
            if truong not in case:
                loi_case.append(f"Thiếu trường bắt buộc: '{truong}'")
        if loi_case:
            ket_qua.append((cid, case.get("domain", ""), loi_case))
            continue

        che_do = case["che_do"]
        dau_vao, dap_an = case["input"], case["expected_output"]
        mode = case["expected_output_mode"]

        if che_do not in CHE_DO_HOP_LE:
            loi_case.append(f"Chế độ không hợp lệ: '{che_do}'")
        if mode not in MODE_HOP_LE:
            loi_case.append(f"Output mode không hợp lệ: '{mode}'")

        # Mã pattern phải có thật trong catalog.
        for pid in case["expected_patterns"]:
            if pid not in catalog:
                loi_case.append(f"Mã pattern không có trong catalog: '{pid}'")

        # Nếu pattern có regex, câu đầu vào phải thật sự dính.
        import re as _re
        for pid in case["expected_patterns"]:
            regexes = catalog.get(pid) or []
            if regexes and not any(_re.search(r, dau_vao, _re.I) for r in regexes):
                loi_case.append(f"Câu đầu vào không dính signal của '{pid}'")

        # Trích dẫn và thực thể bắt buộc phải còn nguyên trong đáp án.
        for c in case["citations"]:
            if c not in dap_an:
                loi_case.append(f"Đáp án mẫu mất thẻ trích dẫn: '{c}'")
        for p in case["must_preserve"]:
            if p not in dap_an:
                loi_case.append(f"Đáp án mẫu mất thực thể bắt buộc: '{p}'")

        # Đáp án mẫu phải sạch lỗi cơ học.
        nang = loi_nang(dap_an, che_do)
        if nang:
            loi_case.append(f"Đáp án mẫu còn lỗi nặng: {nang}")

        # no_change nghĩa là giữ nguyên văn bản.
        if mode == "no_change" and dap_an.strip() != dau_vao.strip():
            loi_case.append("Mode 'no_change' nhưng đáp án khác đầu vào")
        if mode != "no_change" and dap_an.strip() == dau_vao.strip():
            loi_case.append(f"Mode '{mode}' nhưng đáp án trùng hệt đầu vào")

        # blockers và must_not_add là checklist cho người đọc, phải có nội dung.
        for truong in ("blockers", "must_not_add", "constraints"):
            if not case[truong]:
                loi_case.append(f"Trường '{truong}' rỗng, case không nêu điều kiện chặn")

        ket_qua.append((cid, case["domain"], loi_case))
    return ket_qua


def cham_ket_qua_that(cases, actual):
    """Chấm bản viết lại thật của model."""
    ket_qua = []
    for case in cases:
        cid = case["id"]
        loi_case = []
        if cid not in actual:
            ket_qua.append((cid, case["domain"], [f"Thiếu kết quả cho case '{cid}'"]))
            continue

        ra = actual[cid]
        for c in case["citations"]:
            if c not in ra:
                loi_case.append(f"CHẶN: mất thẻ trích dẫn '{c}'")
        for p in case["must_preserve"]:
            if p not in ra:
                loi_case.append(f"CHẶN: mất thực thể bắt buộc '{p}'")
        nang = loi_nang(ra, case["che_do"])
        if nang:
            loi_case.append(f"Còn lỗi cơ học nặng: {nang}")
        if case["expected_output_mode"] == "no_change" and ra.strip() != case["input"].strip():
            loi_case.append("Đáng lẽ giữ nguyên nhưng đã sửa (gọt giũa quá mức)")
        ket_qua.append((cid, case["domain"], loi_case))
    return ket_qua


def in_ket_qua(ket_qua, tieu_de):
    print(tieu_de)
    print("=" * 68)
    dat = 0
    for idx, (cid, domain, loi_case) in enumerate(ket_qua, 1):
        if loi_case:
            print(f"[{idx}/{len(ket_qua)}] FAIL - {cid}: {domain}")
            for e in loi_case:
                print(f"    ✗ {e}")
        else:
            print(f"[{idx}/{len(ket_qua)}] PASS - {cid}: {domain}")
            dat += 1
    print("=" * 68)
    print(f"Kết quả: {dat} đạt, {len(ket_qua) - dat} hỏng trên tổng {len(ket_qua)} case.")
    return 0 if dat == len(ket_qua) else 1


def main():
    p = argparse.ArgumentParser(description="Chạy bộ case chuẩn của Humanizer-VietAcademic.")
    p.add_argument("--actual", help="File JSON chứa bản viết lại thật của model: {case_id: text}")
    a = p.parse_args()

    if not CASES_FILE.exists():
        print(f"Lỗi: không tìm thấy {CASES_FILE}")
        return 1
    cases = json.loads(CASES_FILE.read_text(encoding="utf-8"))

    if a.actual:
        actual = json.loads(Path(a.actual).read_text(encoding="utf-8"))
        ma = cham_ket_qua_that(cases, actual)
        code = in_ket_qua(ma, f"Chấm {len(cases)} case trên kết quả thật từ {a.actual}")
        print("\nCác điều kiện chặn dưới đây cần người đọc tự xác nhận:")
        for case in cases:
            print(f"  {case['id']}: " + "; ".join(case["blockers"]))
        return code

    catalog = nap_catalog()
    kq = kiem_bo_case(cases, catalog)
    return in_ket_qua(kq, f"Kiểm {len(cases)} case trong {CASES_FILE.name} ({len(catalog)} pattern trong catalog)")


if __name__ == "__main__":
    sys.exit(main())
