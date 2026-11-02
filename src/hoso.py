"""Dong goi ho so bang chung Senapp: cac ban da lam + lich su yeu cau + danh sach SHA-256."""
import os, json, hashlib, shutil, glob, zipfile, datetime
S = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(S, 'ho-so-bang-chung')
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
shutil.rmtree(D, ignore_errors=True)
def put(src, sub, name=None):
    dst = os.path.join(D, sub, name or os.path.basename(src)); os.makedirs(os.path.dirname(dst), exist_ok=True)
    (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
# 1. ban goc nguoi dung tai len
put('/root/.claude/uploads/2645776a-48d7-5467-8bed-0fcf75c00226/183b04ea-Sen_-__ng_d_ng_d_y_k__n_ng_m_m.zip', '01-ban-goc-v4', 'Sen-ung-dung-day-ky-nang-mem-v4.zip')
# 2. cac ban phat hanh
for f in ['senapp-website.zip', 'senapp-ma-nguon.zip', 'senapp.v5.zip', 'senapp.v6.zip', 'senapp.v7.zip', 'senapp.v8.zip', 'senapp.v9.zip'] + \
         [f'senapp-v{n}-vibe-code.zip' for n in range(9, 15)] + ['senapp-v14-ssd-hosting.zip']:
    if os.path.exists(os.path.join(S, f)): put(os.path.join(S, f), '02-cac-ban-phat-hanh')
# 3. noi dung bai hoc & nhiem vu (ban doc duoc)
for f in ['week1.json', 'schedule.json', 'SPEC.md', 'SPEC_MISSIONS.md'] + sorted(glob.glob(os.path.join(S, 'v11', 'content', '*.json'))):
    put(f if os.path.isabs(f) else os.path.join(S, 'v11', f), '03-noi-dung-135-bai-va-nhiem-vu')
# 4. ma nguon cong cu & ban va
for f in sorted(glob.glob(os.path.join(S, '*.py'))) + [os.path.join(S, 'v11', x) for x in ('v11.py', 'v12.py', 'validate.py', 'validate_m.py', 'extract.cjs')] + \
         [os.path.join(S, 'vibe', 'server.js'), os.path.join(S, 'vibe', 'package.json'), os.path.join(S, 'legal', 'dieu-khoan.html')]:
    if os.path.exists(f): put(f, '04-ma-nguon-cong-cu')
# 5. so va huy hieu
for f in ['sticker/out/so-cung-sen-khon-lon.pdf', 'sticker/out/to-huy-hieu-60-tuan.pdf', 'sticker/badges.json', 'sticker/badge_lib.js', 'sticker/book.html', 'sticker/sheets.html', 'sticker/mascot.png']:
    put(os.path.join(S, f), '05-so-va-huy-hieu')
put(os.path.join(S, 'sticker', 'out', 'huy-hieu'), '05-so-va-huy-hieu')
# 6. lich su yeu cau cua chu du an (chi tin nhan do nguoi dung go)
rows = []
for line in open('/root/.claude/projects/-home-user-notebooklm-py/2645776a-48d7-5467-8bed-0fcf75c00226.jsonl', encoding='utf-8'):
    try: e = json.loads(line)
    except Exception: continue
    if e.get('type') != 'user' or (e.get('origin') or {}).get('kind') != 'human': continue
    c = e['message']['content']
    if isinstance(c, list): c = '\n'.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    c = c.strip()
    if c: rows.append((e['timestamp'], c))
os.makedirs(os.path.join(D, '06-lich-su-yeu-cau'), exist_ok=True)
with open(os.path.join(D, '06-lich-su-yeu-cau', 'yeu-cau-cua-chu-du-an.txt'), 'w', encoding='utf-8') as f:
    f.write('LỊCH SỬ YÊU CẦU CỦA CHỦ DỰ ÁN SENAPP (trích nguyên văn từ phiên làm việc với Claude Code)\n')
    f.write('Mã phiên: 2645776a-48d7-5467-8bed-0fcf75c00226 · Giờ theo UTC\n\n')
    for n, (ts, c) in enumerate(rows, 1): f.write(f'--- [{n}] {ts} ---\n{c}\n\n')
# README
open(os.path.join(D, 'DOC-TRUOC.md'), 'w', encoding='utf-8').write(f"""# Hồ sơ bằng chứng dự án Senapp

Lập lúc: {NOW:%d/%m/%Y %H:%M} (giờ Việt Nam)

| Thư mục | Nội dung |
|---|---|
| 01-ban-goc-v4 | Bản dự án gốc (v4) chủ dự án tải lên ngày 07/10/2026 |
| 02-cac-ban-phat-hanh | Các bản đã làm từ v5 đến v14 (gói website/hosting) |
| 03-noi-dung-135-bai-va-nhiem-vu | 135 bài học, 135 nhiệm vụ đời thực (dạng đọc được), lịch kỹ năng 9 tuần, yêu cầu viết nội dung |
| 04-ma-nguon-cong-cu | Mã nguồn các bản vá, máy chủ Node.js, trang Điều khoản sử dụng |
| 05-so-va-huy-hieu | Sổ “Cùng Sen khôn lớn”, tờ 60 huy hiệu, ảnh từng huy hiệu, linh vật Sen |
| 06-lich-su-yeu-cau | Nguyên văn {len(rows)} yêu cầu của chủ dự án theo thời gian — thể hiện ý tưởng và quyết định sáng tạo |

`DANH-SACH-SHA256.txt` liệt kê mọi tệp với mã SHA-256, dung lượng và thời điểm tạo/sửa. Chỉ cần một byte thay đổi là mã SHA-256 khác hẳn, nên danh sách này chứng minh nội dung không bị sửa sau ngày lập.

## Cách lưu bằng chứng
1. Gửi tệp zip này (hoặc tải lên Google Drive rồi gửi link) tới email của chính mình; ghi mã SHA-256 của tệp zip vào nội dung email. Email có dấu thời gian do Google ghi nhận.
2. Lưu thêm một bản trên USB hoặc ổ cứng riêng.
3. Lập vi bằng tại văn phòng thừa phát lại: mang tệp zip, `DANH-SACH-SHA256.txt` in ra giấy và giấy tờ tuỳ thân; thừa phát lại ghi nhận sự tồn tại của các tệp và mã kiểm tra tại thời điểm lập.
4. Dùng hồ sơ này khi nộp đơn đăng ký quyền tác giả (Cục Bản quyền tác giả) và nhãn hiệu “Senapp” (Cục Sở hữu trí tuệ).

Kiểm tra lại mã: Windows `certutil -hashfile <tệp> SHA256` · macOS/Linux `shasum -a 256 <tệp>`.
""")
# danh sach sha256
lines = []
for root, _, files in os.walk(D):
    for fn in sorted(files):
        p = os.path.join(root, fn); rel = os.path.relpath(p, D)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(p), NOW.tzinfo)
        lines.append(f'{h}  {os.path.getsize(p):>10}  {mt:%Y-%m-%d %H:%M:%S}  {rel}')
lines.sort(key=lambda x: x.split('  ')[-1])
open(os.path.join(D, 'DANH-SACH-SHA256.txt'), 'w', encoding='utf-8').write(
    f'DANH SÁCH MÃ KIỂM TRA SHA-256 · Senapp · lập {NOW:%d/%m/%Y %H:%M} (UTC+7)\nSHA-256 | Dung lượng (byte) | Ngày tạo/sửa (UTC+7) | Tệp\n\n' + '\n'.join(lines) + f'\n\nTổng: {len(lines)} tệp\n')
# zip
out = os.path.join(S, f'senapp-ho-so-bang-chung-{NOW:%Y-%m-%d}.zip')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(D):
        for fn in files:
            p = os.path.join(root, fn); z.write(p, os.path.join('senapp-ho-so-bang-chung', os.path.relpath(p, D)))
zh = hashlib.sha256(open(out, 'rb').read()).hexdigest()
open(out + '.sha256.txt', 'w').write(f'{zh}  {os.path.basename(out)}\n')
print(out, os.path.getsize(out), zh, len(lines), 'files', len(rows), 'requests')
