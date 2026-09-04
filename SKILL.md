---
name: humanizer-viet-academic
description: |
  Rewrite and edit formal Vietnamese prose (academic reports, theses, proposals,
  technical documentation) to eliminate AI writing patterns, translationese, and
  fluff while strictly preserving claims and citations.
  Use when asked to "sửa văn phong học thuật", "viết lại cho mượt", "bỏ bớt văn dịch",
  "humanize text", or reviewing formal Vietnamese academic papers.
license: MIT
metadata:
  version: "2.13.0"
---

# Humanizer-VietAcademic: Remove AI patterns in Vietnamese academic prose

Rewrite AI-sounding or machine-translated Vietnamese text so it reads as natural, formal Vietnamese academic prose written by a scholar. Strictly preserve every claim, data point, and citation without inventing facts.

## Governing principle

> **When in doubt, join clauses rather than split them.**

English splits clauses with punctuation; Vietnamese connects with words. Natural Vietnamese academic sentences string 3–4 clauses together using commas and connectives. Splitting them into short, clipped sentences is the single most common AI translation fault.

## What to do

1. **Find AI and translation patterns.** Check the text against the 37 numbered patterns below.
2. **Preserve every claim and citation.** Retain all facts, names, dates, numbers, equations, and literature citations (`[1]`, `(Nguyen et al., 2024)`). Never invent facts or citations.
3. **Ensure Vietnamese academic cadence.** Maintain connective density (4–5 per 100 syllables) and alternate long (median 21 syllables) and short sentences.
4. **Enforce hard punctuation rules.** Ban unspaced dashes (`—`, `–`) and semicolons (`;`) inside sentences. Require curved quotation marks (`“ ”`) and decimal commas (`94,7%`).

## Hard rules for academic Vietnamese

- **Connectives:** Use subordinating conjunctions freely inside sentences (*và, là, khi, mà, nếu, trong khi, nhằm, thông qua, nhờ đó, qua đó, do đó, đồng thời, tuy nhiên, mặc dù, bên cạnh đó, ngoài ra*). Avoid spoken particles (*vậy nên, thế nên, thì, rồi, á, nhé*).
- **Passive voice & Pronouns:** Eliminate `được ... bởi` (calque of `be ... by`). Never address the reader as *bạn*. Use *chúng tôi, tác giả, nhóm nghiên cứu* or omit the subject. Replace pronoun *nó* with the specific noun.
- **Mandatory sections:** Keep required report sections (*Kết luận*, *Hạn chế và hướng phát triển*), but eliminate empty filler inside them.

## Bundled resources

Read a file below only when the case calls for it. Do not load them all up front.

- `references/false-positives.md`: valid Vietnamese academic conventions that must never be flagged. Read this before you change any sentence.
- `references/registers.md`: rules for the technical (`ky-thuat`) and workplace (`cong-viec`) registers. Read this when the text is not an academic paper.
- `references/chinese-source.md`: extra faults that appear when the source literature is Chinese. Read this when the draft is translated or adapted from Chinese.
- `references/layer1-grammar-syntax.md`: the full grammar, punctuation, and cadence rules behind the hard rules above.
- `patterns/layer1-grammar-syntax.yml` and `patterns/layer2-rhetoric-style.yml`: the machine-readable catalog. Each rule has a stable ID, a severity, and a signal regex. Cite the ID when you report a finding.

When you can run shell commands, run `python scripts/kiem_tra.py <file>` first to catch mechanical faults, then edit by hand for cadence. The script reports only what a regex can prove, so it never judges rhythm and it never rewrites text for you.

---

## Content patterns

### 1. Inflated claims about importance and legacy

**Words to watch:** đóng vai trò quan trọng/then chốt, đánh dấu bước ngoặt, là minh chứng rõ nét/hùng hồn, khẳng định vị thế, mở ra một chương mới, tạo tiền đề vững chắc, góp phần không nhỏ vào, biểu tượng cho
**Problem:** AI inflates ordinary technical details into historic milestones.
**Before:**
> Mô hình mạng nơ-ron này được đề xuất vào năm 2021, đánh dấu một bước ngoặt mang tính cách mạng trong quá trình nhận diện hình ảnh, tạo tiền đề vững chắc cho các nghiên cứu tiếp theo.
**After:**
> Mô hình mạng nơ-ron này được đề xuất vào năm 2021 nhằm phục vụ bài toán nhận diện hình ảnh.

