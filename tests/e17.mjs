// v17: App mien phi 100%, tao tai khoan gia dinh trong App, "Moi Sen ly Coffee", sao luu / khoi phuc.
// Chay: (cd public && python3 -m http.server 8771) &  roi  BASE=http://localhost:8771/ SHOTS=/tmp/ QRDIR=<thu muc co node_modules/jsqr,pngjs> node tests/e17.mjs
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { createRequire } from 'module';
import fs from 'fs';
const S = process.env.SHOTS || './', B = process.env.BASE || 'http://localhost:8771/';
const req = createRequire((process.env.QRDIR || '.') + '/x.js');
let jsQR = null, PNG = null; try { jsQR = req('jsqr'); PNG = req('pngjs').PNG; } catch (e) { console.log('(bo qua giai ma QR: chua cai jsqr/pngjs)'); }
const decode = (dataUrl) => { if (!jsQR) return null; const png = PNG.sync.read(Buffer.from(dataUrl.split(',')[1], 'base64'));
  const r = jsQR(new Uint8ClampedArray(png.data), png.width, png.height); return r && r.data; };
const crc = (s) => { let c = 0xFFFF; for (const ch of s) { c ^= ch.charCodeAt(0) << 8; for (let i = 0; i < 8; i++) c = c & 0x8000 ? ((c << 1) ^ 0x1021) & 0xFFFF : (c << 1) & 0xFFFF; } return c.toString(16).toUpperCase().padStart(4, '0'); };
const qrOk = (p, amount) => !!p && p.includes('5405' + String(amount).padStart(5, '0').slice(-5)) && p.includes('Thank you Sen nha') && p.includes('0113VQRQAGLRC3078') && crc(p.slice(0, -4)) === p.slice(-4);

const qrSrc = async (L) => L.locator('[role=img][aria-label^="Mã QR"]').evaluate(async e => { const u = (getComputedStyle(e).backgroundImage.match(/url\("?(.*?)"?\)$/) || [])[1] || '';
  if (!u) return ''; const bl = await (await fetch(u)).blob(); return await new Promise(r => { const f = new FileReader(); f.onload = () => r(f.result); f.readAsDataURL(bl); }); });
const b = await chromium.launch(); const errs = []; let pass = 0, fail = 0;
const ok = (name, cond, extra) => { cond ? pass++ : fail++; console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' · ' + extra : '')); };
const mk = async () => { const c = await b.newContext({ viewport: { width: 390, height: 844 }, acceptDownloads: true }); const pg = await c.newPage(); pg.setDefaultTimeout(6000);
  pg.on('pageerror', e => errs.push(e.message)); pg.on('response', r => { if (r.status() >= 400 && !r.url().includes('image-slots')) errs.push(r.status() + ' ' + r.url()); }); return pg; };
const T = async l => (await l.innerText()).replace(/\s+/g, ' ');
const PRICE = /\d{2,3}\.000đ|Học phí|Thanh toán|[Tt]hêm con giảm|Gói 6 tháng|Gói 12 tháng|chuyển khoản đúng số tiền|Bộ Công Thương/;

// ---------- 1. trang chu
let pg = await mk();
await pg.goto(B + 'trang-chu/'); await pg.waitForTimeout(2500);
let t = await T(pg.locator('body'));
ok('trang chu: khong con gia / thanh toan', !PRICE.test(t), (t.match(PRICE) || [])[0]);
ok('trang chu: mien phi 100%', /Miễn phí 100%/.test(t) && /Không học phí\. Không quảng cáo\. Không bán gì cả\./.test(t));
ok('trang chu: moi ly coffee', /Mời ly Coffee để Sen có thêm sức mạnh đồng hành và phát triển cùng các con nha ba mẹ ☕/.test(t) && /Thank you Sen nha/.test(t) && /141431319191/.test(t));
ok('trang chu: lien ket Bamedonghanh', await pg.locator('a[href="https://mhtiny3ds-a11y.github.io/my_app/"]').count() >= 2);
ok('trang chu: nut dung mien phi -> ?dangky', await pg.locator('a[href="../?dangky"]').count() >= 2);
const U = pg.locator('#ung-ho');
for (const [name, amount] of [['Sữa đá', 40000], ['Latte', 56000], ['Cà phê Muối', 66000]]) {
  await U.getByText(name, { exact: true }).click(); await pg.waitForTimeout(250);
  const src = await qrSrc(U);
  const p = src && src.startsWith('data:image/png') ? decode(src) : null;
  ok('trang chu: ma QR ' + name, jsQR ? qrOk(p, amount) : !!src, p ? p.slice(-40) : src && src.slice(0, 30));
}
const [dl] = await Promise.all([pg.waitForEvent('download'), U.getByText('⬇️ Tải mã QR').click()]);
ok('trang chu: tai ma QR', /ma-qr-moi-sen-coffee-ca-phe-muoi\.png/.test(dl.suggestedFilename()), dl.suggestedFilename());
await U.screenshot({ path: S + 'w17-ungho.png' });
await pg.locator('#mien-phi').screenshot({ path: S + 'w17-mienphi.png' });

