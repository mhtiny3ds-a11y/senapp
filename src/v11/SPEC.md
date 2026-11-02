# Viết bài học mới cho App Sen (Senapp)

Senapp là app học kỹ năng mềm cho trẻ Việt Nam, song ngữ Việt–Anh. Mỗi nhóm tuổi có 45 bài = 9 tuần × 5 bài. Tuần 1 đã có (xem `week1.json`). Bạn viết **tuần 2 → 9 (40 bài)** cho MỘT nhóm tuổi.

Thư mục làm việc: `/tmp/claude-0/-home-user-notebooklm-py/2645776a-48d7-5467-8bed-0fcf75c00226/scratchpad/v11/`

## Nhóm tuổi và nhân vật
| khoá | tuổi hiển thị | nhân vật chính | độ dài câu chuyện (vi) | thời lượng `m` |
|---|---|---|---|---|
| `5-8` | 6–8 | Bin (bạn thân: Na) | 1–2 câu, ≤ 35 từ, từ ngữ rất đơn giản | "5 phút"–"7 phút" |
| `9-12` | 9–11 | An | 2–3 câu, ≤ 50 từ | "8 phút"–"10 phút" |
| `13-16` | 12–15 | Khoa | 2–3 câu, ≤ 60 từ | "10 phút"–"14 phút" |

Nhân vật phụ: ba, mẹ, ông bà, em/anh chị, cô giáo/thầy giáo, bạn cùng lớp (tên Việt phổ biến: Na, Tí, Mai, Huy, Linh, Nam, Vy, Bảo…). Không dùng tên người nổi tiếng/thương hiệu.

## 9 kỹ năng (`sk`)
0 Giao tiếp · 1 Quản lý cảm xúc · 2 Làm việc nhóm · 3 Tự lập · 4 Giải quyết vấn đề · 5 Tư duy phản biện · 6 An toàn & ranh giới · 7 Quản lý thời gian · 8 Tài chính cá nhân

Thứ tự kỹ năng trong mỗi tuần là CỐ ĐỊNH, lấy từ `schedule.json` (`schedule[band][tuần-2]`). Validator sẽ kiểm tra.

## Định dạng — mỗi tuần một file `content/<band>-w<N>.json` (N = 2..9), là mảng đúng 5 bài
Xem mẫu đầy đủ: `example-lesson.json`. Mỗi bài:
```json
{
  "sk": 7,
  "t": ["Tên bài tiếng Việt", "English title"],
  "m": ["10 phút", "10 min"],
  "base": "A",
  "story": ["Câu chuyện chính (bối cảnh = base)", "English"],
  "cq": ["Câu hỏi lựa chọn", "English"],
  "co": [["Lựa chọn", "Option", 0, "Mẹo của Sen giải thích vì sao", "Sen's tip why"], [..., 1, ...], [..., 0, ...]],
  "qq": ["Câu đố nguyên tắc chung", "English"],
  "qo": [["Đáp án", "Answer"], ["...", "..."], ["...", "..."]],
  "qa": 2,
  "ctx": {
    "B": {"s": ["Câu chuyện ở trường", "..."], "q": ["Câu hỏi", "..."], "o": [[5 phần tử] ×3]},
    "C": {"s": ["Câu chuyện ngoài đời", "..."], "q": [...], "o": [...]}
  }
}
```
- Ba bối cảnh: **A = Ở nhà** (với người trong nhà), **B = Trên lớp** (bạn bè, thầy cô), **C = Ngoài đời** (cửa hàng, khu phố, công viên… luôn có người lớn quen đi cùng hoặc ở gần với nhóm nhỏ tuổi). `base` là bối cảnh của `story/cq/co`; `ctx` chứa đúng 2 bối cảnh còn lại. Cùng một kỹ năng/nguyên tắc ở cả 3 bối cảnh.
- Mỗi bộ lựa chọn: đúng 3 lựa chọn, đúng 1 lựa chọn đúng (1). **Đổi vị trí lựa chọn đúng** (không phải lúc nào cũng ở giữa). Các lựa chọn sai phải là điều trẻ hay làm thật, không ngớ ngẩn.
- Mẹo của Sen: 1–2 câu, ấm áp, không chê trách, nói rõ VÌ SAO; lựa chọn sai thì gợi cách tốt hơn.
- `qa`: vị trí đáp án đúng của câu đố — **thay đổi 0/1/2** giữa các bài.
- Tiếng Anh: tự nhiên, ngắn, kiểu Anh (Mum, colour). Dùng nháy cong ’ “ ”. Không dùng ký tự `<` hoặc `{{`.
- Không trùng chủ đề với bài tuần 1 (`week1.json`) và các bài theo mùa (khối `const SEASONS` trong `../audit/app10.tpl`, dòng ~2098–2160). 40 bài trong nhóm tuổi phải khác chủ đề nhau; cùng kỹ năng thì đi từ dễ → khó qua các tuần.

