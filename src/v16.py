"""Senapp v16 (ap dung tren v15, truoc v14): 12 thang noi dung (48 tuan x 5 bai cho 6-8 & 9-11),
bang gia moi (299k/6 thang, 499k/nam, them con -50%, bo Classic & hoa hong), danh muc bai/nhiem vu cho ba me:
tim kiem, loc ky nang, nhom theo chang, an/hien, them bai moi vao tuan bat ky, xoa bai tu tao, them/bot lua chon, tinh huong, dap an.
Dung: python3 v16.py <thu muc ban build>"""
import json, re, sys, os
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(S, 'v11')); import v11 as V
Y12 = os.environ.get('Y12', os.path.join(S, 'y12'))

def sub(h, a, b, n=1):
    c = h.count(a); assert c == n, (a[:140], c); return h.replace(a, b)

# ---------------- du lieu ----------------
def lesson_obj(l, oi, mi):
    cx = []
    for k, c in enumerate('ABC'):
        v = l['ctx'].get(c) or (l['base'] == c and {'s': l['story'], 'q': l['cq'], 'o': l['co']})
        assert v, (oi, c); cx.append({'k': k, 's': v['s'], 'q': v['q'], 'o': v['o']})
    return {'t': l['t'], 'sk': l['sk'], 'm': l['m'], 'oi': oi, 'story': cx[0]['s'], 'cq': cx[0]['q'], 'co': cx[0]['o'],
            'qq': l['qq'], 'qo': l['qo'], 'qa': l['qa'], 'cx': cx, 'mi': {'t': mi['t'], 's': mi['s'], 'rw': mi['rw'], 'lv': mi['lv']}}

def build_data():
    W = json.load(open(os.path.join(S, 'v11', 'week1.json'), encoding='utf-8')); V.fix_week1(W)
    L, STG = {}, {}
    for b in V.BANDS:
        arr = list(W[b])
        for wk in range(2, 10): arr += json.load(open(os.path.join(S, 'v11', 'content', f'{b}-w{wk}.json'), encoding='utf-8'))
        M = json.load(open(os.path.join(S, 'v11', 'content', f'missions-{b}.json'), encoding='utf-8'))
        out = [lesson_obj(l, oi, M[oi]) for oi, l in enumerate(arr)]
        if b in ('5-8', '9-12'):
            for wk in range(10, 49):
                for l in json.load(open(os.path.join(Y12, 'content', f'{b}-w{wk}.json'), encoding='utf-8')):
                    out.append(lesson_obj(l, len(out), l['mi']))
            assert len(out) == 240, (b, len(out))
            plan = json.load(open(os.path.join(Y12, 'plan', f'{b}.json'), encoding='utf-8'))
            STG[b] = [c['theme'] for c in sorted(plan['chang'], key=lambda c: c['n'])]
            assert len(STG[b]) == 12
        else:
            STG[b] = ['Nói “không” và giữ mình', 'Tự chủ và kế hoạch', 'Tự lập và tiền bạc']
        L[b] = out
    js = 'const L = {\n' + ',\n'.join(f"'{b}': [\n" + ',\n'.join(json.dumps(x, ensure_ascii=False) for x in L[b]) + '\n]' for b in V.BANDS) + '\n};\n'
    js += 'const STAGES = ' + json.dumps(STG, ensure_ascii=False) + ';\n\n'
    return js

# ---------------- giao dien danh muc ----------------
SBTN = V.SBTN
LBL = V.LBL
INP = V.INP
ROW = """<div style="{{{{ r.card }}}}">
                            <div style="{{{{ r.dot }}}}">{{{{ r.n }}}}</div>
                            <div sc-camel-on-click="{{{{ r.edit }}}}" style="flex:1;min-width:0;cursor:pointer">
                              <div style="font-size:14px;font-weight:700;color:#221A15;line-height:1.3">{{{{ r.title }}}}</div>
                              <div style="font-size:11.5px;color:#8B7867;margin-top:2px">{{{{ r.sub }}}}</div>
                              <div style="font-size:11.5px;color:#8F6A1E;margin-top:2px">🎯 {{{{ r.mis }}}}</div>
                            </div>
                            <div style="display:flex;gap:4px;flex:none;flex-wrap:wrap;justify-content:flex-end;max-width:72px">
                              <div sc-camel-on-click="{{{{ r.up }}}}" aria-label="{{{{ r.upLabel }}}}" style="{{{{ r.upStyle }}}}">↑</div>
                              <div sc-camel-on-click="{{{{ r.down }}}}" aria-label="{{{{ r.downLabel }}}}" style="{{{{ r.downStyle }}}}">↓</div>
                              <div sc-camel-on-click="{{{{ r.hide }}}}" aria-label="{{{{ r.hideLabel }}}}" style="{SBTN}">{{{{ r.hideIcon }}}}</div>
                              <div sc-camel-on-click="{{{{ r.edit }}}}" aria-label="{{{{ r.editLabel }}}}" style="{SBTN};background:#FBE3E7;color:#C8102E">✎</div>
                            </div>
                          </div>""".format(SBTN=SBTN)

