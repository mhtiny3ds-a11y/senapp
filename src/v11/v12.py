"""Senapp v12 (ap dung tren v11):
- bai hoc dan con di het 3 tinh huong (o nha -> tren lop -> ngoai doi), moi tinh huong: chuyen -> cau hoi -> meo, roi moi den cau do
- moi bai dung 1 nhiem vu doi thuc (hien ngay o buoc cuoi bai); ba me sua text nhiem vu/phan thuong trong khung cua bai do
- lien he: admin.senapp@gmail.com; "Zalo/Viber ho tro" 0975 860 488; phan hoi cham nhat trong 24h
Dung: python3 v12.py <app index.html> <landing index.html> <thu muc v11>"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v11 as V

def sub(h, a, b, n=1):
    c = h.count(a); assert c == n, (a[:140], c); return h.replace(a, b)

def build_L(d):
    js = V.build_L(d)
    M = {b: json.load(open(os.path.join(d, 'content', f'missions-{b}.json'), encoding='utf-8')) for b in V.BANDS}
    out, band = [], None
    for line in js.split('\n'):
        m = re.match(r"^'(5-8|9-12|13-16)': \[$", line)
        if m: band = m.group(1)
        if line.startswith('{"t":'):
            trail = ',' if line.endswith(',') else ''
            l = json.loads(line[:-1] if trail else line)
            mi = M[band][l['oi']]; assert mi['oi'] == l['oi']
            l['mi'] = {'t': mi['t'], 's': mi['s'], 'rw': mi['rw'], 'lv': mi['lv']}
            line = json.dumps(l, ensure_ascii=False) + trail
        out.append(line)
    return '\n'.join(out)

def store_load(key, dflt):
    return f"(() => {{ try {{ return JSON.parse(localStorage.getItem('{key}') || 'null') || {dflt}; }} catch (e) {{ return {dflt}; }} }})()"

LBL, INP, TXA, SBTN = V.LBL, V.INP, V.TXA, V.SBTN

ED_PARTS = """                <div style="display:flex;background:#F3E6D3;border-radius:12px;padding:3px;gap:3px">
                  <sc-for list="{{ edParts }}" as="x" hint-placeholder-count="2">
                    <div sc-camel-on-click="{{ x.pick }}" style="{{ x.style }}">{{ x.label }}</div>
                  </sc-for>
                </div>
"""

ED_MISSION = f"""                <sc-if value="{{{{ edIsMission }}}}" hint-placeholder-val="{{{{ false }}}}">
                  <div style="display:flex;flex-direction:column;gap:10px">
                    <div style="font-size:12px;color:#8B7867;line-height:1.5">{{{{ edMiFrom }}}}</div>
                    <div style="{LBL}">{{{{ edMiTitleLabel }}}}</div>
                    <input value="{{{{ edMiTitle }}}}" sc-camel-on-change="{{{{ edOnMiTitle }}}}" style="{INP};font-weight:700">
                    <div style="{LBL}">{{{{ edMiSubLabel }}}}</div>
                    <textarea value="{{{{ edMiSub }}}}" sc-camel-on-change="{{{{ edOnMiSub }}}}" style="{TXA};min-height:110px"></textarea>
                    <div style="font-size:11.5px;color:#1B6B4F;background:#DDF0E6;border-radius:12px;padding:8px 10px;line-height:1.5">{{{{ edMiHint }}}}</div>
                    <div style="{LBL}">🎁 {{{{ edMiRwLabel }}}}</div>
                    <input value="{{{{ edMiRw }}}}" sc-camel-on-change="{{{{ edOnMiRw }}}}" style="{INP};background:#FFF6E4;border-style:dashed;border-color:#F0CE8C">
                    <div style="{LBL}">{{{{ edMiLvLabel }}}}</div>
                    <sc-for list="{{{{ edMiLevels }}}}" as="lv" hint-placeholder-count="3">
                      <div style="display:flex;gap:6px;align-items:flex-start">
                        <div style="font-size:11px;font-weight:700;color:#C8102E;width:62px;flex:none;padding-top:10px">{{{{ lv.label }}}}</div>
                        <textarea value="{{{{ lv.text }}}}" sc-camel-on-change="{{{{ lv.on }}}}" style="{TXA};min-height:48px;flex:1;width:auto;min-width:0"></textarea>
                      </div>
                    </sc-for>
                  </div>
                </sc-if>
