# Lập dàn bài 12 tháng cho App Sen (một nhóm tuổi tiểu học)

Thư mục: `/tmp/claude-0/-home-user-notebooklm-py/2645776a-48d7-5467-8bed-0fcf75c00226/scratchpad/y12/`

App Sen dạy 9 kỹ năng sống cho con tiểu học. Mỗi tuần 5 bài (mỗi bài 1 kỹ năng), mỗi bài có 3 tình huống (ở nhà / trên lớp / ngoài đời), câu đố và **một nhiệm vụ đời thực**. Hành trình 12 tháng = **12 chặng × 4 tuần = 48 tuần = 240 bài**. Tuần 1–9 đã có (`existing-<band>.txt`). Bạn lập **dàn bài cho tuần 10–48 (195 bài)**. Người khác sẽ viết chi tiết theo dàn bài của bạn, nên dàn bài phải rõ, không trùng lặp.

Kỹ năng (sk): 0 Giao tiếp · 1 Quản lý cảm xúc · 2 Làm việc nhóm · 3 Tự lập · 4 Giải quyết vấn đề · 5 Tư duy phản biện · 6 An toàn & ranh giới · 7 Quản lý thời gian · 8 Tài chính cá nhân.
Thứ tự kỹ năng mỗi tuần CỐ ĐỊNH theo `schedule.json` (khoá là số tuần "10".."48").

Nhóm tuổi: `5-8` = 6–8 tuổi (lớp 1–3, nhân vật Bin, bạn Na; ba mẹ đọc cùng con; tình huống rất gần gũi, ngắn) · `9-12` = 9–11 tuổi (lớp 4–5, nhân vật An).

## Yêu cầu
- Mỗi chặng (4 tuần) có một **chủ đề** gắn đời sống con tiểu học, đi từ dễ → khó, từ bản thân → gia đình → lớp học → cộng đồng. Không gắn tháng dương lịch cụ thể (con có thể bắt đầu bất kỳ lúc nào). Chặng 1–3 đã có một phần (tuần 1–9): đặt tên chủ đề cho chúng cho khớp nội dung hiện có.
- 195 tên bài **không trùng** nhau, không trùng tuần 1–9 (`existing-<band>.txt`) và không trùng các bài theo dịp (khối `const SEASONS` trong `../audit/app13.tpl`, dòng ~2359–2421). Cùng kỹ năng thì các tuần sau khó hơn tuần trước; có thể quay lại một chủ đề cũ ở mức sâu hơn nhưng góc nhìn phải mới.
- Mỗi bài: tên bài (vi + en), ý chính 1 câu (vi), gợi ý nhiệm vụ đời thực 1 câu (vi) — làm được trong 5–20 phút, an toàn, có ba mẹ xác nhận.
- Quy tắc nội dung bắt buộc: hoàn toàn tích cực, phù hợp lứa tuổi, tuân thủ pháp luật Việt Nam và thuần phong mỹ tục. KHÔNG chính trị, lãnh tụ, tôn giáo, chiến tranh, bạo lực, ma quỷ, rượu bia, thuốc lá, cờ bạc, yêu đương, thương hiệu, mạng xã hội/trò chơi cụ thể, phân biệt đối xử. KHÔNG khuyến khích trẻ đi làm kiếm tiền, buôn bán, vay mượn, đầu tư. An toàn: không đi một mình với người lạ, không gặp người quen trên mạng, không giữ bí mật xấu; luôn tìm người lớn tin cậy. Vai trò giới bình đẳng.

## Đầu ra: `plan/<band>.json`
```json
{"chang": [{"n": 1, "theme": "…", "weeks": [1,2,3,4]}, … 12 chặng],
 "weeks": {"10": [{"sk": 0, "t": ["Tên bài", "English title"], "gist": "Ý chính", "mission": "Gợi ý nhiệm vụ"}, …5 bài theo đúng thứ tự sk của schedule], … "48": […]}}
```
Viết bằng Python (`json.dump(..., ensure_ascii=False, indent=1)`). Tự kiểm tra: đủ tuần 10–48, mỗi tuần 5 bài đúng sk, không trùng tên (so cả với existing). Báo cáo ngắn: 12 chủ đề chặng + số bài mỗi kỹ năng. Không sửa file nào khác.