CATALOG = f"""<sc-if value="{{{{ cuShowList }}}}" hint-placeholder-val="{{{{ true }}}}">
              <div style="display:flex;flex-direction:column;gap:10px">
                <div style="display:flex;gap:6px;flex-wrap:wrap">
                  <sc-for list="{{{{ cuBands }}}}" as="x" hint-placeholder-count="3">
                    <div sc-camel-on-click="{{{{ x.pick }}}}" style="{{{{ x.style }}}}">{{{{ x.label }}}}</div>
                  </sc-for>
                </div>
                <input value="{{{{ cuQ }}}}" sc-camel-on-change="{{{{ cuOnQ }}}}" placeholder="{{{{ cuQPh }}}}" aria-label="{{{{ cuQPh }}}}" style="{INP}">
                <div style="display:flex;gap:5px;flex-wrap:wrap">
                  <sc-for list="{{{{ cuSkills }}}}" as="x" hint-placeholder-count="10">
                    <div sc-camel-on-click="{{{{ x.pick }}}}" style="{{{{ x.style }}}}">{{{{ x.label }}}}</div>
                  </sc-for>
                </div>
                <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
                  <div style="flex:1;min-width:160px;font-size:12px;color:#8B7867;line-height:1.5">{{{{ cuListHint }}}}</div>
                  <div sc-camel-on-click="{{{{ cuHidToggle }}}}" style="{{{{ cuHidStyle }}}}">{{{{ cuHidLabel }}}}</div>
                </div>
                <sc-if value="{{{{ cuBrowse }}}}" hint-placeholder-val="{{{{ true }}}}">
                  <sc-for list="{{{{ cuStages }}}}" as="g" hint-placeholder-count="3">
                    <div style="display:flex;flex-direction:column;gap:8px">
                      <div sc-camel-on-click="{{{{ g.toggle }}}}" style="{{{{ g.head }}}}">
                        <div style="flex:1;min-width:0">
                          <div style="font-size:11px;font-weight:800;letter-spacing:.06em;color:#C8102E">{{{{ g.kicker }}}}</div>
                          <div style="font-family:'Baloo 2',cursive;font-size:16px;font-weight:800;color:#221A15;line-height:1.2">{{{{ g.theme }}}}</div>
                        </div>
                        <div style="font-size:18px;color:#8B7867;flex:none">{{{{ g.chev }}}}</div>
                      </div>
                      <sc-if value="{{{{ g.open }}}}" hint-placeholder-val="{{{{ false }}}}">
                        <sc-for list="{{{{ g.weeks }}}}" as="w" hint-placeholder-count="4">
                          <div style="display:flex;flex-direction:column;gap:6px;padding-left:4px">
                            <div style="display:flex;align-items:center;gap:8px">
                              <div style="flex:1;font-family:'Baloo 2',cursive;font-size:15px;font-weight:800;color:#5C4B3C">{{{{ w.title }}}}</div>
                              <div sc-camel-on-click="{{{{ w.add }}}}" style="font-size:12px;font-weight:700;color:#C8102E;cursor:pointer;padding:4px 8px;border:1.5px dashed #C8102E;border-radius:99px">{{{{ w.addLabel }}}}</div>
                            </div>
                            <sc-for list="{{{{ w.rows }}}}" as="r" hint-placeholder-count="5">
                          {ROW}
                            </sc-for>
                          </div>
                        </sc-for>
                      </sc-if>
                    </div>
                  </sc-for>
                </sc-if>
                <sc-if value="{{{{ cuSearching }}}}" hint-placeholder-val="{{{{ false }}}}">
                  <div style="font-size:12.5px;font-weight:700;color:#5C4B3C">{{{{ cuFound }}}}</div>
                  <sc-for list="{{{{ cuResults }}}}" as="r" hint-placeholder-count="3">
                          {ROW}
                  </sc-for>
                </sc-if>
              </div>
            </sc-if>

            """

MISROW = """<div sc-camel-on-click="{{ r.editMi }}" style="{{ r.card }}">
                            <div style="{{ r.dot }}">{{ r.n }}</div>
                            <div style="flex:1;min-width:0">
                              <div style="font-size:11px;color:#8B7867">{{ r.lessonLine }}</div>
                              <div style="font-size:14px;font-weight:700;color:#221A15;line-height:1.3;margin-top:1px">{{ r.misTitle }}</div>
                              <div style="font-size:11.5px;color:#8F6A1E;margin-top:3px">🎁 {{ r.rw }}</div>
                            </div>
                            <div style="%s;background:#FBE3E7;color:#C8102E">✎</div>
                          </div>""" % SBTN

MIS_TAB = f"""<sc-if value="{{{{ cuShowMis }}}}" hint-placeholder-val="{{{{ false }}}}">
              <div style="display:flex;flex-direction:column;gap:10px">
                <div style="display:flex;gap:6px;flex-wrap:wrap">
                  <sc-for list="{{{{ cuBands }}}}" as="x" hint-placeholder-count="3">
                    <div sc-camel-on-click="{{{{ x.pick }}}}" style="{{{{ x.style }}}}">{{{{ x.label }}}}</div>
                  </sc-for>
                </div>
                <div style="font-size:12px;color:#8B7867;line-height:1.5">{{{{ cuMisHint }}}}</div>
                <sc-for list="{{{{ cuStages }}}}" as="g" hint-placeholder-count="3">
                  <div style="display:flex;flex-direction:column;gap:8px">
                    <div sc-camel-on-click="{{{{ g.toggle }}}}" style="{{{{ g.head }}}}">
                      <div style="flex:1;min-width:0">
                        <div style="font-size:11px;font-weight:800;letter-spacing:.06em;color:#C8102E">{{{{ g.kicker }}}}</div>
                        <div style="font-family:'Baloo 2',cursive;font-size:16px;font-weight:800;color:#221A15;line-height:1.2">{{{{ g.theme }}}}</div>
                      </div>
                      <div style="font-size:18px;color:#8B7867;flex:none">{{{{ g.chev }}}}</div>
                    </div>
                    <sc-if value="{{{{ g.open }}}}" hint-placeholder-val="{{{{ false }}}}">
                      <sc-for list="{{{{ g.weeks }}}}" as="w" hint-placeholder-count="4">
                        <div style="display:flex;flex-direction:column;gap:6px;padding-left:4px">
                          <div style="font-family:'Baloo 2',cursive;font-size:15px;font-weight:800;color:#5C4B3C">{{{{ w.title }}}}</div>
                          <sc-for list="{{{{ w.rows }}}}" as="r" hint-placeholder-count="5">
                          {MISROW}
                          </sc-for>
                        </div>
                      </sc-for>
                    </sc-if>
                  </div>
                </sc-for>
              </div>
            </sc-if>

            """

def mini_btn(val, label_key, style='font-size:12.5px;font-weight:700;color:#C8102E;cursor:pointer;padding:6px 10px;border:1.5px dashed #C8102E;border-radius:12px;align-self:flex-start'):
    return f'<sc-if value="{{{{ {val} }}}}" hint-placeholder-val="{{{{ true }}}}"><div sc-camel-on-click="{{{{ {label_key}Fn }}}}" style="{style}">{{{{ {label_key} }}}}</div></sc-if>\n'

