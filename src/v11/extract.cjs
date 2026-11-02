// Xuat 15 bai goc + boi canh ra JSON (dinh dang giong file noi dung moi)
const fs = require('fs');
const tpl = fs.readFileSync(process.argv[2], 'utf8'), vjs = fs.readFileSync(process.argv[3], 'utf8');
const a = tpl.indexOf('const L = {'), b = tpl.indexOf('const SEASONS');
const L = new Function(tpl.slice(a, b) + '; return L;')();
const window = {}; new Function('window', vjs)(window);
const V = window.SEN_VARIANTS, out = {};
for (const band of Object.keys(L)) out[band] = L[band].map((l, i) => {
  const vs = V[band][i], baseIdx = vs.indexOf(null), ctx = {};
  vs.forEach((v, k) => { if (v) ctx['ABC'[k]] = v; });
  return { sk:l.sk, t:l.t, m:l.m, base:'ABC'[baseIdx], story:l.story, cq:l.cq, co:l.co, qq:l.qq, qo:l.qo, qa:l.qa, ctx };
});
fs.writeFileSync(process.argv[4], JSON.stringify(out, null, 1));
console.log(Object.entries(out).map(([k, v]) => k + ':' + v.length).join(' '));