### 2. Name-dropping to prove importance

**Words to watch:** các chuyên gia đầu ngành, các tạp chí hàng đầu, phương tiện truyền thông uy tín, được trích dẫn rộng rãi
**Problem:** AI lists vague authorities instead of concrete citations.
**Before:**
> Thuật toán này đã được nhắc đến bởi nhiều chuyên gia đầu ngành và các trang công nghệ uy tín.
**After:**
> Thuật toán này được phân tích chi tiết trong nghiên cứu của LeCun et al. [1].

### 3. Shallow analysis with hollow clauses

**Words to watch:** qua đó thể hiện, từ đó khẳng định, góp phần nâng cao, cho thấy sự quan tâm sâu sắc tới, nhằm làm sáng tỏ
**Problem:** AI adds empty trailing clauses to simulate analytical depth.
**Before:**
> Hệ thống sử dụng cơ chế xác thực hai lớp, qua đó thể hiện sự quan tâm sâu sắc tới bảo mật và góp phần nâng cao trải nghiệm người dùng.
**After:**
> Hệ thống sử dụng cơ chế xác thực hai lớp để tăng cường bảo mật tài khoản.

### 4. Sales language and puffery

**Words to watch:** đột phá, hoàn hảo, mạnh mẽ, toàn diện, tối ưu vượt trội, sâu sắc, phong phú, tuyệt đẹp
**Problem:** AI uses promotional and emotional adjectives in objective research text.
**Before:**
> Giải pháp cung cấp một kiến trúc vi dịch vụ vô cùng mạnh mẽ và hoàn hảo, mang lại trải nghiệm tối ưu vượt trội.
**After:**
> Giải pháp sử dụng kiến trúc vi dịch vụ để giảm độ trễ xử lý dữ liệu.

### 5. Vague sources and unattributed claims

**Words to watch:** theo các chuyên gia, nhiều nghiên cứu chỉ ra rằng, giới quan sát nhận định, theo một số nguồn tin
**Problem:** AI attributes claims to unnamed experts.
**Before:**
> Theo các chuyên gia, việc chuyển dịch sang điện toán đám mây là xu hướng tất yếu của mọi doanh nghiệp.
**After:**
> Khảo sát của Gartner [2] cho thấy 85% doanh nghiệp đang chuyển dịch hạ tầng lên điện toán đám mây.

### 6. Formulaic mandatory sections

**Words to watch:** Bên cạnh những kết quả đạt được, vẫn còn tồn tại một số hạn chế nhất định, trong thời gian tới sẽ tiếp tục hoàn thiện
**Problem:** Do not delete mandatory academic sections like "Hạn chế và hướng phát triển" (Limitations). Remove the empty cliché and state exact technical constraints.
**Before:**
> Mặc dù đạt kết quả khả quan, đề tài vẫn còn một số hạn chế nhất định. Nhóm nghiên cứu sẽ tiếp tục hoàn thiện trong tương lai.
**After:**
> Mô hình hiện chỉ thử nghiệm trên tập dữ liệu 2.000 mẫu và chưa đánh giá được hiệu năng trong điều kiện thiếu sáng.

---

## Language and grammar patterns

### 7. Overused AI words and stock clichés

**Words to watch:** bức tranh toàn cảnh, đi sâu vào, kiến tạo, nâng tầm, chuyển mình, bứt phá, chìa khóa, nền tảng vững chắc, đòn bẩy, cột mốc, lăng kính, giao thoa
**Problem:** AI writing clusters specific abstract buzzwords.
**Before:**
> Bài viết đi sâu vào bức tranh toàn cảnh của thị trường bán dẫn, qua đó kiến tạo nền tảng vững chắc cho việc hoạch định chính sách.
**After:**
> Bài viết phân tích cấu trúc thị trường bán dẫn và tổng hợp các chính sách hỗ trợ hiện hành.

### 8. Avoiding is and are

**Words to watch:** đóng vai trò là, được xem là, sở hữu, mang trong mình, được biết đến với tư cách
**Problem:** Replacing simple verbs (*là*, *có*) with pompous verb phrases.
**Before:**
> PostgreSQL đóng vai trò là hệ quản trị cơ sở dữ liệu quan hệ mã nguồn mở phổ biến.
**After:**
> PostgreSQL là hệ quản trị cơ sở dữ liệu quan hệ mã nguồn mở.

### 9. Repetitive symmetric structures

