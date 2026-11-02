# Đưa Senapp v9 lên hosting Tenten

## A. Vibe Code Hosting (ưu tiên)
File: senapp-v9-vibe-code.zip (mã nguồn nằm ngay ở thư mục gốc của file zip: package.json, server.js, public/)

1. Trỏ tên miền về hosting theo hướng dẫn DNS của Tenten.
2. Đăng nhập Vibe Code Hosting → mở plugin "Tenten 1-Click Launch Website".
3. Bấm "Tạo dự án đầu tiên" → chọn tải file zip → kéo thả senapp-v9-vibe-code.zip.
4. Chọn tên miền senapp.com → "Triển khai ngay" → đợi thông báo "đã cài thành công dự án".
5. Bấm AutoSSL để bật https.
6. Kiểm tra: https://senapp.com (App Sen) và https://senapp.com/trang-chu/ (trang bán hàng).
   Kiểm tra nhanh máy chủ: https://senapp.com/healthz phải hiện chữ "ok".

Nếu plugin hỏi lệnh khởi chạy: dùng `npm start` (hoặc file khởi chạy `server.js`). Không cần cài thêm thư viện nào.
Nếu trang vẫn mở bằng http: trong cài đặt dự án, thêm biến môi trường FORCE_HTTPS = 1 rồi bấm "Khởi động lại".

Cập nhật bản mới: "Dừng" → "Xoá" dự án cũ → tải zip mới → "Triển khai". (Khi chuyển sang GitHub: chỉ cần bấm "Đồng bộ".)

## B. Dự phòng: SSD Hosting Linux v2 – Basic
File: senapp-v9-ssd-hosting.zip

1. Trỏ tên miền về hosting, bật SSL miễn phí (AutoSSL / Let's Encrypt) trong trang quản trị.
2. Mở File Manager → thư mục public_html (xoá trang mặc định index nếu có).
3. Tải senapp-v9-ssd-hosting.zip lên public_html → bấm Extract (giải nén) ngay tại đó.
4. Bật "Hiện file ẩn" để chắc chắn có file .htaccess trong public_html.
5. Kiểm tra như mục A bước 6.

## Sau khi lên mạng
- Gửi thử 1 đăng ký trên trang bán hàng để kích hoạt FormSubmit (bấm xác nhận trong mail gửi về mh.senapp@gmail.com).
- Trên điện thoại: mở App Sen → thử "Đưa Sen ra màn hình điện thoại", bật thông báo nhắc học, tải sổ "Cùng Sen khôn lớn".
