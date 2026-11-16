// Tao ma tran QR cho cac muc "Moi Sen ly Coffee" (cung tai khoan voi 3 app Bamedonghanh).
// Dung: node src/donate/gen.cjs > src/donate/donate.json
const qrcode = require('./qrcode.js');
const DONATE = { name: 'TAO MINH HIEN', acct: '141431319191', bank: 'MB Bank' };
// Noi dung ma QR goc cua tai khoan (lay tu app Toan Vui cung Pi)
const DONATE_PAYLOAD = '00020101021138570010A000000727012700069704220113VQRQAGLRC30780208QRIBFTTA53037045802VN62150107NPS686908006304F754';
const LEVELS = [
  { name: 'Sữa đá', amount: 40000, slug: 'sua-da' },
  { name: 'Latte', amount: 56000, slug: 'latte' },
  { name: 'Cà phê Muối', amount: 66000, slug: 'ca-phe-muoi' }
];
const NOTE = 'Thank you Sen nha';
function emvCrc(str) { let c = 0xFFFF; for (const ch of str) { c ^= ch.charCodeAt(0) << 8; for (let i = 0; i < 8; i++) c = c & 0x8000 ? ((c << 1) ^ 0x1021) & 0xFFFF : (c << 1) & 0xFFFF; } return c.toString(16).toUpperCase().padStart(4, '0'); }
function tlvParse(s) { const out = []; let i = 0; while (i + 4 <= s.length) { const tag = s.slice(i, i + 2), len = +s.slice(i + 2, i + 4); out.push([tag, s.slice(i + 4, i + 4 + len)]); i += 4 + len; } return out; }
const tlvBuild = arr => arr.map(([t, v]) => t + String(v.length).padStart(2, '0') + v).join('');
function payload(amount) {
  let f = tlvParse(DONATE_PAYLOAD).filter(([t]) => t !== '63' && t !== '54');
  f = f.map(([t, v]) => {
    if (t === '01') return [t, '12'];
    if (t === '62') { const sub = tlvParse(v).filter(([k]) => k !== '08'); sub.push(['08', NOTE]); sub.sort((a, b) => a[0].localeCompare(b[0])); return [t, tlvBuild(sub)]; }
    return [t, v];
  });
  f.push(['54', String(amount)]); f.sort((a, b) => a[0].localeCompare(b[0]));
  const body = tlvBuild(f) + '6304'; return body + emvCrc(body);
}
const matrix = p => { const q = qrcode(0, 'M'); q.addData(p); q.make(); const n = q.getModuleCount(); let rows = [];
  for (let r = 0; r < n; r++) { let s = ''; for (let c = 0; c < n; c++) s += q.isDark(r, c) ? '1' : '0'; rows.push(s); } return rows; };
// tu kiem tra: ma goc phai co CRC dung
const base = DONATE_PAYLOAD.slice(0, -4); if (emvCrc(base) !== DONATE_PAYLOAD.slice(-4)) throw new Error('CRC ma goc sai');
console.log(JSON.stringify({ donate: DONATE, note: NOTE, levels: LEVELS.map(l => ({ ...l, payload: payload(l.amount), qr: matrix(payload(l.amount)) })) }));