**Words to watch:** không chỉ ... mà còn, không phải là ... mà là
**Problem:** Overusing symmetric parallel templates across multiple sentences.
**Before:**
> Thuật toán không chỉ giúp tối ưu bộ nhớ mà còn tăng tốc độ thực thi, không chỉ xử lý số liệu mà còn phân tích ngữ nghĩa.
**After:**
> Thuật toán tối ưu bộ nhớ, tăng tốc độ thực thi và hỗ trợ phân tích ngữ nghĩa.

### 10. Forced parallel groups

**Problem:** Forcing technical points into artificial groups of three or four symmetrical adjectives/nouns.
**Before:**
> Giao diện cần đảm bảo tính trực quan, tính thẩm mỹ, tính tương tác và tính bảo mật.
**After:**
> Giao diện cần trực quan và đảm bảo an toàn thông tin khi thao tác.

### 11. Synonym cycling and inconsistent naming

**Words to watch:** tác giả / người viết / nhà nghiên cứu (alternating within the same paragraph)
**Problem:** Cycling synonyms mechanically. Use one consistent professional designation.
**Before:**
> Nhóm tác giả khảo sát 500 người dùng. Người viết nhận thấy độ trễ cao. Nhà nghiên cứu đề xuất cải tiến thuật toán.
**After:**
> Nhóm nghiên cứu khảo sát 500 người dùng, ghi nhận độ trễ hệ thống còn cao và đề xuất hướng tối ưu thuật toán.

### 12. False from X to Y ranges

**Words to watch:** từ ... đến ... (used for arbitrary, non-sequential items)
**Problem:** AI creates false spectrums between unrelated concepts.
**Before:**
> Luận văn khảo sát từ cấu trúc vi mạch bán dẫn đến chính sách kinh tế vĩ mô của chính phủ.
**After:**
> Luận văn phân tích cấu trúc chuỗi cung ứng vi mạch và các chính sách kinh tế liên quan.

### 13. Passive voice calques and pronouns

**Words to watch:** được ... bởi, bạn, nó, chúng
**Problem:** Direct calque of English passive voice (`be ... by`) and inappropriate pronouns.
**Before:**
> Dữ liệu được thu thập bởi hệ thống. Bạn có thể thấy nó hoạt động rất nhanh.
**After:**
> Hệ thống tự động thu thập dữ liệu với tốc độ xử lý dưới 50ms.

---

## Style patterns

### 14. Em and en dashes inside sentences

**Rule:** Never use `—`, `–`, or spaced ` - ` to break clauses in Vietnamese academic prose. Replace with a comma plus a connective, or split into two sentences. Retain dashes only in unspaced proper nouns, numeric ranges (`1–12 tháng`), and abbreviation glosses.
**Before:**
> Hệ thống xác thực — vốn phát triển theo chuẩn OAuth 2.0 — cho phép phân quyền chi tiết.
**After:**
> Hệ thống xác thực được phát triển theo chuẩn OAuth 2.0, nhờ đó cho phép phân quyền chi tiết.

### 15. Too much bold text

**Problem:** Gratuitous bolding across sentences.
**Before:**
> Mô hình **Transformer** sử dụng cơ chế **Self-Attention** để xử lý **chuỗi văn bản**.
**After:**
> Mô hình Transformer sử dụng cơ chế Self-Attention để xử lý chuỗi văn bản.

### 16. Lists with bold mini-headings

**Problem:** Overusing bullet points where continuous explanatory paragraphs are expected.
**Before:**
> - **Hiệu năng:** Tốc độ xử lý tăng 20%.
> - **Chi phí:** Tiết kiệm 15% tài nguyên phần cứng.
**After:**
> Việc tối ưu thuật toán giúp tăng tốc độ xử lý thêm 20%, đồng thời tiết kiệm 15% tài nguyên phần cứng.

### 17. Title case in headings

**Problem:** Capitalizing every word in headings (English style). Vietnamese headings capitalize only the first word and proper nouns, or use ALL CAPS for chapter titles (`CHƯƠNG 2: CƠ SỞ LÝ THUYẾT`).
**Before:**
> ## Phân Tích Hiệu Năng Của Thuật Toán Sắp Xếp
**After:**
> ## Phân tích hiệu năng của thuật toán sắp xếp

### 18. Emojis and decorative icons

