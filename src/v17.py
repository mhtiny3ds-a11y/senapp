"""Senapp v17 (ap dung sau v16, truoc v14): App MIEN PHI 100%, ung ho "Moi Sen ly Coffee",
dong bo voi 3 app trong gia dinh Bamedonghanh (Lumi English, Hoc Toan Vui, Toan Vui cung Pi).
- Bo moi cho thu tien: bang gia, form dang ky + chuyen khoan, thu phi them con, tab Goi.
- Ba me tu tao tai khoan gia dinh mien phi ngay trong App (ten, SDT, PIN ba me), roi tao tai khoan con/nguoi lon.
- Khoi "Moi ly Coffee" giong 3 app chi em: Sua da / Latte / Ca phe Muoi, ma VietQR co san so tien,
  noi dung "Thank you Sen nha", tai ma QR, chep so tai khoan, luu y ung ho tu nguyen.
- Sao luu / khoi phuc du lieu bang file (du lieu chi nam tren may cua gia dinh).
- Luu y & mien tru trach nhiem 6 muc; bo huy hieu "Da dang ky Bo Cong Thuong"; lien ket ve trang Bamedonghanh.
Dung: python3 v17.py <thu muc ban build>"""
import json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
HUB = 'https://mhtiny3ds-a11y.github.io/my_app/'
DON = json.load(open(os.path.join(HERE, 'donate', 'donate.json'), encoding='utf-8'))
MASCOT_APP = 'f37ca7cb-1419-41a5-be40-151490144349'
MASCOT_LAND = '71007c86-dc57-46d4-a073-d094f0520fee'


def sub(h, a, b, n=1):
    c = h.count(a); assert c == n, (a[:140], c); return h.replace(a, b)


# ------------------------------------------------------------ thu vien ung ho (dung chung)
DONATE_LIB = '''
const DONATE = %s, DONATE_NOTE = %s;
const DONATE_LEVELS = %s;
const DQR = {};
/* Ve the ma QR (ten loai cafe, nguoi nhan; khong in so tien) ra anh PNG de hien thi va tai ve */
const donateImage = (k) => {
  const lv = DONATE_LEVELS[k] || DONATE_LEVELS[0];
  if (DQR[lv.slug]) return DQR[lv.slug];
  try {
    const n = lv.qr.length, cell = Math.floor(440 / (n + 8)), qs = cell * (n + 8);
    const W = 520, H = qs + 250, cv = document.createElement('canvas'); cv.width = W; cv.height = H; const x = cv.getContext('2d');
    x.fillStyle = '#FFF1E6'; x.fillRect(0, 0, W, H);
    x.fillStyle = '#fff'; x.beginPath(); if (x.roundRect) x.roundRect(20, 20, W - 40, H - 40, 24); else x.rect(20, 20, W - 40, H - 40); x.fill();
    x.fillStyle = '#C8102E'; x.font = '800 30px "Baloo 2", sans-serif'; x.textAlign = 'center'; x.fillText('Mời Sen ly Coffee ☕', W / 2, 66);
    const ox = (W - qs) / 2, oy = 84; x.fillStyle = '#fff'; x.fillRect(ox, oy, qs, qs); x.fillStyle = '#111';
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (lv.qr[r].charCodeAt(c) === 49) x.fillRect(ox + (c + 4) * cell, oy + (r + 4) * cell, cell, cell);
    x.fillStyle = '#2E9E7E'; x.font = '800 40px "Baloo 2", sans-serif'; x.fillText(lv.name, W / 2, oy + qs + 46);
    x.fillStyle = '#221A15'; x.font = '800 22px sans-serif'; x.fillText(DONATE.name, W / 2, oy + qs + 82);
    x.fillStyle = '#6D5B4B'; x.font = '700 18px sans-serif'; x.fillText(DONATE.bank + ' · ' + DONATE.acct, W / 2, oy + qs + 110);
    x.font = '700 15px sans-serif'; x.fillText('Nội dung: ' + DONATE_NOTE + ' · Ủng hộ tự nguyện', W / 2, oy + qs + 136);
    return (DQR[lv.slug] = cv.toDataURL('image/png'));
  } catch (e) { return ''; }
};
/* style="" cua mau tach theo dau ';' nen khong dung data URL (co ';base64') trong background: doi sang blob URL */
const DQRB = {};
const donateUrl = (k) => { const lv = DONATE_LEVELS[k] || DONATE_LEVELS[0]; if (DQRB[lv.slug]) return DQRB[lv.slug];
  const d = donateImage(k); if (!d) return '';
  try { const bin = atob(d.split(',')[1]), u = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    return (DQRB[lv.slug] = URL.createObjectURL(new Blob([u], { type: 'image/png' }))); } catch (e) { return ''; } };
const donateBox = (k, w) => { const n = (DONATE_LEVELS[k] || DONATE_LEVELS[0]).qr.length, qs = Math.floor(440 / (n + 8)) * (n + 8);
  return 'width:100%%;max-width:' + w + 'px;align-self:center;aspect-ratio:520/' + (qs + 250) + ';border-radius:18px;border:2px solid #F0E4D4;background:#FFF1E6 center/contain no-repeat url(' + donateUrl(k) + ')'; };
const donateSave = (k) => { const lv = DONATE_LEVELS[k] || DONATE_LEVELS[0], a = document.createElement('a');
  a.href = donateImage(k); a.download = 'ma-qr-moi-sen-coffee-' + lv.slug + '.png'; document.body.appendChild(a); a.click(); a.remove(); };
const donateCopy = () => { try { return navigator.clipboard.writeText(DONATE.acct).then(() => true, () => false); } catch (e) { return Promise.resolve(false); } };
const DONATE_HOW = 'Quét mã bằng ứng dụng ngân hàng, hoặc bấm Tải mã QR rồi mở ứng dụng ngân hàng → chọn quét QR → chọn ảnh từ thư viện. Trên iPhone, nếu ảnh mở ra trang mới, nhấn giữ ảnh → Lưu vào Ảnh.';
const DONATE_WARN = 'Lưu ý: việc mời cafe (ủng hộ) là hoàn toàn tự nguyện, mang tính cho tặng, không phải tiền mua sản phẩm hay dịch vụ. Mời hay không đều dùng ứng dụng như nhau, không kèm quyền lợi, không phát sinh hợp đồng, nghĩa vụ hay trách nhiệm pháp lý nào giữa hai bên và không hoàn lại. Ba mẹ vui lòng kiểm tra tên người nhận và số tiền hiện trong ứng dụng ngân hàng trước khi xác nhận chuyển.';
''' % (json.dumps(DON['donate'], ensure_ascii=False), json.dumps(DON['note'], ensure_ascii=False),
       json.dumps([{'name': l['name'], 'slug': l['slug'], 'qr': l['qr']} for l in DON['levels']], ensure_ascii=False, separators=(',', ':')))

