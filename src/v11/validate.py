"""Kiem tra file noi dung bai hoc: python3 validate.py content/<band>-w<N>.json [...]"""
import json, sys, re
SCHED = json.load(open(__file__.rsplit('/',1)[0] + '/schedule.json'))
def pair(x, where):
    assert isinstance(x, list) and len(x) == 2 and all(isinstance(s, str) and s.strip() for s in x), f'{where}: can [vi, en] khong rong'
def opts(o, where):
    assert isinstance(o, list) and len(o) == 3, f'{where}: can dung 3 lua chon'
    for k, c in enumerate(o):
        assert isinstance(c, list) and len(c) == 5, f'{where}[{k}]: can [vi, en, 0|1, meo_vi, meo_en]'
        pair(c[:2], f'{where}[{k}]'); pair(c[3:], f'{where}[{k}] meo'); assert c[2] in (0, 1), f'{where}[{k}]: dung/sai phai la 0 hoac 1'
    assert sum(c[2] for c in o) == 1, f'{where}: phai co dung 1 lua chon dung'
bad = 0
for path in sys.argv[1:]:
    try:
        m = re.search(r'(5-8|9-12|13-16)-w(\d+)\.json$', path); assert m, 'ten file phai la <band>-w<N>.json'
        band, wk = m.group(1), int(m.group(2)); assert 2 <= wk <= 9, 'tuan 2..9'
        data = json.load(open(path, encoding='utf-8'))
        assert isinstance(data, list) and len(data) == 5, 'moi file dung 5 bai'
        assert [d.get('sk') for d in data] == SCHED[band][wk-2], f'thu tu ky nang phai la {SCHED[band][wk-2]}'
        for n, d in enumerate(data):
            w = f'bai {n+1}'
            for f in ('t', 'm', 'story', 'cq', 'qq'): pair(d.get(f), f'{w}.{f}')
            opts(d.get('co'), f'{w}.co')
            qo = d.get('qo'); assert isinstance(qo, list) and len(qo) == 3, f'{w}.qo: 3 dap an'
            for k, q in enumerate(qo): pair(q, f'{w}.qo[{k}]')
            assert d.get('qa') in (0, 1, 2), f'{w}.qa'
            base = d.get('base'); assert base in ('A', 'B', 'C'), f'{w}.base phai la A/B/C'
            ctx = d.get('ctx'); assert isinstance(ctx, dict) and set(ctx) == {'A', 'B', 'C'} - {base}, f'{w}.ctx phai co dung 2 boi canh con lai'
            for c, v in ctx.items():
                pair(v.get('s'), f'{w}.ctx.{c}.s'); pair(v.get('q'), f'{w}.ctx.{c}.q'); opts(v.get('o'), f'{w}.ctx.{c}.o')
            blob = json.dumps(d, ensure_ascii=False)
            assert '<' not in blob and '{{' not in blob, f'{w}: khong dung ky tu < hoac {{{{'
        print('OK  ', path)
    except Exception as e:
        bad += 1; print('LOI ', path, '->', e)
sys.exit(1 if bad else 0)