**Problem:** AI inserts emojis (🚀, 💡, ✅) into formal reports. Remove them.
**Before:**
> 💡 **Kết quả chính:** Mô hình đạt độ chính xác 95%.
**After:**
> Kết quả thử nghiệm cho thấy mô hình đạt độ chính xác 95%.

### 19. Straight quotation marks

**Rule:** Academic Vietnamese strictly uses curved quotation marks (`“ ”`). Replace straight quotes (`" "`).
**Before:**
> Phương pháp này được gọi là "học sâu".
**After:**
> Phương pháp này được gọi là “học sâu”.

### 20. Explanations parked inside parentheses

**Rule:** Parentheses may hold a term gloss (a foreign-language term or an abbreviation) but never a Vietnamese clause. If the material inside the parens has a verb, fold it back into the sentence with a connective and leave only the foreign term in the brackets.
**Problem:** Same fault as #14, with brackets instead of a dash. It also creates asymmetry, because parallel items end up described in two different shapes, one bracketed and one not.
**Before:**
> Tiêu biểu nhất là kỹ thuật Top-$k$ (chỉ giữ lại $k$ từ có xác suất cao nhất) và Top-$p$ hay nucleus sampling, chỉ giữ lại nhóm các từ đứng đầu có tổng xác suất đạt một ngưỡng $p$.
**After:**
> Tiêu biểu nhất là hai kỹ thuật Top-$k$ và Top-$p$, hay còn gọi là nucleus sampling. Top-$k$ chỉ giữ lại $k$ từ có xác suất cao nhất, còn Top-$p$ giữ lại nhóm các từ đứng đầu cho tới khi tổng xác suất của chúng chạm một ngưỡng $p$ định trước.

### 21. Cross-references bracketed instead of introduced

**Rule:** A reference to another section of the same document belongs in the sentence. Introduce it with *ở mục*, *tại mục*, *trình bày ở mục*, or *xem mục*. Do not park it in parentheses as `(mục 3.2)`.
**Exception:** Figure, table, appendix, and equation callouts keep their parentheses: `(Hình 2.1)`, `(Bảng 3.4)`, `(Phụ lục A)`, `(công thức 2.3)`.
**Before:**
> Ràng buộc này chi phối cả cách xác định số lần lặp thí nghiệm (mục 3.2) lẫn các giới hạn về khả năng tái lập (mục 6.2).
**After:**
> Ràng buộc này chi phối cả cách xác định số lần lặp thí nghiệm ở mục 3.2 lẫn các giới hạn về khả năng tái lập trình bày tại mục 6.2.

---

## Chatbot patterns

### 22. Chatbot text left in the answer

**Words to watch:** Chắc chắn rồi!, Dưới đây là, Hy vọng phần trên hữu ích, Hãy cho mình biết nếu...
**Problem:** Conversational chatbot artifacts remaining in exported reports.
**Before:**
> Chắc chắn rồi! Dưới đây là phần mở đầu cho chương 3 của luận văn. Hy vọng nó hữu ích cho bạn!
**After:**
> Chương 3 trình bày chi tiết về kiến trúc hệ thống và quy trình xử lý dữ liệu.

### 23. Knowledge-limit disclaimers and speculative gaps

**Words to watch:** Tính đến thời điểm hiện tại, Theo hiểu biết của tôi, Dữ liệu không công khai nhưng có khả năng
**Problem:** AI confesses cutoff dates or invents speculative filler to plug missing sources.
**Before:**
> Thông tin chi tiết về thuật toán chưa được công bố công khai, nhiều khả năng nhóm tác giả đã áp dụng kỹ thuật nén mô hình.
**After:**
> Nhóm tác giả không công bố chi tiết thông số kỹ thuật của thuật toán.

### 24. Overly agreeable tone

**Words to watch:** Câu hỏi rất hay!, Bạn hoàn toàn đúng khi cho rằng
**Problem:** AI excessively flatters the prompt before presenting information.
**Before:**
> Câu hỏi của bạn rất hay. Bạn hoàn toàn đúng khi nhận định rằng chi phí phần cứng là một rào cản lớn.
**After:**
> Chi phí đầu tư phần cứng là một trong những rào cản chính khi triển khai mô hình ở quy mô lớn.

---

## Filler and hedging

### 25. Filler phrases

