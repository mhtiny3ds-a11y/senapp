import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const S=process.env.SHOTS||'./', B='http://localhost:8768/';
const b = await chromium.launch(); const pg = await (await b.newContext({viewport:{width:390,height:844}})).newPage(); pg.setDefaultTimeout(6000);
const errs=[]; pg.on('pageerror',e=>errs.push(e.message)); pg.on('response', r=>{ if (r.status()>=400 && !r.url().includes('image-slots')) errs.push(r.status()+' '+r.url()); });
const ov = s => pg.locator(`[data-screen-label="${s}"]`); const T = async l => (await l.innerText()).replace(/\s+/g,' ');
const pin = async c => { for (const d of c) { await ov('02 PIN').getByText(d,{exact:true}).click(); await pg.waitForTimeout(60);} };
const kid = async () => { await pg.getByText('Con đăng nhập',{exact:true}).click(); await ov('01b Kid login').getByText('Minh Phúc').click(); await pin('1234'); await pg.waitForTimeout(500); };
const toW = async () => { await pg.locator('.app-header > div').first().click(); await pg.waitForTimeout(300); };
await pg.goto(B+'?demo'); await pg.waitForTimeout(3000);
await kid(); let t = await T(ov('03 Home'));
console.log('1 home:', t.match(/Tuần 1\/\d+ Chặng[^›]*/)?.[0]);
await toW(); await pg.getByText('Ba mẹ đăng nhập',{exact:true}).click(); await pin('9999'); await pg.waitForTimeout(500);
const P = ov('08 Parent'); console.log('2 card:', (await T(P)).match(/Danh mục bài học & nhiệm vụ.{0,110}/)?.[0]);
await P.getByText('Danh mục bài học & nhiệm vụ').first().click(); await pg.waitForTimeout(400);
const C = ov('13 Custom'); await C.getByText('9–11 tuổi').click(); await pg.waitForTimeout(300);
t = await T(C); console.log('3 catalog:', t.match(/CHẶNG 1.{0,200}/)?.[0]);
console.log('   stages:', (t.match(/CHẶNG \d+/g)||[]).length);
// hide lesson 2 of week 1
await C.locator('div[aria-label="Ẩn khỏi lộ trình"]').nth(1).click(); await pg.waitForTimeout(300);
console.log('4 after hide:', (await T(C)).match(/Xem bài đã ẩn \(\d+\)/)?.[0]);
// search
await C.locator('input').first().fill('xin lỗi'); await pg.waitForTimeout(300);
console.log('5 search:', (await T(C)).match(/\d+ kết quả.{0,120}/)?.[0]);
await C.locator('input').first().fill(''); await pg.waitForTimeout(200);
// skill filter
await C.getByText('Tài chính cá nhân',{exact:true}).first().click(); await pg.waitForTimeout(300);
console.log('6 filter:', (await T(C)).match(/Tuần 1.{0,160}/)?.[0]);
await C.getByText('Tất cả',{exact:true}).click(); await pg.waitForTimeout(200);
// add lesson to week 1
await C.getByText('＋ Thêm bài',{exact:true}).first().click(); await pg.waitForTimeout(400);
t = await T(C); console.log('7 editor new:', /KỸ NĂNG/.test(t), /＋ Thêm tình huống/.test(t), /＋ Thêm lựa chọn/.test(t), /Xoá bài ba mẹ tạo/.test(t));
await C.locator('input').first().fill('Bài riêng của nhà mình'); await C.getByText('＋ Thêm tình huống',{exact:true}).click(); await pg.waitForTimeout(200);
await C.getByText('Quản lý thời gian',{exact:true}).first().click(); await pg.waitForTimeout(200);
t = await T(C); console.log('   ctx count:', (t.match(/\d\. [ABC] · /g)||[]).join(','));
await pg.screenshot({path:S+'w16-editor.png'});
await C.getByText('Xong',{exact:true}).click(); await pg.waitForTimeout(300);
console.log('8 week1 now:', (await T(C)).match(/Tuần 1 ＋ Thêm bài.{0,400}/)?.[0]);
await pg.screenshot({path:S+'w16-catalog.png'});
// kid sees changes
await toW(); await kid(); t = await T(ov('03 Home'));
console.log('9 kid week:', t.match(/Tuần 1\/\d+.{0,420}/)?.[0]);
// plan screen price
await toW(); await pg.getByText('Ba mẹ đăng nhập',{exact:true}).click(); await pin('9999'); await pg.waitForTimeout(400);
await pg.locator('.app-nav > *').nth(1).click(); await pg.waitForTimeout(400);
console.log('10 plan:', (await T(ov('09 Plan'))).slice(0,300));
await pg.goto(B+'trang-chu/'); await pg.waitForTimeout(2500);
t = await T(pg.locator('body')); console.log('11 land:', t.match(/Chưa tới 1\.400đ.{0,80}/)?.[0], '|', t.match(/Gói 12 tháng 499\.000đ[^·]*/)?.[0]);
console.log('ERR', errs); await b.close();
