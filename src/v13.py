"""Senapp v13: thay cau ca dao tren trang chu bang ca bai ca dao 4 cau. Dung: python3 v13.py <landing index.html>"""
import json, re, sys
OLD = '<div style="font-family:\'Baloo 2\',cursive;font-weight:700;font-size:clamp(22px,2.4vw,28px);line-height:1.3;color:#C8102E">“Gần bùn mà chẳng hôi tanh mùi bùn”</div>\n        <div style="font-size:13.5px;color:#7A6A5C;margin-top:6px">Câu ca dao về hoa sen mà người Việt nào cũng thuộc từ thuở nhỏ.</div>'
NEW = '<div style="font-family:\'Baloo 2\',cursive;font-weight:700;font-size:clamp(16px,4.2vw,26px);line-height:1.5;color:#C8102E">Trong đầm gì đẹp bằng sen,<br>Lá xanh bông trắng lại chen nhị vàng.<br>Nhị vàng bông trắng lá xanh,<br>Gần bùn mà chẳng hôi tanh mùi bùn.</div>\n        <div style="font-size:13.5px;color:#7A6A5C;margin-top:8px">Bài ca dao về hoa sen mà người Việt nào cũng thuộc từ thuở nhỏ.</div>'
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', s, re.S)
t = json.loads(m.group(2))
if NEW in t: print('da patch'); sys.exit()
assert t.count(OLD) == 1; t = t.replace(OLD, NEW)
s = s[:m.start(2)] + json.dumps(t, ensure_ascii=False).replace('</', '<\\/') + s[m.end(2):]
open(p, 'w', encoding='utf-8').write(s); print('ok', p)