DISCLAIMER = [
    ('1. Về ứng dụng.', 'Senapp là ứng dụng cá nhân, độc lập, miễn phí hoàn toàn, không quảng cáo, không bán hàng, không thu phí dưới bất kỳ hình thức nào. Ứng dụng không đại diện, không liên kết và không được bảo trợ bởi bất kỳ tổ chức, cơ quan hay đơn vị nào.'),
    ('2. Về nội dung bài học.', 'Bài học, câu chuyện, câu hỏi và nhiệm vụ do Senapp tự biên soạn, chỉ mang tính tham khảo, có thể còn sai sót, không thay thế giáo viên, chuyên gia tâm lý hay sự dạy dỗ của gia đình. Ứng dụng được cung cấp “nguyên trạng”, không cam kết về kết quả. Mọi nhiệm vụ đời thực cần có người lớn giám sát phù hợp.'),
    ('3. Về sao thưởng.', 'Quy đổi “1 sao = 1.000đ” chỉ là gợi ý để ba mẹ tự thỏa thuận và tự thưởng cho con trong gia đình. Ứng dụng không giữ tiền, không chuyển tiền, không phát sinh nghĩa vụ tài chính hay ràng buộc nào giữa ứng dụng với người dùng.'),
    ('4. Về ủng hộ (donate).', 'Việc ủng hộ là hoàn toàn tự nguyện, mang tính chất cho tặng, không phải tiền mua sản phẩm hay dịch vụ. Ủng hộ hay không đều dùng ứng dụng như nhau; người ủng hộ không nhận thêm quyền lợi, không có hợp đồng, không phát sinh nghĩa vụ hay trách nhiệm pháp lý nào giữa hai bên, và khoản ủng hộ không được hoàn lại. Vui lòng chỉ ủng hộ trong khả năng của mình và tự kiểm tra kỹ thông tin trước khi chuyển.'),
    ('5. Về dữ liệu.', 'Tài khoản, tiến độ và sao chỉ lưu trong trình duyệt trên máy của gia đình. Ứng dụng không gửi đi và không lưu dữ liệu học của con trên máy chủ nào. Ba mẹ tự chịu trách nhiệm sao lưu; dữ liệu có thể mất khi xóa dữ liệu trình duyệt.'),
    ('6. Giới hạn trách nhiệm.', 'Người phát triển không chịu trách nhiệm đối với bất kỳ thiệt hại trực tiếp hay gián tiếp nào phát sinh từ việc sử dụng ứng dụng. Việc sử dụng ứng dụng đồng nghĩa với việc ba mẹ đã đọc và đồng ý với các lưu ý trên.'),
]


def disclaimer_html(size='12.5px'):
    return ''.join(f'<p style="margin:0 0 8px;font-size:{size};line-height:1.55"><b>{a}</b> {b}</p>' for a, b in DISCLAIMER)


# ------------------------------------------------------------ trang chu
FREE_SECTION = '''<section id="mien-phi" style="background:#FFF;padding:72px 0">
  <div style="max-width:1160px;margin:0 auto;padding:0 clamp(16px,4vw,40px)">
    <div style="text-align:center;max-width:800px;margin:0 auto 30px">
      <div style="display:inline-flex;flex-wrap:wrap;justify-content:center;gap:6px 10px;background:#E3F4EC;color:#1F5E4A;border-radius:999px;padding:7px 16px;font-size:13.5px;font-weight:800;margin-bottom:14px">🎁 Miễn phí 100% <span style="opacity:.45">•</span> Không quảng cáo <span style="opacity:.45">•</span> Không cần cài đặt</div>
      <h2 style="font-family:'Baloo 2',cursive;font-weight:800;font-size:clamp(30px,3.8vw,48px);line-height:1.08;margin:0">Không học phí. Không quảng cáo. <span style="color:#C8102E">Không bán gì cả.</span></h2>
      <p style="font-size:17px;line-height:1.7;color:#5C4B3C;margin:18px auto 0;max-width:62ch">Trọn bộ 9 kỹ năng, <strong>240 bài học và 240 nhiệm vụ đời thực</strong> cho 48 tuần. Bao nhiêu con cũng được, mỗi con một lộ trình đúng tuổi. Ba mẹ tự sửa, thêm, bớt bài cho hợp với con.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:16px;max-width:1000px;margin:0 auto">
      <div style="border-radius:28px;background:#FFF8EF;border:2px solid #F0E4D4;padding:22px;display:flex;flex-direction:column;gap:8px">
        <div style="width:44px;height:44px;border-radius:14px;background:#C8102E;color:#FFF;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:22px">1</div>
        <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:20px">Mở App Sen</div>
        <div style="font-size:14.5px;line-height:1.6;color:#5C4B3C">Chạy ngay trên trình duyệt điện thoại, máy tính bảng hay máy tính. Không cần tải từ kho ứng dụng.</div>
      </div>
      <div style="border-radius:28px;background:#FFF8EF;border:2px solid #F0E4D4;padding:22px;display:flex;flex-direction:column;gap:8px">
        <div style="width:44px;height:44px;border-radius:14px;background:#F2A93B;color:#221A15;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:22px">2</div>
        <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:20px">Tạo tài khoản gia đình</div>
        <div style="font-size:14.5px;line-height:1.6;color:#5C4B3C">Ba mẹ nhập tên, số điện thoại và đặt mã PIN 4 số. Mất chưa tới một phút, hoàn toàn miễn phí.</div>
      </div>
      <div style="border-radius:28px;background:#FFF8EF;border:2px solid #F0E4D4;padding:22px;display:flex;flex-direction:column;gap:8px">
        <div style="width:44px;height:44px;border-radius:14px;background:#2E9E7E;color:#FFF;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:22px">3</div>
        <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:20px">Thêm con, con học ngay</div>
        <div style="font-size:14.5px;line-height:1.6;color:#5C4B3C">Mỗi con một mã PIN, một lộ trình. Ông bà, người thân cũng có thể có tài khoản riêng để cùng xác nhận nhiệm vụ.</div>
      </div>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:28px">
      <a href="../?dangky" style="background:#C8102E;color:#FFF;border-radius:18px;padding:15px 26px;font-family:'Baloo 2',cursive;font-weight:700;font-size:19px;box-shadow:0 6px 0 #8F0B20">Tạo tài khoản gia đình miễn phí</a>
      <a href="../?demo" style="background:#FFF;color:#C8102E;border:2px solid #C8102E;border-radius:18px;padding:13px 22px;font-family:'Baloo 2',cursive;font-weight:700;font-size:18px">Xem gia đình mẫu</a>
    </div>
    <div style="max-width:760px;margin:30px auto 0;border-radius:24px;background:#FFF1E6;padding:16px 20px;display:flex;gap:14px;align-items:center;flex-wrap:wrap">
      <div style="font-size:30px;line-height:1">💛</div>
      <div style="flex:1;min-width:220px;font-size:14.5px;line-height:1.6;color:#3A2E24">Senapp là một App trong gia đình <strong>Bamedonghanh</strong>, cùng <strong>Lumi English</strong>, <strong>Học Toán Vui</strong> và <strong>Toán Vui cùng Pi</strong>. Tất cả đều miễn phí cho các bạn nhỏ tiểu học.</div>
      <a href="__HUB__" target="_blank" rel="noopener" style="font-weight:800;color:#C8102E;white-space:nowrap">Xem cả 4 App →</a>
    </div>
  </div>
</section>'''.replace('__HUB__', HUB)

