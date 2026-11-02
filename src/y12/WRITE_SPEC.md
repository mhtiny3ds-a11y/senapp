# Viết bài học + nhiệm vụ (tuần 10–48) cho App Sen

Thư mục: `/tmp/claude-0/-home-user-notebooklm-py/2645776a-48d7-5467-8bed-0fcf75c00226/scratchpad/y12/`

1. Đọc kỹ `../v11/SPEC.md` (định dạng bài, quy tắc nội dung BẮT BUỘC, văn phong, độ dài theo tuổi) và `../v11/SPEC_MISSIONS.md` (quy tắc nhiệm vụ đời thực). Mẫu bài: `../v11/example-lesson.json`; mẫu nhiệm vụ: `../v11/content/missions-<band>.json`.
2. Dàn bài đã chốt: `plan/<band>.json` (khoá `weeks` → tuần → 5 bài: sk, t, gist, mission). **Viết đúng tên bài, đúng kỹ năng, đúng thứ tự** theo dàn bài; có thể chỉnh tên cho tự nhiên hơn nhưng giữ ý.
3. Mỗi tuần một file `content/<band>-w<N>.json` = mảng 5 bài. Mỗi bài theo định dạng SPEC.md (sk, t, m, base, story, cq, co, qq, qo, qa, ctx) **cộng thêm** khoá nhiệm vụ:
```json
"mi": {"t": ["Tên nhiệm vụ", "Mission title"], "s": ["Hướng dẫn 1–2 câu", "…"],
       "lv": [["Mức 1 làm cùng ba mẹ …", "…"], ["Mức 2 ba mẹ nhắc một lần …", "…"], ["Mức 3 con tự làm, kể lại …", "…"]],
       "rw": ["Phần thưởng nhỏ của gia đình (không phải tiền)", "…"]}
```
4. Lưu ý: vị trí lựa chọn đúng thay đổi đều A/B/C; `qa` thay đổi 0/1/2; base A/B/C đa dạng; tiếng Anh dùng nháy cong ’ “ ” (KHÔNG dùng nháy thẳng '), không dùng `<` hoặc `{{`. Nhóm `5-8` (6–8 tuổi, Bin/Na): câu chuyện ≤ 35 từ, m = "5 phút"–"7 phút", ba mẹ đọc cùng con. Nhóm `9-12` (9–11 tuổi, An): ≤ 50 từ, m = "8 phút"–"10 phút". Phần thưởng đa dạng, không lặp quá nhiều.
5. Viết bằng Python + `json.dump(..., ensure_ascii=False, indent=1)`. Chạy `python3 validate.py content/<band>-w<N>.json …` cho tới khi tất cả OK. Tự rà soát theo quy tắc nội dung.
6. Chỉ ghi các file tuần được giao. Không sửa file khác. Báo cáo ngắn: kết quả validator + 3 ví dụ tên bài/nhiệm vụ.
