import json, os
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content')
def O(vi, en, c, tv, te): return [vi, en, c, tv, te]
def L(sk, t, m, base, sc, qq, qo, qa, mi):
    s, q, o = sc[base]
    d = {"sk": sk, "t": list(t), "m": [f"{m} phút", f"{m} min"], "base": base,
         "story": list(s), "cq": list(q), "co": o, "qq": list(qq), "qo": [list(x) for x in qo], "qa": qa,
         "ctx": {k: {"s": list(v[0]), "q": list(v[1]), "o": v[2]} for k, v in sc.items() if k != base}}
    mt, ms, lv, rw = mi
    d["mi"] = {"t": list(mt), "s": list(ms), "lv": [list(x) for x in lv], "rw": list(rw)}
    return d
SEQ = [2, 0, 1, 1, 2, 0, 0, 1, 2, 1, 0, 2]
QSEQ = [1, 2, 0, 2, 0, 1, 0, 1, 2, 2, 1, 0]
def _place(o, tgt):
    c = next(x for x in o if x[2] == 1); r = [x for x in o if x is not c]; r.insert(tgt, c); return r
def save(band, wk, lessons):
    k = wk * 5
    for i, d in enumerate(lessons):
        d["co"] = _place(d["co"], SEQ[k % 12]); k += 1
        for c in sorted(d["ctx"]):
            d["ctx"][c]["o"] = _place(d["ctx"][c]["o"], SEQ[k % 12]); k += 1
        t = QSEQ[(wk * 5 + i) % 12]; qo = d["qo"]; ok = qo[d["qa"]]; r = [x for x in qo if x is not ok]; r.insert(t, ok)
        d["qo"] = r; d["qa"] = t
    p = os.path.join(OUT, f"{band}-w{wk}.json")
    json.dump(lessons, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', p)