DONATE_SECTION = '''<section id="ung-ho" style="padding:64px 0">
    <div style="border-radius:40px;background:#1BA39C;padding:clamp(20px,4vw,48px);position:relative">
      <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:24px;color:#FFF">
        <img src="__M__" alt="" style="width:84px;height:84px;object-fit:contain;flex:none;animation:senBob 3.2s ease-in-out infinite">
        <div style="flex:1;min-width:240px">
          <h2 style="font-family:'Baloo 2',cursive;font-weight:800;font-size:clamp(24px,3vw,38px);line-height:1.12;margin:0">Mời ly Coffee để Sen có thêm sức mạnh đồng hành và phát triển cùng các con nha ba mẹ ☕</h2>
          <div style="font-size:15px;line-height:1.6;opacity:.95;margin-top:8px">Senapp miễn phí 100% và sẽ luôn miễn phí. Nếu Sen giúp được gia đình mình, ba mẹ mời Sen một ly cà phê nhé. Không mời vẫn dùng như nhau.</div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:18px">
        <div style="background:#FFF;border-radius:28px;padding:22px;display:flex;flex-direction:column;gap:14px;align-items:stretch">
          <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px" role="radiogroup" aria-label="Chọn ly cafe">
            <sc-for list="{{ donLevels }}" as="d" hint-placeholder-count="3">
              <div sc-camel-on-click="{{ d.pick }}" role="radio" aria-checked="{{ d.on }}" style="{{ d.style }}">{{ d.name }}</div>
            </sc-for>
          </div>
          <div role="img" aria-label="{{ donAlt }}" style="{{ donImgStyle }}"></div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center">
            <div sc-camel-on-click="{{ donSave }}" style="cursor:pointer;background:#2E9E7E;color:#FFF;border-radius:14px;padding:11px 16px;font-weight:800;font-size:14.5px">⬇️ Tải mã QR</div>
            <div sc-camel-on-click="{{ donCopy }}" style="cursor:pointer;background:#FFF;color:#221A15;border:2px solid #F0E4D4;border-radius:14px;padding:9px 14px;font-weight:800;font-size:14.5px">📋 Chép số tài khoản</div>
          </div>
          <sc-if value="{{ donMsgShow }}" hint-placeholder-val="{{ false }}">
            <div style="text-align:center;font-size:13.5px;font-weight:700;color:#1F5E4A;background:#E3F4EC;border-radius:12px;padding:8px 12px">{{ donMsg }}</div>
          </sc-if>
        </div>
        <div style="background:#FFF;border-radius:28px;padding:22px;display:flex;flex-direction:column;gap:12px">
          <div style="text-align:center">
            <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:22px">__NAME__</div>
            <div style="font-size:14.5px;font-weight:700;color:#5C4B3C">__BANK__ · <span style="user-select:all">__ACCT__</span></div>
            <div style="font-size:14px;font-weight:700;color:#5C4B3C;margin-top:2px">Nội dung chuyển khoản: <strong style="color:#C8102E">__NOTE__</strong></div>
          </div>
          <div style="font-size:13.5px;line-height:1.6;color:#5C4B3C">{{ donHow }}</div>
          <div style="font-size:13px;line-height:1.6;color:#6D5B4B;background:#FFF8EF;border-radius:16px;padding:12px 14px">{{ donWarn }}</div>
          <div style="border-top:1.5px dashed #F0E4D4;padding-top:12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap">
            <div style="flex:1;min-width:200px"><div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:17px">Lan tỏa Senapp nha ba mẹ 💛</div><div style="font-size:13.5px;color:#5C4B3C;font-weight:600">Ba mẹ hãy đồng hành cùng con 7 phút mỗi ngày nhé.</div></div>
            <div sc-camel-on-click="{{ share }}" style="cursor:pointer;background:#F2A93B;color:#221A15;border-radius:14px;padding:11px 16px;font-weight:800;font-size:14.5px">🔗 Chia sẻ cho bạn bè</div>
          </div>
        </div>
      </div>
    </div>
  </section>'''.replace('__M__', MASCOT_LAND).replace('__NAME__', DON['donate']['name']).replace('__BANK__', DON['donate']['bank']).replace('__ACCT__', DON['donate']['acct']).replace('__NOTE__', DON['note'])

LAND_FAQ = '''const FAQ = [
  ['Senapp có thật sự miễn phí không?', 'Có. Senapp miễn phí 100%: trọn bộ 9 kỹ năng, 240 bài học, 240 nhiệm vụ đời thực, không quảng cáo, không bán hàng, không thu phí dưới bất kỳ hình thức nào. Ba mẹ muốn thì mời Sen một ly cà phê; không mời vẫn dùng như nhau.'],
  __KEEP0__,
  ['Bắt đầu thế nào?', 'Mở App Sen, bấm “Tạo tài khoản gia đình”, nhập tên, số điện thoại và đặt mã PIN 4 số cho ba mẹ. Sau đó vào Quản lý tài khoản, thêm tài khoản cho con (mỗi con một mã PIN), cho ba/mẹ còn lại và ông bà nếu cần. Con đăng nhập bằng mã PIN của mình là học được ngay.'],
  ['Một tài khoản dùng được cho mấy con?', 'Bao nhiêu con cũng được, không mất thêm phí. Mỗi con một mã PIN, một lộ trình đúng tuổi. Ông bà, người thân cũng có thể có tài khoản người lớn riêng để cùng xác nhận nhiệm vụ.'],
  __KEEP1__,
  ['Mời Sen ly cà phê (ủng hộ) thế nào?', 'Ở mục “Mời ly Coffee” trên trang này và tab “Ủng hộ” trong App có mã VietQR: chọn Sữa đá, Latte hoặc Cà phê Muối rồi quét bằng ứng dụng ngân hàng. Việc ủng hộ là hoàn toàn tự nguyện, mang tính cho tặng, không phải tiền mua sản phẩm hay dịch vụ, không kèm quyền lợi và không hoàn lại.'],
  ['Dữ liệu của con lưu ở đâu?', 'Tài khoản, tiến độ và sao chỉ lưu trong trình duyệt trên máy của gia đình, không gửi lên máy chủ. Senapp không thu vị trí, khuôn mặt hay giọng nói, không bán dữ liệu, không quảng cáo. Ba mẹ nên vào Quản lý tài khoản → Tải file sao lưu định kỳ, và dùng file này khi chuyển sang máy khác.'],
  ['Làm sao để Sen đến với nhiều gia đình hơn?', 'Ba mẹ chia sẻ link Senapp cho bạn bè, nhóm phụ huynh lớp con. Mỗi gia đình đồng hành cùng con 7 phút mỗi ngày là Sen vui lắm rồi 💛'],
];'''


