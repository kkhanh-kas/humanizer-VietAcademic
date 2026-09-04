# False Positives & Legitimate Academic Conventions

This reference defines valid Vietnamese academic conventions that must **NEVER** be flagged or modified as errors by Humanizer-VietAcademic.

## What NOT to Flag

### 1. Long, Compound Sentences
- **Standard:** Sentences running 25 to 45 syllables connected logically by commas and subordinating connectives (*nhờ đó, qua đó, trong khi, đồng thời*) are the norm in Vietnamese scientific writing.
- **Rule:** Do NOT shorten a sentence simply because it is long, provided it preserves its logical thread.

### 2. High Density of Sino-Vietnamese Terminology
- **Standard:** Technical concepts and abstract nouns in formal Vietnamese legitimately rely on Sino-Vietnamese roots.
- **Example:** Always prefer *“khả năng xác minh”* over conversational *“khả năng kiểm tra lại được”*.

### 3. Subject Ellipsis
- **Standard:** Omission of grammatical subject across sequential sentences where context is established.
- **Example:** *“Qua đó, giảm sự phụ thuộc vào bên trung gian.”* is fully grammatical and natural.

### 4. Isolated Use of "Được"
- **Standard:** The passive particle *“được”* on its own is standard and frequent in academic writing.
- **Rule:** ONLY flag the agentive calque pair *“được ... bởi”* (`be ... by`).

### 5. Mandatory Thesis Sections & Content Fluff
- **Standard:** Sections like *“CHƯƠNG X:”*, *“TÀI LIỆU THAM KHẢO”*, *“KẾT LUẬN”*, and *“HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN”* are mandatory in Vietnamese theses.
- **Rule:** Never delete mandatory section headings; remove only the empty filler inside them.

### 6. Citation Tags and Mathematical Notation
- **Standard:** In-text references such as `[1, 2]`, `[3-7]`, or `(Nguyen et al., 2024)`, and LaTeX/mathematical formulas.
- **Rule:** Strictly preserve every bracket, number, author, and citation position.

### 7. Curved Quotation Marks and Decimal Comma
- **Standard:** Curved quotes `“ ”` and decimal comma (`94,7%`).
- **Rule:** These represent national Vietnamese typographic standards and must not be altered to western conventions.

### 8. Parenthetical Term Glosses and Figure Callouts
- **Standard:** Parentheses holding a foreign-language term (`(self-attention)`), a full-form-plus-abbreviation pair (`(multi-agent system, MAS)`), a figure, table, appendix or equation callout (`(Hình 2.1)`, `(Bảng 3.4)`, `(Phụ lục A)`), a Vietnamese noun phrase with no verb (`(mô hình sinh văn bản)`), a citation (`(Nguyễn và cộng sự, 2024)`), or a statistic (`(n = 30)`, `(p < 0,05)`).
- **Rule:** Flag a parenthesis ONLY when its content is a Vietnamese clause carrying a verb (VA-L2-36), or a bare section pointer such as `(mục 3.2)` (VA-L1-20). Never strip a term gloss. When a clause must come out of the brackets, shrink the parenthesis back to the foreign term instead of deleting it.