CUST_EXTRA = r"""
      cuQ: st.cuQ || '', cuOnQ: (e) => this.set({cuQ: e.target.value}), cuQPh: i ? 'Search lessons or missions…' : 'Tìm bài học hoặc nhiệm vụ…',
      cuSkills: [[-1, i ? 'All' : 'Tất cả']].concat(SKILLS.map((s, k) => [k, s[i]])).map(([k, label]) => ({ label,
        style: `padding:5px 10px;border-radius:99px;font-size:12px;font-weight:700;cursor:pointer;color:${(st.cuSk ?? -1) === k ? '#FFF' : '#5C4B3C'};background:${(st.cuSk ?? -1) === k ? RED : '#F3E6D3'}`,
        pick: () => this.set({cuSk: k}) })),
      cuHidLabel: st.cuShowHid ? (i ? 'Hide hidden lessons' : 'Ẩn bài đã ẩn') : (i ? `Show hidden (${lessons.filter(l => l.hidden).length})` : `Xem bài đã ẩn (${lessons.filter(l => l.hidden).length})`),
      cuHidStyle: `font-size:12px;font-weight:700;padding:5px 10px;border-radius:99px;cursor:pointer;color:${st.cuShowHid ? '#FFF' : '#5C4B3C'};background:${st.cuShowHid ? INK : '#F3E6D3'}`,
      cuHidToggle: () => this.set({cuShowHid: !st.cuShowHid}),
      ...(() => {
        const q = (st.cuQ || '').trim().toLowerCase(), skf = st.cuSk ?? -1;
        const rowOf = (l, at) => { const mi = l.mi || DEFAULT_MI, w = Math.floor(at / WK);
          return { n: String(at % WK + 1), title: l.t[i], mis: mi.t[i],
            sub: (i ? 'Week ' : 'Tuần ') + (w + 1) + ' · ' + SKILLS[l.sk][i] + (l.mine ? (i ? ' · parent-made' : ' · ba mẹ tạo') : '') + (l.edited ? (i ? ' · edited' : ' · đã sửa') : '') + (l.hidden ? (i ? ' · hidden' : ' · đang ẩn') : ''),
            card: `display:flex;gap:9px;align-items:center;padding:10px;border-radius:16px;background:${l.hidden ? '#F3EDE4' : '#FFF'};opacity:${l.hidden ? .6 : 1};border:1.5px solid ${l.edited || l.mine ? '#F0CE8C' : '#EFE3D2'}`,
            dot: `width:28px;height:28px;border-radius:10px;flex:none;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:14px;color:#FFF;background:${l.mine ? JADE : GOLD}`,
            up: () => this.moveLesson(band, l.id, at - 1), down: () => this.moveLesson(band, l.id, at + 1),
            edit: () => this.set({edId: l.id, edCx: 0, edPart: 'lesson', edDel: false}), editMi: () => this.set({edId: l.id, edCx: 0, edPart: 'mission', edDel: false}),
            hide: () => this.setState(p => this.custPatch(p, c => { c.hide = c.hide || {}; if (c.hide[l.id]) delete c.hide[l.id]; else c.hide[l.id] = 1; })),
            hideIcon: l.hidden ? '👁' : '🙈', hideLabel: l.hidden ? (i ? 'Show again' : 'Hiện lại') : (i ? 'Hide from path' : 'Ẩn khỏi lộ trình'),
            upStyle: sb(at > 0), downStyle: sb(at < lessons.length - 1), upLabel: i ? 'Move up' : 'Lên', downLabel: i ? 'Move down' : 'Xuống', editLabel: i ? 'Edit' : 'Sửa',
            lessonLine: (i ? 'Week ' : 'Tuần ') + (w + 1) + ' · ' + l.t[i], misTitle: mi.t[i], rw: mi.rw[i] }; };
        const keep = (l) => (st.cuShowHid || !l.hidden) && (skf < 0 || l.sk === skf);
        const stages = STAGES[band] || [], nS = Math.max(stages.length, Math.ceil(nW / 4)), open = st.cuOpen || {0: true};
        const stageList = Array.from({length: nS}, (_, g) => { const ws = [];
          for (let w = g * 4; w < Math.min(nW, g * 4 + 4); w++) {
            const rows = lessons.slice(w * WK, w * WK + WK).map((l, j) => [l, w * WK + j]).filter(([l]) => keep(l)).map(([l, at]) => rowOf(l, at));
            ws.push({ title: (i ? 'Week ' : 'Tuần ') + (w + 1), rows, add: () => this.addLessonAt(band, w), addLabel: i ? '＋ Add lesson' : '＋ Thêm bài' }); }
          return { kicker: (i ? 'STAGE ' : 'CHẶNG ') + (g + 1) + (i ? ' · WEEKS ' : ' · TUẦN ') + (g * 4 + 1) + '–' + Math.min(nW, g * 4 + 4), theme: stages[g] || (i ? 'Extra weeks' : 'Các tuần thêm'),
            open: !!open[g], chev: open[g] ? '▾' : '▸', weeks: ws,
            head: `display:flex;align-items:center;gap:8px;padding:10px 12px;border-radius:16px;cursor:pointer;background:${open[g] ? '#FFF6E4' : '#FFF'};border:1.5px solid ${open[g] ? '#F0CE8C' : '#EFE3D2'}`,
            toggle: () => this.setState(p => ({cuOpen: {...(p.cuOpen || {0: true}), [g]: !(p.cuOpen || {0: true})[g]}})) }; });
        const found = q ? lessons.map((l, at) => [l, at]).filter(([l]) => keep(l) && [l.t[0], l.t[1], (l.mi || DEFAULT_MI).t[0], (l.mi || DEFAULT_MI).t[1]].join(' ').toLowerCase().includes(q)) : [];
        return { cuStages: stageList, cuBrowse: !q, cuSearching: !!q, cuResults: found.slice(0, 40).map(([l, at]) => rowOf(l, at)),
          cuFound: i ? `${found.length} result${found.length === 1 ? '' : 's'}` + (found.length > 40 ? ' · showing 40' : '') : `${found.length} kết quả` + (found.length > 40 ? ' · hiện 40 đầu tiên' : '') };
      })(),
      edSkillLabel: i ? 'SKILL' : 'KỸ NĂNG',
      edSkills: !ed ? [] : SKILLS.map((s, k) => ({ label: s[i], style: chip(ed.sk === k), pick: () => E(d => { d.sk = k; }) })),
      edAddCtx: !!ed && ed.cx.length < 3, edAddCtxLabel: i ? '＋ Add a situation' : '＋ Thêm tình huống',
      edAddCtxFn: () => { if (!ed) return; const used = ed.cx.map(c => c.k), k = [0, 1, 2].find(x => !used.includes(x)) ?? 0;
        E(d => { d.cx.push({k, s: ['Câu chuyện mới…', 'New story…'], q: ['Con sẽ làm gì?', 'What would you do?'], o: [['Lựa chọn A', 'Option A', 1, 'Mẹo của Sen', 'Sen’s tip'], ['Lựa chọn B', 'Option B', 0, 'Mẹo của Sen', 'Sen’s tip']]}); });
        this.set({edCx: ed.cx.length}); },
      edAddOpt: !!cx && cx.o.length < 4, edAddOptLabel: i ? '＋ Add a choice' : '＋ Thêm lựa chọn',
      edAddOptFn: () => E(d => { d.cx[cxi].o.push([i ? 'Lựa chọn mới' : 'Lựa chọn mới', 'New choice', 0, 'Mẹo của Sen', 'Sen’s tip']); }),
      edAddQo: !!ed && ed.qo.length < 4, edAddQoLabel: i ? '＋ Add an answer' : '＋ Thêm đáp án',
      edAddQoFn: () => E(d => { d.qo.push(['Đáp án mới', 'New answer']); }),
      edHidLabel: ed && ed.hidden ? (i ? '👁 Show this lesson again' : '👁 Hiện lại bài này') : (i ? '🙈 Hide from the path' : '🙈 Ẩn khỏi lộ trình của con'),
      edHid: () => ed && this.setState(p => this.custPatch(p, c => { c.hide = c.hide || {}; if (c.hide[ed.id]) delete c.hide[ed.id]; else c.hide[ed.id] = 1; })),
      edCanDel: !!(ed && ed.mine), edDelLabel: st.edDel ? (i ? 'Tap again to delete for good' : 'Bấm lần nữa để xoá hẳn') : (i ? '🗑 Delete this lesson' : '🗑 Xoá bài ba mẹ tạo'),
      edDelFn: () => { if (!ed) return; if (!st.edDel) return this.set({edDel: true}); this.setState(p => ({...this.custPatch(p, c => { c.del = c.del || {}; c.del[ed.id] = 1; }), edId: null, edDel: false})); },
"""

