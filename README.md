# Senapp · Cùng Sen khôn lớn

© 2026 Senapp. Bảo lưu mọi quyền. **Repo riêng tư — không chia sẻ, không sao chép.**

Web app (PWA) dạy kỹ năng sống cho con tiểu học (6–11 tuổi), có linh vật Sen. Trang bán hàng ở `/trang-chu/`, App ở tên miền gốc.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `server.js`, `package.json`, `public/` | **Bản phát hành đang chạy (v16).** Dùng được ngay cho Vibe Code Hosting (Node.js ≥ 18, `npm start`) hoặc chép `public/` lên hosting tĩnh. |
| `src/base-v13/` | Bản gốc v13 — đầu vào của bước build. |
| `src/v15.py`, `src/v16.py`, `src/v14.py` | Các bản vá áp lên bản gốc (tập trung tiểu học → 12 tháng nội dung + danh mục cho ba mẹ + bảng giá → ©, Điều khoản, thu gọn mã). |
| `src/v11/` | Nội dung tuần 1–9 (`week1.json`, `content/*.json`), nhiệm vụ, đặc tả, bộ kiểm tra. |
| `src/y12/` | Nội dung tuần 10–48 (`content/`), kế hoạch 12 chặng (`plan/`), lịch kỹ năng, đặc tả, bộ kiểm tra `validate.py`. |
| `src/legal/` | Trang Điều khoản sử dụng. |
| `src/v13.py`, `src/v11/v11.py`, `src/v11/v12.py` | Các bước vá cũ (đã nằm sẵn trong `base-v13`), giữ lại để tham khảo. |
| `src/hoso.py` | Đóng hồ sơ bằng chứng (SHA-256). |
| `tests/` | Kiểm thử Playwright (e12, e16). |
| `docs/` | Hướng dẫn đưa lên hosting, kế hoạch lợi nhuận, sách số. |

## Build lại

```bash
./build.sh            # ghi đè public/
./build.sh out-test   # build ra thư mục khác để so sánh
SEN_NOMIN=1 ./build.sh out-debug   # không thu gọn/làm rối mã, dễ gỡ lỗi
SEN_VERSION=17 ./build.sh          # tăng số bộ nhớ đệm khi phát hành bản mới
```

Sửa nội dung bài học: chỉnh JSON trong `src/v11/content/` hoặc `src/y12/content/`, chạy `python3 src/y12/validate.py` rồi `./build.sh`.

## Kiểm thử

```bash
(cd public && python3 -m http.server 8768) &
SHOTS=/tmp/ node tests/e16.mjs
```

## Liên hệ

admin.senapp@gmail.com · Zalo/Viber 0975 860 488
