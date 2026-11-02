// Senapp – may chu Node.js cho Vibe Code Hosting (Tenten).
// Khong can thu vien ngoai: chi dung http, fs, path, zlib co san cua Node.js.
// Phat website tinh trong thu muc public/:  /  = App Sen,  /trang-chu/ = trang ban hang.
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const PORT = process.env.PORT || 3000;
const ROOT = path.join(__dirname, 'public');
const FORCE_HTTPS = process.env.FORCE_HTTPS === '1'; // bat neu hosting chua tu chuyen http -> https

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.webmanifest': 'application/manifest+json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.pdf': 'application/pdf',
  '.woff2': 'font/woff2',
  '.txt': 'text/plain; charset=utf-8',
};
const COMPRESSIBLE = new Set(['.html', '.js', '.css', '.json', '.webmanifest', '.svg', '.txt']);
const gzCache = new Map(); // duong dan -> { mtimeMs, buf }

function cacheControl(ext, rel) {
  if (rel === '/sw.js') return 'no-cache';                 // ban cap nhat moi toi tay nguoi dung ngay
  if (ext === '.html' || ext === '.webmanifest') return 'no-cache';
  return 'public, max-age=604800';                        // anh, PDF, icon: 7 ngay
}

function send(res, status, body, headers) {
  res.writeHead(status, Object.assign({
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
  }, headers));
  res.end(body);
}

function resolveFile(urlPath) {
  let rel;
  try { rel = decodeURIComponent(urlPath.split('?')[0].split('#')[0]); } catch (e) { return null; }
  const full = path.normalize(path.join(ROOT, rel));
  if (full !== ROOT && !full.startsWith(ROOT + path.sep)) return null; // chan ../ thoat ra ngoai public/
  return { rel, full };
}

const server = http.createServer((req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, 'Method Not Allowed', { Allow: 'GET, HEAD' });

  if (FORCE_HTTPS && req.headers['x-forwarded-proto'] === 'http') {
    return send(res, 301, '', { Location: 'https://' + req.headers.host + req.url });
  }
  if (req.url === '/healthz') return send(res, 200, 'ok', { 'Content-Type': 'text/plain' });

  const r = resolveFile(req.url);
  if (!r) return send(res, 400, 'Bad Request', { 'Content-Type': 'text/plain' });

  fs.stat(r.full, (err, st) => {
    let file = r.full, rel = r.rel;
    if (!err && st.isDirectory()) {
      if (!rel.endsWith('/')) return send(res, 301, '', { Location: rel + '/' + (req.url.includes('?') ? req.url.slice(req.url.indexOf('?')) : '') });
      file = path.join(r.full, 'index.html'); rel = rel + 'index.html';
    }
    fs.stat(file, (err2, st2) => {
      if (err2 || !st2.isFile()) {
        return send(res, 404, '<!doctype html><meta charset="utf-8"><title>Không tìm thấy trang</title>'
          + '<body style="font-family:sans-serif;text-align:center;padding:60px 16px;background:#FFF8EF;color:#221A15">'
          + '<h1 style="color:#C8102E">Không tìm thấy trang</h1><p>Trang này không có trên Senapp.</p>'
          + '<p><a href="/" style="color:#C8102E;font-weight:700">Mở App Sen</a> · <a href="/trang-chu/" style="color:#C8102E;font-weight:700">Trang chủ</a></p></body>',
          { 'Content-Type': 'text/html; charset=utf-8' });
      }
      const ext = path.extname(file).toLowerCase();
      const headers = {
        'Content-Type': TYPES[ext] || 'application/octet-stream',
        'Cache-Control': cacheControl(ext, rel),
        'Last-Modified': st2.mtime.toUTCString(),
      };
      if (rel === '/sw.js') headers['Service-Worker-Allowed'] = '/';
      if (req.headers['if-modified-since'] && new Date(req.headers['if-modified-since']) >= new Date(st2.mtime.toUTCString())) {
        return send(res, 304, '', headers);
      }
      const wantsGz = COMPRESSIBLE.has(ext) && /\bgzip\b/.test(req.headers['accept-encoding'] || '');
      if (wantsGz) {
        const hit = gzCache.get(file);
        const done = (buf) => { headers['Content-Encoding'] = 'gzip'; headers['Vary'] = 'Accept-Encoding'; headers['Content-Length'] = buf.length;
          send(res, 200, req.method === 'HEAD' ? '' : buf, headers); };
        if (hit && hit.mtimeMs === st2.mtimeMs) return done(hit.buf);
        return fs.readFile(file, (e, data) => {
          if (e) return send(res, 500, 'Server Error', { 'Content-Type': 'text/plain' });
          zlib.gzip(data, { level: 9 }, (ze, buf) => { if (ze) return send(res, 500, 'Server Error', { 'Content-Type': 'text/plain' });
            gzCache.set(file, { mtimeMs: st2.mtimeMs, buf }); done(buf); });
        });
      }
      headers['Content-Length'] = st2.size;
      res.writeHead(200, Object.assign({ 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'strict-origin-when-cross-origin' }, headers));
      if (req.method === 'HEAD') return res.end();
      fs.createReadStream(file).pipe(res);
    });
  });
});

server.listen(PORT, () => console.log('Senapp dang chay tai cong ' + PORT));
