"""Senapp v14 (ap dung tren v13): dong (c) + trang Dieu khoan su dung; thu gon & lam roi ma App.
Dung: python3 v14.py <thu muc ban build>   (sua index.html, trang-chu/index.html, them dieu-khoan/index.html)"""
import json, re, sys, os, base64, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
TERSER = os.path.join(HERE, 'tools', 'node_modules', '.bin', 'terser')
COPY = '© 2026 Senapp. Bảo lưu mọi quyền.'
KEY = 'senapp-sen'

def sub(h, a, b, n=1):
    c = h.count(a); assert c == n, (a[:120], c); return h.replace(a, b)

def landing(t):
    t = sub(t, '<div style="font-size:14px;line-height:1.7">Bảo vệ dữ liệu cá nhân theo Luật 91/2025/QH15 · Điều khoản sử dụng</div>',
               '<div style="font-size:14px;line-height:1.7">Bảo vệ dữ liệu cá nhân theo Luật 91/2025/QH15 · <a href="../dieu-khoan/" style="font-weight:700;text-decoration:underline">Điều khoản sử dụng</a></div>')
    t = sub(t, '<div style="font-size:12.5px;color:#8B7867">© 2026 Senapp · senapp.com</div>',
               '<div style="font-size:12.5px;color:#8B7867;line-height:1.6;max-width:62ch">' + COPY + ' Nội dung, bài học, hình ảnh và linh vật Sen được bảo hộ quyền tác giả; nghiêm cấm sao chép dưới mọi hình thức khi chưa được cho phép. · <a href="../dieu-khoan/" style="text-decoration:underline">Điều khoản sử dụng</a></div>')
    t = sub(t, '<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="copyright" content="' + COPY + '">')
    return t

def encode_L(js):
    # lam roi du lieu bai hoc: dich ma tung ky tu (+3), van nen gzip tot (khong dung base64)
    a = js.index('const L = {'); b = js.index('const STAGES') if 'const STAGES' in js else js.index('const SEASONS')
    src = js[a + len('const L = '):b].strip().rstrip(';')
    src = re.sub(r"^'(5-8|9-12|13-16)':", r'"\1":', src, flags=re.M)
    data = json.dumps(json.loads(src), ensure_ascii=False, separators=(',', ':'))
    u = data.encode('utf-16-le'); units = [u[n] | (u[n + 1] << 8) for n in range(0, len(u), 2)]
    assert not any(0x3000 <= x < 0x3003 for x in units)
    enc = bytes(b for x in units for b in ((x + 3 if x < 0x3000 else x).to_bytes(2, 'little'))).decode('utf-16-le', 'surrogatepass')
    lit = json.dumps(enc, ensure_ascii=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    dec = ('const L = (s => { let o = ""; for (let n = 0; n < s.length; n++) { const c = s.charCodeAt(n); o += String.fromCharCode(c < 0x3003 ? c - 3 : c); } '
           'return JSON.parse(o); })(' + lit + ');\n')
    return js[:a] + dec + js[b:]

def minify(js):
    tmp_in, tmp_out = os.path.join(HERE, 'tools', 'in.js'), os.path.join(HERE, 'tools', 'out.js')
    open(tmp_in, 'w', encoding='utf-8').write(js)
    subprocess.run([TERSER, tmp_in, '-o', tmp_out, '--ecma', '2020', '--compress', 'passes=2', '--mangle',
                    '--keep-classnames', '--comments', 'false'], check=True)
    out = open(tmp_out, encoding='utf-8').read()
    assert 'class Component extends DCLogic' in out, 'mat ten lop Component'
    out = out.replace('</', '<\\/')  # khong de '</' trong the script
    return '/*! ' + COPY + ' Nghiêm cấm sao chép, dịch ngược. */\n' + out

def app(t):
    t = sub(t, '{{ wcHelp }} <a href="mailto:admin.senapp@gmail.com" style="font-weight:700">admin.senapp@gmail.com</a></div>',
               '{{ wcHelp }} <a href="mailto:admin.senapp@gmail.com" style="font-weight:700">admin.senapp@gmail.com</a><br>' + COPY + ' · <a href="dieu-khoan/" style="font-weight:700">Điều khoản sử dụng</a></div>', 2)
    t = sub(t, '<div class="app-foot" style="max-width:540px;text-align:center;font-size:12px;color:#8B7867;line-height:1.6">{{ footerHint }}</div>',
               '<div class="app-foot" style="max-width:540px;text-align:center;font-size:12px;color:#8B7867;line-height:1.6">{{ footerHint }}<br>' + COPY + ' · <a href="dieu-khoan/">Điều khoản sử dụng</a></div>')
    t = sub(t, '<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="copyright" content="' + COPY + '">')
    if os.environ.get('SEN_NOMIN') == '1': return t  # ban chay mau tren Claude: giu ma doc duoc de dong goi
    m = re.search(r'(<script type="text/x-dc"[^>]*>)(.*?)(</script>)', t, re.S)
    js = minify(encode_L(m.group(2)))
    assert '</' not in js.replace('<\\/', ''), 'co chuoi </ trong ma'
    return t[:m.start(2)] + js + t[m.end(2):]

def patch(path, fn):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', s, re.S)
    t = fn(json.loads(m.group(2)))
    s = s[:m.start(2)] + json.dumps(t, ensure_ascii=False).replace('</', '<\\/') + s[m.end(2):]
    open(path, 'w', encoding='utf-8').write(s); print('ok', path, len(s))

if __name__ == '__main__':
    d = sys.argv[1]
    patch(os.path.join(d, 'trang-chu', 'index.html'), landing)
    patch(os.path.join(d, 'index.html'), app)
    os.makedirs(os.path.join(d, 'dieu-khoan'), exist_ok=True)
    shutil.copy(os.path.join(HERE, 'legal', 'dieu-khoan.html'), os.path.join(d, 'dieu-khoan', 'index.html'))
    print('ok dieu-khoan')