"""

MIS_TAB = f"""<sc-if value="{{{{ cuShowMis }}}}" hint-placeholder-val="{{{{ false }}}}">
              <div style="display:flex;flex-direction:column;gap:10px">
                <div style="display:flex;gap:6px;flex-wrap:wrap">
                  <sc-for list="{{{{ cuBands }}}}" as="x" hint-placeholder-count="3">
                    <div sc-camel-on-click="{{{{ x.pick }}}}" style="{{{{ x.style }}}}">{{{{ x.label }}}}</div>
                  </sc-for>
                </div>
                <div style="font-size:12px;color:#8B7867;line-height:1.5">{{{{ cuMisHint }}}}</div>
                <sc-for list="{{{{ cuMisWeeks }}}}" as="w" hint-placeholder-count="2">
                  <div style="display:flex;flex-direction:column;gap:6px">
                    <div style="font-family:'Baloo 2',cursive;font-size:16px;font-weight:800;color:#C8102E;margin-top:4px">{{{{ w.title }}}}</div>
                    <sc-for list="{{{{ w.rows }}}}" as="r" hint-placeholder-count="5">
                      <div sc-camel-on-click="{{{{ r.edit }}}}" style="{{{{ r.card }}}}">
                        <div style="{{{{ r.dot }}}}">{{{{ r.n }}}}</div>
                        <div style="flex:1;min-width:0">
                          <div style="font-size:11px;color:#8B7867">{{{{ r.lesson }}}}</div>
                          <div style="font-size:14px;font-weight:700;color:#221A15;line-height:1.3;margin-top:1px">{{{{ r.title }}}}</div>
                          <div style="font-size:11.5px;color:#8F6A1E;margin-top:3px">🎁 {{{{ r.rw }}}}</div>
                        </div>
                        <div style="{SBTN};background:#FBE3E7;color:#C8102E">✎</div>
                      </div>
                    </sc-for>
                  </div>
                </sc-for>
              </div>
            </sc-if>

            """

CUST_VALS = r"""
      cuMisHint: i ? 'Each lesson has exactly one real-life mission. Tap a mission to edit the text or the reward — you can write several small tasks into the same instructions box.'
                   : 'Mỗi bài có đúng một nhiệm vụ đời thực. Bấm vào nhiệm vụ để sửa chữ hoặc phần thưởng — ba mẹ có thể viết thêm nhiều việc nhỏ vào cùng khung hướng dẫn.',
      cuMisWeeks: Array.from({length: nW}, (_, w) => ({ title: (i ? 'Week ' : 'Tuần ') + (w + 1),
        rows: lessons.slice(w * WK, w * WK + WK).map((l, j) => { const mi = l.mi || DEFAULT_MI;
          return { n: String(j + 1), lesson: (i ? 'Lesson: ' : 'Bài: ') + l.t[i], title: mi.t[i], rw: mi.rw[i],
            card: `display:flex;gap:9px;align-items:center;padding:10px;border-radius:16px;cursor:pointer;background:#FFF;border:1.5px solid ${l.edited ? '#F0CE8C' : '#EFE3D2'}`,
            dot: `width:28px;height:28px;border-radius:10px;flex:none;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:14px;color:#FFF;background:${GOLD}`,
            edit: () => this.set({edId: l.id, edCx: 0, edPart: 'mission'}) }; }) })),
      edParts: [['lesson', i ? 'Lesson content' : 'Nội dung bài'], ['mission', i ? 'Mission & reward' : 'Nhiệm vụ & phần thưởng']].map(([k, label]) =>
        ({label, style: pill((st.edPart || 'lesson') === k), pick: () => this.set({edPart: k})})),
      edIsLesson: (st.edPart || 'lesson') === 'lesson', edIsMission: st.edPart === 'mission',
      edMiFrom: ed ? (i ? 'Mission for the lesson “' + ed.t[1] + '”. It appears right after the quiz.' : 'Nhiệm vụ của bài “' + ed.t[0] + '”. Con nhận nhiệm vụ này ngay sau câu đố.') : '',
      edMiTitleLabel: i ? 'MISSION' : 'NHIỆM VỤ', edMiTitle: ed ? (ed.mi || DEFAULT_MI).t[i] : '',
      edOnMiTitle: (e) => { const v = e.target.value; E(d => { d.mi.t[i] = v; }); },
      edMiSubLabel: i ? 'WHAT TO DO' : 'HƯỚNG DẪN', edMiSub: ed ? (ed.mi || DEFAULT_MI).s[i] : '',
      edOnMiSub: (e) => { const v = e.target.value; E(d => { d.mi.s[i] = v; }); },
      edMiHint: i ? 'Want your child to do more in one go? Add the extra tasks here, e.g. “1) … 2) … 3) …”. It stays one mission.'
                  : 'Muốn con làm nhiều việc trong một buổi? Ba mẹ viết thêm ngay trong khung này, ví dụ “1) … 2) … 3) …”. Vẫn là một nhiệm vụ.',
      edMiRwLabel: i ? 'REWARD' : 'PHẦN THƯỞNG', edMiRw: ed ? (ed.mi || DEFAULT_MI).rw[i] : '',
      edOnMiRw: (e) => { const v = e.target.value; E(d => { d.mi.rw[i] = v; }); },
      edMiLvLabel: i ? 'THREE DIFFICULTY LEVELS' : 'BA MỨC KHÓ',
      edMiLevels: !ed ? [] : ((ed.mi || DEFAULT_MI).lv || DEFAULT_LV).map((x, n) => ({ label: [i ? '1 · Together' : '1 · Cùng làm', i ? '2 · Nudge' : '2 · Có nhắc', i ? '3 · Alone' : '3 · Tự làm'][n], text: x[i],
        on: (e) => { const v = e.target.value; E(d => { d.mi.lv = d.mi.lv || JSON.parse(JSON.stringify(DEFAULT_LV)); d.mi.lv[n][i] = v; }); } })),
