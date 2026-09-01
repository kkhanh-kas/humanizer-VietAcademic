# Register & Tone Guidelines

Humanizer-VietAcademic supports four registers. The `che_do` field on every pattern in `patterns/*.yml` names the registers that rule applies to, and `scripts/kiem_tra.py --che-do` reads that same field. A rule that does not list a register is skipped in that register.

| Register | Use for | Second-person `bạn` | Spoken particles | Decimal comma & curved quotes |
|---|---|---|---|---|
| `hoc-thuat` (default) | Theses, journal papers, proposals | Never | Never | Required |
| `ky-thuat` | Software docs, READMEs, API specs, RFCs | Allowed in instructions | Never | Required |
| `cong-viec` | Work email, business proposals, status reports | Never, use hierarchical pronouns | Never | Required |
| `doi-thuong` | Informal prose, checked for translationese only | Allowed | Allowed | Not enforced |

## 1. Academic Register (`hoc-thuat`, mặc định)
- **Use for:** Dissertations, theses, capstone projects, journal papers, technical proposals.
- **Pronouns:** Strict third-person or collective first-person (*chúng tôi, tác giả, nhóm nghiên cứu*). Never use *bạn*. Omit the subject when natural.
- **Passive Voice:** Limit passive structures; eliminate `được ... bởi`.
- **Formatting:** Continuous paragraphs, curved quotes `“ ”`, decimal comma `94,7%`.

## 2. Technical Register (`ky-thuat`)
- **Use for:** Software documentation, READMEs, API specifications, engineering architecture RFCs.
- **Pronouns:** Neutral and concise. Second-person *bạn* is permitted only when giving direct procedural instructions to developers.
- **Passive Voice:** Permissible when the action or system process is the focus rather than the operator (e.g., *“Cấu hình được lưu tự động”*).
- **Invariants:** Preserve code blocks, inline code, identifier names, endpoint paths, and YAML/JSON syntax completely unmodified.

## 3. Workplace & Professional Register (`cong-viec`)
- **Use for:** Formal work emails, business proposals, project status reports.
- **Pronouns:** Formal hierarchical pronouns (*anh, chị, em, quý đối tác, ban giám đốc*). Never flatten formal Vietnamese workplace pronouns to generic *bạn*.
- **Tone:** Courteous, direct, free of bureaucratic filler phrases.

## 4. Everyday Register (`doi-thuong`)
- **Use for:** Informal prose that only needs its translationese removed. Rewriting informal Vietnamese as a craft belongs to a separate skill; this register exists so the linter can check such text without imposing academic rules on it.
- **Rules that still apply:** the register-neutral calques, namely `được ... bởi` (`VA-L1-02`), redundant `một cách` (`VA-L1-03`), Chinese helper verbs (`VA-L1-15`), and dashes cutting into a sentence (`VA-L2-14`).
- **Rules that do not apply:** academic pronouns, spoken particles, semicolon and decimal-comma conventions, cadence and connective density, and every Layer 2 rhetoric rule.
