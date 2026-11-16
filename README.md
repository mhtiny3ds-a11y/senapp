# Senapp · Cùng Sen khôn lớn

© 2026 Senapp. Bảo lưu mọi quyền. **Repo riêng tư — không chia sẻ, không sao chép.**

Web app (PWA) dạy kỹ năng sống cho con tiểu học (6–11 tuổi), có linh vật Sen. **Miễn phí 100%, không quảng cáo**, ủng hộ tự nguyện bằng "Mời Sen ly Coffee". Một App trong gia đình [Bamedonghanh](https://mhtiny3ds-a11y.github.io/my_app/), cùng Lumi English, Học Toán Vui, Toán Vui cùng Pi. Trang giới thiệu ở `/trang-chu/`, App ở tên miền gốc.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `server.js`, `package.json`, `public/` | **Bản phát hành đang chạy (v17, miễn phí).** Dùng được ngay cho Vibe Code Hosting (Node.js ≥ 18, `npm start`) hoặc chép `public/` lên hosting tĩnh. |
| `src/base-v13/` | Bản gốc v13 — đầu vào của bước build. |
| `src/v15.py`, `src/v16.py`, `src/v17.py`, `src/v14.py` | Các bản vá theo thứ tự: tập trung tiểu học → 12 tháng nội dung + danh mục cho ba mẹ → **miễn phí 100%, tạo tài khoản gia đình trong App, Mời Sen ly Coffee, sao lưu/khôi phục** → ©, Điều khoản, thu gọn mã. |
| `src/donate/` | Thông tin ủng hộ (MB Bank · 141431319191 · TAO MINH HIEN, cùng tài khoản với 3 app chị em), mã QR gốc, 3 mức Sữa đá / Latte / Cà phê Muối, nội dung "Thank you Sen nha". Sửa `gen.cjs` rồi chạy `node src/donate/gen.cjs > src/donate/donate.json`. |
| `src/v11/` | Nội dung tuần 1–9 (`week1.json`, `content/*.json`), nhiệm vụ, đặc tả, bộ kiểm tra. |
| `src/y12/` | Nội dung tuần 10–48 (`content/`), kế hoạch 12 chặng (`plan/`), lịch kỹ năng, đặc tả, bộ kiểm tra `validate.py`. |
| `src/legal/` | Trang Điều khoản sử dụng. |
| `src/v13.py`, `src/v11/v11.py`, `src/v11/v12.py` | Các bước vá cũ (đã nằm sẵn trong `base-v13`), giữ lại để tham khảo. |
| `src/hoso.py` | Đóng hồ sơ bằng chứng (SHA-256). |
| `tests/` | Kiểm thử Playwright (e12, e16, e17). |
| `docs/` | Hướng dẫn đưa lên hosting, kế hoạch lợi nhuận, sách số. |

## Build lại

```bash
./build.sh            # ghi đè public/
./build.sh out-test   # build ra thư mục khác để so sánh
SEN_NOMIN=1 ./build.sh out-debug   # không thu gọn/làm rối mã, dễ gỡ lỗi
SEN_VERSION=18 ./build.sh          # tăng số bộ nhớ đệm khi phát hành bản mới
```

Sửa nội dung bài học: chỉnh JSON trong `src/v11/content/` hoặc `src/y12/content/`, chạy `python3 src/y12/validate.py` rồi `./build.sh`.

## Kiểm thử

```bash
(cd public && python3 -m http.server 8768) &
SHOTS=/tmp/ node tests/e16.mjs
```

## Liên hệ

admin.senapp@gmail.com · Zalo/Viber 0975 860 488

## Tài khoản & dữ liệu (từ v17)

- Ba mẹ tự tạo **tài khoản gia đình miễn phí** ngay trong App (tên, số điện thoại, mã PIN ba mẹ), rồi thêm tài khoản cho con (mỗi con một PIN, không giới hạn số con) và người lớn khác.
- Dữ liệu chỉ nằm trong trình duyệt của từng máy. **Quản lý tài khoản → Tải file sao lưu**; trên máy mới bấm **Khôi phục từ file sao lưu**.
- Link mở thẳng màn tạo tài khoản: `/?dangky`. Gia đình mẫu: `/?demo` (ba mẹ ID `0901234567`, PIN `9999`).
- Kiểm thử v17 cần thêm `jsqr` và `pngjs` để giải mã thử mã QR: `npm i jsqr pngjs` trong một thư mục rồi chạy `QRDIR=<thư mục đó> node tests/e17.mjs`.