## Quy tắc nội dung (BẮT BUỘC)
App bán rộng rãi cho trẻ em tại Việt Nam. Nội dung phải hoàn toàn tích cực, phù hợp lứa tuổi, tuân thủ pháp luật Việt Nam và thuần phong mỹ tục:
- KHÔNG: chính trị, lãnh tụ, nhân vật lịch sử/chính trị, tôn giáo, quân sự, chiến tranh, biên giới/lãnh thổ, bạo lực, vũ khí, máu, ma quỷ/kinh dị, chất cấm, rượu bia, thuốc lá, cờ bạc, cá cược, tình cảm yêu đương, nội dung người lớn, phân biệt vùng miền/giới tính/dân tộc/ngoại hình, chê bai người khuyết tật, thương hiệu/sản phẩm thật, mạng xã hội cụ thể (nói "nhóm chat lớp", "mạng" chung chung), trò chơi điện tử cụ thể.
- KHÔNG khuyến khích trẻ đi làm kiếm tiền, buôn bán, vay mượn tiền, đầu tư, tiền ảo. Tài chính chỉ là: tiền tiêu vặt, tiết kiệm, so sánh giá, cần/muốn, chia sẻ, giữ tiền cẩn thận.
- An toàn: không bao giờ khuyến khích trẻ đi một mình với người lạ, gặp người quen trên mạng, gửi ảnh/thông tin cá nhân, giữ bí mật với ba mẹ. Lựa chọn đúng luôn có hướng **tìm người lớn tin cậy** khi có nguy hiểm. Không mô tả chi tiết đáng sợ. Không mô tả hành vi nguy hiểm có thể bắt chước.
- Giờ giấc hợp tuổi (về nhà trước 19h–19h30 với 12–15 tuổi; trẻ nhỏ luôn có người lớn).
- Vai trò giới bình đẳng (ba cũng nấu ăn, con gái cũng sửa đồ…). Gia đình đa dạng nhưng không đi sâu chuyện riêng tư (ly hôn, bệnh nặng, mất người thân).
- Không hứa hẹn kết quả, không so sánh trẻ này với trẻ khác theo kiểu hạ thấp.
- Văn phong: tiếng Việt chuẩn, tự nhiên, xưng hô đúng (con – ba mẹ, em – thầy cô, mình/tớ – bạn), không tiếng lóng, không từ nước ngoài khi có từ Việt.

## Quy trình
1. Đọc `SPEC.md`, `schedule.json`, `week1.json`, `example-lesson.json`, khối SEASONS trong `../audit/app10.tpl`.
2. Lên danh sách 40 chủ đề (tên bài) cho nhóm tuổi của bạn trước, kiểm tra không trùng.
3. Viết từng tuần vào `content/<band>-w<N>.json` (dùng Python/`json.dump(..., ensure_ascii=False, indent=1)` để đảm bảo JSON hợp lệ).
4. Chạy `python3 validate.py content/<band>-w*.json` cho đến khi tất cả OK.
5. Tự rà soát lại toàn bộ 40 bài theo **Quy tắc nội dung**; sửa nếu có chỗ nhạy cảm.
6. Báo cáo ngắn: danh sách 40 tên bài (vi) theo tuần, và kết quả validator.