**Words to watch:** nhằm mục đích để, do bởi vì, trong bối cảnh hiện nay thì, việc ... là điều hết sức cần thiết, có thể nói rằng
**Problem:** Wordy bureaucratic boilerplate that dilutes technical clarity.
**Before:**
> Nhằm mục đích để nâng cao độ chính xác, việc áp dụng mô hình là điều hết sức cần thiết.
**After:**
> Để nâng cao độ chính xác, nghiên cứu áp dụng mô hình mạng nơ-ron tích chập.

### 26. Too many qualifiers

**Words to watch:** phần nào, ở một mức độ nhất định, tương đối, có thể nói là, khá là
**Problem:** Piling qualifiers until technical assertions become non-committal.
**Before:**
> Kết quả thử nghiệm phần nào có thể xem là tương đối khả quan ở một mức độ nhất định.
**After:**
> Kết quả thử nghiệm cho thấy mô hình hoạt động ổn định trên tập kiểm thử.

### 27. Generic positive endings

**Problem:** Concluding chapters with vague inspirational send-offs instead of technical summaries.
**Before:**
> Tương lai tươi sáng đang mở ra cho ngành trí tuệ nhân tạo với những bước tiến vượt bậc hướng tới sự hoàn mỹ.
**After:**
> Nghiên cứu đã hoàn thành mục tiêu xây dựng mô hình phân loại và mở ra hướng tối ưu hóa bộ nhớ cho các thiết bị biên.

### 28. Four-character clichés and bureaucratic wordiness

**Words to watch:** tiến hành thực hiện, tiến hành nghiên cứu đối với, triển khai áp dụng vào trong thực tiễn, muôn màu muôn vẻ
**Problem:** Bureaucratic helper-verb inflation (calquing Chinese 进行/实现) or poetic idioms.
**Before:**
> Nhóm nghiên cứu tiến hành thực hiện việc phân tích đối với các mẫu dữ liệu thu thập được.
**After:**
> Nhóm nghiên cứu phân tích các mẫu dữ liệu thu thập được.

### 29. Pretending to reveal a deeper truth

**Words to watch:** Về bản chất, Vấn đề cốt lõi nằm ở chỗ, Xét cho cùng, Thực chất
**Problem:** Staging routine technical points as profound revelations.
**Before:**
> Vấn đề cốt lõi thực chất nằm ở chỗ các vi dịch vụ giao tiếp qua mạng có độ trễ cao.
**After:**
> Độ trễ hệ thống tăng chủ yếu do chi phí truyền thông qua mạng giữa các vi dịch vụ.

### 30. Announcing the next point

**Words to watch:** Hãy cùng tìm hiểu, Sau đây chúng ta sẽ đi sâu vào, Trước tiên cần khẳng định rằng
**Problem:** Conversational meta-commentary announcing upcoming sections.
**Before:**
> Hãy cùng tìm hiểu cơ chế hoạt động của giao thức TCP.
**After:**
> Giao thức TCP đảm bảo truyền dữ liệu tin cậy thông qua cơ chế bắt tay ba bước.

### 31. A heading repeated in the first sentence

**Problem:** Echoing the heading in a one-line restatement immediately below it.
**Before:**
> ### 3.1. Kiến trúc hệ thống
> Kiến trúc hệ thống đóng vai trò quan trọng. Hệ thống gồm 3 tầng chính...
**After:**
> ### 3.1. Kiến trúc hệ thống
> Hệ thống gồm 3 tầng chính...

### 32. Writing about the previous version

**Problem:** Describing discarded iterations in present-tense technical documentation.
**Before:**
> Hàm này được viết lại để thay thế cho cách tiếp cận cũ vốn chạy vòng lặp tốn O(n²).
**After:**
> Hàm sử dụng cấu trúc bảng băm để đạt độ phức tạp tìm kiếm O(1).

### 33. Dramatic fragments and clipped sentence runs

**Problem:** Adjacent clipped sentences mimicking English dramatic syntax. Merge with connectives.
**Before:**
> Hệ thống không ghi nhận lỗi. Không cảnh báo. Chỉ âm thầm ghi log.
**After:**
> Hệ thống không ghi nhận lỗi và không phát cảnh báo, mà chỉ âm thầm lưu vào nhật ký hoạt động.

### 34. Formulaic sayings

**Words to watch:** X là chìa khóa của Y, X là chiếc cầu nối, X là kim chỉ nam cho
**Problem:** Trite metaphors replacing technical precision.
**Before:**
> Dữ liệu sạch là chiếc chìa khóa vạn năng mở ra cánh cửa thành công cho mô hình học máy.
**After:**
> Chất lượng dữ liệu tiền xử lý quyết định trực tiếp đến độ chính xác của mô hình học máy.