def landing(t):
    t = sub(t, '<a class="lp-navlink" href="#gia" style="font-size:14px;font-weight:600;color:#5C4B3C;padding:8px 10px">Học phí</a>',
               '<a class="lp-navlink" href="#ung-ho" style="font-size:14px;font-weight:600;color:#5C4B3C;padding:8px 10px">Mời Sen ly Coffee ☕</a>')
    t = sub(t, '<a href="#dang-ky" class="lp-regbtn" style="background:#C8102E;color:#FFF;border-radius:99px;padding:10px 20px;font-weight:700;font-size:14px;white-space:nowrap">Đăng ký</a>',
               '<a href="../?dangky" class="lp-regbtn" style="background:#C8102E;color:#FFF;border-radius:99px;padding:10px 20px;font-weight:700;font-size:14px;white-space:nowrap">Dùng miễn phí</a>')
    t = sub(t, '<a href="#dang-ky" style="background:#C8102E;color:#FFF;border-radius:18px;padding:15px 26px;font-family:\'Baloo 2\',cursive;font-weight:700;font-size:19px;box-shadow:0 6px 0 #8F0B20">Đăng ký cho con</a>',
               '<a href="../?dangky" style="background:#C8102E;color:#FFF;border-radius:18px;padding:15px 26px;font-family:\'Baloo 2\',cursive;font-weight:700;font-size:19px;box-shadow:0 6px 0 #8F0B20">Dùng miễn phí cho con</a>')
    t = sub(t, '<p style="font-size:13px;color:#8B7867;margin:18px 0 0"><a href="../?demo" style="color:#2E9E7E;font-weight:700">Dùng thử miễn phí</a> · trọn năm 499.000đ · không tự động gia hạn</p>',
               '<p style="display:inline-flex;flex-wrap:wrap;gap:4px 10px;font-size:13.5px;font-weight:800;color:#1F5E4A;background:#E3F4EC;border-radius:999px;padding:7px 14px;margin:18px 0 0">🎁 Miễn phí 100% <span style="opacity:.45">•</span> Không quảng cáo <span style="opacity:.45">•</span> Không cần cài đặt</p>')
    # bang gia -> mien phi; form dang ky -> moi ly coffee
    a = t.index('<section id="gia"'); b = t.index('</section>', a) + len('</section>')
    t = t[:a] + FREE_SECTION + t[b:]
    a = t.index('<section id="dang-ky"'); b = t.index('</section>', a) + len('</section>')
    t = t[:a] + DONATE_SECTION + t[b:]
    # chan trang
    a = t.index('<div style="font-size:12.5px;font-weight:700;color:#8B7867;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px">Thanh toán</div>')
    b = t.index('</div>', t.index('TAO MINH HIEN', a)) + len('</div>')
    t = t[:a] + ('<div style="font-size:12.5px;font-weight:700;color:#8B7867;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px">Ủng hộ</div>\n'
                 '      <div style="font-size:14px;line-height:1.7"><a href="#ung-ho" style="font-weight:700">Mời Sen ly Coffee ☕</a><br>' + DON['donate']['bank'] + ' · ' + DON['donate']['acct'] + ' · ' + DON['donate']['name'] + '</div>') + t[b:]
    a = t.index('<div style="display:inline-flex;align-items:center;gap:10px;background:#FFF;border:1.5px solid #1F5FAD')
    b = t.index('Bộ Công Thương</div>', a); b = t.index('</div>', b + len('Bộ Công Thương</div>')) + len('</div>')
    t = t[:a] + ('<a href="' + HUB + '" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:8px;background:#FFF;border:1.5px solid #F0E4D4;border-radius:12px;padding:8px 14px;font-weight:800;font-size:13.5px;color:#C8102E">'
                 'Một App của Bamedonghanh <span style="color:#E8517A">♥</span></a>') + t[b:]
    assert 'Công Thương' not in t
    # FAQ
    m = re.search(r'const FAQ = \[\n(.*?)\n\];', t, re.S)
    rows = m.group(1).split('\n')
    keep0 = next(r for r in rows if 'Con tôi cài app nào cũng bỏ' in r).strip().rstrip(',')
    keep1 = next(r for r in rows if 'Con tôi 6 tuổi, đọc chưa tốt' in r).strip().rstrip(',')
    t = t[:m.start()] + LAND_FAQ.replace('__KEEP0__', keep0).replace('__KEEP1__', keep1) + t[m.end():]
    # logic
    t = sub(t, "const PLANS = [", DONATE_LIB + "const SHARE_TEXT = 'Senapp: App kỹ năng sống miễn phí cho con tiểu học. Học 7 phút, làm một việc thật. Ba mẹ đồng hành cùng con nhé!';\nconst PLANS = [")
    t = sub(t, "state = { faqOpen: 0, plan: 1,", "state = { faqOpen: 0, donIdx: 1, donMsg: '', plan: 1,")
    t = sub(t, "pickClassic: () => this.setState({ plan: 0 }), pickPremium: () => this.setState({ plan: 1 }),",
            "pickClassic: () => this.setState({ plan: 0 }), pickPremium: () => this.setState({ plan: 1 }),\n"
            "      donLevels: DONATE_LEVELS.map((v, k) => ({ name: v.name, on: String(st.donIdx === k), pick: () => this.setState({ donIdx: k, donMsg: '' }),\n"
            "        style: 'cursor:pointer;text-align:center;border-radius:14px;padding:10px 6px;font-weight:800;font-size:14px;' + (st.donIdx === k ? 'background:#2E9E7E;color:#FFF;border:2px solid #2E9E7E' : 'background:#FFF8EF;color:#221A15;border:2px solid #F0E4D4') })),\n"
            "      donImgStyle: donateBox(st.donIdx, 280), donAlt: 'Mã QR mời Sen ly ' + DONATE_LEVELS[st.donIdx].name + ': ' + DONATE.name + ', ' + DONATE.bank + ', số tài khoản ' + DONATE.acct,\n"
            "      donSave: () => donateSave(st.donIdx), donHow: DONATE_HOW, donWarn: DONATE_WARN,\n"
            "      donCopy: () => donateCopy().then(ok => this.setState({ donMsg: ok ? 'Đã chép số tài khoản ' + DONATE.acct : 'Ba mẹ chọn và chép số tài khoản ' + DONATE.acct + ' giúp Sen nhé.' })),\n"
            "      donMsgShow: !!st.donMsg, donMsg: st.donMsg,\n"
            "      share: () => { const url = location.origin + location.pathname; try { if (navigator.share) return navigator.share({ title: 'Senapp', text: SHARE_TEXT, url }).catch(() => {}); } catch (e) {}\n"
            "        try { navigator.clipboard.writeText(SHARE_TEXT + ' ' + url).then(() => this.setState({ donMsg: 'Đã chép link Senapp, ba mẹ dán gửi bạn bè nhé!' })); } catch (e) {} },")
    t = sub(t, "'Chọn gói 6 hoặc 12 tháng'", "'Tạo tài khoản gia đình miễn phí'")
    for bad in ('499.000', '299.000', 'Học phí', 'Đăng ký cho con', '#dang-ky', 'Thanh toán</div>', 'gia đình mẫu trước khi đăng ký'):
        assert bad not in t, bad
    return t


# ------------------------------------------------------------ App
REG_FORM = '''<div style="border-radius:22px;background:#FFF;border:2px solid #F2A93B;padding:14px;display:flex;flex-direction:column;gap:9px">
            <div style="display:flex;align-items:center;gap:8px">
              <div style="flex:1;font-family:'Baloo 2',cursive;font-weight:800;font-size:19px;color:#221A15;line-height:1.2">{{ rgFormTitle }}</div>
              <div style="background:#2E9E7E;color:#FFF;border-radius:99px;padding:4px 10px;font-size:11px;font-weight:800;flex:none">{{ rgFreeBadge }}</div>
            </div>
            <input value="{{ rgName }}" onChange="{{ onRgName }}" placeholder="{{ rgNamePh }}" autocomplete="name" style="border:1.5px solid #EFE3D2;background:#FFFBF4;border-radius:14px;padding:12px;font-size:16px;color:#221A15;width:100%;box-sizing:border-box" />
            <input value="{{ rgPhone }}" onChange="{{ onRgPhone }}" placeholder="{{ rgPhonePh }}" inputmode="tel" autocomplete="tel" style="border:1.5px solid #EFE3D2;background:#FFFBF4;border-radius:14px;padding:12px;font-size:16px;color:#221A15;width:100%;box-sizing:border-box" />
            <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px">
              <input type="password" value="{{ rgPin }}" onChange="{{ onRgPin }}" placeholder="{{ rgPinPh }}" inputmode="numeric" autocomplete="new-password" style="border:1.5px solid #EFE3D2;background:#FFFBF4;border-radius:14px;padding:12px;font-size:16px;color:#221A15;width:100%;box-sizing:border-box;letter-spacing:4px" />
              <input type="password" value="{{ rgPin2 }}" onChange="{{ onRgPin2 }}" placeholder="{{ rgPin2Ph }}" inputmode="numeric" autocomplete="new-password" style="border:1.5px solid #EFE3D2;background:#FFFBF4;border-radius:14px;padding:12px;font-size:16px;color:#221A15;width:100%;box-sizing:border-box;letter-spacing:4px" />
            </div>
            <div onClick="{{ rgToggleAgree }}" style="{{ rgAgreeRow }}">
              <div style="{{ rgAgreeBox }}">{{ rgAgreeTick }}</div>
              <div style="flex:1;font-size:12px;line-height:1.45;color:#5C4B3C">{{ rgAgreeText }} <a href="dieu-khoan/" target="_blank" rel="noopener" style="font-weight:700;color:#C8102E">{{ rgTermsLink }}</a></div>
            </div>
            <sc-if value="{{ rgHasErr }}" hint-placeholder-val="{{ false }}">
              <div style="background:#FFE3E6;color:#8F0B20;border-radius:12px;padding:9px 12px;font-size:12.5px;font-weight:600;line-height:1.45">{{ rgErr }}</div>
            </sc-if>
            <div onClick="{{ doFreeRegister }}" style="height:54px;border-radius:18px;background:#C8102E;color:#FFF;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:19px;cursor:pointer;box-shadow:0 6px 0 #8F0B20;flex:none">{{ rgCta }}</div>
          </div>
          '''

RESTORE_LINE = '''<label style="text-align:center;font-size:12.5px;font-weight:700;color:#5C4B3C;cursor:pointer;padding:2px">{{ rgRestore }}<input type="file" accept="application/json,.json" onChange="{{ bkImport }}" style="display:none" /></label>
          '''