def app(t):
    a = t.index('const L = {'); b = t.index('const SEASONS')
    t = t[:a] + build_data() + t[b:]
    # --- lesson objects: an / xoa ---
    t = sub(t, "    base.forEach(l => { const o = les[l.id]; const m = o ? {...l, ...o, edited: true} : {...l};",
               "    const hide = c.hide || {}, del = c.del || {};\n    base.forEach(l => { if (del[l.id]) return; const o = les[l.id]; const m = o ? {...l, ...o, edited: true} : {...l}; if (hide[l.id]) m.hidden = true;")
    t = sub(t, "    base.forEach(l => { if (!seen.has(l.id)) ord.push(l.id); });\n    return ord.map(id => byId[id]);",
               "    base.forEach(l => { if (!seen.has(l.id) && byId[l.id]) ord.push(l.id); });\n    return ord.map(id => byId[id]);")
    t = sub(t, "const d = JSON.parse(JSON.stringify({t: cur.t, cx: cur.cx, qq: cur.qq, qo: cur.qo, qa: cur.qa, mi: cur.mi || DEFAULT_MI})); fn(d);",
               "const d = JSON.parse(JSON.stringify({t: cur.t, sk: cur.sk, cx: cur.cx, qq: cur.qq, qo: cur.qo, qa: cur.qa, mi: cur.mi || DEFAULT_MI})); fn(d);")
    t = sub(t, "  resetLesson(id){", """  addLessonAt(band, w){
    this.setState(p => { const list = ((p.customLessons || {})[band] || []).slice(), n = list.length, id = band + ':c' + n;
      list.push({t:['Bài mới của ba mẹ','A new lesson'], sk:0, m:['7 phút','7 min'], mine:true,
        story:['Ba mẹ viết câu chuyện ở đây…','Write the story here…'], cq:['Con sẽ làm gì?','What would you do?'],
        co:[['Lựa chọn A','Option A',1,'Mẹo của Sen','Sen’s tip'],['Lựa chọn B','Option B',0,'Mẹo của Sen','Sen’s tip'],['Lựa chọn C','Option C',0,'Mẹo của Sen','Sen’s tip']],
        qq:['Điều con nhớ nhất từ bài này?','What will you remember?'], qo:[['Đáp án đúng','Right answer'],['Đáp án khác','Another answer'],['Đáp án khác','Another answer']], qa:0,
        mi: JSON.parse(JSON.stringify(DEFAULT_MI))});
      const ids = this.effLessons(band, p).map(l => l.id), at = Math.min(ids.length, w * 5 + 4); ids.splice(at, 0, id);
      return {customLessons: {...(p.customLessons || {}), [band]: list}, ...this.custPatch(p, c => { c.order[band] = ids; }), edId: id, edCx: 0, edPart: 'lesson', edDel: false}; });
  }
  resetLesson(id){""")
    # --- duong hoc cua con: bo qua bai an ---
    t = sub(t, "    const weekIdx = w => lessons.map((_, x) => x).slice(w * WK, w * WK + WK);",
               "    const weekIdx = w => lessons.map((_, x) => x).slice(w * WK, w * WK + WK).filter(x => !lessons[x].hidden);")
    t = sub(t, "    const doneCount = lessons.filter(isDone).length;", "    const doneCount = lessons.filter(l => !l.hidden && isDone(l)).length, shownCount = lessons.filter(l => !l.hidden).length;")
    t = sub(t, "tileProgressSub: (i?'Done ':'Đã học ') + doneCount + '/' + lessons.length + (i?' lessons':' bài'),", "tileProgressSub: (i?'Done ':'Đã học ') + doneCount + '/' + shownCount + (i?' lessons':' bài'),")
    t = sub(t, "          n:String(idx - viewWk*WK + 1),", "          n:String(weekIdx(viewWk).indexOf(idx) + 1),")
    t = sub(t, "      wkMeta: (() => {", "      wkStage: (() => { const g = Math.floor(viewWk / 4), th = (STAGES[band] || [])[g]; return (i ? 'Stage ' : 'Chặng ') + (g + 1) + (th ? ' · ' + th : ''); })(),\n      wkMeta: (() => {")
    t = sub(t, """                <div style="font-size:11.5px;color:#8B7867;margin-top:1px">{{ wkMeta }}</div>""",
               """                <div style="font-size:11px;font-weight:700;color:#C8102E;margin-top:1px;line-height:1.3">{{ wkStage }}</div>
                <div style="font-size:11.5px;color:#8B7867;margin-top:1px">{{ wkMeta }}</div>""")
    # --- danh muc trong tai khoan ba me ---
    a = t.index('<sc-if value="{{ cuShowList }}"'); b = t.index('<sc-if value="{{ cuShowEd }}"')
    t = t[:a] + CATALOG + t[b:]
    a = t.index('<sc-if value="{{ cuShowMis }}"'); b = t.index('<div sc-camel-on-click="{{ cuResetAll }}"')
    t = t[:a] + MIS_TAB + t[b:]
    t = sub(t, "      cuListHint: i ?", CUST_EXTRA + "      cuListHint: i ?")
    t = re.sub(r"cuListHint: i \? '[^']*' : '[^']*',", "cuListHint: i ? 'Every 5 lessons make one week, 48 weeks in 12 stages. ↑ ↓ reorder, 🙈 hide, ✎ edit, ＋ add.' : 'Mỗi 5 bài là một tuần, 48 tuần chia 12 chặng. ↑ ↓ đổi thứ tự, 🙈 ẩn bài, ✎ sửa, ＋ thêm bài.',", t, count=1)
    t = sub(t, "    const lessons = this.effLessons(band), WK = 5, nW = Math.max(1, Math.ceil(lessons.length / WK));",
               "    const lessons = this.effLessons(band), WK = 5, nW = Math.max(1, Math.ceil(lessons.length / WK));\n    const chip = (on) => `padding:6px 12px;border-radius:99px;font-size:12.5px;font-weight:700;cursor:pointer;color:${on ? '#FFF' : '#5C4B3C'};background:${on ? INK : '#F3E6D3'}`;")
    t = sub(t, "    const chip = (on) => `padding:6px 12px;border-radius:99px;font-size:12.5px;font-weight:700;cursor:pointer;color:${on ? '#FFF' : '#5C4B3C'};background:${on ? INK : '#F3E6D3'}`;\n    const ed =",
               "    const ed =")
    t = sub(t, "cuMisHint: i ? 'Each lesson has exactly one real-life mission.", "cuMisHint: i ? 'Each lesson has exactly one real-life mission, grouped by stage.")
    a = t.index("      cuMisWeeks: Array.from("); b = t.index("      edParts:")
    t = t[:a] + t[b:]
    # tuan: hien 48 nut -> chi hien tuan trong chang hien tai +- (van du dung)
    # editor: ky nang, them/bot tinh huong, lua chon, dap an, an/xoa
    t = sub(t, '                <sc-if value="{{ edHasCtx }}" hint-placeholder-val="{{ true }}">',
               f'                <div style="{LBL}">{{{{ edSkillLabel }}}}</div>\n                <div style="display:flex;gap:5px;flex-wrap:wrap">\n                  <sc-for list="{{{{ edSkills }}}}" as="x" hint-placeholder-count="9">\n                    <div sc-camel-on-click="{{{{ x.pick }}}}" style="{{{{ x.style }}}}">{{{{ x.label }}}}</div>\n                  </sc-for>\n                </div>\n                <sc-if value="{{{{ edHasCtx }}}}" hint-placeholder-val="{{{{ true }}}}">')
    t = sub(t, "      edHasCtx: !!ed && ed.cx.length > 1,", "      edHasCtx: !!ed,")
    t = sub(t, """                        <div sc-camel-on-click="{{ c.down }}" style="{{ c.downStyle }}">↓</div>
                      </div>
                    </sc-for>""", """                        <div sc-camel-on-click="{{ c.down }}" style="{{ c.downStyle }}">↓</div>
                        <div sc-camel-on-click="{{ c.del }}" style="{{ c.delStyle }}">✕</div>
                      </div>
                    </sc-for>
                    """ + mini_btn('edAddCtx', 'edAddCtxLabel').replace('edAddCtxLabelFn', 'edAddCtxFn'))
    t = sub(t, "        upStyle: sb(k > 0), downStyle: sb(k < ed.cx.length - 1) })),",
               "        upStyle: sb(k > 0), downStyle: sb(k < ed.cx.length - 1),\n        del: () => { if (ed.cx.length < 2) return; E(d => { d.cx.splice(k, 1); }); this.set({edCx: 0}); }, delStyle: sb(ed.cx.length > 1) })),")
    t = sub(t, """                      <div sc-camel-on-click="{{ o.down }}" style="{{ o.downStyle }}">↓</div>
                    </div>
                    <textarea""", """                      <div sc-camel-on-click="{{ o.down }}" style="{{ o.downStyle }}">↓</div>
                      <div sc-camel-on-click="{{ o.del }}" style="{{ o.delStyle }}">✕</div>
                    </div>
                    <textarea""")
    t = sub(t, "        up: () => E(d => swap(d.cx[cxi].o, k, k - 1)), down: () => E(d => swap(d.cx[cxi].o, k, k + 1)),\n        upStyle: sb(k > 0), downStyle: sb(k < cx.o.length - 1) })),",
               "        up: () => E(d => swap(d.cx[cxi].o, k, k - 1)), down: () => E(d => swap(d.cx[cxi].o, k, k + 1)),\n        upStyle: sb(k > 0), downStyle: sb(k < cx.o.length - 1),\n"
               "        del: () => E(d => { const o = d.cx[cxi].o; if (o.length < 3) return; const was = o[k][2]; o.splice(k, 1); if (was) o[0][2] = 1; }), delStyle: sb(cx.o.length > 2) })),")
    # cuoi danh sach lua chon -> nut them
    t = sub(t, """                </sc-for>
                <div style="font-size:11.5px;font-weight:700;color:#8B7867;letter-spacing:.3px">{{ edQqLabel }}</div>""",
               "                </sc-for>\n                " + mini_btn('edAddOpt', 'edAddOptLabel').replace('edAddOptLabelFn', 'edAddOptFn') +
               """                <div style="font-size:11.5px;font-weight:700;color:#8B7867;letter-spacing:.3px">{{ edQqLabel }}</div>""")
    t = sub(t, """                    <div sc-camel-on-click="{{ o.down }}" style="{{ o.downStyle }}">↓</div>
                  </div>
                </sc-for>
                  </div>
                </sc-if>""", """                    <div sc-camel-on-click="{{ o.down }}" style="{{ o.downStyle }}">↓</div>
                    <div sc-camel-on-click="{{ o.del }}" style="{{ o.delStyle }}">✕</div>
                  </div>
                </sc-for>
                """ + mini_btn('edAddQo', 'edAddQoLabel').replace('edAddQoLabelFn', 'edAddQoFn') + """                  </div>
                </sc-if>""")
    t = sub(t, "        down: () => E(d => { swap(d.qo, k, k + 1); d.qa = d.qa === k ? k + 1 : d.qa === k + 1 ? k : d.qa; }),\n        upStyle: sb(k > 0), downStyle: sb(k < ed.qo.length - 1) })),",
               "        down: () => E(d => { swap(d.qo, k, k + 1); d.qa = d.qa === k ? k + 1 : d.qa === k + 1 ? k : d.qa; }),\n        upStyle: sb(k > 0), downStyle: sb(k < ed.qo.length - 1),\n"
               "        del: () => E(d => { if (d.qo.length < 3) return; d.qo.splice(k, 1); d.qa = d.qa === k ? 0 : d.qa > k ? d.qa - 1 : d.qa; }), delStyle: sb(ed.qo.length > 2) })),")
    t = sub(t, "{{ edResetLabel }}</div>\n                  </sc-if>\n                </div>",
               "{{ edResetLabel }}</div>\n                  </sc-if>\n                </div>\n"
               "                <div style=\"display:flex;gap:8px;flex-wrap:wrap\">\n"
               "                  <div sc-camel-on-click=\"{{ edHid }}\" style=\"flex:1;text-align:center;background:#F3E6D3;color:#5C4B3C;border-radius:14px;padding:11px;font-weight:700;font-size:13px;cursor:pointer\">{{ edHidLabel }}</div>\n"
               "                  <sc-if value=\"{{ edCanDel }}\" hint-placeholder-val=\"{{ false }}\"><div sc-camel-on-click=\"{{ edDelFn }}\" style=\"flex:1;text-align:center;background:#FFF;color:#C8102E;border:1.5px solid #C8102E;border-radius:14px;padding:10px;font-weight:700;font-size:13px;cursor:pointer\">{{ edDelLabel }}</div></sc-if>\n"
               "                </div>")
    t = sub(t, "custTab:'lessons', custBand:null, edId:null, edCx:0, custReset:false,", "custTab:'lessons', custBand:null, edId:null, edCx:0, custReset:false, cuQ:'', cuSk:-1, cuShowHid:false, cuOpen:{0:true}, edDel:false,")
    t = sub(t, "cuCardTitle: i ? 'Customise lessons & missions' : 'Tuỳ chỉnh bài học & nhiệm vụ',", "cuCardTitle: i ? 'Lesson & mission catalogue' : 'Danh mục bài học & nhiệm vụ',")
    t = sub(t, "cuCardSub: i ? 'Reorder lessons, edit stories, missions and rewards — for your family only.' : 'Đổi thứ tự bài, sửa câu chuyện, nhiệm vụ và phần thưởng — chỉ riêng gia đình mình.',",
               "cuCardSub: i ? '240 lessons and missions for 12 months. Reorder, hide, add or edit anything — for your family only.' : '240 bài và nhiệm vụ cho 12 tháng. Đổi thứ tự, ẩn, thêm bớt, sửa tự do — chỉ riêng gia đình mình.',")
    t = sub(t, "cuTitle: i ? 'Family customisation' : 'Tuỳ chỉnh của gia đình',", "cuTitle: i ? 'Lessons & missions' : 'Danh mục bài học & nhiệm vụ',")
    return pricing(t)

