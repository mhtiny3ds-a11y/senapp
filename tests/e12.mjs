import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const B='http://localhost:8768/?demo', S=process.env.SHOTS||'./';
const b = await chromium.launch(); const pg = await (await b.newContext({viewport:{width:390,height:844}})).newPage(); pg.setDefaultTimeout(5000);
const errs=[]; pg.on('pageerror',e=>errs.push(e.message)); pg.on('console', m=>{ if (m.type()==='error') errs.push('console: '+m.text().slice(0,200)); });
const ov = s => pg.locator(`[data-screen-label="${s}"]`);
const T = async l => (await l.innerText()).replace(/\s+/g,' ');
const pin = async c => { for (const d of c) { await ov('02 PIN').getByText(d,{exact:true}).click(); await pg.waitForTimeout(70);} };
const kidLogin = async () => { await pg.getByText('Con đăng nhập',{exact:true}).click(); await ov('01b Kid login').getByText('Minh Phúc').click(); await pin('1234'); await pg.waitForTimeout(500); };
const toWelcome = async () => { await pg.locator('.app-header > div').first().click(); await pg.waitForTimeout(300); };
const nav = async n => { await pg.locator('.app-nav > *').nth(n).click(); await pg.waitForTimeout(300); };
const clickBtn = async (L, re) => L.evaluate((el, src) => { const re = new RegExp(src); const ds=[...el.querySelectorAll('div')].filter(d=>getComputedStyle(d).cursor==='pointer'); const b = ds.find(d=>re.test(d.innerText.trim())); if (b) { b.click(); return b.innerText.trim(); } return null; }, re.source);
await pg.goto(B); await pg.waitForTimeout(2500); await kidLogin();
await ov('03 Home').getByText('Bắt đầu học',{exact:true}).click(); await pg.waitForTimeout(300);
const L = ov('04 Lesson'); const seq = [];
for (let g=0; g<20; g++) {
  const t = await T(L);
  if (/Tuyệt vời!/.test(t)) { seq.push('REWARD'); break; }
  seq.push((t.match(/\d+\/\d+/)||[''])[0] + ':' + ((t.match(/Tình huống \d\/\d/)||[''])[0]));
  let r = await clickBtn(L, /^(Tiếp tục|Làm câu đố|Hoàn thành bài|Tình huống tiếp theo: .*)$/);
  if (!r) r = await clickBtn(L, /^[AB]\s\S/);
  if (!r) break; seq.push('  > ' + r.slice(0,40)); await pg.waitForTimeout(200);
}
console.log(seq.join('\n'));
let t = await T(L); console.log('REWARD:', t.slice(t.indexOf('Tuyệt vời'), t.indexOf('Tuyệt vời')+500));
await pg.screenshot({path:S+'w12-reward.png', fullPage:true});
await L.getByText('✓ Con làm xong rồi!').click(); await pg.waitForTimeout(200);
console.log('after done:', (await T(L)).match(/Đang chờ ba mẹ xác nhận…/)?.[0]);
await nav(1); t = await T(ov('05 Missions')); console.log('MISSIONS TAB:', t.slice(0,400), '| count cards:', (t.match(/Con làm xong rồi|Đang chờ ba mẹ|Ba mẹ đã xác nhận/g)||[]).length);
await toWelcome(); await pg.getByText('Ba mẹ đăng nhập',{exact:true}).click(); await pin('9999'); await pg.waitForTimeout(500);
const P = ov('08 Parent'); t = await T(P); await P.getByText('✓ Xác nhận').first().click().catch(e=>console.log('no approve btn')); await pg.waitForTimeout(200); console.log('after approve:', (await T(P)).match(/Không còn việc nào chờ|\d+ nhiệm vụ đang chờ/)?.[0]);
console.log('PARENT pending:', t.match(/Chờ xác nhận.{0,60}/)?.[0], '| approvals:', (t.match(/Nhiệm vụ thử[^·]{0,40}/g)||[]).slice(0,3));
console.log('creators:', (t.match(/Tạo [^·]{0,30}/g)||[]).slice(0,6));
await P.getByText('Danh mục bài học & nhiệm vụ').first().click(); await pg.waitForTimeout(300);
const C = ov('13 Custom'); await C.getByText('Nhiệm vụ & phần thưởng').click(); await pg.waitForTimeout(300);
t = await T(C); console.log('CUST MIS:', t.slice(t.indexOf('Mỗi bài có'), t.indexOf('Mỗi bài có')+300));
await C.getByText('Một lời xin lỗi đủ ba phần').first().click(); await pg.waitForTimeout(300);
await C.locator('textarea').first().fill('1) Xin lỗi Bo. 2) Dọn bàn. 3) Kể ba mẹ nghe.'); await C.locator('input').nth(1).fill('Đi ăn phở sáng Chủ nhật'); await pg.waitForTimeout(200);
await pg.screenshot({path:S+'w12-mised.png'});
t = await T(C); console.log('EDITOR:', t.slice(t.indexOf('Về danh sách'), t.indexOf('Về danh sách')+250));
// account support block
await toWelcome();
const ws = await T(ov('01 Welcome')); console.log('WELCOME:', ws.match(/admin\.senapp@gmail\.com|mh\.senapp@gmail\.com/g));
await pg.getByText('Quản lý tài khoản').first().click().catch(()=>{}); await pg.waitForTimeout(400);
const mlog = ov('12a Manage login'); if (await mlog.count()) { await mlog.locator('input').first().fill('0901234567'); await mlog.locator('input').nth(1).fill('9999'); await mlog.getByText(/Đăng nhập/).last().click(); await pg.waitForTimeout(500); }
const A = ov('12 Accounts'); if (await A.count()) { t = await T(A); console.log('SUPPORT:', t.match(/Zalo\/Viber hỗ trợ.{0,170}/)?.[0]); console.log('  link:', await A.locator('a[href*="zalo"]').getAttribute('href')); }
// kid sees edited mission
await ov('12 Accounts').getByText('Quay lại').first().click().catch(()=>{}); await pg.waitForTimeout(300); if (!(await pg.getByText('Con đăng nhập',{exact:true}).count())) await toWelcome(); await kidLogin(); await nav(1); console.log('KID MIS:', (await T(ov('05 Missions'))).match(/1\) Xin lỗi Bo[^·]{0,60}|Đi ăn phở[^·]{0,20}/g));
console.log('ERR', errs); await b.close();