BACKUP_CARD = '''<div style="border-radius:20px;background:#FFF;border:1.5px solid #EFE3D2;padding:14px;display:flex;flex-direction:column;gap:8px">
                <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:16px;color:#221A15">{{ bkTitle }}</div>
                <div style="font-size:12px;color:#8B7867;line-height:1.5">{{ bkSub }}</div>
                <div style="display:flex;gap:8px;flex-wrap:wrap">
                  <div onClick="{{ bkExport }}" style="cursor:pointer;background:#2E9E7E;color:#FFF;border-radius:12px;padding:10px 14px;font-weight:700;font-size:13px">{{ bkExportLabel }}</div>
                  <label style="cursor:pointer;background:#FFF;color:#221A15;border:1.5px solid #EFE3D2;border-radius:12px;padding:9px 13px;font-weight:700;font-size:13px">{{ bkImportLabel }}<input type="file" accept="application/json,.json" onChange="{{ bkImport }}" style="display:none" /></label>
                </div>
                <sc-if value="{{ bkMsgShow }}" hint-placeholder-val="{{ false }}">
                  <div style="background:#E3F4EC;color:#1F5E4A;border-radius:12px;padding:9px 12px;font-size:12.5px;font-weight:600;line-height:1.45">{{ bkMsg }}</div>
                </sc-if>
              </div>
              '''

DONATE_SCREEN = '''<div data-screen-label="09 Plan" style="display:flex;flex-direction:column;gap:12px;animation:senSlide .3s ease">
            <div style="border-radius:22px;padding:15px;background:#DDF0E6;border:1.5px solid #B9DFCB">
              <div style="font-family:'Baloo 2',cursive;font-size:18px;font-weight:800;color:#1B6B4F">{{ dnFreeTitle }}</div>
              <div style="font-size:12.5px;color:#3F7A63;line-height:1.55;margin-top:4px">{{ dnFreeSub }}</div>
            </div>
            <div style="border-radius:22px;padding:15px;background:#FFF;border:1.5px solid #EFE3D2;display:flex;flex-direction:column;gap:10px">
              <div style="display:flex;gap:10px;align-items:center">
                <img src="__M__" alt="" style="width:52px;height:52px;object-fit:contain;flex:none">
                <div style="flex:1;min-width:0;font-family:'Baloo 2',cursive;font-weight:800;font-size:16px;line-height:1.3;color:#221A15">{{ dnTitle }}</div>
              </div>
              <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px">
                <sc-for list="{{ dnLevels }}" as="dl" hint-placeholder-count="3">
                  <div onClick="{{ dl.pick }}" style="{{ dl.style }}">{{ dl.name }}</div>
                </sc-for>
              </div>
              <div role="img" aria-label="{{ dnAlt }}" style="{{ dnImgStyle }}"></div>
              <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
                <div onClick="{{ dnSave }}" style="cursor:pointer;background:#2E9E7E;color:#FFF;border-radius:12px;padding:10px 14px;font-weight:700;font-size:13px">⬇️ {{ dnSaveLabel }}</div>
                <div onClick="{{ dnCopy }}" style="cursor:pointer;background:#FFF;color:#221A15;border:1.5px solid #EFE3D2;border-radius:12px;padding:9px 13px;font-weight:700;font-size:13px">📋 {{ dnCopyLabel }}</div>
              </div>
              <sc-if value="{{ dnMsgShow }}" hint-placeholder-val="{{ false }}">
                <div style="text-align:center;background:#E3F4EC;color:#1F5E4A;border-radius:12px;padding:8px 12px;font-size:12.5px;font-weight:700">{{ dnMsg }}</div>
              </sc-if>
              <div style="text-align:center;font-size:12.5px;color:#5C4B3C;line-height:1.5"><b style="font-size:14px;color:#221A15">__NAME__</b><br>__BANK__ · <span style="user-select:all;font-weight:700">__ACCT__</span><br>{{ dnNoteLabel }} <b>__NOTE__</b></div>
              <div style="font-size:11.5px;color:#8B7867;line-height:1.55">{{ dnHow }}</div>
              <div style="font-size:11.5px;color:#6D5B4B;line-height:1.55;background:#FFF8EF;border-radius:12px;padding:10px 12px">{{ dnWarn }}</div>
            </div>
            <div style="border-radius:22px;padding:15px;background:#FFF8E6;display:flex;flex-direction:column;gap:8px">
              <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:16px;color:#221A15">{{ dnShareTitle }}</div>
              <div style="font-size:12.5px;color:#5C4B3C;font-weight:600">{{ dnShareSub }}</div>
              <div onClick="{{ dnShare }}" style="align-self:flex-start;cursor:pointer;background:#F2A93B;color:#221A15;border-radius:12px;padding:10px 14px;font-weight:700;font-size:13px">🔗 {{ dnShareBtn }}</div>
            </div>
            <a href="__HUB__" target="_blank" rel="noopener" style="border-radius:22px;padding:13px 15px;background:#FFF;border:1.5px solid #EFE3D2;display:flex;gap:10px;align-items:center;text-decoration:none;color:#221A15">
              <div style="font-size:24px">💛</div>
              <div style="flex:1;min-width:0;font-size:12.5px;line-height:1.5">{{ dnFamily }}</div>
              <div style="font-weight:800;color:#C8102E;font-size:13px">›</div>
            </a>
            <details style="border-radius:22px;padding:13px 15px;background:#FFF;border:1.5px solid #EFE3D2">
              <summary style="font-weight:800;font-size:13.5px;cursor:pointer;color:#221A15">📜 Lưu ý &amp; miễn trừ trách nhiệm</summary>
              <div style="margin-top:10px;color:#5C4B3C">__DISC__</div>
            </details>
          </div>'''.replace('__M__', MASCOT_APP).replace('__HUB__', HUB).replace('__NAME__', DON['donate']['name']).replace('__BANK__', DON['donate']['bank']).replace('__ACCT__', DON['donate']['acct']).replace('__NOTE__', DON['note']).replace('__DISC__', disclaimer_html())

APP_QA = '''  [['Senapp có mất phí không?','Does Senapp cost anything?'],
   ['Không. Senapp miễn phí 100%: trọn bộ 9 kỹ năng, 240 bài, 240 nhiệm vụ, bao nhiêu con cũng được, không quảng cáo, không bán hàng, không thu phí dưới bất kỳ hình thức nào.',
    'No. Senapp is 100% free: all 9 skills, 240 lessons, 240 missions, as many children as you like, no ads, nothing to buy.']],
  [['Mời Sen ly cà phê (ủng hộ) thế nào?','How do I buy Sen a coffee?'],
   ['Vào tab “Ủng hộ”, chọn Sữa đá, Latte hoặc Cà phê Muối rồi quét mã VietQR bằng ứng dụng ngân hàng (nội dung “Thank you Sen nha”). Việc ủng hộ là hoàn toàn tự nguyện, mang tính cho tặng, không phải tiền mua sản phẩm hay dịch vụ, không kèm quyền lợi và không hoàn lại.',
    'Open the “Support” tab, pick Iced milk coffee, Latte or Salted coffee and scan the VietQR code with your banking app. Donations are entirely voluntary gifts, not a purchase, come with no extra benefits and are not refunded.']],
  [['Một tài khoản dùng được cho mấy con?','How many children per account?'],
   ['Bao nhiêu con cũng được. Mỗi con một mã PIN, một lộ trình theo tuổi, sao và huy hiệu riêng. Ông bà, người thân cũng có thể có tài khoản người lớn.',
    'As many as you like. Each child has their own PIN, age-based path, stars and badges. Grandparents and relatives can have adult accounts too.']],
  [['Đổi máy thì dữ liệu có mất không?','What if I change devices?'],
   ['Dữ liệu chỉ nằm trên máy của gia đình. Ba mẹ vào Quản lý tài khoản → Tải file sao lưu, rồi trên máy mới bấm “Khôi phục từ file sao lưu”. Nên tải file sao lưu định kỳ.',
    'Data lives only on your device. In Manage accounts tap “Download backup”, then on the new device tap “Restore from file”. Back up now and then.']],
'''