def pricing(t):
    t = sub(t, "const PRICES = {classic:{6:89000,12:149000}, premium:{6:129000,12:199000}};", "const PRICES = {classic:{6:299000,12:499000}, premium:{6:299000,12:499000}};")
    t = sub(t, "const PROF = {6:59000,12:99000};", "const PROF = {6:149000,12:249000};")
    t = sub(t, "premiumSub:'Hai gói cho cả gia đình. Mua 6 tháng tặng 1 tháng, mua 12 tháng tặng 2 tháng. Không tự động gia hạn.'", "premiumSub:'Một gói trọn bộ 9 kỹ năng, chọn 6 hoặc 12 tháng. Thêm con giảm 50%. Không tự động gia hạn.'")
    t = sub(t, "premiumSub:'Two family plans. Buy 6 months, get 1 free; buy 12 months, get 2 free. No auto-renewal.'", "premiumSub:'One full plan with all 9 skills, for 6 or 12 months. Extra children 50% off. No auto-renewal.'")
    t = sub(t, "? (i ? 'Premium · all 9 skills unlocked for every profile in this family.' : 'Premium · trọn bộ 9 kỹ năng đã mở cho mọi hồ sơ trong gia đình.')", "? (i ? 'Full plan · all 9 skills and 240 lessons unlocked.' : 'Trọn bộ · đã mở cả 9 kỹ năng và 240 bài.')")
    t = sub(t, "owned:{0:true,1:true,2:true,3:true,4:true,5:true}, curPlan:'classic',", "owned:{0:true,1:true,2:true,3:true,4:true,5:true,6:true,7:true,8:true}, curPlan:'premium',")
    t = sub(t, "termTabs: [[6, i?'6 months +1 free':'6 tháng +1 tặng'],[12, i?'12 months +2 free':'12 tháng +2 tặng']]", "termTabs: [[6, i?'6 months':'6 tháng'],[12, i?'12 months · save 17%':'12 tháng · tiết kiệm 17%']]")
    t = sub(t, "planCards: [['classic','CLASSIC',t.classicList],['premium','PREMIUM',t.premiumList]].map(", "planCards: [['premium',i?'FULL PLAN':'TRỌN BỘ',t.premiumList]].map(")
    t = sub(t, "per: term===6 ? (i?'per 6 months · +1 month free':'/ 6 tháng · tặng 1 tháng') : (i?'per year · +2 months free':'/ năm · tặng 2 tháng'),",
               "per: term===6 ? (i?'per 6 months · 24 weeks':'/ 6 tháng · 24 tuần học') : (i?'per year · 48 weeks, 240 lessons':'/ năm · 48 tuần, 240 bài'),")
    t = sub(t, "premiumList:'Trọn bộ 9 kỹ năng · bài theo dịp · ba mẹ tự tạo bài · Affiliate · tối đa 5 hồ sơ con',", "premiumList:'Trọn bộ 9 kỹ năng · 240 bài và 240 nhiệm vụ cho 12 tháng · ba mẹ tuỳ chỉnh tự do · 1 hồ sơ con, thêm con giảm 50%',")
    t = sub(t, "premiumList:'All 9 skills · seasonal lessons · parent-made lessons · affiliate · up to 5 child profiles',", "premiumList:'All 9 skills · 240 lessons and missions for 12 months · fully customisable · 1 child, extra children 50% off',")
    t = re.sub(r"priceNote: \(plan==='premium' \? \(i\?'Premium · all 9 skills':'Premium · trọn bộ 9 kỹ năng'\)[^\n]*",
               "priceNote: (i?'Full plan · all 9 skills · ':'Trọn bộ 9 kỹ năng · ') + (term===6?(i?'6 months':'6 tháng'):(i?'12 months':'12 tháng')) + (i?' · no auto-renewal':' · không tự động gia hạn'),", t, count=1)
    t = sub(t, "(payIsProfile ? 'Hoso' : (plan==='premium'?'Premium':'Classic'))", "(payIsProfile ? 'Themcon' : 'TronBo')")
    t = sub(t, "affEligible: st.curPlan==='premium', affLocked: st.curPlan!=='premium',", "affEligible: false, affLocked: false,")
    # 1 con trong goi, them con -50%
    t = sub(t, "      if (st.profiles.filter(x=>x.kid).length >= 5) return this.setState({pendingProfile:np,", "      if (st.profiles.filter(x=>x.kid).length >= 1 && !st.demo) return this.setState({pendingProfile:np,")
    t = sub(t, "extraProfile: st.creator==='profile' && kidCount>=5,", "extraProfile: st.creator==='profile' && kidCount>=1 && !st.demo,")
    t = sub(t, "saveLabel: (st.creator==='profile' && kidCount>=5) ?", "saveLabel: (st.creator==='profile' && kidCount>=1 && !st.demo) ?")
    t = re.sub(r"profilesMeta: i \? [^\n]*", "profilesMeta: i ? kidCount+' child profile(s) · each extra child: 149,000₫/6 mo or 249,000₫/year (50% off)' : kidCount+' hồ sơ con · mỗi con thêm: 149.000đ/6 tháng hoặc 249.000đ/năm (giảm 50%)',", t, count=1)
    t = re.sub(r"extraNote: i\?'Your plan already has 5 child profiles[^\n]*", "extraNote: i?'Your plan covers one child. Each extra child is 50% off: 149,000₫ for 6 months or 249,000₫ for a year.':'Gói đã gồm 1 con. Mỗi con thêm giảm 50%: 149.000đ/6 tháng hoặc 249.000đ/năm.',", t, count=1)
    t = re.sub(r"if \(f\.kind==='kid' && st\.profiles\.filter\(p=>p\.kid\)\.length >= 5\) return err\([^\n]*",
               "if (f.kind==='kid' && st.profiles.filter(p=>p.kid).length >= 1 && !st.demo) return err('Gói đã gồm 1 con. Để thêm con, ba mẹ đăng nhập → tab Ba mẹ → Thêm hồ sơ con để thanh toán phần giảm 50% (149.000đ/6 tháng hoặc 249.000đ/năm).','Your plan covers one child. To add another, log in → Parent tab → add a child profile and pay the 50%-off fee (149,000₫/6 mo or 249,000₫/year).');", t, count=1)
    t = sub(t, "['Mỗi gói đã gồm tối đa 5 hồ sơ con. Từ trẻ thứ 6, phí mở hồ sơ là 59.000đ/trẻ/6 tháng hoặc 99.000đ/trẻ/12 tháng. Kỹ năng đã mở áp dụng cho mọi hồ sơ; mỗi hồ sơ có lộ trình, sao và huy hiệu riêng.',\n    'Every plan includes up to 5 child profiles. From the 6th child, each extra profile is 59,000₫ for 6 months or 99,000₫ for 12 months. Unlocked skills apply to every profile; each keeps its own path, stars and badges.']",
               "['Mỗi gói gồm 1 hồ sơ con. Con thứ hai trở đi được giảm 50%: 149.000đ/6 tháng hoặc 249.000đ/năm. Mỗi con có lộ trình theo tuổi, sao và huy hiệu riêng.',\n    'Each plan covers one child. Every extra child is 50% off: 149,000₫ for 6 months or 249,000₫ a year. Each child keeps their own age-based path, stars and badges.']")
    t = sub(t, "['♥', '#F2A93B', i?'One plan, up to 5 children':'Một gói, tối đa 5 con', i?'Each child has their own PIN and path; grandparents can join too.':'Mỗi con một mã PIN, một lộ trình; ông bà cũng tham gia được.'],",
               "['♥', '#F2A93B', i?'Extra children 50% off':'Thêm con giảm 50%', i?'Each child has their own PIN and path; grandparents can join too.':'Mỗi con một mã PIN, một lộ trình; ông bà cũng tham gia được.'],")
    t = t.replace("i?'9 life skills, 45 lessons for your child’s age':'9 kỹ năng sống, 45 bài đúng tuổi của con'", "i?'9 life skills, 240 lessons for your child’s age':'9 kỹ năng sống, 240 bài đúng tuổi của con'")
    return t