// ---------- 2. App: tao tai khoan mien phi
await pg.goto(B + '?dangky'); await pg.waitForTimeout(2500);
let R = pg.locator('[data-screen-label="00 Register"]');
ok('App: ?dangky mo form tao tai khoan', await R.isVisible());
t = await T(R); ok('App: man dang ky khong con gia', !PRICE.test(t) && /MIỄN PHÍ 100%/.test(t), (t.match(PRICE) || [])[0]);
const inp = R.locator('input:not([type=file])');
await R.getByText('Tạo tài khoản miễn phí', { exact: true }).click(); await pg.waitForTimeout(200);
ok('App: thieu ten -> bao loi', /Ba mẹ điền giúp Sen tên nhé/.test(await T(R)));
await inp.nth(0).fill('Trần Thu Hà'); await inp.nth(1).fill('0912 345 678'); await inp.nth(2).fill('1234'); await inp.nth(3).fill('1234');
await R.getByText('Tạo tài khoản miễn phí', { exact: true }).click(); await pg.waitForTimeout(200);
ok('App: PIN de doan -> bao loi', /dễ đoán/.test(await T(R)));
await inp.nth(2).fill('4826'); await inp.nth(3).fill('4827');
await R.getByText('Tạo tài khoản miễn phí', { exact: true }).click(); await pg.waitForTimeout(200);
ok('App: PIN khong khop -> bao loi', /chưa khớp/.test(await T(R)));
await inp.nth(3).fill('4826');
await R.getByText('Tạo tài khoản miễn phí', { exact: true }).click(); await pg.waitForTimeout(200);
ok('App: chua dong y -> bao loi', /đồng ý với Điều khoản/.test(await T(R)));
await pg.screenshot({ path: S + 'w17-dangky.png' });
await R.getByText('Tôi là ba mẹ/người giám hộ', { exact: false }).click();
await R.getByText('Tạo tài khoản miễn phí', { exact: true }).click(); await pg.waitForTimeout(500);
let A = pg.locator('[data-screen-label="12 Accounts"]');
t = await T(A);
ok('App: tao xong -> Quan ly tai khoan', /Chào mừng gia đình đến với Sen!/.test(t) && /Trần Thu Hà/.test(t) && !/Minh Phúc/.test(t));
ok('App: khong gioi han con, mien phi', /không giới hạn/.test(t) && /Miễn phí 100%/.test(t) && !PRICE.test(t), (t.match(PRICE) || [])[0]);
// them 2 con, khong bi doi thanh toan
for (const [nm, age, pin] of [['Bông', '7', '3907'], ['Tí', '9', '5162']]) {
  await A.getByText(/^\+ ?Thêm tài khoản cho con$/).first().click(); await pg.waitForTimeout(300);
  const f = A.locator('input:not([type=file])'); await f.nth(0).fill(nm); await f.nth(1).fill(age); await f.nth(2).fill(pin); await f.nth(3).fill(pin);
  await A.getByText('Tôi là cha mẹ', { exact: false }).click(); await pg.waitForTimeout(100);
  await A.getByText('Tạo tài khoản', { exact: false }).last().click(); await pg.waitForTimeout(400);
  t = await T(A); ok('App: them con ' + nm, new RegExp('Đã tạo tài khoản cho ' + nm).test(t), t.match(/Gói đã gồm[^.]*\./)?.[0]);
}
ok('App: khong hien man thanh toan', !(await pg.locator('[data-screen-label="11 Payment"]').count()));
await pg.screenshot({ path: S + 'w17-quanly.png', fullPage: true });
// sao luu
const [bk] = await Promise.all([pg.waitForEvent('download'), A.getByText('⬇️ Tải file sao lưu').click()]);
const bkPath = S + 'senapp-backup-test.json'; await bk.saveAs(bkPath);
const bkj = JSON.parse(fs.readFileSync(bkPath, 'utf8'));
ok('App: file sao luu', bkj.app === 'senapp' && /Trần Thu Hà/.test(bkj.data['senapp.family']) && /Bông/.test(bkj.data['senapp.profiles'] || ''), bk.suggestedFilename());