APP_METHODS = r'''  freeRegister(){
    // Tao tai khoan gia dinh mien phi ngay tren may nay (khong can may chu, khong thu phi)
    const st = this.state, vi = st.lang==='vi', f = st.rg || {};
    const name = (f.name||'').trim().replace(/\s+/g,' '), ph = (f.phone||'').replace(/\D/g,'');
    const err = (v,e) => this.set({rgErr: vi ? v : e});
    if (st.family) return err(`Máy này đã có tài khoản gia đình (số ${st.family.phone}). Ba mẹ bấm “Đã có tài khoản? Đăng nhập” để vào Quản lý tài khoản.`, `This device already has a family account (${st.family.phone}). Tap “Already registered? Log in”.`);
    if (name.length < 2) return err('Ba mẹ điền giúp Sen tên nhé.', 'Please enter your name.');
    if (!/^0\d{9}$/.test(ph)) return err('Số điện thoại cần đủ 10 số, bắt đầu bằng 0. Số này là ID đăng nhập của ba mẹ.', 'The phone number needs 10 digits starting with 0. It is your login ID.');
    if (!/^\d{4}$/.test(f.pin||'')) return err('Mã PIN ba mẹ gồm đúng 4 chữ số.', 'Your PIN must be exactly 4 digits.');
    if (WEAK_PINS.includes(f.pin)) return err('Mã này dễ đoán quá (như 1234, 0000). Chọn mã khác nhé.', 'That PIN is too easy to guess. Pick another.');
    if (f.pin !== f.pin2) return err('Hai lần nhập mã PIN chưa khớp nhau.', 'The two PINs do not match.');
    if (!f.agree) return err('Ba mẹ đánh dấu ô đồng ý với Điều khoản & lưu ý giúp Sen nhé.', 'Please tick the box to agree to the terms.');
    const family = {name, phone: ph, pin: f.pin, plan: 'Miễn phí', planKey: 'free', status: 'active', code: '', pinChanged: true, createdAt: new Date().toISOString()};
    saveFamily(family);
    try { sessionStorage.removeItem('senapp.demo'); } catch (e) {}
    const profiles = [{name, role:0, band:'parent', pin: f.pin, phone: ph, stars:0, av:3, kid:false}];
    this.set({family, profiles, demo:false, doneMissions:{}, approved:{}, mLevel:{}, mFlag:{}, gate:'manage', active:0, acctFrom:'welcome', afterPin:null,
      acctForm:null, acctErr:'', acctDel:null, pinEdit:null, rg:{}, rgErr:'',
      acctMsg: vi ? `Chào mừng gia đình đến với Sen! Ba mẹ bấm “Thêm tài khoản cho con” để tạo tài khoản và mã PIN cho con, thêm ba/mẹ còn lại và ông bà nếu cần.` : `Welcome to Sen! Tap “Add a child account” to create your child’s account and PIN, then add the other parent and grandparents if you like.`});
  }

  backupExport(){
    const vi = this.state.lang==='vi', data = {};
    try { for (let n = 0; n < localStorage.length; n++) { const k = localStorage.key(n); if (k && k.indexOf('senapp.') === 0) data[k] = localStorage.getItem(k); } } catch (e) {}
    if (!data['senapp.family']) return this.set({bkMsg: vi ? 'Máy này chưa có tài khoản gia đình để sao lưu.' : 'There is no family account on this device yet.'});
    const d = new Date(), day = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
    try {
      const blob = new Blob([JSON.stringify({app:'senapp', v:1, at:d.toISOString(), data}, null, 1)], {type:'application/json'});
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'senapp-sao-luu-' + day + '.json';
      document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 4000);
      this.set({bkMsg: vi ? 'Đã tải file sao lưu. Ba mẹ cất file này cẩn thận, dùng khi đổi máy hoặc lỡ xoá dữ liệu trình duyệt.' : 'Backup downloaded. Keep it safe for a new device or if browser data is cleared.'});
    } catch (e) { this.set({bkMsg: vi ? 'Trình duyệt này chưa cho tải file. Ba mẹ thử bằng Chrome hoặc Safari nhé.' : 'This browser cannot download files. Try Chrome or Safari.'}); }
  }

  backupImport(e){
    const vi = this.state.lang==='vi', file = e && e.target && e.target.files && e.target.files[0];
    if (!file) return;
    const say = (v, en) => this.set({bkMsg: vi ? v : en, rgErr: vi ? v : en});
    const rd = new FileReader();
    rd.onload = () => {
      let o = null; try { o = JSON.parse(String(rd.result)); } catch (x) {}
      if (!o || o.app !== 'senapp' || !o.data || !o.data['senapp.family']) return say('File này không phải file sao lưu Senapp.', 'This is not a Senapp backup file.');
      let fam = {}; try { fam = JSON.parse(o.data['senapp.family']) || {}; } catch (x) {}
      if (!window.confirm((vi ? 'Khôi phục tài khoản gia đình ' : 'Restore the family account ') + (fam.name || '') + ' (' + (fam.phone || '') + ')? ' + (vi ? 'Dữ liệu Senapp hiện có trên máy này sẽ được thay bằng bản trong file.' : 'Senapp data on this device will be replaced.'))) return;
      try {
        const old = []; for (let n = 0; n < localStorage.length; n++) { const k = localStorage.key(n); if (k && k.indexOf('senapp.') === 0) old.push(k); }
        old.forEach(k => localStorage.removeItem(k));
        Object.keys(o.data).forEach(k => { if (k.indexOf('senapp.') === 0 && typeof o.data[k] === 'string') localStorage.setItem(k, o.data[k]); });
        sessionStorage.removeItem('senapp.demo');
      } catch (x) { return say('Chưa khôi phục được (bộ nhớ trình duyệt bị chặn).', 'Could not restore (browser storage is blocked).'); }
      location.replace(location.pathname);
    };
    rd.readAsText(file);
    try { e.target.value = ''; } catch (x) {}
  }

'''


