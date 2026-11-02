# Viết nhiệm vụ đời thực cho từng bài học — App Sen

Mỗi bài học trong App Sen kết thúc bằng **đúng MỘT nhiệm vụ đời thực**: một việc con làm thật ở nhà/ngoài đời trong hôm nay hoặc vài ngày tới, áp dụng đúng điều vừa học. Ba mẹ bấm xác nhận thì con nhận sao.

Thư mục: `/tmp/claude-0/-home-user-notebooklm-py/2645776a-48d7-5467-8bed-0fcf75c00226/scratchpad/v11/`

- Danh sách 45 bài của nhóm tuổi bạn: `lessons-<band>.txt` (oi = số thứ tự bài 0..44, kỹ năng, tên bài, câu đố, câu chuyện). Đọc thêm chi tiết bài trong `week1.json` (5 bài đầu, oi 0–4) và `content/<band>-w<N>.json` (oi = (N-1)*5 + vị trí 0..4) nếu cần.
- Viết file `content/missions-<band>.json`: mảng **đúng 45** phần tử theo thứ tự oi:

```json
{
  "oi": 0,
  "t":  ["Tên nhiệm vụ ngắn (≤ 12 từ)", "Short mission title"],
  "s":  ["Hướng dẫn 1–2 câu: làm gì, với ai, khi nào, làm xong thì kể/cho ba mẹ xem gì", "English"],
  "lv": [["Mức 1 – làm cùng ba mẹ: ...", "Level 1 – together: ..."],
         ["Mức 2 – ba mẹ nhắc một lần, con tự làm: ...", "..."],
         ["Mức 3 – con tự nhớ, tự làm, kể lại: ...", "..."]],
  "rw": ["Phần thưởng nhỏ của gia đình", "Small family reward"]
}
```
(Viết nội dung mức khó không cần chữ "Mức 1 –"; app tự gắn nhãn. Mẫu văn phong: "Ba mẹ nói mẫu trước, con nói theo một câu." / "Ba mẹ nhắc một lần, con tự nói trong bữa tối." / "Con tự mở lời, nói đủ “Con cảm thấy… vì…” và nghe ba mẹ đáp lại.")

## Yêu cầu
- Nhiệm vụ gắn chặt với kỹ năng và nguyên tắc của đúng bài đó; cụ thể, làm được trong 5–20 phút, đo được (ba mẹ nhìn thấy/nghe thấy để xác nhận).
- Phù hợp tuổi: 6–8 tuổi (`5-8`, rất đơn giản, luôn có người lớn), 9–11 (`9-12`), 12–15 (`13-16`, tự chủ hơn nhưng vẫn báo ba mẹ).
- An toàn tuyệt đối: không ra ngoài một mình (trẻ nhỏ), không bếp/dao/điện/nước sâu nếu không có người lớn trực tiếp làm cùng, không liên lạc người lạ, không đăng ảnh/thông tin lên mạng, không mua bán, không kiếm tiền, không vay mượn tiền.
- Phần thưởng (`rw`): nhỏ, ấm áp, **không phải tiền**, không quà đắt, hạn chế đồ ngọt và thời gian màn hình. Ví dụ: được chọn truyện đọc tối nay, chọn trò chơi cả nhà chơi cuối tuần, ba mẹ kể một chuyện hồi nhỏ, cùng đi dạo công viên, cả nhà nấu món con thích, được chọn bài hát trên đường đi học, một cái ôm thật chặt và lời khen trước cả nhà. Đa dạng, không lặp lại quá 3 lần trong 45 nhiệm vụ.
- Không chính trị, tôn giáo, bạo lực, thương hiệu, mạng xã hội cụ thể; tiếng Việt chuẩn, xưng hô "con – ba mẹ"; tiếng Anh tự nhiên kiểu Anh, nháy cong ’ “ ”; không ký tự `<` hoặc `{{`.
- Giờ giấc hợp tuổi (không hẹn sau 19h30 ở ngoài).

## Quy trình
1. Đọc spec, `lessons-<band>.txt`.
2. Viết bằng Python + `json.dump(..., ensure_ascii=False, indent=1)` vào `content/missions-<band>.json`.
3. Chạy `python3 validate_m.py content/missions-<band>.json` đến khi OK.
4. Tự rà soát theo yêu cầu an toàn & nội dung. Báo cáo ngắn: kết quả validator + 5 ví dụ nhiệm vụ.
Không sửa file nào khác.
