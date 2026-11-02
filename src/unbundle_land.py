"""Mo goi file HTML dong goi thanh trang tu chua cho Artifact (ban chay mau)."""
import json, re, sys, gzip, base64
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
t = json.loads(re.search(r'<script type="__bundler/template">(.*?)</script>', s, re.S).group(1))
mf = json.loads(re.search(r'<script type="__bundler/manifest">(.*?)</script>', s, re.S).group(1))
def raw(u):
    d = base64.b64decode(mf[u]['data'])
    return gzip.decompress(d) if mf[u].get('compressed') in (True, 'True', 'true') else d
# script -> inline
def dyn(js):
    b64 = base64.b64encode(js.encode('utf-8')).decode()
    return ('<script>(function(){var s=document.createElement("script");'
            's.textContent=new TextDecoder().decode(Uint8Array.from(atob("' + b64 + '"),function(c){return c.charCodeAt(0)}));'
            'var me=document.currentScript;me.parentNode.insertBefore(s,me);s.remove();me.remove();})()</script>')
def inl(m):
    u = m.group(1); js = raw(u).decode('utf-8')
    if 'function evalDcLogic(src) {' in js:
        js = js.replace('function evalDcLogic(src) {', 'function evalDcLogic(src) {\n    if (window.__dcPrecompiled) return window.__dcPrecompiled(StreamableLogic, StreamableLogic, getReact());', 1)
    if 'unpkg' in js: print('script', u[:8], 'refs unpkg:', sorted(set(re.findall(r'https://unpkg\.com/[^"\'\s)]+', js))))
    b64 = base64.b64encode(js.encode('utf-8')).decode()
    return ('<script>(function(){var s=document.createElement("script");'
            's.textContent=new TextDecoder().decode(Uint8Array.from(atob("' + b64 + '"),function(c){return c.charCodeAt(0)}));'
            'var me=document.currentScript;me.parentNode.insertBefore(s,me);s.remove();me.remove();})()</script>')
t = re.sub(r'<script src="([0-9a-f-]{36})"></script>', inl, t)
# anh, font -> data URI
MASCOT = 'f37ca7cb-1419-41a5-be40-151490144349'
for u, v in mf.items():
    if u not in t: continue
    if u == MASCOT:
        t = t.replace(u, 'data:image/webp;base64,' + base64.b64encode(open('mascot-400.webp','rb').read()).decode()); continue
    t = t.replace(u, 'data:' + v['mime'] + ';base64,' + base64.b64encode(raw(u)).decode())
# bo PWA, doi tieu de
t = re.sub(r'<link rel="(icon|manifest|apple-touch-icon)"[^>]*>\n?|<meta name="(theme-color|apple-mobile-web-app-[a-z-]+|mobile-web-app-capable)"[^>]*>\n?', '', t)
t = t.replace('<title>App Sen – Kỹ năng mềm</title>', '')
# ban xem truoc trang chu
def one(a, b, n=1):
    global t; assert t.count(a) == n, (a, t.count(a)); t = t.replace(a, b)
one("await fetch('https://formsubmit.co/ajax/mh.senapp@gmail.com', {", "await (async () => ({ ok: true, status: 200 }))('ban-xem-truoc', {")
one('href="../"', 'href="https://claude.ai/artifact/7ArVtgo2tEmXyv9KxTnjDA" target="_blank" rel="noopener"', 6)
# nap san logic (khong can eval)
lm = re.search(r'(<script type="text/x-dc"[^>]*>)(.*?)(</script>)', t, re.S)
pre = 'window.__dcPrecompiled = function (DCLogic, StreamableLogic, React) {\n' + lm.group(2) + '\n;return (typeof Component!=="undefined"&&Component)||undefined;\n};'
t = t[:lm.start()] + dyn(pre) + '\n' + t[lm.start():]
# bo khung tai lieu (Artifact tu boc)
t = re.sub(r'<!DOCTYPE html>\s*<html>\s*<head>', '', t, count=1)
t = t.replace('</head>\n<body>', '', 1).replace('</body>', '').replace('</html>', '')
t = '<title>Senapp Trang Chủ</title>\n' + t
left = [u for u in mf if u in t]
open(out, 'w', encoding='utf-8').write(t)
print('ok', out, len(t), 'uuid left:', left)