# ---------------- trang chu ----------------
PRICE_SECTION = """<section id="gia" style="background:#FFF;padding:72px 0">
  <div style="max-width:1160px;margin:0 auto;padding:0 clamp(16px,4vw,40px)">
    <div style="text-align:center;max-width:780px;margin:0 auto 32px">
      <div style="font-size:13px;font-weight:700;color:#C8102E;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px">Học phí</div>
      <h2 style="font-family:'Baloo 2',cursive;font-weight:800;font-size:clamp(30px,3.8vw,48px);line-height:1.08;margin:0">Chưa tới 1.400đ mỗi ngày cho một năm con tự lớn lên</h2>
      <p style="font-size:17px;line-height:1.7;color:#5C4B3C;margin:18px auto 0;max-width:60ch">Trọn bộ 9 kỹ năng, <strong>240 bài học và 240 nhiệm vụ đời thực</strong> cho 48 tuần, chia 12 chặng. Ba mẹ xem trước toàn bộ danh mục và tự sửa, thêm, bớt cho hợp với con.</p>
      <a href="../?demo" style="display:inline-flex;align-items:center;gap:8px;margin-top:18px;background:#2E9E7E;color:#FFF;border-radius:999px;padding:10px 20px;font-weight:700;font-size:15px">Dùng thử miễn phí với gia đình mẫu →</a>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:18px;max-width:900px;margin:0 auto">
      <div style="border-radius:30px;background:#FFF8EF;border:2px solid #F0E4D4;padding:28px;display:flex;flex-direction:column;gap:12px">
        <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:24px;color:#5C4B3C">Gói 6 tháng</div>
        <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:40px;line-height:1">299.000đ</div>
        <div style="font-size:14px;color:#6D5B4B">24 tuần học · 120 bài · khoảng 1.650đ/ngày</div>
        <ul style="margin:0;padding-left:20px;font-size:14.5px;line-height:1.9;color:#3A2E24">
          <li>Trọn bộ 9 kỹ năng, nhiệm vụ đời thực, huy hiệu</li>
          <li>Ba mẹ tuỳ chỉnh danh mục tự do</li>
          <li>1 hồ sơ con · thêm con giảm 50%</li>
        </ul>
        <a href="#dang-ky" sc-camel-on-click="{{ pickClassic }}" style="margin-top:auto;text-align:center;background:#FFF;color:#C8102E;border:2px solid #C8102E;border-radius:16px;padding:13px;font-family:'Baloo 2',cursive;font-weight:700;font-size:18px">Chọn gói 6 tháng</a>
      </div>
      <div style="border-radius:30px;background:#C8102E;color:#FFF;padding:28px;display:flex;flex-direction:column;gap:12px;position:relative;box-shadow:0 18px 40px rgba(200,16,46,.22)">
        <div style="position:absolute;top:-14px;right:24px;background:#F2A93B;color:#221A15;border-radius:99px;padding:5px 14px;font-size:12.5px;font-weight:800">Tiết kiệm 17%</div>
        <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:24px">Gói 12 tháng</div>
        <div style="font-family:'Baloo 2',cursive;font-weight:800;font-size:40px;line-height:1">499.000đ</div>
        <div style="font-size:14px;opacity:.92">Trọn hành trình 48 tuần · 240 bài · khoảng 1.370đ/ngày</div>
        <ul style="margin:0;padding-left:20px;font-size:14.5px;line-height:1.9">
          <li>Cả 12 chặng, 240 bài và 240 nhiệm vụ</li>
          <li>Bài theo dịp mỗi tháng, nhắc giờ học</li>
          <li>1 hồ sơ con · thêm con giảm 50% (249.000đ/năm)</li>
        </ul>
        <a href="#dang-ky" sc-camel-on-click="{{ pickPremium }}" style="margin-top:auto;text-align:center;background:#FFF;color:#C8102E;border-radius:16px;padding:13px;font-family:'Baloo 2',cursive;font-weight:700;font-size:18px">Chọn gói 12 tháng</a>
      </div>
    </div>
    <p style="font-size:13px;line-height:1.7;color:#8B7867;margin:24px auto 0;max-width:72ch;text-align:center">Không tự động gia hạn. Thanh toán đơn giản với VietQR, nội dung “Senapp + mã khách hàng + tên gói”. Giới thiệu một gia đình bạn đăng ký: cả hai được tặng thêm 1 tháng.</p>
  </div>
</section>"""