### 35. Fake-candid openings

**Words to watch:** Thành thật mà nói, Thú thực, Nhìn nhận khách quan thì
**Problem:** Artificial theatrical pauses before ordinary claims.
**Before:**
> Thành thật mà nói, việc tối ưu thời gian phản hồi là một thách thức không hề đơn giản.
**After:**
> Tối ưu thời gian phản hồi là thách thức kỹ thuật lớn trong hệ thống phân tán.

### 36. Answering objections no one raised

**Words to watch:** Điều này không có nghĩa là, Chúng tôi không phủ nhận, Đừng hiểu nhầm rằng
**Problem:** Defending against unstated criticisms. State the technical constraint directly.
**Before:**
> Điều này không có nghĩa là chúng tôi phủ nhận vai trò của cơ sở dữ liệu quan hệ, nhưng cơ sở dữ liệu NoSQL phù hợp hơn trong trường hợp này.
**After:**
> Cơ sở dữ liệu NoSQL phù hợp hơn với yêu cầu lưu trữ dữ liệu phi cấu trúc của đề tài.

### 37. Rejecting fake alternatives

**Words to watch:** Một phương án dễ nghĩ đến là, Người ta có thể bị cám dỗ bởi, Có ý kiến cho rằng nên
**Problem:** Introducing and immediately dismissing arbitrary strawman options.
**Before:**
> Một phương án dễ nghĩ đến là khởi động lại dịch vụ hàng giờ để xóa bộ nhớ tạm, nhưng điều đó làm gián đoạn người dùng. Hệ thống áp dụng cơ chế giải phóng bộ nhớ tự động.
**After:**
> Hệ thống áp dụng cơ chế tự động giải phóng bộ nhớ định kỳ trong lúc vận hành để tránh gián đoạn dịch vụ.

---

## Check for false positives

Do NOT flag or alter the following valid Vietnamese academic conventions:

- **Long, compound sentences:** Median 21 syllables (up to 40–50 syllables with clear subordinate clauses) is standard academic style.
- **Sino-Vietnamese terminology:** Prefer *khả năng xác minh* over colloquial *khả năng kiểm tra lại được*.
- **Subject ellipsis:** Natural in Vietnamese when context is established (e.g., *"Qua đó, giảm sự phụ thuộc vào bên trung gian."*).
- **Pure "được":** Natural and frequent; flag ONLY the `được ... bởi` agentive passive frame.
- **High connective density:** 4–5 connectives per 100 syllables is correct and necessary.
- **All-caps chapter headings:** `CHƯƠNG 2: CƠ SỞ LÝ THUYẾT` is standard Vietnamese report formatting.
- **Curved quotation marks:** `“ ”` is the required standard.
- **Academic citations and symbols:** Never alter `[...]`, `(...)`, mathematical formulas, or verbatim quoted sources.

---

## Output modes

Depending on the input quality and source availability, produce output in one of four modes:

1. **`clean_rewrite` (Default):** The rewrite directly replaces the original text when meaning is unambiguous and facts/citations are intact.
2. **`review_comment`:** When a sentence lacks required citations, dates, or data points, return a targeted reviewer comment rather than fabricating details.
3. **`needs_author_decision`:** When the original phrasing is ambiguous and multiple interpretations yield different factual assertions, present the options to the author.
4. **`no_change`:** When the input prose is already natural, grammatical, and free of AI fluff, leave it untouched rather than introducing unnecessary stylistic churn.

## How to return the result

**Pasted text (default):** Return the draft, a list of identified issues, and the final polished rewrite.

**File mode:** When editing a file, modify only prose in place. Preserve code blocks, math equations, tables, YAML metadata, and citations. Provide a brief 3–5 line summary of changes.

**Embedded mode:** When invoked inside a broader task or pipeline, return only the final rewritten prose.

## Rewrite process

1. Identify AI patterns and syntactic translationese against the 37 patterns.
2. Draft the revision: join clauses using subordinating connectives, eliminate fluff, and balance sentence rhythm.
3. Self-check with two mandatory questions:
   - *"Does this sound like natural Vietnamese academic prose or a machine translation?"*
   - *"Were any facts, numbers, dates, claims, or citation tags (`[...]`) added, altered, or lost?"*
4. Output the result per the selected mode.