// ---------- 3. con dang nhap, ba me vao tab Ung ho
const ov = s => pg.locator(`[data-screen-label="${s}"]`);
const pinpad = async c => { for (const d of c) { await ov('02 PIN').getByText(d, { exact: true }).click(); await pg.waitForTimeout(60); } };
await pg.goto(B); await pg.waitForTimeout(2500);
t = await T(ov('01 Welcome'));
ok('App: man chao co nhan mien phi + Bamedonghanh', /Miễn phí 100% · Không quảng cáo/.test(t) && /Một App của Bamedonghanh/.test(t) && /Quản lý tài khoản/.test(t));
await pg.getByText('Con đăng nhập', { exact: true }).click(); await ov('01b Kid login').getByText('Bông').click(); await pinpad('3907'); await pg.waitForTimeout(500);
t = await T(ov('03 Home')); ok('App: con hoc duoc ngay', /Bắt đầu học/.test(t) && !PRICE.test(t), t.match(/BÀI HỌC HÔM NAY.{0,60}/)?.[0]);
await pg.locator('.app-header > div').first().click(); await pg.waitForTimeout(300);
await pg.getByText('Ba mẹ đăng nhập', { exact: true }).click(); await pg.waitForTimeout(300);
if (await ov('01b Kid login').count()) { await ov('01b Kid login').getByText('Trần Thu Hà').click(); await pg.waitForTimeout(200); }
await pinpad('4826'); await pg.waitForTimeout(500);
t = await T(ov('08 Parent')); ok('App: tab Ba me khong con gia', !PRICE.test(t), (t.match(PRICE) || [])[0]);
const nav = await T(pg.locator('.app-nav')); ok('App: tab Ung ho thay tab Goi', /Ủng hộ/.test(nav) && !/Gói/.test(nav), nav);
await pg.locator('.app-nav > *').nth(1).click(); await pg.waitForTimeout(500);
const D = ov('09 Plan'); t = await T(D);
ok('App: man Ung ho', /Senapp miễn phí 100%/.test(t) && /Mời ly Coffee để Sen có thêm sức mạnh/.test(t) && /Lưu ý & miễn trừ trách nhiệm/.test(t) && !PRICE.test(t), (t.match(PRICE) || [])[0]);
for (const [name, amount] of [['Sữa đá', 40000], ['Latte', 56000], ['Cà phê Muối', 66000]]) {
  await D.getByText(name, { exact: true }).click(); await pg.waitForTimeout(250);
  const src = await qrSrc(D); const p = src && src.startsWith('data:image/png') ? decode(src) : null;
  ok('App: ma QR ' + name, jsQR ? qrOk(p, amount) : !!src, p ? p.slice(-40) : '');
}
await D.getByText('Latte', { exact: true }).click(); await pg.waitForTimeout(250);
await pg.screenshot({ path: S + 'w17-app-ungho.png', fullPage: true });

// ---------- 4. may moi: khoi phuc tu file sao luu
const pg2 = await mk();
await pg2.goto(B + '?dangky'); await pg2.waitForTimeout(2500);
pg2.on('dialog', d => d.accept());
await pg2.locator('[data-screen-label="00 Register"] input[type=file]').setInputFiles(bkPath); await pg2.waitForTimeout(2500);
const fam = await pg2.evaluate(() => JSON.parse(localStorage.getItem('senapp.family') || 'null'));
ok('May moi: khoi phuc tu file', fam && fam.phone === '0912345678');
await pg2.getByText('Con đăng nhập', { exact: true }).click(); await pg2.waitForTimeout(300);
t = await T(pg2.locator('[data-screen-label="01b Kid login"]')); ok('May moi: thay ho so con', /Bông/.test(t) && /Tí/.test(t));

// ---------- 5. gia dinh mau van xem duoc
const pg3 = await mk(); await pg3.goto(B + '?demo'); await pg3.waitForTimeout(2500);
ok('Gia dinh mau mo duoc', /Ba mẹ đăng nhập/.test(await T(pg3.locator('body'))));

console.log(`\n${pass} PASS, ${fail} FAIL`); console.log('ERR', errs); await b.close();
process.exit(fail || errs.length ? 1 : 0);
