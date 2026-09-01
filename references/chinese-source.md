# Cleaning Translationese from Chinese Academic Sources

When Vietnamese academic text is translated or adapted from Chinese source literature, it exhibits specific structural and rhetorical faults that differ markedly from English-origin translationese.

## Key Faults and Solutions

### 1. Reverse Modifier Structures (Mệnh đề định ngữ ngược chiều)
- **Problem:** Chinese places long relative clauses and modifiers *before* the noun (using 的). Machine translations often retain this inverted order or pad sentences with unnatural *“của”*.
- **Fix:** Invert the modifier to follow the head noun in Vietnamese.
- **Example:**
  - ✗ *“Đây là một dựa trên học sâu tự động phát hiện xâm nhập của hệ thống.”*
  - ✓ *“Đây là hệ thống tự động phát hiện xâm nhập hoạt động dựa trên học sâu.”*

### 2. False Friends (Từ đồng hình dị nghĩa)
Direct Sino-Vietnamese transliteration of certain modern Chinese terms creates semantic confusion:

| Chinese Term | Literal Calque | Correct Academic Vietnamese |
|---|---|---|
| 手段 (shǒuduàn) | thủ đoạn | phương pháp, biện pháp |
| 表现良好 (biǎoxiàn) | biểu hiện tốt | thể hiện tốt, đạt hiệu quả cao |
| 情况 (qíngkuàng) | tình huống | tình hình, trạng thái |
| 方便 (fāngbiàn) | phương tiện | thuận tiện, dễ dàng |
| 认真 (rènzhēn) | nhận chân | nghiêm túc, kỹ lưỡng |

### 3. Redundant Verbal Frames (进行 / 实现)
- **Problem:** Chinese academic writing frequently pads verbs with 进行 (tiến hành) and 实现 (thực hiện).
- **Fix:** Drop the helper verbs; use the direct action verb.
- **Example:**
  - ✗ *“Nghiên cứu này tiến hành thực hiện việc phân tích đối với dữ liệu.”*
  - ✓ *“Nghiên cứu này phân tích dữ liệu.”*

### 4. Chinese Four-Character Slogans & Bureaucratic Fluff
- **Problem:** Heavy bureaucratic idioms (具有重要的理论意义和现实意义 / 为...奠定了坚实的基础) map directly to Layer 2 inflated claims.
- **Fix:** Strip the empty fluff and state empirical contributions directly.
