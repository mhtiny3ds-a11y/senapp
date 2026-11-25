"""Nhung san font cho cac trang ngoai App (chay sau v14).
App va trang chu da mang san font (woff2) ben trong tep. Buoc nay tach dung cac tep font do
ra thu muc fonts/ va gan vao trang Dieu khoan, de khong trang nao phai tai font tu Google.
Dung: python3 fonts.py <thu muc ban build>"""
import base64, gzip, json, os, re, sys

KEEP = {('Be Vietnam Pro', '400'), ('Be Vietnam Pro', '700'), ('Baloo 2', '800')}
SUBSETS = ('vietnamese', 'latin-ext', 'latin')


def extract(app_html):
    s = open(app_html, encoding='utf-8').read()
    t = json.loads(re.search(r'<script type="__bundler/template">(.*?)</script>', s, re.S).group(1))
    mf = json.loads(re.search(r'<script type="__bundler/manifest">(.*?)</script>', s, re.S).group(1))
    out = []
    for sub, body in re.findall(r'/\* (\S+) \*/\s*@font-face \{(.*?)\}', t, re.S):
        fam = re.search(r"font-family: '([^']+)'", body).group(1)
        w = re.search(r'font-weight: (\d+)', body).group(1)
        uid = re.search(r'src: url\("([0-9a-f-]{36})"\)', body).group(1)
        rng = re.search(r'unicode-range: ([^;]+);', body).group(1)
        if (fam, w) not in KEEP or sub not in SUBSETS: continue
        v = mf[uid]; data = base64.b64decode(v['data'])
        if v.get('compressed') in (True, 'True', 'true'): data = gzip.decompress(data)
        assert data[:4] == b'wOF2', (fam, w, sub)
        out.append((fam, w, sub, rng, data))
    assert len(out) == len(KEEP) * len(SUBSETS), len(out)
    return out


def main(d):
    faces = extract(os.path.join(d, 'index.html'))
    os.makedirs(os.path.join(d, 'fonts'), exist_ok=True)
    css = []
    for fam, w, sub, rng, data in faces:
        name = fam.lower().replace(' ', '-') + '-' + w + '-' + sub + '.woff2'
        open(os.path.join(d, 'fonts', name), 'wb').write(data)
        css.append("@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;src:url(../fonts/%s) format('woff2');unicode-range:%s}" % (fam, w, name, rng))
    p = os.path.join(d, 'dieu-khoan', 'index.html'); h = open(p, encoding='utf-8').read()
    css.append("body{font-family:'Be Vietnam Pro',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}.brand,h1,h2{font-family:'Baloo 2','Be Vietnam Pro',sans-serif}")
    assert h.count('</head>') == 1
    h = h.replace('</head>', '<style>/* font nhung san (SIL OFL 1.1, xem OFL-fonts.txt) */\n' + '\n'.join(css) + '</style>\n</head>')
    open(p, 'w', encoding='utf-8').write(h)
    print('ok fonts', len(faces), 'tep ->', os.path.join(d, 'fonts'))


if __name__ == '__main__':
    main(sys.argv[1])
