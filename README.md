# Humanizer-VietAcademic

[![skills.sh installs](https://skills.sh/b/kkhanh-kas/humanizer)](https://skills.sh/kkhanh-kas/humanizer)

Humanizer-VietAcademic là công cụ tối ưu hóa văn phong học thuật tiếng Việt cho AI agent. Kỹ năng này viết lại các văn bản tiếng Việt mang giọng điệu AI hoặc dịch thô từ tiếng nước ngoài (Anh, Trung) thành văn phong học thuật chuẩn mực, tự nhiên như văn của giảng viên và nhà nghiên cứu người Việt, đồng thời **bảo toàn tuyệt đối mọi dữ kiện, số liệu và trích dẫn khoa học**, không bịa đặt nội dung.

## Cách thức hoạt động

Humanizer-VietAcademic xây dựng bộ 35 pattern trên cơ sở danh mục [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) của Wikipedia, kết hợp với hệ thống quy chuẩn ngữ pháp, nhịp điệu và dấu câu của văn bản học thuật tiếng Việt.

> **Nguyên lý cốt lõi:** *Khi phân vân, hãy ghép mệnh đề thay vì tách câu.*

Tiếng Anh ngắt câu bằng dấu câu, còn tiếng Việt nối câu bằng từ nối. Văn phong học thuật tiếng Việt tự nhiên nối liền 3–4 mệnh đề trong một câu bằng dấu phẩy và các liên từ phụ thuộc (*nhờ đó, qua đó, trong khi, đồng thời*), duy trì nhịp điệu trung bình 21 âm tiết/câu và mật độ từ nối đạt 4–5%.

### Quy chuẩn cứng cho văn học thuật tiếng Việt

- **Không dùng dấu gạch ngang giữa câu:** Cấm dùng dấu gạch ngang (`—`, `–`) hoặc ` - ` để chen ngang ý giữa câu. Hãy thay bằng dấu phẩy và từ nối.
- **Không dùng dấu chấm phẩy:** Văn xuôi tiếng Việt hiện đại không dùng dấu chấm phẩy (`;`), chỉ dùng dấu phẩy và dấu chấm.
- **Bảo toàn nguyên vẹn trích dẫn:** Tuyệt đối giữ nguyên vị trí và ký hiệu trích dẫn tài liệu tham khảo (`[1]`, `[3-5]`, `(Nguyen et al., 2024)`) cũng như các biểu thức toán học.
- **Chuẩn hóa ngoặc kép cong:** Luôn dùng ngoặc kép cong `“ ”` (không dùng ngoặc kép thẳng `" "`).
- **Xóa bỏ triệt để văn dịch:** Loại bỏ thể bị động ngoại lai `được ... bởi` và đại từ ngôi thứ hai `bạn` trong văn bản học thuật.

## Cài đặt (Installation)

### 1. Cài đặt qua Skills CLI
Cài đặt toàn cục cho mọi agent:
```bash
npx skills add kkhanh-kas/humanizer --global
```
*(Bỏ cờ `--global` nếu chỉ muốn cài đặt cho dự án hiện tại. Thêm `--agent <tên>` hoặc `--agent '*'` để chỉ định agent nhận kỹ năng, sau đó tải lại danh sách skills).*

Cập nhật phiên bản mới nhất:
```bash
npx skills update humanizer --global
```

### 2. Cài đặt như một Claude Plugin
Dành cho Claude Code 2.1.142 trở lên:
```text
/plugin marketplace add kkhanh-kas/humanizer
/plugin install humanizer@humanizer
```
Lệnh gọi plugin trong Claude: `/humanizer:humanizer-viet-academic`.

### 3. Cài đặt trên Claude Desktop
Tải repository này dưới dạng file ZIP và tải lên (upload) trong mục Skills của Claude Desktop.

### 4. Cài đặt thủ công (Manual install)
Sao chép toàn bộ thư mục repository vào thư mục skills của agent. Lưu ý: Không chỉ sao chép mỗi file `SKILL.md`, vì trong quá trình hoạt động prompt sẽ tự động đọc các file tham chiếu trong `references/` và catalog trong `patterns/`.

## Hướng dẫn sử dụng (Usage)

Gọi trực tiếp kỹ năng bằng lệnh:
```text
/humanizer-viet-academic

[Dán đoạn văn bản học thuật cần chỉnh sửa vào đây]
```

Hoặc yêu cầu bằng ngôn ngữ tự nhiên:
```text
Sửa lại đoạn văn này theo văn phong học thuật tiếng Việt: [nội dung đoạn văn]
```

Để chỉnh sửa trực tiếp một file Markdown hoặc LaTeX:
```text
Humanize the academic prose in chapters/chapter2.md
```

## Các chế độ đầu ra (Output modes)

Humanizer-VietAcademic hỗ trợ 4 chế độ kết quả linh hoạt:

1. **`clean_rewrite` (Mặc định):** Trực tiếp viết lại đoạn văn mượt mà và thay thế vào văn bản gốc khi ngữ nghĩa rõ ràng và dữ kiện đầy đủ.
2. **`review_comment`:** Trả về nhận xét phản biện khi văn bản gốc thiếu nguồn trích dẫn, thiếu số liệu thực nghiệm hoặc có khẳng định chưa được chứng minh, thay vì tự bịa thêm thông tin.
3. **`needs_author_decision`:** Đặt câu hỏi và đưa ra các lựa chọn cho tác giả khi câu gốc mơ hồ và có nhiều cách hiểu kỹ thuật khác nhau.
4. **`no_change`:** Giữ nguyên văn bản gốc khi câu chữ đã tự nhiên, chuẩn xác và không mắc lỗi AI.

## Bộ 35 pattern

### Nhóm nội dung

| # | Pattern | Trước khi sửa | Sau khi sửa |
|---|---------|--------|-------|
| 1 | **Thổi phồng tầm quan trọng và di sản** | "đánh dấu bước ngoặt mang tính cách mạng trong quá trình nhận diện hình ảnh..." | "được đề xuất vào năm 2021 nhằm phục vụ bài toán nhận diện hình ảnh" |
| 2 | **Kể tên mơ hồ để tạo uy tín** | "được nhắc đến bởi nhiều chuyên gia đầu ngành và tạp chí uy tín" | "được phân tích chi tiết trong nghiên cứu của LeCun et al. [1]" |
| 3 | **Phân tích hời hợt với mệnh đề rỗng** | "qua đó thể hiện sự quan tâm sâu sắc và góp phần nâng cao trải nghiệm" | "để tăng cường bảo mật tài khoản" |
| 4 | **Ngôn ngữ quảng cáo, thương mại** | "cung cấp kiến trúc vi dịch vụ vô cùng mạnh mẽ và hoàn hảo" | "sử dụng kiến trúc vi dịch vụ để giảm độ trễ xử lý dữ liệu" |
| 5 | **Nguồn trích dẫn mập mờ** | "Theo các chuyên gia, việc chuyển dịch đám mây là tất yếu" | "Khảo sát của Gartner [2] cho thấy 85% doanh nghiệp đang chuyển dịch hạ tầng" |
| 6 | **Công thức sáo rỗng trong các phần bắt buộc** | "Bên cạnh kết quả, vẫn còn hạn chế nhất định... sẽ tiếp tục hoàn thiện" | "Mô hình hiện chỉ thử nghiệm trên tập 2.000 mẫu và chưa đánh giá khi thiếu sáng" |

### Nhóm ngôn ngữ và ngữ pháp

| # | Pattern | Trước khi sửa | Sau khi sửa |
|---|---------|--------|-------|
| 7 | **Lạm dụng từ ngữ AI đặc trưng** | "bức tranh toàn cảnh... đi sâu vào... kiến tạo nền tảng vững chắc" | "phân tích cấu trúc... tổng hợp các chính sách hỗ trợ" |
| 8 | **Tránh dùng từ 'là' và 'có'** | "PostgreSQL đóng vai trò là hệ quản trị cơ sở dữ liệu..." | "PostgreSQL là hệ quản trị cơ sở dữ liệu quan hệ mã nguồn mở" |
| 9 | **Cặp cấu trúc đối xứng lặp lại** | "không chỉ giúp tối ưu bộ nhớ mà còn tăng tốc... không chỉ xử lý số liệu mà còn..." | "tối ưu bộ nhớ, tăng tốc độ thực thi và hỗ trợ phân tích ngữ nghĩa" |
| 10 | **Gượng ép ghép nhóm bộ ba, bộ bốn** | "đảm bảo tính trực quan, tính thẩm mỹ, tính tương tác và tính bảo mật" | "trực quan và đảm bảo an toàn thông tin khi thao tác" |
| 11 | **Đổi tên gọi tùy tiện và lặp đầu câu** | "tác giả... người viết... nhà nghiên cứu luân phiên trong cùng đoạn" | Dùng nhất quán một danh xưng ("nhóm nghiên cứu") |
| 12 | **Phạm vi giả định 'từ X đến Y'** | "khảo sát từ cấu trúc vi mạch bán dẫn đến chính sách kinh tế vĩ mô" | "phân tích chuỗi cung ứng vi mạch và các chính sách kinh tế liên quan" |
| 13 | **Bị động dịch thô và sai đại từ xưng hô** | "Dữ liệu được thu thập bởi hệ thống. Bạn có thể thấy nó hoạt động..." | "Hệ thống tự động thu thập dữ liệu với tốc độ xử lý dưới 50ms" |

### Nhóm văn phong và trình bày

| # | Pattern | Trước khi sửa | Sau khi sửa |
|---|---------|--------|-------|
| 14 | **Dấu gạch ngang giữa câu (— / –)** | "Hệ thống xác thực — vốn phát triển theo OAuth 2.0 — cho phép..." | "Hệ thống xác thực được phát triển theo OAuth 2.0, nhờ đó cho phép..." |
| 15 | **Lạm dụng in đậm (Bold)** | "Mô hình **Transformer** sử dụng cơ chế **Self-Attention**..." | "Mô hình Transformer sử dụng cơ chế Self-Attention..." |
| 16 | **Danh sách gạch đầu dòng in đậm tiêu đề** | "- **Hiệu năng:** Tăng 20%.\n- **Chi phí:** Tiết kiệm 15%." | "Tối ưu thuật toán giúp tăng tốc 20%, đồng thời tiết kiệm 15% phần cứng" |
| 17 | **Viết hoa kiểu Title Case ở tiêu đề** | "## Phân Tích Hiệu Năng Của Thuật Toán" | "## Phân tích hiệu năng của thuật toán" |
| 18 | **Sử dụng Emoji và biểu tượng trang trí** | "💡 **Kết quả chính:** Đạt 95%" | "Kết quả thử nghiệm cho thấy mô hình đạt độ chính xác 95%" |
| 19 | **Dấu ngoặc kép thẳng** | `gọi là "học sâu"` | `gọi là “học sâu”` |

### Nhóm dấu vết chatbot

| # | Pattern | Trước khi sửa | Sau khi sửa |
|---|---------|--------|-------|
| 20 | **Lời chào và xã giao của Chatbot** | "Chắc chắn rồi! Dưới đây là phần mở đầu... Hy vọng hữu ích cho bạn!" | "Chương 3 trình bày chi tiết về kiến trúc hệ thống và quy trình xử lý dữ liệu" |
| 21 | **Tuyên bố giới hạn tri thức và phỏng đoán** | "Chưa công bố công khai, nhiều khả năng nhóm tác giả đã áp dụng nén..." | "Nhóm tác giả không công bố chi tiết thông số kỹ thuật của thuật toán" |
| 22 | **Giọng điệu nịnh nọt, tán đồng thái quá** | "Câu hỏi của bạn rất hay! Bạn hoàn toàn đúng khi nhận định..." | "Chi phí đầu tư phần cứng là một trong những rào cản chính khi triển khai" |

### Nhóm sáo rỗng và rào đón

| # | Pattern | Trước khi sửa | Sau khi sửa |
|---|---------|--------|-------|
| 23 | **Cụm từ đệm rườm rà** | "Nhằm mục đích để nâng cao độ chính xác, việc áp dụng mô hình là cần thiết" | "Để nâng cao độ chính xác, nghiên cứu áp dụng mô hình mạng nơ-ron" |
| 24 | **Từ ngữ rào đón, thiếu dứt khoát** | "Kết quả phần nào có thể xem là tương đối khả quan ở mức độ nhất định" | "Kết quả thử nghiệm cho thấy mô hình hoạt động ổn định trên tập kiểm thử" |
| 25 | **Kết bài lạc quan sáo rỗng** | "Tương lai tươi sáng đang mở ra cho ngành AI với những bước tiến vượt bậc" | Kết bài bằng kết quả thực nghiệm cụ thể hoặc phương hướng nghiên cứu |
| 26 | **Động từ phụ tiếng Trung & thành ngữ sáo ngữ** | "tiến hành thực hiện việc phân tích đối với các mẫu dữ liệu" | "phân tích các mẫu dữ liệu thu thập được" |
| 27 | **Lên gân triết lý, giả vờ hé lộ chân lý** | "Vấn đề cốt lõi thực chất nằm ở chỗ..." | "Độ trễ hệ thống tăng chủ yếu do..." |
| 28 | **Thông báo sắp trình bày điều gì** | "Hãy cùng tìm hiểu cơ chế hoạt động..." | "Giao thức TCP đảm bảo truyền dữ liệu tin cậy qua cơ chế bắt tay ba bước" |
| 29 | **Lặp lại tiêu đề ngay câu đầu tiên** | "### 3.1. Kiến trúc hệ thống\nKiến trúc hệ thống đóng vai trò quan trọng..." | Trình bày trực tiếp nội dung kiến trúc ngay dưới tiêu đề |
| 30 | **Mô tả phiên bản cũ đã bị loại bỏ** | "Hàm này viết lại để thay thế cách tiếp cận cũ vốn chạy O(n²)" | "Hàm sử dụng cấu trúc bảng băm để đạt độ phức tạp tìm kiếm O(1)" |
| 31 | **Câu cụt kịch tính, ngắt câu gãy khúc** | "Hệ thống không ghi nhận lỗi. Không cảnh báo. Chỉ âm thầm ghi log." | "Hệ thống không ghi nhận lỗi và không cảnh báo, mà chỉ âm thầm ghi log" |
| 32 | **Ẩn dụ, ví von sáo mòn** | "Dữ liệu sạch là chiếc chìa khóa vạn năng mở ra cánh cửa thành công..." | "Chất lượng tiền xử lý dữ liệu quyết định độ chính xác của mô hình" |
| 33 | **Mở đầu bộc bạch giả tạo** | "Thành thật mà nói, việc tối ưu thời gian phản hồi là..." | "Tối ưu thời gian phản hồi là thách thức kỹ thuật lớn..." |
| 34 | **Phòng thủ, giải thích cho thắc mắc không ai hỏi** | "Điều này không có nghĩa là chúng tôi phủ nhận vai trò của RDBMS, nhưng..." | "Cơ sở dữ liệu NoSQL phù hợp hơn với yêu cầu lưu trữ phi cấu trúc" |
| 35 | **Đưa phương án giả định để tự bác bỏ** | "Một phương án dễ nghĩ đến là khởi động lại dịch vụ hàng giờ, nhưng..." | "Hệ thống áp dụng cơ chế tự động giải phóng bộ nhớ định kỳ khi vận hành" |

## Ví dụ minh họa thực tế (Full example)

**Trước khi sửa (Đậm giọng điệu AI và văn dịch thô):**
> Mô hình Transformer đóng vai trò vô cùng quan trọng, đánh dấu một bước ngoặt mang tính cách mạng trong quá trình xử lý ngôn ngữ tự nhiên. Theo các chuyên gia, đây là chiếc chìa khóa vạn năng mở ra một kỷ nguyên mới đầy hứa hẹn. Hệ thống xác thực — vốn được phát triển bởi nhóm tác giả dựa trên chuẩn OAuth 2.0 — cho phép phân quyền người dùng một cách tối ưu vượt trội. Bạn có thể thấy nó đạt độ chính xác 94.7% trên tập kiểm thử [1]. Bên cạnh những kết quả đạt được, đề tài vẫn còn tồn tại một số hạn chế nhất định. Trong thời gian tới, chúng tôi sẽ tiếp tục hoàn thiện để hướng tới tương lai tươi sáng.

**Sau khi biên tập (Văn phong học thuật tự nhiên, chuẩn mực):**
> Mô hình Transformer được ứng dụng phổ biến trong các bài toán xử lý ngôn ngữ tự nhiên hiện đại. Hệ thống xác thực được phát triển dựa trên chuẩn OAuth 2.0, nhờ đó cho phép phân quyền người dùng chi tiết, đồng thời dữ liệu đạt độ chính xác 94,7% trên tập kiểm thử [1]. Tuy nhiên, nghiên cứu hiện mới thử nghiệm trên tập dữ liệu 2.000 mẫu và chưa đánh giá được hiệu năng trong điều kiện thiếu sáng.

## Cấu trúc thư mục repository

```text
.
├── SKILL.md                          # Prompt chính điều phối kỹ năng và 35 pattern
├── patterns/
│   ├── schema.json                   # JSON schema chuẩn hóa định dạng các pattern
│   ├── layer1-grammar-syntax.yml     # Quy tắc Lớp 1: Ngữ pháp, dấu câu và nhịp điệu
│   └── layer2-rhetoric-style.yml     # Quy tắc Lớp 2: Tu từ, sáo ngữ AI và văn phong
├── references/
│   ├── layer1-grammar-syntax.md      # Tài liệu chi tiết về cú pháp và dấu câu Lớp 1
│   ├── false-positives.md            # Danh mục các quy ước học thuật không được báo sai
│   ├── registers.md                  # Hướng dẫn 4 phân hệ văn phong (Học thuật, Kỹ thuật, Công việc, Đời thường)
│   └── chinese-source.md             # Cẩm nang xử lý văn dịch từ nguồn tài liệu tiếng Trung
├── benchmarks/
│   ├── rubric.md                     # Rubric 10 tiêu chí đánh giá chất lượng
│   └── cases/academic-cases.json     # Bộ ca kiểm thử benchmark tự động
└── scripts/
    ├── catalog.py                    # Module duy nhất đọc và nạp YAML catalog
    ├── validate-package.py           # Script kiểm tra tính nhất quán toàn bộ package
    ├── validate-patterns.py          # Script kiểm thực catalog YAML theo schema
    ├── run-benchmark.py              # Script chạy benchmark và chấm điểm mô hình
    ├── test-kiem-tra.py              # Bộ test hồi quy cho linter
    └── kiem_tra.py                   # Script linter tự động kiểm tra lỗi cơ học tiếng Việt
```

## Đóng góp và Ghi công (Attributions & Acknowledgments)

Repository này được fork từ **blader/humanizer** và tích hợp các nghiên cứu chuyên sâu về văn phong tiếng Việt từ **vietnamese-humanizer**. Thông tin bản quyền của cả hai tác giả gốc đều được bảo lưu đầy đủ trong [LICENSE](LICENSE) theo đúng giấy phép MIT.

1. **[blader/humanizer](https://github.com/blader/humanizer)** (Giấy phép MIT): Cấu trúc phân loại pattern gốc, tích hợp Wikipedia AI Cleanup và kiến trúc kỹ thuật prompt.
2. **[vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer)** bởi **longhang2004** (Giấy phép MIT): Thiết kế schema phân tầng Lớp 1 và Lớp 2, phương pháp đánh giá benchmark và hệ thống quy tắc đặc trưng cho tiếng Việt.

## Lịch sử phiên bản (Version history)

<details>
<summary>Xem nhật ký phát hành</summary>

- **2.12.0**: Chuẩn hóa pattern catalog thành nguồn chân lý duy nhất (single source of truth): `scripts/kiem_tra.py` tự động đọc tín hiệu từ `patterns/*.yml` và lọc theo văn phong đã chọn. Khắc phục 3 trường hợp báo oan (từ nối nguyên nhân `bởi vì`, chuỗi 2 câu ngắn, và từ nằm trong ngoặc kép trích dẫn) kèm bài test trong `scripts/test-kiem-tra.py`. Tái cấu trúc benchmark runner hỗ trợ chấm điểm output thực tế bằng `--actual`. Bổ sung 4 quy tắc Lớp 1 (ngày tháng, chuỗi `của` lặp, thừa từ chỉ số nhiều, thừa từ `sẽ`) và tích hợp toàn bộ kiểm tra vào CI.
- **2.11.2**: Nâng cấp toàn diện thành Humanizer-VietAcademic: tích hợp ngữ pháp/nhịp điệu tiếng Việt, 35 pattern học thuật hóa, danh mục YAML, benchmark runner và tài liệu tham chiếu đa phân hệ.
- **2.11.1**: Bổ sung gói phát hành tương thích với Claude Desktop.
- **2.11.0**: Viết lại hướng dẫn prompt theo phong cách Plain Language dễ hiểu.
- **1.0.0**: Phiên bản phát hành đầu tiên.

</details>

## Giấy phép (License)

Giấy phép MIT, bao gồm bản quyền của cả hai tác giả gốc. Xem [LICENSE](LICENSE) để biết thêm chi tiết.
