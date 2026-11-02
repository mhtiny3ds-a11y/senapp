import json, os, sys
S = '/tmp/claude-0/-home-user-notebooklm-py/2645776a-48d7-5467-8bed-0fcf75c00226/scratchpad'
sys.path.insert(0, os.path.join(S, 'v11')); import v11 as V
W = json.load(open(os.path.join(S, 'v11', 'week1.json'), encoding='utf-8')); V.fix_week1(W)
SK = ['Giao tiếp','Quản lý cảm xúc','Làm việc nhóm','Tự lập','Giải quyết vấn đề','Tư duy phản biện','An toàn & ranh giới','Quản lý thời gian','Tài chính cá nhân']
out = {'skills': SK, 'bands': []}
for b, label, hero in [('5-8','6–8 tuổi','Bin'),('9-12','9–11 tuổi','An'),('13-16','12–15 tuổi','Khoa')]:
    arr = list(W[b])
    for wk in range(2, 10): arr += json.load(open(os.path.join(S, 'v11', 'content', f'{b}-w{wk}.json'), encoding='utf-8'))
    M = json.load(open(os.path.join(S, 'v11', 'content', f'missions-{b}.json'), encoding='utf-8'))
    L = []
    for oi, l in enumerate(arr):
        cx = []
        for k, c in enumerate('ABC'):
            v = l['ctx'].get(c) or {'s': l['story'], 'q': l['cq'], 'o': l['co']}
            cx.append({'k': k, 's': v['s'][0], 'q': v['q'][0], 'o': [[o[0], o[2], o[3]] for o in v['o']]})
        m = M[oi]
        L.append({'t': l['t'][0], 'sk': l['sk'], 'm': l['m'][0], 'cx': cx, 'qq': l['qq'][0], 'qo': [q[0] for q in l['qo']], 'qa': l['qa'],
                  'mi': {'t': m['t'][0], 's': m['s'][0], 'lv': [x[0] for x in m['lv']], 'rw': m['rw'][0]}})
    out['bands'].append({'id': b, 'label': label, 'hero': hero, 'lessons': L})
json.dump(out, open(os.path.join(S, 'ebook', 'book.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(os.path.getsize(os.path.join(S, 'ebook', 'book.json')))