"""

def app(h, d):
    # ---- du lieu: them nhiem vu cho tung bai ----
    a = h.index('const L = {'); b = h.index('const SEASONS')
    h = h[:a] + build_L(d) + h[b:]
    h = sub(h, "const WEEK_CAP = 50,", "const DEFAULT_MI = {t:['Làm điều con vừa học cùng ba mẹ','Try what you just learnt with a parent'], s:['Kể cho ba mẹ nghe con sẽ làm gì, rồi làm thật một lần hôm nay.','Tell a parent what you will do, then really do it once today.'], rw:['Một cái ôm thật chặt và lời khen của ba mẹ','A big hug and praise from your parents'], lv:DEFAULT_LV};\nconst WEEK_CAP = 50,")

    # ---- state + luu tru nhiem vu ----
    h = sub(h, "    doneMissions:{}, approved:{}, joined:", f"    doneMissions: {store_load('senapp.mDone', '{}')}, approved: {store_load('senapp.mApproved', '{}')}, joined:")
    h = sub(h, "variant:0, mLevel:{},", f"variant:0, mLevel: {store_load('senapp.mLevel', '{}')}, edPart:'lesson',")
    h = sub(h, "reading:false, mFlag:{},", f"reading:false, mFlag: {store_load('senapp.mFlag', '{}')},")
    h = sub(h, "['customMissions','senapp.customMissions']]) {",
            "['customMissions','senapp.customMissions'],['doneMissions','senapp.mDone'],['approved','senapp.mApproved'],['mLevel','senapp.mLevel'],['mFlag','senapp.mFlag']]) {")
    # nhiem vu gan voi bai, khong xoa moi tuan
    h = sub(h, "if (this.state.missionWeek !== wk) this.setState({missionWeek:wk, doneMissions:{}, approved:{}, mFlag:{}});",
               "if (this.state.missionWeek !== wk) this.setState({missionWeek:wk});")

    # ---- danh sach nhiem vu: moi bai da hoc = 1 nhiem vu ----
    h = sub(h, """    const pendingList = [];
    st.profiles.forEach((p, pi) => {
      if (!p.kid) return;
      allMissions.forEach((m, k) => {
        const mk = pi + '-' + k;
        if (st.doneMissions[mk] && !st.approved[mk]) pendingList.push({m, mk, child:p.name, cav:p.av, lv:st.mLevel[mk]||0});
      });
    });