def landing(t):
    a = t.index('<section id="gia"'); b = t.index('</section>', a) + len('</section>')
    t = t[:a] + PRICE_SECTION + t[b:]
    t = re.sub(r'<p style="font-size:13px;color:#8B7867;margin:18px 0 0">Chỉ từ 89\.000đ[^\n]*</p>',
               '<p style="font-size:13px;color:#8B7867;margin:18px 0 0"><a href="../?demo" style="color:#2E9E7E;font-weight:700">Dùng thử miễn phí</a> · trọn năm 499.000đ · không tự động gia hạn</p>', t, count=1)
    t = sub(t, '<div style="font-family:\'Baloo 2\',cursive;font-weight:800;font-size:28px;color:#1BA39C;line-height:1">45</div>',
               '<div style="font-family:\'Baloo 2\',cursive;font-weight:800;font-size:28px;color:#1BA39C;line-height:1">240</div>')
    t = sub(t, '>bài cho tuổi của con</div>', '>bài trong 12 tháng</div>')
    t = sub(t, "const PLANS = [['classic',6,'Classic','6 tháng + tặng 1 tháng',89000],['classic',12,'Classic','12 tháng + tặng 2 tháng',149000],['premium',6,'Premium','6 tháng + tặng 1 tháng',129000],['premium',12,'Premium','12 tháng + tặng 2 tháng',199000]];",
               "const PLANS = [['premium',6,'TronBo','6 tháng',299000],['premium',12,'TronBo','12 tháng',499000]];")
    t = sub(t, "state = { faqOpen: 0, plan: 3,", "state = { faqOpen: 0, plan: 1,")
    t = sub(t, "pickClassic: () => this.setState({ plan: 0 }), pickPremium: () => this.setState({ plan: 3 }),", "pickClassic: () => this.setState({ plan: 0 }), pickPremium: () => this.setState({ plan: 1 }),")
    t = sub(t, "planOpts: PLANS.map((x, k) => ({ name: x[2], term: x[3],", "planOpts: PLANS.map((x, k) => ({ name: 'Trọn bộ', term: x[3],")
    t = sub(t, "planLabel: p[2] + ' · ' + p[3] + ' · ' + fmt(p[4]),", "planLabel: 'Trọn bộ · ' + p[3] + ' · ' + fmt(p[4]),")
    t = sub(t, "'Chọn Classic hoặc Premium'", "'Chọn gói 6 hoặc 12 tháng'")
    def faq(t, q, ans):
        a = t.index("  ['" + q); b = t.index("'],\n", a) + 4
        return t[:a] + f"  ['{q}', '{ans}'],\n" + t[b:]
    t = faq(t, '89.000đ cho 6 tháng — có đáng không?', '')
    t = sub(t, "  ['89.000đ cho 6 tháng — có đáng không?', ''],\n",
            "  ['499.000đ một năm — có đáng không?', 'Chưa tới 1.400đ mỗi ngày cho 240 bài và 240 nhiệm vụ đời thực trong 48 tuần. Đổi lại là một năm con tự làm những việc mà trước đây ba mẹ phải nhắc cả trăm lần. Ba mẹ có thể dùng thử với gia đình mẫu trước khi đăng ký.'],\n")
    t = faq(t, 'Classic và Premium khác nhau thế nào?', '')
    t = sub(t, "  ['Classic và Premium khác nhau thế nào?', ''],\n",
            "  ['Gói 6 tháng và 12 tháng khác nhau thế nào?', 'Hai gói đều mở trọn bộ 9 kỹ năng và mọi tính năng. Gói 6 tháng (299.000đ) đi được 24 tuần, 120 bài. Gói 12 tháng (499.000đ) đi trọn 48 tuần, 240 bài và rẻ hơn 17% mỗi tháng.'],\n")
    t = faq(t, 'Một gói dùng được cho mấy con?', '')
    t = sub(t, "  ['Một gói dùng được cho mấy con?', ''],\n",
            "  ['Một gói dùng được cho mấy con?', 'Mỗi gói gồm 1 hồ sơ con với lộ trình đúng tuổi. Con thứ hai trở đi được giảm 50%: 149.000đ/6 tháng hoặc 249.000đ/năm, mỗi con một mã PIN, một lộ trình riêng.'],\n")
    t = faq(t, 'Giới thiệu bạn bè có được gì không?', '')
    t = sub(t, "  ['Giới thiệu bạn bè có được gì không?', ''],\n",
            "  ['Giới thiệu bạn bè có được gì không?', 'Có. Mỗi gia đình bạn giới thiệu đăng ký gói, cả hai gia đình được tặng thêm 1 tháng học.'],\n")
    t = sub(t, '“Senapp K7M2Q9 Premium12T”', '“Senapp K7M2Q9 TronBo12T”')
    bad = [t[m.start()-60:m.end()+20] for m in re.finditer(r'(?<!pick)(Classic|Premium)|89\.000', t)]
    assert not bad, bad[:3]
    return t

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
