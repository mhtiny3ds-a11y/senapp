"""Kiem tra file nhiem vu: python3 validate_m.py content/missions-<band>.json"""
import json, sys, re
bad = 0
for path in sys.argv[1:]:
    try:
        d = json.load(open(path, encoding='utf-8'))
        assert isinstance(d, list) and len(d) == 45, 'can dung 45 nhiem vu'
        for n, m in enumerate(d):
            w = f'nv {n}'
            assert m.get('oi') == n, f'{w}: oi phai bang {n}'
            for f in ('t', 's', 'rw'):
                x = m.get(f); assert isinstance(x, list) and len(x) == 2 and all(isinstance(s, str) and s.strip() for s in x), f'{w}.{f}: [vi, en]'
            lv = m.get('lv'); assert isinstance(lv, list) and len(lv) == 3, f'{w}.lv: 3 muc'
            for k, x in enumerate(lv): assert isinstance(x, list) and len(x) == 2 and all(s.strip() for s in x), f'{w}.lv[{k}]'
            blob = json.dumps(m, ensure_ascii=False); assert '<' not in blob and '{{' not in blob, f'{w}: khong dung < hoac {{{{'
            assert not re.search(r'\d+[.,]?\d*\s*(đ|đồng|k\b|nghìn|VND)', m['rw'][0]), f'{w}: phan thuong khong dung tien'
        print('OK  ', path)
    except Exception as e:
        bad += 1; print('LOI ', path, '->', e)
sys.exit(1 if bad else 0)