""", """    const misOf = (l) => { const x = l.mi || DEFAULT_MI; return {t:x.t, s:x.s, rw:x.rw, lv:x.lv || DEFAULT_LV, k:l.sk, from:l.t}; };
    const pendingList = [];
    st.profiles.forEach((p, pi) => {
      if (!p.kid) return;
      const pp = this.progOf(st, p.name, p.band);
      this.effLessons(p.band).forEach(l => { if (!pp.done[l.id]) return; const mk = pi + '-L' + l.id;
        if (st.doneMissions[mk] && !st.approved[mk]) pendingList.push({m: misOf(l), mk, child:p.name, cav:p.av, lv:st.mLevel[mk]||0}); });
    });
""")
    h = sub(h, "    const openMissions = allMissions.filter((_,k)=> !st.approved[st.active+'-'+k]).length;\n",
        "    const openMissions = isParentUser ? 0 : lessons.filter(l => isDone(l) && !st.approved[st.active + '-L' + l.id]).length;\n"
        "    const kidMissions = isParentUser ? [] : lessons.filter(isDone).map(l => ({m: misOf(l), mk: st.active + '-L' + l.id, at: +pgr.done[l.id] || 0}))\n"
        "      .sort((x, y) => y.at - x.at).filter((x, n) => !st.approved[x.mk] || n < 3);\n"
        "    const lessonMis = {m: misOf(lesson), mk: st.active + '-L' + lesson.id};\n")
    h = sub(h, """      missions: this.mOrderOf(allMissions.length).map(k=>{ const m = allMissions[k];
        const mk = st.active + '-' + k, s = st.doneMissions[mk], ap = st.approved[mk];""",
"""      ...(() => { const cards = [lessonMis].concat(kidMissions).map(({m, mk})=>{
        const s = st.doneMissions[mk], ap = st.approved[mk];""")
    h = sub(h, "        };\n      }),\n\n      seasonTitle:",
               "        };\n      }); return {rewardMission: cards.slice(0, 1), missions: cards.slice(1), noMissions: cards.length < 2}; })(),\n\n      seasonTitle:")
    h = sub(h, "          by: m.mine ? t.byParent : '',\n          byChip: m.mine ? 'font-size:11px;font-weight:600;padding:4px 9px;border-radius:99px;background:#FBE3E7;color:#C8102E' : 'display:none',",
               "          by: m.from ? (i?'Lesson: ':'Bài: ') + m.from[i] : '',\n          byChip: m.from ? 'font-size:11px;font-weight:600;padding:4px 9px;border-radius:99px;background:#FBE3E7;color:#C8102E' : 'display:none',")
    # toReward: luu thoi diem hoan thanh de xep nhiem vu moi nhat len dau
    h = sub(h, "...this.progPatch(p, active.name, band, {...pp, done:{...pp.done, [lid]:1}}),", "...this.progPatch(p, active.name, band, {...pp, done:{...pp.done, [lid]: pp.done[lid] || Date.now()}}),")

    # ---- buoc cuoi bai: hien ngay 1 nhiem vu cua bai ----
    tpl_a = h.index('            <sc-for list="{{ missions }}" as="m" hint-placeholder-count="4">')
    tpl_b = h.index('\n            </sc-for>\n', tpl_a) + len('\n            </sc-for>\n')
    card = h[tpl_a:tpl_b]
    rcard = card.replace('<sc-for list="{{ missions }}" as="m" hint-placeholder-count="4">', '<sc-for list="{{ rewardMission }}" as="m" hint-placeholder-count="1">')
    h = sub(h, """                <div sc-camel-on-click="{{ goMissions }}" style="{{ btnPrimary }}">{{ t.toMission }}</div>
                <div sc-camel-on-click="{{ goHome }}" style="font-size:13px;color:#8B7867;cursor:pointer;padding:4px">{{ t.backHome }}</div>""",
"""                <div style="align-self:stretch;text-align:left;display:flex;flex-direction:column;gap:8px;margin-top:4px">
                  <div style="font-family:'Baloo 2',cursive;font-size:18px;font-weight:800;color:#221A15">{{ t.toMission }}</div>
                  <div style="font-size:12.5px;color:#8B7867;line-height:1.5">{{ rewardMisHint }}</div>
""" + rcard.replace('\n            ', '\n                  ').replace('            <sc-for', '                  <sc-for', 1) + """                </div>
                <div sc-camel-on-click="{{ goHome }}" style="{{ btnPrimary }};align-self:stretch">{{ t.backHome }}</div>""")
    h = sub(h, "toMission:'Nhận nhiệm vụ đời thực'", "toMission:'Nhiệm vụ đời thực của bài này'")
    h = sub(h, "toMission:'Get a real-life mission'", "toMission:'This lesson’s real-life mission'")
    h = sub(h, "      rewardLine: i ?", "      rewardMisHint: i ? 'Pick a level, do it for real, then tap “I did it!” — a parent confirms and you get stars.' : 'Chọn mức khó, làm thật ngoài đời rồi bấm “Con làm xong rồi!” — ba mẹ xác nhận là con nhận sao.',\n      rewardLine: i ?")
    # tab Nhiem vu cua con: chua co bai nao
    h = sub(h, """            <div style="border-radius:20px;border:1.5px dashed #D9C7AF;padding:14px;font-size:12.5px;color:#7A6A5C;line-height:1.6">{{ t.missionNote }}</div>""",
"""            <sc-if value="{{ noMissions }}" hint-placeholder-val="{{ false }}">
              <div style="border-radius:20px;background:#FFF;padding:16px;font-size:13.5px;color:#5C4B3C;line-height:1.6;text-align:center">{{ noMissionsText }}</div>
            </sc-if>
            <div style="border-radius:20px;border:1.5px dashed #D9C7AF;padding:14px;font-size:12.5px;color:#7A6A5C;line-height:1.6">{{ t.missionNote }}</div>""")
    h = sub(h, "      rewardMisHint:", "      noMissionsText: i ? 'Finish a lesson to get its real-life mission.' : 'Học xong một bài là con nhận được nhiệm vụ đời thực của bài đó.',\n      rewardMisHint:")
    h = sub(h, "missionsSub:'Làm ngoài đời, ba mẹ xác nhận, nhận sao.'", "missionsSub:'Mỗi bài học một nhiệm vụ. Làm ngoài đời, ba mẹ xác nhận, nhận sao.'")
    h = sub(h, "missionsSub:'Do it offline, a parent confirms, you earn stars.'", "missionsSub:'One mission per lesson. Do it offline, a parent confirms, you earn stars.'")
    # bo tao nhiem vu rieng (moi bai chi 1 nhiem vu)
    h = sub(h, "        open:()=>this.set({creator:['lesson','mission','group','profile'][k], formA:'', formB:'', formC:0, formD:1, formPin:''})\n      })),",
               "        open:()=>this.set({creator:['lesson','mission','group','profile'][k], formA:'', formB:'', formC:0, formD:1, formPin:''})\n      })).filter((_, k) => k !== 1),")

    # ---- bai hoc: di het 3 tinh huong roi moi den cau do ----
    h = sub(h, "      progressFill:`height:100%;width:${{story:20,choice:45,feedback:65,quiz:85,reward:100}[st.step]}%;background:${RED};border-radius:99px;transition:width .3s`,\n      progressLabel:`${{story:1,choice:2,feedback:3,quiz:4,reward:5}[st.step]}/5`,",
        "      ...(() => { const nC = lesson.cx.length, vI = Math.min(st.variant, nC - 1), tot = 3 * nC + 2;\n"
        "        const n = st.step === 'quiz' ? 3 * nC + 1 : st.step === 'reward' ? tot : vI * 3 + ({story:1, choice:2, feedback:3}[st.step] || 1);\n"
        "        return { progressFill:`height:100%;width:${Math.round(n * 100 / tot)}%;background:${RED};border-radius:99px;transition:width .3s`, progressLabel:`${n}/${tot}` }; })(),")
    h = sub(h, """          const on = st.variant===k;
          return { label:v[0], pick:()=>{ this.stopSpeak(); this.set({variant:k, step:'story', choice:null, quiz:null, reading:false}); },
            style:`flex:1;text-align:center;padding:7px 4px;border-radius:12px;font-size:11.5px;font-weight:700;cursor:pointer;color:${on?'#FFF':'#8B7867'};background:${on?RED:'transparent'}` };""",
"""          const vI = Math.min(st.variant, vset.length - 1), on = vI===k, past = k < vI;
          return { label:(past?'✓ ':'') + v[0], pick:()=>{},
            style:`flex:1;text-align:center;padding:7px 4px;border-radius:12px;font-size:11.5px;font-weight:700;cursor:default;color:${on?'#FFF':past?'#1B6B4F':'#B5A28C'};background:${on?RED:past?'#DDF0E6':'transparent'}` };""")
    h = sub(h, "      variantHint: !vset ? (i?'A lesson your parent wrote — it has one situation.':'Bài do ba mẹ tự tạo — bài này chỉ có một tình huống.')\n        : vv.k===0 ?",
               "      variantHint: !vset ? (i?'A lesson your parent wrote — it has one situation.':'Bài do ba mẹ tự tạo — bài này chỉ có một tình huống.')\n        : ((i?'Situation ':'Tình huống ') + (Math.min(st.variant, vset.length - 1) + 1) + '/' + vset.length + ' · ') + (vv.k===0 ?")
    h = sub(h, "        : (i?'Out in the world: shops, the street, the neighbourhood.':'Ra ngoài đời: cửa hàng, đường phố, khu mình sống.'),",
               "        : (i?'Out in the world: shops, the street, the neighbourhood.':'Ra ngoài đời: cửa hàng, đường phố, khu mình sống.')),\n"
               "      ...(() => { const nC = lesson.cx.length, vI = Math.min(st.variant, nC - 1), more = vI < nC - 1;\n"
               "        const nx = more ? [[i?'At home':'Ở nhà'], [i?'At school':'Trên lớp'], [i?'Out there':'Ngoài đời']][lesson.cx[vI + 1].k][0] : '';\n"
               "        return { fbNextLabel: more ? (i ? `Next situation: ${nx} →` : `Tình huống tiếp theo: ${nx} →`) : t.toQuiz,\n"
               "          fbNext: () => { this.stopSpeak(); return more ? this.set({variant: vI + 1, step:'story', choice:null, reading:false}) : this.set({step:'quiz'}); } }; })(),")
    h = sub(h, '<div sc-camel-on-click="{{ toQuiz }}" style="{{ btnPrimary }}">{{ t.toQuiz }}</div>',
               '<div sc-camel-on-click="{{ fbNext }}" style="{{ btnPrimary }}">{{ fbNextLabel }}</div>')

    # ---- man hinh tuy chinh: nhiem vu nam trong tung bai ----
    h = sub(h, "const d = JSON.parse(JSON.stringify({t: cur.t, cx: cur.cx, qq: cur.qq, qo: cur.qo, qa: cur.qa})); fn(d);",
               "const d = JSON.parse(JSON.stringify({t: cur.t, cx: cur.cx, qq: cur.qq, qo: cur.qo, qa: cur.qa, mi: cur.mi || DEFAULT_MI})); fn(d);")
    h = sub(h, "cuShowList: tab === 'lessons' && !ed, cuShowEd: tab === 'lessons' && !!ed, cuShowMis: tab === 'missions',",
               "cuShowList: tab === 'lessons' && !ed, cuShowEd: !!ed, cuShowMis: tab === 'missions' && !ed,")
    h = sub(h, "edit: () => this.set({edId: l.id, edCx: 0})", "edit: () => this.set({edId: l.id, edCx: 0, edPart: 'lesson'})")
    a = h.index("      cuMisHint: i ?"); b = h.index("      cuAddMissionLabel:")
    h = h[:a] + CUST_VALS.lstrip('\n') + h[b:]
    a = h.index('<sc-if value="{{ cuShowMis }}"'); b = h.index('<div sc-camel-on-click="{{ cuResetAll }}"')
    h = h[:a] + MIS_TAB + h[b:]
    # editor: chia 2 phan
    a = h.index(f'                <div style="{LBL}">{{{{ edTitleLabel }}}}</div>')
    b = h.index('                <div style="font-size:11.5px;color:#8B7867;line-height:1.5">{{ edSavedNote }}</div>')
    body = h[a:b]
    h = h[:a] + ED_PARTS + '                <sc-if value="{{ edIsLesson }}" hint-placeholder-val="{{ true }}">\n                  <div style="display:flex;flex-direction:column;gap:10px">\n' \
        + body + '                  </div>\n                </sc-if>\n' + ED_MISSION + h[b:]
    return h

def contact(h, app_side):
    if app_side:
        h = sub(h, "['Gửi mail về mh.senapp@gmail.com. Số điện thoại hỗ trợ giờ hành chính nằm trong mục Quản lý tài khoản.',\n    'Email mh.senapp@gmail.com. The office-hours support number is inside Manage accounts.']",
                   "['Gửi mail về admin.senapp@gmail.com, hoặc nhắn Zalo/Viber tới số hỗ trợ trong mục Quản lý tài khoản. Sen phản hồi chậm nhất trong 24h.',\n    'Email admin.senapp@gmail.com, or message the Zalo/Viber support number inside Manage accounts. Sen replies within 24 hours at the latest.']")
        h = sub(h, "kích hoạt nhanh trong giờ hành chính.", "kích hoạt nhanh, chậm nhất trong 24h.")
        h = sub(h, "activate it quickly during office hours.", "activate it quickly, within 24 hours at the latest.")
        h = sub(h, "qua Zalo hoặc SMS trong giờ hành chính.", "qua Zalo hoặc SMS chậm nhất trong 24h.", 2)
        h = sub(h, "by Zalo or SMS during office hours.", "by Zalo or SMS within 24 hours.", 2)
        h = sub(h, "contactSub: i?'Email Sen · we reply during office hours':'Gửi mail cho Sen · trả lời trong giờ hành chính'",
                   "contactSub: i?'Email Sen · we reply within 24 hours':'Gửi mail cho Sen · phản hồi chậm nhất trong 24h'")
        h = sub(h, "supTitle: i?'Support hotline':'Hỗ trợ qua điện thoại'", "supTitle: i?'Zalo/Viber support':'Zalo/Viber hỗ trợ'")
        h = sub(h, "supHours: i?'Office hours only: 8:00–17:00, Monday to Friday.':'Chỉ trong giờ hành chính: 8:00 – 17:00, thứ Hai – thứ Sáu.'",
                   "supHours: i?'Just send a message — Sen will reply within 24 hours at the latest.':'Ba mẹ cứ nhắn, Sen sẽ phản hồi lại chậm nhất trong 24h nhé ba mẹ.'")
        h = sub(h, "supMail: i?'Any other time, email':'Ngoài giờ, ba mẹ gửi mail tới'", "supMail: i?'Or email':'Hoặc ba mẹ gửi mail tới'")
        h = sub(h, '<a href="tel:0975860488" style=', '<a href="https://zalo.me/0975860488" target="_blank" rel="noopener" style=')
        assert 'giờ hành chính' not in h and 'office hours' not in h.lower(), 'con sot gio hanh chinh'
    # dia chi lien he hien thi -> admin.senapp@gmail.com (giu nguyen kenh FormSubmit nhan don dang ky ve mh.senapp)
    h = re.sub(r'(?<!formsubmit\.co/ajax/)mh\.senapp@gmail\.com', 'admin.senapp@gmail.com', h)
    return h

def patch(path, fn):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', s, re.S)
    t = fn(json.loads(m.group(2)))
    s = s[:m.start(2)] + json.dumps(t, ensure_ascii=False).replace('</', '<\\/') + s[m.end(2):]
    open(path, 'w', encoding='utf-8').write(s); print('ok', path)

if __name__ == '__main__':
    appf, landf, d = sys.argv[1:4]
    patch(appf, lambda t: contact(app(t, d), True))
    patch(landf, lambda t: contact(t, False))
