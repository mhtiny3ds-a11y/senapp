import json, os
OUT = '/tmp/claude-0/-home-user-notebooklm-py/2645776a-48d7-5467-8bed-0fcf75c00226/scratchpad/y12/content'
def L(sk, t, m, base, story, cq, co, qq, qo, qa, ctx, mi):
    return {"sk": sk, "t": list(t), "m": [m + " phút", m + " min"], "base": base,
            "story": list(story), "cq": list(cq), "co": [list(c) for c in co],
            "qq": list(qq), "qo": [list(q) for q in qo], "qa": qa,
            "ctx": {k: {"s": list(v[0]), "q": list(v[1]), "o": [list(c) for c in v[2]]} for k, v in ctx.items()},
            "mi": {"t": list(mi[0]), "s": list(mi[1]), "lv": [list(x) for x in mi[2]], "rw": list(mi[3])}}
def _mv(o, t):
    c = [x for x in o if x[2] == 1][0]; r = [x for x in o if x[2] == 0]
    r.insert(t, c); return r
def save(wk, lessons):
    for i, x in enumerate(lessons):
        n = wk + i
        x['co'] = _mv(x['co'], n % 3)
        for j, k in enumerate(sorted(x['ctx'])):
            x['ctx'][k]['o'] = _mv(x['ctx'][k]['o'], (n + 1 + j) % 3)
    with open(os.path.join(OUT, f'9-12-w{wk}.json'), 'w', encoding='utf-8') as f:
        json.dump(lessons, f, ensure_ascii=False, indent=1)
def swap(x, nb):
    ob = x['base']; c = x['ctx'].pop(nb)
    x['ctx'][ob] = {"s": x['story'], "q": x['cq'], "o": x['co']}
    x['story'], x['cq'], x['co'], x['base'] = c['s'], c['q'], c['o'], nb
    x['ctx'] = dict(sorted(x['ctx'].items()))
    return x