def app(t):
    # thu vien ung ho, dat sau du lieu bai hoc (v14 lam roi tu "const L" toi "const STAGES")
    t = sub(t, "const saveFamily = (f) =>", DONATE_LIB + "const HUB_URL = '" + HUB + "';\nconst SHARE_TEXT = 'Senapp: App kỹ năng sống miễn phí cho con tiểu học. Học 7 phút, làm một việc thật. Ba mẹ đồng hành cùng con nhé!';\nconst saveFamily = (f) =>")
    t = sub(t, "  if (/[?&#]demo\\b/.test(location.href)) b.demo = true;\n  return b;",
               "  if (/[?&#]demo\\b/.test(location.href)) b.demo = true;\n  if (/[?&#]dangky\\b/.test(location.href) && !b.family && !b.demo) b.gate = 'register';\n  return b;")
    t = sub(t, "mPhone:'', mPin:'', mErr:'', mFrom:'welcome',",
               "rg:{name:'', phone:'', pin:'', pin2:'', agree:false}, rgErr:'', dnIdx:1, dnMsg:'', bkMsg:'', mPhone:'', mPin:'', mErr:'', mFrom:'welcome',")
    t = sub(t, "  mLogin(){", APP_METHODS + "  mLogin(){")
    # --- man Chao: nut tao tai khoan mien phi, nhan "Mien phi 100%", lien ket Bamedonghanh
    t = sub(t, '<div style="font-size:13.5px;color:#6D5B4B">{{ wcTag }}</div>',
               '<div style="font-size:13.5px;color:#6D5B4B">{{ wcTag }}</div>\n            <div style="font-size:12px;font-weight:800;color:#1F5E4A;background:#E3F4EC;border-radius:99px;padding:5px 12px;margin-top:6px">{{ wcFree }}</div>')
    t = sub(t, '{{ wcNote }}<br>{{ wcHelp }}',
               '{{ wcNote }}<br><a href="' + HUB + '" target="_blank" rel="noopener" style="font-weight:700;color:#C8102E">{{ wcFamily }}</a><br>{{ wcHelp }}')
    t = sub(t, "      wcCreate: i?'Manage accounts':'Quản lý tài khoản',",
               "      wcCreate: (st.family || st.demo) ? (i?'Manage accounts':'Quản lý tài khoản') : (i?'Create a free family account':'Tạo tài khoản gia đình'),\n"
               "      wcFree: i?'🎁 100% free · No ads':'🎁 Miễn phí 100% · Không quảng cáo',\n"
               "      wcFamily: i?'One of the Bamedonghanh apps ♥':'Một App của Bamedonghanh ♥',")
    t = sub(t, "      createFamily:()=>this.set({gate:'mlogin',",
               "      createFamily:()=> (!st.family && !st.demo) ? this.set({gate:'register', rgErr:''}) : this.set({gate:'mlogin',")
    t = sub(t, "showNotReg: !st.family,", "showNotReg: false,")
    # --- man Dang ky -> tao tai khoan mien phi
    a = t.index('<div style="border-radius:20px;background:#FFF8E6;border:2px solid #F2A93B;padding:12px 14px;display:flex;align-items:center;gap:12px">')
    b = t.index('<div onClick="{{ haveAccount }}"', a)
    t = t[:a] + REG_FORM + t[b:]
    a = t.index('<div onClick="{{ tryDemo }}"'); b = t.index('</div>', a) + len('</div>')
    t = t[:b] + '\n          ' + RESTORE_LINE.rstrip() + t[b:]
    t = sub(t, "      rgCta: i?'Register now →':'Đăng ký ngay →',",
               "      rgCta: i?'Create my free account':'Tạo tài khoản miễn phí',\n"
               "      rgFormTitle: i?'Family account':'Tài khoản gia đình', rgFreeBadge: i?'100% FREE':'MIỄN PHÍ 100%',\n"
               "      rgNamePh: i?'Parent’s name':'Tên ba mẹ', rgPhonePh: i?'Phone number (your login ID)':'Số điện thoại (ID đăng nhập)',\n"
               "      rgPinPh: i?'Parent PIN (4 digits)':'Mã PIN ba mẹ (4 số)', rgPin2Ph: i?'Repeat PIN':'Nhập lại mã PIN',\n"
               "      rgName: st.rg.name, rgPhone: st.rg.phone, rgPin: st.rg.pin, rgPin2: st.rg.pin2,\n"
               "      onRgName:(e)=>this.set({rg:{...st.rg, name:e.target.value}, rgErr:''}),\n"
               "      onRgPhone:(e)=>this.set({rg:{...st.rg, phone:e.target.value.replace(/[^\\d ]/g,'').slice(0,13)}, rgErr:''}),\n"
               "      onRgPin:(e)=>this.set({rg:{...st.rg, pin:e.target.value.replace(/\\D/g,'').slice(0,4)}, rgErr:''}),\n"
               "      onRgPin2:(e)=>this.set({rg:{...st.rg, pin2:e.target.value.replace(/\\D/g,'').slice(0,4)}, rgErr:''}),\n"
               "      rgToggleAgree:()=>this.set({rg:{...st.rg, agree:!st.rg.agree}, rgErr:''}),\n"
               "      rgAgreeRow:'display:flex;gap:10px;align-items:flex-start;border-radius:14px;padding:10px 12px;cursor:pointer;' + (st.rg.agree ? 'background:#DDF3F1;border:1.5px solid #1BA39C' : 'background:#FFFBF4;border:1.5px solid #EFE3D2'),\n"
               "      rgAgreeBox:'width:22px;height:22px;border-radius:7px;flex:none;display:flex;align-items:center;justify-content:center;font-weight:800;color:#FFF;font-size:13px;background:' + (st.rg.agree ? '#1BA39C' : '#E4D6C2'),\n"
               "      rgAgreeTick: st.rg.agree ? '✓' : '',\n"
               "      rgAgreeText: i?'I am the child’s parent or guardian and agree to the':'Tôi là ba mẹ/người giám hộ của con, đã đọc và đồng ý với', rgTermsLink: i?'terms & notes':'Điều khoản & lưu ý',\n"
               "      rgHasErr: !!st.rgErr, rgErr: st.rgErr, doFreeRegister:()=>this.freeRegister(),\n"
               "      rgRestore: i?'New device? Restore from a backup file':'Dùng máy mới? ⬆️ Khôi phục từ file sao lưu',\n"
               "      bkImport:(e)=>this.backupImport(e), bkExport:()=>this.backupExport(),\n"
               "      bkTitle: i?'Back up your data':'Sao lưu dữ liệu', bkSub: i?'Accounts, progress and stars live only in this browser. Download a backup now and then, and use it on a new device.':'Tài khoản, tiến độ và sao chỉ nằm trong trình duyệt trên máy này. Ba mẹ nên tải file sao lưu định kỳ và dùng file này khi chuyển sang máy khác.',\n"
               "      bkExportLabel: i?'⬇️ Download backup':'⬇️ Tải file sao lưu', bkImportLabel: i?'⬆️ Restore from file':'⬆️ Khôi phục từ file',\n"
               "      bkMsgShow: !!st.bkMsg, bkMsg: st.bkMsg,")
    t = sub(t, "      rgDemo: i?'Just looking — try the app with sample data':'Xem thử app với dữ liệu mẫu',",
               "      rgDemo: i?'Want a look first? Open the sample family':'Muốn xem thử? Mở gia đình mẫu',")
    t = sub(t, "['♥', '#F2A93B', i?'Extra children 50% off':'Thêm con giảm 50%',", "['♥', '#F2A93B', i?'As many children as you like':'Bao nhiêu con cũng được',")
    t = sub(t, "rgKicker: i?'For primary-school kids 6–11 · 7 minutes a day':'Cho con tiểu học 6–11 tuổi · 7 phút mỗi ngày',",
               "rgKicker: i?'100% free · primary-school kids · 7 minutes a day':'Miễn phí 100% · con tiểu học · 7 phút mỗi ngày',")
    # --- Quan ly tai khoan: sao luu, bo gioi han / phi them con
    t = sub(t, '<div style="border-radius:20px;background:#FFF;border:1.5px solid #EFE3D2;padding:14px;display:flex;flex-direction:column;gap:5px">\n                <div style="font-family:\'Baloo 2\',cursive;font-weight:800;font-size:16px;color:#221A15">{{ supTitle }}</div>',
               BACKUP_CARD + '<div style="border-radius:20px;background:#FFF;border:1.5px solid #EFE3D2;padding:14px;display:flex;flex-direction:column;gap:5px">\n                <div style="font-family:\'Baloo 2\',cursive;font-weight:800;font-size:16px;color:#221A15">{{ supTitle }}</div>')
    a = t.index("    if (f.kind==='kid' && st.profiles.filter(p=>p.kid).length >= 1 && !st.demo) return err("); b = t.index('\n', a) + 1
    t = t[:a] + t[b:]
    t = sub(t, "      if (st.profiles.filter(x=>x.kid).length >= 1 && !st.demo) return this.setState({pendingProfile:np, payKind:'profile', pay:'idle', payRefCopied:false, creator:null, formA:'', formB:'', formPin:''});\n", "")
    t = sub(t, "profilesMeta: i ? kidCount+' child profile(s) · each extra child: 149,000₫/6 mo or 249,000₫/year (50% off)' : kidCount+' hồ sơ con · mỗi con thêm: 149.000đ/6 tháng hoặc 249.000đ/năm (giảm 50%)',",
               "profilesMeta: i ? kidCount+' child profile(s) · add as many as you like, free' : kidCount+' hồ sơ con · thêm bao nhiêu con cũng được, miễn phí',")
    t = sub(t, "extraProfile: st.creator==='profile' && kidCount>=1 && !st.demo,", "extraProfile: false,")
    t = sub(t, "payTitle:'Thanh toán & hoá đơn', payBody:'Gói trả theo 6 tháng (tặng 1 tháng) hoặc 12 tháng (tặng 2 tháng), không tự động gia hạn. Hết kỳ ba mẹ chủ động gia hạn bằng chuyển khoản VietQR — Sen không lưu số thẻ.',",
               "payTitle:'Miễn phí 100%', payBody:'Senapp không thu phí, không quảng cáo, không bán hàng. Muốn thì ba mẹ mời Sen ly cà phê ở tab Ủng hộ; không mời vẫn dùng như nhau.',")
    t = sub(t, "payTitle:'Billing & invoices', payBody:'Paid for 6 months (+1 free) or 12 months (+2 free) with no auto-renewal. Renew yourself by VietQR bank transfer when the term ends — Sen stores no card numbers.',",
               "payTitle:'100% free', payBody:'Senapp charges nothing, shows no ads and sells nothing. If you like, buy Sen a coffee in the Support tab; it changes nothing in the app.',")
    t = sub(t, "qaSub:'Thanh toán, hoa hồng, quyền riêng tư',", "qaSub:'Miễn phí, ủng hộ, sao lưu, quyền riêng tư',")
    t = sub(t, "qaSub:'Billing, commission, privacy',", "qaSub:'Free, donations, backup, privacy',")
    t = sub(t, "acctKidsCount: kidCount + (i?'/5 in your plan':'/5 trong gói'),", "acctKidsCount: kidCount + (i?' · no limit':' · không giới hạn'),")
    a = t.index('      acctPlan: st.family ?'); b = t.index('\n', a)
    t = t[:a] + "      acctPlan: st.family ? (i?'Free forever · no ads · data stays on this device':'Miễn phí 100% · không quảng cáo · dữ liệu nằm trên máy này') : ''," + t[b:]
    t = sub(t, "mSub: i?'Log in with the phone number you registered and the PIN Sen gave you.':'Đăng nhập bằng số điện thoại đã đăng ký và mã PIN Sen cấp khi đăng ký.',",
               "mSub: i?'Log in with your phone number and the parent PIN you set when creating the account.':'Đăng nhập bằng số điện thoại và mã PIN ba mẹ đặt khi tạo tài khoản.',")
    t = sub(t, "mHint: st.family ? (i?'Your PIN was shown for 10 seconds when you registered. Remember to change it within 24 hours.':'Mã PIN hiện 10 giây khi ba mẹ đăng ký thành công. Nhớ đổi mã PIN trong vòng 24 giờ.') :",
               "mHint: st.family ? (i?'Your data lives on this device. Download a backup in Manage accounts now and then.':'Dữ liệu nằm trên máy này. Ba mẹ nhớ tải file sao lưu trong Quản lý tài khoản nhé.') :")
    t = sub(t, "return err('Chưa tìm thấy tài khoản với số này. Ba mẹ kiểm tra lại số đã đăng ký, hoặc bấm “Đăng ký ngay”.','No account found for this number. Check the registered phone number, or register first.');",
               "return err('Máy này chưa có tài khoản với số này. Ba mẹ tạo tài khoản gia đình miễn phí, hoặc khôi phục từ file sao lưu nếu đã dùng Sen ở máy khác.','No account for this number on this device. Create a free family account, or restore from a backup file made on another device.');")
    # --- tab Goi -> Ung ho (Moi ly Coffee)
    t = sub(t, "tabs:['Học','Nhiệm vụ','Nhóm','Hồ sơ','Ba mẹ','Gói'],", "tabs:['Học','Nhiệm vụ','Nhóm','Hồ sơ','Ba mẹ','Ủng hộ'],")
    t = sub(t, "tabs:['Learn','Missions','Group','Profile','Parent','Plan'],", "tabs:['Learn','Missions','Group','Profile','Parent','Support'],")
    a = t.index('<!-- PREMIUM -->'); a = t.index('<div data-screen-label="09 Plan"', a)
    b = t.index('\n        </sc-if>', a)
    t = t[:a] + DONATE_SCREEN + t[b:]
    t = sub(t, "      goHome:()=>this.set({screen:'home'}), goPremium:",
               "      dnFreeTitle: i?'🎁 Senapp is 100% free':'🎁 Senapp miễn phí 100%',\n"
               "      dnFreeSub: i?'All 9 skills, 240 lessons and 240 real-life missions, as many children as you like, no ads. Nothing to buy, ever.':'Trọn bộ 9 kỹ năng, 240 bài và 240 nhiệm vụ đời thực, bao nhiêu con cũng được, không quảng cáo. Không có gì phải mua cả.',\n"
               "      dnTitle: 'Mời ly Coffee để Sen có thêm sức mạnh đồng hành và phát triển cùng các con nha ba mẹ ☕',\n"
               "      dnLevels: DONATE_LEVELS.map((v, k) => ({ name: v.name, pick: () => this.set({dnIdx:k, dnMsg:''}),\n"
               "        style: 'cursor:pointer;text-align:center;border-radius:12px;padding:9px 4px;font-weight:800;font-size:12.5px;' + (st.dnIdx===k ? 'background:#2E9E7E;color:#FFF;border:1.5px solid #2E9E7E' : 'background:#FFF8EF;color:#221A15;border:1.5px solid #EFE3D2') })),\n"
               "      dnImgStyle: st.screen==='premium' ? donateBox(st.dnIdx, 260) : '', dnAlt: 'Mã QR mời Sen ly ' + DONATE_LEVELS[st.dnIdx].name + ': ' + DONATE.name + ', ' + DONATE.bank + ', số tài khoản ' + DONATE.acct,\n"
               "      dnSave:()=>donateSave(st.dnIdx), dnSaveLabel: i?'Download QR':'Tải mã QR', dnCopyLabel: i?'Copy account no.':'Chép số tài khoản',\n"
               "      dnCopy:()=>donateCopy().then(ok=>this.set({dnMsg: ok ? 'Đã chép số tài khoản ' + DONATE.acct : 'Ba mẹ chọn và chép số tài khoản ' + DONATE.acct + ' giúp Sen nhé.'})),\n"
               "      dnMsgShow: !!st.dnMsg, dnMsg: st.dnMsg, dnNoteLabel: 'Nội dung chuyển khoản:', dnHow: DONATE_HOW, dnWarn: DONATE_WARN,\n"
               "      dnShareTitle: i?'Spread the word 💛':'Lan tỏa Senapp nha ba mẹ 💛', dnShareSub: i?'Spend 7 minutes a day with your child.':'Ba mẹ hãy đồng hành cùng con 7 phút mỗi ngày nhé.', dnShareBtn: i?'Share with friends':'Chia sẻ cho bạn bè',\n"
               "      dnShare:()=>{ const url = location.origin + location.pathname.replace(/[^/]*$/, '') + 'trang-chu/'; try { if (navigator.share) return navigator.share({title:'Senapp', text:SHARE_TEXT, url}).catch(()=>{}); } catch (e) {}\n"
               "        try { navigator.clipboard.writeText(SHARE_TEXT + ' ' + url).then(()=>this.set({dnMsg:'Đã chép link Senapp, ba mẹ dán gửi bạn bè nhé!'})); } catch (e) {} },\n"
               "      dnFamily: i?'Senapp is one of the Bamedonghanh apps, with Lumi English, Học Toán Vui and Toán Vui cùng Pi. All free.':'Senapp là một App trong gia đình Bamedonghanh, cùng Lumi English, Học Toán Vui và Toán Vui cùng Pi. Tất cả đều miễn phí.',\n"
               "      goHome:()=>this.set({screen:'home'}), goPremium:")
    t = sub(t, "goRegister:()=>{ window.location.href = LANDING_URL + '#dang-ky'; },", "goRegister:()=>this.freeRegister(),")
    # --- Hoi dap trong App: bo cau ve thanh toan, goi, hoa hong; them cau ve mien phi, ung ho, sao luu
    a = t.index("  [['Ba mẹ thanh toán bằng cách nào?'"); b = t.index("  [['Liên hệ Sen bằng cách nào?'", a)
    t = t[:a] + APP_QA + t[b:]
    a = t.index("  [['Hoa hồng Affiliate tính thế nào?'"); b = t.index("  [['Dữ liệu của con có an toàn không?'", a)
    t = t[:a] + t[b:]
    for bad in ('102111988', 'Classic', 'Affiliate tính', '149.000đ/6 tháng'):
        assert bad not in t[t.index('const QA = ['):t.index('const VERSIONS')], bad
    return t


def patch(path, fn):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', s, re.S)
    t = fn(json.loads(m.group(2)))
    s = s[:m.start(2)] + json.dumps(t, ensure_ascii=False).replace('</', '<\\/') + s[m.end(2):]
    open(path, 'w', encoding='utf-8').write(s); print('ok', path)


if __name__ == '__main__':
    d = sys.argv[1]
    patch(os.path.join(d, 'trang-chu', 'index.html'), landing)
    patch(os.path.join(d, 'index.html'), app)
