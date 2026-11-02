"""Kiem tra bai hoc 12 thang: python3 validate.py content/<band>-w<N>.json [...]"""
import json, sys, re, os
H = os.path.dirname(os.path.abspath(__file__))
SCHED = json.load(open(os.path.join(H, 'schedule.json')))
def pair(x, w):
    assert isinstance(x, list) and len(x) == 2 and all(isinstance(s, str) and s.strip() for s in x), f'{w}: can [vi, en] khong rong'
def opts(o, w):
    assert isinstance(o, list) and len(o) == 3, f'{w}: can dung 3 lua chon'
    for k, c in enumerate(o):
        assert isinstance(c, list) and len(c) == 5, f'{w}[{k}]: can [vi, en, 0|1, meo_vi, meo_en]'
        pair(c[:2], f'{w}[{k}]'); pair(c[3:], f'{w}[{k}] meo'); assert c[2] in (0, 1), f'{w}[{k}]: 0|1'
    assert sum(c[2] for c in o) == 1, f'{w}: dung 1 lua chon dung'
bad = 0
for path in sys.argv[1:]:
    try:
        m = re.search(r'(5-8|9-12)-w(\d+)\.json$', path); assert m, 'ten file <band>-w<N>.json'
        band, wk = m.group(1), int(m.group(2)); assert 10 <= wk <= 48, 'tuan 10..48'
        plan = json.load(open(os.path.join(H, 'plan', band + '.json'), encoding='utf-8'))['weeks'][str(wk)]
        d = json.load(open(path, encoding='utf-8')); assert isinstance(d, list) and len(d) == 5, '5 bai'
        assert [x.get('sk') for x in d] == SCHED[str(wk)], f'thu tu ky nang phai la {SCHED[str(wk)]}'
        for n, x in enumerate(d):
            w = f'bai {n+1}'
            for f in ('t', 'm', 'story', 'cq', 'qq'): pair(x.get(f), f'{w}.{f}')
            opts(x.get('co'), f'{w}.co')
            qo = x.get('qo'); assert isinstance(qo, list) and len(qo) == 3, f'{w}.qo'
            for k, q in enumerate(qo): pair(q, f'{w}.qo[{k}]')
            assert x.get('qa') in (0, 1, 2), f'{w}.qa'
            base = x.get('base'); assert base in ('A', 'B', 'C'), f'{w}.base'
            ctx = x.get('ctx'); assert isinstance(ctx, dict) and set(ctx) == {'A', 'B', 'C'} - {base}, f'{w}.ctx'
            for c, v in ctx.items(): pair(v.get('s'), f'{w}.ctx.{c}.s'); pair(v.get('q'), f'{w}.ctx.{c}.q'); opts(v.get('o'), f'{w}.ctx.{c}.o')
            mi = x.get('mi'); assert isinstance(mi, dict), f'{w}.mi'
            for f in ('t', 's', 'rw'): pair(mi.get(f), f'{w}.mi.{f}')
            assert isinstance(mi.get('lv'), list) and len(mi['lv']) == 3, f'{w}.mi.lv'
            for k, y in enumerate(mi['lv']): pair(y, f'{w}.mi.lv[{k}]')
            assert not re.search(r'\d+[.,]?\d*\s*(đ|đồng|k\b|nghìn|VND)', mi['rw'][0]), f'{w}: phan thuong khong dung tien'
            blob = json.dumps(x, ensure_ascii=False); assert '<' not in blob and '{{' not in blob, f'{w}: khong dung < hoac {{{{'
            assert "'" not in blob, f"{w}: khong dung nhay thang ' (dung ’)"
        print('OK  ', path)
    except Exception as e:
        bad += 1; print('LOI ', path, '->', e)
sys.exit(1 if bad else 0)
