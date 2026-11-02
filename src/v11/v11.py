"""Senapp v11 (ap dung tren v10): du 45 bai/nhom tuoi (9 tuan x 5 bai), nut "Hoc tuan tiep theo",
ba me tuy chinh thu tu bai, noi dung bai, nhiem vu, phan thuong (luu rieng trong tai khoan gia dinh tren may).
Dung: python3 v11.py <app index.html> <thu muc v11>"""
import json, re, sys, os, gzip, base64, random

def sub(h, a, b, n=1):
    c = h.count(a); assert c == n, (a[:120], c); return h.replace(a, b)

BANDS = ['5-8', '9-12', '13-16']

# ---------- du lieu bai hoc ----------
def fix_week1(W):
    # 12-15 bai 3: boi canh A con noi ve viec lam them -> doi thanh tham gia doi tinh nguyen
    l = W['13-16'][2]
    l['ctx']['A'] = {
        's': ['Khoa muốn tham gia đội tình nguyện của trường vào sáng cuối tuần. Ba mẹ lo ảnh hưởng việc học và chưa đồng ý.',
              'Khoa wants to join the school volunteer team on weekend mornings. The parents worry about schoolwork and have said no for now.'],
        'q': ['Khoa nên trình bày thế nào?', 'How should Khoa make the case?'],
        'o': [['“Bạn con đứa nào cũng vào đội hết rồi.”', '“All my friends have already joined.”', 0,
               'So với bạn không trả lời được nỗi lo của ba mẹ, vốn là việc học.', 'Comparing to friends doesn’t answer the actual worry, which is school.'],
              ['“Con đi hai buổi sáng cuối tuần, vẫn giữ lịch học tối. Thử một tháng, điểm tụt thì con xin nghỉ.”',
               '“Two weekend mornings, evening study unchanged. Trial for a month — if my marks drop, I’ll stop.”', 1,
               'Thuyết phục người lớn giống phỏng vấn: phương án cụ thể, có giới hạn và có điều kiện dừng.', 'Persuading adults is like an interview: a specific plan, bounded, with an exit condition.'],
              ['Tự đăng ký rồi báo sau', 'Sign up and tell them afterwards', 0,
               'Làm rồi báo sau là mất niềm tin, thứ khó xin lại hơn cả sự cho phép.', 'Acting first costs trust, which is harder to win back than permission.']]}
    # 12-15 bai 5: boi canh C "9h toi phai ve" -> 7 gio toi
    o = W['13-16'][4]['ctx']['C']['o'][1]
    o[0] = o[0].replace('“9h tớ phải về”', '“7 giờ tối tớ phải về”'); o[1] = o[1].replace('“I have to leave at nine”', '“I have to leave at seven”')
    assert '7 giờ tối' in o[0] and 'seven' in o[1]

def build_L(d):
    W = json.load(open(os.path.join(d, 'week1.json'), encoding='utf-8')); fix_week1(W)
    L = {}
    for b in BANDS:
        arr = list(W[b])
        for wk in range(2, 10):
            arr += json.load(open(os.path.join(d, 'content', f'{b}-w{wk}.json'), encoding='utf-8'))
        assert len(arr) == 45, (b, len(arr))
        out = []
        for oi, l in enumerate(arr):
            cx = []
            for k, c in enumerate('ABC'):
                v = l['ctx'].get(c) or (l['base'] == c and {'s': l['story'], 'q': l['cq'], 'o': l['co']})
                assert v, (b, oi, c)
                cx.append({'k': k, 's': v['s'], 'q': v['q'], 'o': v['o']})
            out.append({'t': l['t'], 'sk': l['sk'], 'm': l['m'], 'oi': oi, 'story': cx[0]['s'], 'cq': cx[0]['q'], 'co': cx[0]['o'],
                        'qq': l['qq'], 'qo': l['qo'], 'qa': l['qa'], 'cx': cx})
        L[b] = out
    js = 'const L = {\n' + ',\n'.join(f"'{b}': [\n" + ',\n'.join(json.dumps(x, ensure_ascii=False) for x in L[b]) + '\n]' for b in BANDS) + '\n};\n\n'
    return js

# ---------- giao dien ----------
HOME_WEEK = """
            <div style="display:flex;align-items:center;gap:8px;background:#FFF;border-radius:18px;padding:8px;border:1.5px solid #EFE3D2">
              <div sc-camel-on-click="{{ wkPrev }}" style="{{ wkPrevStyle }}">‹</div>
              <div style="flex:1;min-width:0;text-align:center">
                <div style="font-family:'Baloo 2',cursive;font-size:17px;font-weight:800;color:#221A15;line-height:1.15">{{ wkLabel }}</div>
                <div style="font-size:11.5px;color:#8B7867;margin-top:1px">{{ wkMeta }}</div>
              </div>
              <div sc-camel-on-click="{{ wkFwd }}" style="{{ wkFwdStyle }}">›</div>
            </div>
            <div style="height:8px;border-radius:99px;background:#F3E6D3;overflow:hidden;margin-top:-6px"><div style="{{ wkFill }}"></div></div>"""

HOME_NEXT = """            <sc-if value="{{ wkCanNext }}" hint-placeholder-val="{{ false }}">
              <div style="display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center;background:linear-gradient(160deg,#E2F6EE,#FFF6DA);border:2px solid #8FCBAA;border-radius:24px;padding:16px 14px;animation:senPop .35s ease">
                <div style="font-family:'Baloo 2',cursive;font-size:20px;font-weight:800;color:#1B6B4F;line-height:1.15">{{ wkDoneTitle }}</div>
                <div style="font-size:13px;color:#3A2E24;line-height:1.5">{{ wkDoneText }}</div>
                <div sc-camel-on-click="{{ nextWeek }}" style="background:#C8102E;color:#FFF;border-radius:16px;padding:12px 22px;font-family:'Baloo 2',cursive;font-size:17px;font-weight:700;cursor:pointer;box-shadow:0 4px 0 #8F0B20">{{ wkNextLabel }}</div>
              </div>
            </sc-if>
            <sc-if value="{{ wkFinished }}" hint-placeholder-val="{{ false }}">
              <div style="display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;background:linear-gradient(160deg,#FFF6DA,#FFE3EA);border:2px solid #F2C35A;border-radius:24px;padding:16px 14px">
                <div style="font-family:'Baloo 2',cursive;font-size:20px;font-weight:800;color:#C8102E;line-height:1.15">{{ wkFinTitle }}</div>
                <div style="font-size:13px;color:#3A2E24;line-height:1.5">{{ wkFinText }}</div>
              </div>
            </sc-if>
            <sc-if value="{{ wkBack }}" hint-placeholder-val="{{ false }}">
              <div sc-camel-on-click="{{ wkToCur }}" style="align-self:center;font-size:13px;font-weight:700;color:#C8102E;cursor:pointer;padding:6px 10px">{{ wkBackLabel }}</div>
            </sc-if>
"""

PARENT_CARD = """            <div sc-camel-on-click="{{ goCustom }}" style="border-radius:22px;background:#FFF;border:1.5px solid #EFE3D2;padding:14px;display:flex;align-items:center;gap:12px;cursor:pointer">
              <div style="width:42px;height:42px;border-radius:14px;background:#2E9E7E;display:flex;align-items:center;justify-content:center;font-size:21px;flex:none">✏️</div>
              <div style="flex:1;min-width:0">
                <div style="font-family:'Baloo 2',cursive;font-size:18px;font-weight:800;color:#221A15;line-height:1.15">{{ cuCardTitle }}</div>
                <div style="font-size:12px;color:#7A6A5C;line-height:1.45">{{ cuCardSub }}</div>
              </div>
              <div style="font-size:22px;color:#C8102E;flex:none">›</div>
            </div>
"""

LBL = "font-size:11.5px;font-weight:700;color:#8B7867;letter-spacing:.3px"
INP = "border:1.5px solid #EFE3D2;background:#FFF;border-radius:12px;padding:10px 12px;font-size:14px;color:#221A15;width:100%;box-sizing:border-box;font-family:'Be Vietnam Pro',sans-serif"
TXA = INP + ";min-height:74px;resize:vertical;line-height:1.5"
SBTN = "width:30px;height:30px;border-radius:10px;background:#F3E6D3;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;color:#5C4B3C;cursor:pointer;flex:none"

CUSTOM = f"""
        <!-- CUSTOM (ba me tuy chinh noi dung) -->
        <sc-if value="{{{{ isCustom }}}}" hint-placeholder-val="{{{{ false }}}}">
          <div data-screen-label="13 Custom" style="display:flex;flex-direction:column;gap:12px;animation:senSlide .3s ease">
            <div style="display:flex;align-items:center;gap:10px">
              <div sc-camel-on-click="{{{{ cuBack }}}}" style="width:32px;height:32px;border-radius:10px;background:#F3E6D3;display:flex;align-items:center;justify-content:center;font-size:17px;color:#221A15;cursor:pointer;flex:none">‹</div>
              <div style="font-family:'Baloo 2',cursive;font-size:21px;font-weight:800;color:#221A15;line-height:1.1">{{{{ cuTitle }}}}</div>
            </div>
            <div style="background:#DDF0E6;color:#1B6B4F;border-radius:16px;padding:11px 13px;font-size:12.5px;line-height:1.55;font-weight:600">🔒 {{{{ cuNote }}}}</div>
            <div style="display:flex;background:#F3E6D3;border-radius:14px;padding:3px;gap:3px">
              <sc-for list="{{{{ cuTabs }}}}" as="x" hint-placeholder-count="2">
                <div sc-camel-on-click="{{{{ x.pick }}}}" style="{{{{ x.style }}}}">{{{{ x.label }}}}</div>
              </sc-for>
            </div>

            <sc-if value="{{{{ cuShowList }}}}" hint-placeholder-val="{{{{ true }}}}">
              <div style="display:flex;flex-direction:column;gap:10px">
                <div style="display:flex;gap:6px;flex-wrap:wrap">
                  <sc-for list="{{{{ cuBands }}}}" as="x" hint-placeholder-count="3">
                    <div sc-camel-on-click="{{{{ x.pick }}}}" style="{{{{ x.style }}}}">{{{{ x.label }}}}</div>
                  </sc-for>
                </div>
                <div style="font-size:12px;color:#8B7867;line-height:1.5">{{{{ cuListHint }}}}</div>
                <sc-for list="{{{{ cuWeeks }}}}" as="w" hint-placeholder-count="2">
                  <div style="display:flex;flex-direction:column;gap:6px">
                    <div style="font-family:'Baloo 2',cursive;font-size:16px;font-weight:800;color:#C8102E;margin-top:4px">{{{{ w.title }}}}</div>
                    <sc-for list="{{{{ w.rows }}}}" as="r" hint-placeholder-count="5">
                      <div style="{{{{ r.card }}}}">
                        <div style="{{{{ r.dot }}}}">{{{{ r.n }}}}</div>
                        <div sc-camel-on-click="{{{{ r.edit }}}}" style="flex:1;min-width:0;cursor:pointer">
                          <div style="font-size:14px;font-weight:700;color:#221A15;line-height:1.3">{{{{ r.title }}}}</div>
                          <div style="font-size:11.5px;color:#8B7867;margin-top:2px">{{{{ r.sub }}}}</div>
                        </div>
                        <div style="display:flex;gap:4px;flex:none">
                          <div sc-camel-on-click="{{{{ r.up }}}}" aria-label="{{{{ r.upLabel }}}}" style="{{{{ r.upStyle }}}}">↑</div>
                          <div sc-camel-on-click="{{{{ r.down }}}}" aria-label="{{{{ r.downLabel }}}}" style="{{{{ r.downStyle }}}}">↓</div>
                          <div sc-camel-on-click="{{{{ r.edit }}}}" aria-label="{{{{ r.editLabel }}}}" style="{SBTN};background:#FBE3E7;color:#C8102E">✎</div>
                        </div>
                      </div>
                    </sc-for>
                  </div>
                </sc-for>
                <div sc-camel-on-click="{{{{ cuAddLesson }}}}" style="text-align:center;border:1.5px dashed #C8102E;color:#C8102E;border-radius:16px;padding:12px;font-weight:700;font-size:14px;cursor:pointer">{{{{ cuAddLessonLabel }}}}</div>
              </div>
            </sc-if>

            <sc-if value="{{{{ cuShowEd }}}}" hint-placeholder-val="{{{{ false }}}}">
              <div style="display:flex;flex-direction:column;gap:10px;background:#FFF;border-radius:22px;padding:14px;border:1.5px solid #EFE3D2">
                <div style="display:flex;align-items:center;gap:8px">
                  <div sc-camel-on-click="{{{{ edClose }}}}" style="font-size:13px;font-weight:700;color:#C8102E;cursor:pointer">{{{{ edCloseLabel }}}}</div>
                  <div style="flex:1"></div>
                  <div style="font-size:11px;font-weight:700;padding:4px 9px;border-radius:99px;background:#FFF0D2;color:#8F6A1E">{{{{ edLangNote }}}}</div>
                </div>
                <div style="{LBL}">{{{{ edTitleLabel }}}}</div>
                <input value="{{{{ edTitle }}}}" sc-camel-on-change="{{{{ edOnTitle }}}}" style="{INP};font-weight:700">
                <div style="{LBL}">{{{{ edWeekLabel }}}}</div>
                <div style="display:flex;gap:5px;flex-wrap:wrap">
                  <sc-for list="{{{{ edWeeks }}}}" as="x" hint-placeholder-count="9">
                    <div sc-camel-on-click="{{{{ x.pick }}}}" style="{{{{ x.style }}}}">{{{{ x.label }}}}</div>
                  </sc-for>
                </div>
                <sc-if value="{{{{ edHasCtx }}}}" hint-placeholder-val="{{{{ true }}}}">
                  <div style="display:flex;flex-direction:column;gap:6px">
                    <div style="{LBL}">{{{{ edCtxLabel }}}}</div>
                    <sc-for list="{{{{ edCtxs }}}}" as="c" hint-placeholder-count="3">
                      <div style="{{{{ c.row }}}}">
                        <div sc-camel-on-click="{{{{ c.pick }}}}" style="flex:1;font-size:13px;font-weight:700;cursor:pointer">{{{{ c.label }}}}</div>
                        <div sc-camel-on-click="{{{{ c.up }}}}" style="{{{{ c.upStyle }}}}">↑</div>
                        <div sc-camel-on-click="{{{{ c.down }}}}" style="{{{{ c.downStyle }}}}">↓</div>
                      </div>
                    </sc-for>
                  </div>
                </sc-if>
                <div style="{LBL}">{{{{ edStoryLabel }}}}</div>
                <textarea value="{{{{ edStory }}}}" sc-camel-on-change="{{{{ edOnStory }}}}" style="{TXA}"></textarea>
                <div style="{LBL}">{{{{ edQLabel }}}}</div>
                <input value="{{{{ edQ }}}}" sc-camel-on-change="{{{{ edOnQ }}}}" style="{INP}">
                <div style="{LBL}">{{{{ edChoicesLabel }}}}</div>
                <sc-for list="{{{{ edChoices }}}}" as="o" hint-placeholder-count="3">
                  <div style="display:flex;flex-direction:column;gap:6px;background:#FFFBF4;border-radius:16px;padding:10px;border:1.5px solid #EFE3D2">
                    <div style="display:flex;align-items:center;gap:6px">
                      <div style="width:26px;height:26px;border-radius:9px;background:#F3E6D3;color:#5C4B3C;display:flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:700;flex:none">{{{{ o.letter }}}}</div>
                      <div sc-camel-on-click="{{{{ o.toggle }}}}" style="{{{{ o.okStyle }}}}">{{{{ o.okLabel }}}}</div>
                      <div style="flex:1"></div>
                      <div sc-camel-on-click="{{{{ o.up }}}}" style="{{{{ o.upStyle }}}}">↑</div>
                      <div sc-camel-on-click="{{{{ o.down }}}}" style="{{{{ o.downStyle }}}}">↓</div>
                    </div>
                    <textarea value="{{{{ o.text }}}}" sc-camel-on-change="{{{{ o.onText }}}}" style="{TXA};min-height:52px"></textarea>
                    <div style="{LBL}">{{{{ o.tipLabel }}}}</div>
                    <textarea value="{{{{ o.tip }}}}" sc-camel-on-change="{{{{ o.onTip }}}}" style="{TXA};min-height:52px"></textarea>
                  </div>
                </sc-for>
                <div style="{LBL}">{{{{ edQqLabel }}}}</div>
                <input value="{{{{ edQq }}}}" sc-camel-on-change="{{{{ edOnQq }}}}" style="{INP}">
                <sc-for list="{{{{ edQopts }}}}" as="o" hint-placeholder-count="3">
                  <div style="display:flex;align-items:center;gap:6px">
                    <div style="width:26px;height:26px;border-radius:9px;background:#F3E6D3;color:#5C4B3C;display:flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:700;flex:none">{{{{ o.letter }}}}</div>
                    <input value="{{{{ o.text }}}}" sc-camel-on-change="{{{{ o.onText }}}}" style="{INP};flex:1;width:auto;min-width:0">
                    <div sc-camel-on-click="{{{{ o.toggle }}}}" style="{{{{ o.okStyle }}}}">✓</div>
                    <div sc-camel-on-click="{{{{ o.up }}}}" style="{{{{ o.upStyle }}}}">↑</div>
                    <div sc-camel-on-click="{{{{ o.down }}}}" style="{{{{ o.downStyle }}}}">↓</div>
                  </div>
                </sc-for>
                <div style="font-size:11.5px;color:#8B7867;line-height:1.5">{{{{ edSavedNote }}}}</div>
                <div style="display:flex;gap:8px;flex-wrap:wrap">
                  <div sc-camel-on-click="{{{{ edClose }}}}" style="flex:1;text-align:center;background:#C8102E;color:#FFF;border-radius:14px;padding:12px;font-weight:700;font-size:14px;cursor:pointer">{{{{ edDoneLabel }}}}</div>
                  <sc-if value="{{{{ edEdited }}}}" hint-placeholder-val="{{{{ false }}}}">
                    <div sc-camel-on-click="{{{{ edReset }}}}" style="flex:1;text-align:center;background:#FFF;color:#C8102E;border:1.5px solid #C8102E;border-radius:14px;padding:11px;font-weight:700;font-size:13.5px;cursor:pointer">{{{{ edResetLabel }}}}</div>
                  </sc-if>
                </div>
              </div>
            </sc-if>

            <sc-if value="{{{{ cuShowMis }}}}" hint-placeholder-val="{{{{ false }}}}">
              <div style="display:flex;flex-direction:column;gap:10px">
                <div style="font-size:12px;color:#8B7867;line-height:1.5">{{{{ cuMisHint }}}}</div>
                <sc-for list="{{{{ cuMissions }}}}" as="m" hint-placeholder-count="4">
                  <div style="display:flex;flex-direction:column;gap:7px;background:#FFF;border-radius:20px;padding:12px;border:1.5px solid #EFE3D2">
                    <div style="display:flex;align-items:center;gap:6px">
                      <div style="width:28px;height:28px;border-radius:10px;background:#F2A93B;color:#FFF;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;flex:none">{{{{ m.n }}}}</div>
                      <div style="flex:1;font-size:11.5px;font-weight:700;color:#8B7867">{{{{ m.skill }}}}</div>
                      <div sc-camel-on-click="{{{{ m.up }}}}" style="{{{{ m.upStyle }}}}">↑</div>
                      <div sc-camel-on-click="{{{{ m.down }}}}" style="{{{{ m.downStyle }}}}">↓</div>
                    </div>
                    <div style="{LBL}">{{{{ m.titleLabel }}}}</div>
                    <input value="{{{{ m.title }}}}" sc-camel-on-change="{{{{ m.onTitle }}}}" style="{INP};font-weight:700">
                    <div style="{LBL}">{{{{ m.subLabel }}}}</div>
                    <textarea value="{{{{ m.sub }}}}" sc-camel-on-change="{{{{ m.onSub }}}}" style="{TXA};min-height:52px"></textarea>
                    <div style="{LBL}">🎁 {{{{ m.rwLabel }}}}</div>
                    <input value="{{{{ m.rw }}}}" sc-camel-on-change="{{{{ m.onRw }}}}" style="{INP};background:#FFF6E4;border-style:dashed;border-color:#F0CE8C">
                    <div style="{LBL}">{{{{ m.lvLabel }}}}</div>
                    <sc-for list="{{{{ m.levels }}}}" as="lv" hint-placeholder-count="3">
                      <div style="display:flex;gap:6px;align-items:flex-start">
                        <div style="font-size:11px;font-weight:700;color:#C8102E;width:62px;flex:none;padding-top:10px">{{{{ lv.label }}}}</div>
                        <textarea value="{{{{ lv.text }}}}" sc-camel-on-change="{{{{ lv.on }}}}" style="{TXA};min-height:48px;flex:1;width:auto;min-width:0"></textarea>
                      </div>
                    </sc-for>
                    <sc-if value="{{{{ m.edited }}}}" hint-placeholder-val="{{{{ false }}}}">
                      <div sc-camel-on-click="{{{{ m.reset }}}}" style="align-self:flex-start;font-size:12.5px;font-weight:700;color:#C8102E;cursor:pointer">{{{{ m.resetLabel }}}}</div>
                    </sc-if>
                  </div>
                </sc-for>
                <div sc-camel-on-click="{{{{ cuAddMission }}}}" style="text-align:center;border:1.5px dashed #C8102E;color:#C8102E;border-radius:16px;padding:12px;font-weight:700;font-size:14px;cursor:pointer">{{{{ cuAddMissionLabel }}}}</div>
              </div>
            </sc-if>

            <div sc-camel-on-click="{{{{ cuResetAll }}}}" style="{{{{ cuResetStyle }}}}">{{{{ cuResetLabel }}}}</div>
          </div>
        </sc-if>
"""

METHODS = r"""
  bandLessons(band){ return this.effLessons(band); }

  // ----- noi dung rieng cua gia dinh (chi luu tren may nay, khong gui ve Senapp) -----
  effLessons(band, s = this.state){
    const c = s.cust || {}, les = c.les || {};
    const base = (L[band] || L['9-12']).map(l => ({...l, id: band + ':' + l.oi}))
      .concat(((s.customLessons || {})[band] || []).map((l, n) => ({...l, id: band + ':c' + n})));
    const byId = {};
    base.forEach(l => { const o = les[l.id]; const m = o ? {...l, ...o, edited: true} : {...l};
      if (!m.cx || !m.cx.length) m.cx = [{k: 0, s: m.story, q: m.cq, o: m.co}];
      byId[l.id] = m; });
    const ord = ((c.order || {})[band] || []).filter(id => byId[id]), seen = new Set(ord);
    base.forEach(l => { if (!seen.has(l.id)) ord.push(l.id); });
    return ord.map(id => byId[id]);
  }
  custPatch(p, fn){ const c = JSON.parse(JSON.stringify(p.cust || {})); c.order = c.order || {}; c.les = c.les || {}; c.mis = c.mis || {}; c.mOrder = c.mOrder || []; fn(c); return {cust: c}; }
  moveLesson(band, id, to){ this.setState(p => this.custPatch(p, c => {
    const ids = this.effLessons(band, p).map(l => l.id), from = ids.indexOf(id); if (from < 0) return;
    const dest = Math.max(0, Math.min(ids.length - 1, to)); ids.splice(from, 1); ids.splice(dest, 0, id); c.order[band] = ids; })); }
  editLesson(band, id, fn){ this.setState(p => { const cur = this.effLessons(band, p).find(l => l.id === id); if (!cur) return {};
    const d = JSON.parse(JSON.stringify({t: cur.t, cx: cur.cx, qq: cur.qq, qo: cur.qo, qa: cur.qa})); fn(d);
    return this.custPatch(p, c => { c.les[id] = d; }); }); }
  resetLesson(id){ this.setState(p => this.custPatch(p, c => { delete c.les[id]; })); }
  effMissions(s = this.state){
    const mis = (s.cust || {}).mis || {};
    return MISSIONS.concat(s.customMissions || []).map((m, k) => { const lv = m.lv || MISSION_LEVELS[k] || DEFAULT_LV, o = mis[k];
      return o ? {...m, lv, ...o, edited: true} : {...m, lv}; });
  }
  mOrderOf(n, s = this.state){ const ord = (((s.cust || {}).mOrder) || []).filter(k => k < n), seen = new Set(ord);
    for (let k = 0; k < n; k++) if (!seen.has(k)) ord.push(k); return ord; }
  moveMission(k, dir){ this.setState(p => this.custPatch(p, c => { const ord = this.mOrderOf(this.effMissions(p).length, p), at = ord.indexOf(k), to = at + dir;
    if (at < 0 || to < 0 || to >= ord.length) return; ord.splice(at, 1); ord.splice(to, 0, k); c.mOrder = ord; })); }
  editMission(k, fn){ this.setState(p => { const cur = this.effMissions(p)[k]; if (!cur) return {};
    const d = JSON.parse(JSON.stringify({t: cur.t, s: cur.s, rw: cur.rw || ['', ''], lv: cur.lv})); fn(d);
    return this.custPatch(p, c => { c.mis[k] = d; }); }); }
  resetMission(k){ this.setState(p => this.custPatch(p, c => { delete c.mis[k]; })); }

  // ----- tien do theo tuan cua tung con -----
  progOf(s, name, band){ const p = ((s.prog || {})[name] || {})[band]; return p ? {wk: p.wk || 0, done: p.done || {}} : {wk: 0, done: {}}; }
  progPatch(s, name, band, np){ return {prog: {...(s.prog || {}), [name]: {...((s.prog || {})[name] || {}), [band]: np}}}; }

  custVals(i){
    const st = this.state, kids = st.profiles.filter(p => p.kid);
    const band = st.custBand || (kids[0] && kids[0].band !== 'parent' ? kids[0].band : '9-12');
    const lessons = this.effLessons(band), WK = 5, nW = Math.max(1, Math.ceil(lessons.length / WK));
    const sb = (on) => `{SBTN};opacity:${on ? 1 : .3};pointer-events:${on ? 'auto' : 'none'}`;
    const pill = (on) => `flex:1;text-align:center;padding:8px 6px;border-radius:12px;font-size:13px;font-weight:700;cursor:pointer;color:${on ? '#FFF' : '#8B7867'};background:${on ? RED : 'transparent'}`;
    const chip = (on) => `padding:6px 12px;border-radius:99px;font-size:12.5px;font-weight:700;cursor:pointer;color:${on ? '#FFF' : '#5C4B3C'};background:${on ? INK : '#F3E6D3'}`;
    const ed = st.edId ? lessons.find(l => l.id === st.edId) : null, edAt = ed ? lessons.indexOf(ed) : -1;
    const cxi = ed ? Math.min(st.edCx || 0, ed.cx.length - 1) : 0, cx = ed ? ed.cx[cxi] : null;
    const CXL = [[i ? 'A · At home' : 'A · Ở nhà'], [i ? 'B · At school' : 'B · Trên lớp'], [i ? 'C · Out there' : 'C · Ngoài đời']];
    const E = (fn) => this.editLesson(band, ed.id, fn);
    const swap = (a, x, y) => { const t0 = a[x]; a[x] = a[y]; a[y] = t0; };
    const tab = st.custTab || 'lessons';
    const allM = this.effMissions(), mOrd = this.mOrderOf(allM.length);
    return {
      cuCardTitle: i ? 'Customise lessons & missions' : 'Tuỳ chỉnh bài học & nhiệm vụ',
      cuCardSub: i ? 'Reorder lessons, edit stories, missions and rewards — for your family only.' : 'Đổi thứ tự bài, sửa câu chuyện, nhiệm vụ và phần thưởng — chỉ riêng gia đình mình.',
      goCustom: () => this.set({screen: 'custom', edId: null, custReset: false}),
      cuBack: () => this.set({screen: 'parent', edId: null, custReset: false}),
      cuTitle: i ? 'Family customisation' : 'Tuỳ chỉnh của gia đình',
      cuNote: i ? 'Changes are saved only inside your family account on this device. They are never sent back to Senapp and do not change lessons for other families.'
                : 'Mọi thay đổi chỉ lưu trong tài khoản gia đình mình trên thiết bị này. Senapp không nhận lại và không thay đổi bài của gia đình khác.',
      cuTabs: [['lessons', i ? 'Lessons' : 'Bài học'], ['missions', i ? 'Missions & rewards' : 'Nhiệm vụ & phần thưởng']].map(([k, label]) =>
        ({label, style: pill(tab === k), pick: () => this.set({custTab: k, edId: null})})),
      cuShowList: tab === 'lessons' && !ed, cuShowEd: tab === 'lessons' && !!ed, cuShowMis: tab === 'missions',
      cuBands: ['5-8', '9-12', '13-16'].map(b => ({label: (i ? 'Ages ' : '') + (b === '5-8' ? '6–8' : b === '9-12' ? '9–11' : '12–15') + (i ? '' : ' tuổi'),
        style: chip(b === band), pick: () => this.set({custBand: b, edId: null})})),
      cuListHint: i ? 'Every 5 lessons make one week. Use ↑ ↓ to change the order, ✎ to edit the text.' : 'Mỗi 5 bài là một tuần. Bấm ↑ ↓ để đổi thứ tự, ✎ để sửa nội dung.',
      cuWeeks: Array.from({length: nW}, (_, w) => ({ title: (i ? 'Week ' : 'Tuần ') + (w + 1),
        rows: lessons.slice(w * WK, w * WK + WK).map((l, j) => { const at = w * WK + j;
          return { n: String(j + 1), title: l.t[i], sub: SKILLS[l.sk][i] + (l.mine ? (i ? ' · parent-made' : ' · ba mẹ tạo') : '') + (l.edited ? (i ? ' · edited' : ' · đã sửa') : ''),
            card: `display:flex;gap:9px;align-items:center;padding:10px;border-radius:16px;background:#FFF;border:1.5px solid ${l.edited ? '#F0CE8C' : '#EFE3D2'}`,
            dot: `width:28px;height:28px;border-radius:10px;flex:none;display:flex;align-items:center;justify-content:center;font-family:'Baloo 2',cursive;font-weight:800;font-size:14px;color:#FFF;background:${l.mine ? JADE : GOLD}`,
            up: () => this.moveLesson(band, l.id, at - 1), down: () => this.moveLesson(band, l.id, at + 1), edit: () => this.set({edId: l.id, edCx: 0}),
            upStyle: sb(at > 0), downStyle: sb(at < lessons.length - 1), upLabel: i ? 'Move up' : 'Lên', downLabel: i ? 'Move down' : 'Xuống', editLabel: i ? 'Edit' : 'Sửa' }; }) })),
      cuAddLessonLabel: i ? '＋ Write a new lesson' : '＋ Tự viết bài mới',
      cuAddLesson: () => this.set({creator: 'lesson', formA: '', formB: '', formC: 0, formD: ['5-8', '9-12', '13-16'].indexOf(band), formPin: ''}),
      edClose: () => this.set({edId: null}), edCloseLabel: i ? '‹ Back to the list' : '‹ Về danh sách',
      edLangNote: i ? 'Editing English text' : 'Đang sửa bản tiếng Việt',
      edTitleLabel: i ? 'LESSON TITLE' : 'TÊN BÀI', edTitle: ed ? ed.t[i] : '', edOnTitle: (e) => { const v = e.target.value; E(d => { d.t[i] = v; }); },
      edWeekLabel: i ? 'MOVE TO WEEK' : 'CHUYỂN SANG TUẦN',
      edWeeks: !ed ? [] : Array.from({length: nW}, (_, w) => ({label: String(w + 1), style: chip(Math.floor(edAt / WK) === w),
        pick: () => this.moveLesson(band, ed.id, Math.floor(edAt / WK) === w ? edAt : w < Math.floor(edAt / WK) ? w * WK + WK - 1 : w * WK)})),
      edHasCtx: !!ed && ed.cx.length > 1,
      edCtxLabel: i ? 'SETTINGS — tap to edit, ↑ ↓ to change the order the child sees' : 'BỐI CẢNH — bấm để sửa, ↑ ↓ để đổi thứ tự con thấy',
      edCtxs: !ed ? [] : ed.cx.map((c, k) => ({ label: (k + 1) + '. ' + CXL[c.k][0],
        row: `display:flex;align-items:center;gap:6px;padding:7px 9px;border-radius:12px;color:${k === cxi ? '#FFF' : '#221A15'};background:${k === cxi ? RED : '#F8F1E4'}`,
        pick: () => this.set({edCx: k}),
        up: () => { E(d => swap(d.cx, k, k - 1)); this.set({edCx: k - 1}); }, down: () => { E(d => swap(d.cx, k, k + 1)); this.set({edCx: k + 1}); },
        upStyle: sb(k > 0), downStyle: sb(k < ed.cx.length - 1) })),
      edStoryLabel: i ? 'STORY' : 'CÂU CHUYỆN', edStory: cx ? cx.s[i] : '', edOnStory: (e) => { const v = e.target.value; E(d => { d.cx[cxi].s[i] = v; }); },
      edQLabel: i ? 'QUESTION' : 'CÂU HỎI', edQ: cx ? cx.q[i] : '', edOnQ: (e) => { const v = e.target.value; E(d => { d.cx[cxi].q[i] = v; }); },
      edChoicesLabel: i ? 'CHOICES — ↑ ↓ to reorder, tap “Right answer” to mark it' : 'CÁC LỰA CHỌN — ↑ ↓ để đổi thứ tự, bấm “Đáp án đúng” để chọn',
      edChoices: !cx ? [] : cx.o.map((o, k) => ({ letter: 'ABCDE'[k], text: o[i], tip: o[3 + i], tipLabel: i ? 'Sen’s tip' : 'Mẹo của Sen',
        okLabel: o[2] ? (i ? '✓ Right answer' : '✓ Đáp án đúng') : (i ? 'Mark right' : 'Đặt là đúng'),
        okStyle: `font-size:11.5px;font-weight:700;padding:5px 10px;border-radius:99px;cursor:pointer;color:${o[2] ? '#FFF' : '#5C4B3C'};background:${o[2] ? JADE : '#F3E6D3'}`,
        toggle: () => E(d => { d.cx[cxi].o.forEach((x, n) => { x[2] = n === k ? 1 : 0; }); }),
        onText: (e) => { const v = e.target.value; E(d => { d.cx[cxi].o[k][i] = v; }); },
        onTip: (e) => { const v = e.target.value; E(d => { d.cx[cxi].o[k][3 + i] = v; }); },
        up: () => E(d => swap(d.cx[cxi].o, k, k - 1)), down: () => E(d => swap(d.cx[cxi].o, k, k + 1)),
        upStyle: sb(k > 0), downStyle: sb(k < cx.o.length - 1) })),
      edQqLabel: i ? 'END-OF-LESSON QUIZ' : 'CÂU ĐỐ CUỐI BÀI', edQq: ed ? ed.qq[i] : '', edOnQq: (e) => { const v = e.target.value; E(d => { d.qq[i] = v; }); },
      edQopts: !ed ? [] : ed.qo.map((o, k) => ({ letter: 'ABCDE'[k], text: o[i],
        onText: (e) => { const v = e.target.value; E(d => { d.qo[k][i] = v; }); },
        okStyle: `${SBTN};color:${ed.qa === k ? '#FFF' : '#5C4B3C'};background:${ed.qa === k ? JADE : '#F3E6D3'}`,
        toggle: () => E(d => { d.qa = k; }),
        up: () => E(d => { swap(d.qo, k, k - 1); d.qa = d.qa === k ? k - 1 : d.qa === k - 1 ? k : d.qa; }),
        down: () => E(d => { swap(d.qo, k, k + 1); d.qa = d.qa === k ? k + 1 : d.qa === k + 1 ? k : d.qa; }),
        upStyle: sb(k > 0), downStyle: sb(k < ed.qo.length - 1) })),
      edSavedNote: i ? 'Saved automatically as you type. ✓ marks the right answer.' : 'Tự động lưu khi ba mẹ gõ. Dấu ✓ là đáp án đúng.',
      edDoneLabel: i ? 'Done' : 'Xong', edEdited: !!(ed && ed.edited), edResetLabel: i ? 'Restore original' : 'Khôi phục bài gốc',
      edReset: () => ed && this.resetLesson(ed.id),
      cuMisHint: i ? 'Edit missions, difficulty levels and rewards directly. ↑ ↓ changes the order your children see.' : 'Sửa trực tiếp nhiệm vụ, các mức khó và phần thưởng. ↑ ↓ đổi thứ tự con nhìn thấy.',
      cuMissions: mOrd.map((k, at) => { const m = allM[k], M = (fn) => this.editMission(k, fn);
        return { n: String(at + 1), skill: SKILLS[m.k][i] + (m.mine ? (i ? ' · parent-made' : ' · ba mẹ tạo') : ''),
          titleLabel: i ? 'MISSION' : 'NHIỆM VỤ', title: m.t[i], onTitle: (e) => { const v = e.target.value; M(d => { d.t[i] = v; }); },
          subLabel: i ? 'HOW TO DO IT' : 'HƯỚNG DẪN', sub: m.s[i], onSub: (e) => { const v = e.target.value; M(d => { d.s[i] = v; }); },
          rwLabel: i ? 'REWARD' : 'PHẦN THƯỞNG', rw: m.rw ? m.rw[i] : '', onRw: (e) => { const v = e.target.value; M(d => { d.rw[i] = v; }); },
          lvLabel: i ? 'THREE DIFFICULTY LEVELS' : 'BA MỨC KHÓ',
          levels: m.lv.map((x, n) => ({ label: [i ? '1 · Together' : '1 · Cùng làm', i ? '2 · Nudge' : '2 · Có nhắc', i ? '3 · Alone' : '3 · Tự làm'][n], text: x[i],
            on: (e) => { const v = e.target.value; M(d => { d.lv[n][i] = v; }); } })),
          up: () => this.moveMission(k, -1), down: () => this.moveMission(k, 1), upStyle: sb(at > 0), downStyle: sb(at < mOrd.length - 1),
          edited: !!m.edited, reset: () => this.resetMission(k), resetLabel: i ? '↺ Restore original' : '↺ Khôi phục bản gốc' }; }),
      cuAddMissionLabel: i ? '＋ Create a new mission' : '＋ Tạo nhiệm vụ mới',
      cuAddMission: () => this.set({creator: 'mission', formA: '', formB: '', formC: 0, formD: 1, formPin: '', formR: ''}),
      cuResetLabel: st.custReset ? (i ? 'Tap again to restore all Senapp defaults' : 'Bấm lần nữa để khôi phục toàn bộ mặc định') : (i ? '↺ Restore all defaults' : '↺ Khôi phục toàn bộ mặc định'),
      cuResetStyle: `text-align:center;margin-top:6px;border-radius:14px;padding:11px;font-size:13px;font-weight:700;cursor:pointer;color:${st.custReset ? '#FFF' : '#8B7867'};background:${st.custReset ? RED : 'transparent'};border:1.5px solid ${st.custReset ? RED : '#D9C7AF'}`,
      cuResetAll: () => st.custReset ? this.set({cust: {order: {}, les: {}, mis: {}, mOrder: []}, custReset: false, edId: null}) : this.set({custReset: true}),
    };
  }
""".replace('{SBTN}', SBTN)

def store_load(key, dflt):
    return f"(() => {{ try {{ return JSON.parse(localStorage.getItem('{key}') || 'null') || {dflt}; }} catch (e) {{ return {dflt}; }} }})()"

def app(h, d):
    # 1) du lieu: 45 bai/nhom tuoi, moi bai 3 boi canh
    a = h.index('const L = {'); b = h.index('const SEASONS')
    h = h[:a] + build_L(d) + h[b:]
    h = sub(h, "const WEEK_CAP = 50,", "const DEFAULT_LV = [['Ba mẹ làm mẫu trước, con làm cùng một phần.','A parent models it and you do part of it together.'],['Ba mẹ nhắc một lần, con tự làm phần còn lại.','One reminder, then you do the rest yourself.'],['Con tự nhớ, tự làm rồi kể lại cho ba mẹ nghe.','Remember it, do it alone, then tell a parent how it went.']];\nconst WEEK_CAP = 50,")
    # 2) state
    h = sub(h, "showRank:false, customLessons:{}, customMissions:[], customGroups:[],",
        "showRank:false, customGroups:[],\n"
        f"    cust: {store_load('senapp.custom', '{order:{}, les:{}, mis:{}, mOrder:[]}')},\n"
        f"    customLessons: {store_load('senapp.customLessons', '{}')}, customMissions: {store_load('senapp.customMissions', '[]')},\n"
        f"    prog: {store_load('senapp.progress', '{}')}, viewWeek:null, custTab:'lessons', custBand:null, edId:null, edCx:0, custReset:false,")
    h = sub(h, "\n  bandLessons(band){ return (L[band]||L['9-12']).concat(this.state.customLessons[band]||[]); }\n", METHODS)
    # 3) luu
    h = sub(h, "    if (this._wkSaved !== st.weekLog)",
        "    for (const [k, key] of [['cust','senapp.custom'],['prog','senapp.progress'],['customLessons','senapp.customLessons'],['customMissions','senapp.customMissions']]) {\n"
        "      if ((this._cs = this._cs || {})[k] !== st[k]) { this._cs[k] = st[k]; try { localStorage.setItem(key, JSON.stringify(st[k])); } catch (e) {} } }\n"
        "    if (this._wkSaved !== st.weekLog)")
    # 4) tinh tuan
    h = sub(h, "    const lessons = this.bandLessons(band);\n    const lesson = lessons[Math.min(st.lesson, lessons.length-1)];\n",
        "    const lessons = this.effLessons(band);\n    const lesson = lessons[Math.min(st.lesson, lessons.length-1)];\n"
        "    const WK = 5, nWeeks = Math.max(1, Math.ceil(lessons.length / WK)), pgr = this.progOf(st, active.name, band);\n"
        "    const curWk = Math.min(pgr.wk, nWeeks - 1), viewWk = st.viewWeek == null ? curWk : Math.max(0, Math.min(st.viewWeek, curWk));\n"
        "    const isDone = l => !!pgr.done[l.id], isLocked = l => !st.owned[l.sk] && !l.mine;\n"
        "    const weekIdx = w => lessons.map((_, x) => x).slice(w * WK, w * WK + WK);\n"
        "    const weekDone = weekIdx(curWk).every(x => isDone(lessons[x]) || isLocked(lessons[x])), hasNext = curWk < nWeeks - 1;\n"
        "    const nextWeek = () => this.setState(p => { const pp = this.progOf(p, active.name, band); return {...this.progPatch(p, active.name, band, {...pp, wk: Math.min(nWeeks - 1, pp.wk + 1)}), viewWeek: null}; });\n")
    h = sub(h, "    const vsets = (window.SEN_VARIANTS && window.SEN_VARIANTS[band]) || [];\n    const vset = vsets[st.lesson] || null;\n    const vv = (vset && vset[st.variant]) ? vset[st.variant] : null;\n",
        "    const vset = lesson.cx.length > 1 ? lesson.cx : null;\n    const vv = lesson.cx[Math.min(st.variant, lesson.cx.length - 1)];\n")
    h = sub(h, "const allMissions = MISSIONS.concat(st.customMissions);", "const allMissions = this.effMissions();")
    h = sub(h, "    const todayIdx = lessons.findIndex((l,idx)=> !st.doneLessons[band+'-'+idx] && (st.owned[l.sk] || l.mine));\n    const doneCount = lessons.filter((_,idx)=> st.doneLessons[band+'-'+idx]).length;\n",
        "    const todayIdx = (() => { const x = weekIdx(curWk).find(x => !isDone(lessons[x]) && !isLocked(lessons[x])); return x == null ? -1 : x; })();\n"
        "    const doneCount = lessons.filter(isDone).length;\n")
    h = sub(h, """      todayTitle: todayIdx>=0 ? lessons[todayIdx].t[i] : (i?'All open lessons done':'Con đã học hết bài đang mở'),
      todayMeta: todayIdx>=0 ? SKILLS[lessons[todayIdx].sk][i] + ' · ' + lessons[todayIdx].m[i] : (i?'Unlock more skills to keep going':'Mở thêm kỹ năng để học tiếp'),
      todayBtn: todayIdx>=0 ? (i?'Start':'Bắt đầu học') : (i?'See plans':'Xem gói'),
      openToday: ()=>{ this.stopSpeak(); return todayIdx>=0 ? this.set({screen:'lesson', lesson:todayIdx, step:'story', choice:null, quiz:null, variant:0, reading:false}) : this.set({screen:'premium'}); },""",
"""      todayTitle: todayIdx>=0 ? lessons[todayIdx].t[i] : weekDone && hasNext ? (i?'This week’s lessons are done!':'Con đã xong bài tuần này!') : weekDone ? (i?'Every week is done!':'Con đã học hết các tuần!') : (i?'All open lessons done':'Con đã học hết bài đang mở'),
      todayMeta: todayIdx>=0 ? (i?'Week ':'Tuần ') + (curWk+1) + ' · ' + SKILLS[lessons[todayIdx].sk][i] + ' · ' + lessons[todayIdx].m[i] : weekDone && hasNext ? (i?'Ready for a new week':'Sẵn sàng sang tuần mới') : weekDone ? (i?'Open any week to review':'Mở lại tuần bất kỳ để ôn bài') : (i?'Unlock more skills to keep going':'Mở thêm kỹ năng để học tiếp'),
      todayBtn: todayIdx>=0 ? (i?'Start':'Bắt đầu học') : weekDone && hasNext ? (i?'Next week →':'Học tuần tiếp theo →') : weekDone ? (i?'Review':'Ôn bài') : (i?'See plans':'Xem gói'),
      openToday: ()=>{ this.stopSpeak(); if (todayIdx>=0) return this.set({screen:'lesson', lesson:todayIdx, step:'story', choice:null, quiz:null, variant:0, reading:false});
        if (weekDone && hasNext) return nextWeek(); if (weekDone) return this.set({viewWeek:0}); return this.set({screen:'premium'}); },
      wkLabel: (i?'Week ':'Tuần ') + (viewWk+1) + '/' + nWeeks,
      wkMeta: (() => { const ids = weekIdx(viewWk), dn = ids.filter(x => isDone(lessons[x])).length; return viewWk < curWk ? (i?`Finished · ${dn}/${ids.length} · review freely`:`Đã xong · ${dn}/${ids.length} bài · ôn lại thoải mái`) : (i?`${dn}/${ids.length} lessons done this week`:`Đã xong ${dn}/${ids.length} bài tuần này`); })(),
      wkFill: (() => { const ids = weekIdx(viewWk), dn = ids.filter(x => isDone(lessons[x])).length; return `height:100%;width:${ids.length ? Math.round(dn*100/ids.length) : 0}%;background:${JADE};border-radius:99px;transition:width .3s`; })(),
      wkPrev: () => this.set({viewWeek: Math.max(0, viewWk - 1)}), wkFwd: () => this.set({viewWeek: Math.min(curWk, viewWk + 1)}),
      wkPrevStyle: `width:34px;height:34px;border-radius:12px;background:#F3E6D3;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:800;color:#5C4B3C;cursor:pointer;flex:none;opacity:${viewWk>0?1:.3};pointer-events:${viewWk>0?'auto':'none'}`,
      wkFwdStyle: `width:34px;height:34px;border-radius:12px;background:#F3E6D3;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:800;color:#5C4B3C;cursor:pointer;flex:none;opacity:${viewWk<curWk?1:.3};pointer-events:${viewWk<curWk?'auto':'none'}`,
      wkCanNext: viewWk === curWk && weekDone && hasNext, nextWeek,
      wkDoneTitle: i ? `🎉 Week ${curWk+1} complete!` : `🎉 Con đã xong tuần ${curWk+1}!`,
      wkDoneText: i ? 'All lessons this week are done. Ready for new stories?' : 'Con đã hoàn thành các bài của tuần này. Sẵn sàng học câu chuyện mới chưa?',
      wkNextLabel: i ? `Start week ${curWk+2} →` : `Học tuần ${curWk+2} →`,
      wkFinished: viewWk === curWk && weekDone && !hasNext,
      wkFinTitle: i ? `🏆 All ${nWeeks} weeks done!` : `🏆 Con đã học hết ${nWeeks} tuần!`,
      wkFinText: i ? 'Use ‹ to go back and review any week you like.' : 'Bấm ‹ để mở lại và ôn bất kỳ tuần nào con thích.',
      wkBack: viewWk < curWk, wkToCur: () => this.set({viewWeek: null}), wkBackLabel: i ? `Back to week ${curWk+1} →` : `Về tuần đang học (tuần ${curWk+1}) →`,""")
    h = sub(h, """      lessons: lessons.map((l, idx)=>{
        const locked = !st.owned[l.sk] && !l.mine;
        const done = !!st.doneLessons[band+'-'+idx];
        const cur = !done && !locked && idx===0;
        return {
          n:String(idx+1),""",
"""      lessons: weekIdx(viewWk).map(idx=>{ const l = lessons[idx];
        const locked = isLocked(l);
        const done = isDone(l);
        const cur = idx===todayIdx;
        return {
          n:String(idx - viewWk*WK + 1),""")
    h = sub(h, """      toReward:()=>this.setState(p=>{ const key = band+'-'+p.lesson, again = !!p.doneLessons[key];
        const r = again ? {got:0, patch:{}} : this.grant(p, p.active, LESSON_STARS);
        return {step:'reward', lastLessonDay: new Date().toDateString(), doneLessons:{...p.doneLessons,[key]:true},""",
"""      toReward:()=>this.setState(p=>{ const key = band+'-'+p.lesson, lid = lesson.id, pp = this.progOf(p, active.name, band), again = !!pp.done[lid];
        const r = again ? {got:0, patch:{}} : this.grant(p, p.active, LESSON_STARS);
        return {step:'reward', lastLessonDay: new Date().toDateString(), doneLessons:{...p.doneLessons,[key]:true}, ...this.progPatch(p, active.name, band, {...pp, done:{...pp.done, [lid]:1}}),""")
    h = sub(h, """      variantTabs: !vset ? [] : [[i?'A · At home':'A · Ở nhà'],
                    [i?'B · At school':'B · Trên lớp'],
                    [i?'C · Out there':'C · Ngoài đời']]
""", """      variantTabs: !vset ? [] : vset.map(c => [[i?'A · At home':'A · Ở nhà'], [i?'B · At school':'B · Trên lớp'], [i?'C · Out there':'C · Ngoài đời']][c.k])
""")
    h = sub(h, "        : st.variant===0 ? (", "        : vv.k===0 ? (")
    h = sub(h, "        : st.variant===1 ? (", "        : vv.k===1 ? (")
    h = sub(h, "Object.keys(st.doneLessons).length + (i?' lessons done':' bài đã xong')", "doneCount + (i?' lessons done':' bài đã xong')")
    h = sub(h, "      missions: allMissions.map((m,k)=>{", "      missions: this.mOrderOf(allMissions.length).map(k=>{ const m = allMissions[k];")
    h = sub(h, "        const lvSet = MISSION_LEVELS[k] || [", "        const lvSet = m.lv || [")
    h = sub(h, "const on = st.screen===scr || (scr==='home' && st.screen==='lesson');", "const on = st.screen===scr || (scr==='home' && st.screen==='lesson') || (scr==='parent' && st.screen==='custom');")
    h = sub(h, "isParent:st.screen==='parent',", "isParent:st.screen==='parent', isCustom:st.screen==='custom',")
    h = sub(h, "\n      isManage: st.gate==='manage',", "\n      ...this.custVals(i),\n      isManage: st.gate==='manage',")
    # 5) giao dien
    path_row = """              <div style="font-size:12px;color:#8B7867">{{ pathMeta }}</div>
            </div>
"""
    h = sub(h, path_row, path_row.rstrip('\n') + HOME_WEEK + '\n')
    h = sub(h, """                <div style="{{ l.badge }}">{{ l.state }}</div>
              </div>
            </sc-for>
""", """                <div style="{{ l.badge }}">{{ l.state }}</div>
              </div>
            </sc-for>
""" + HOME_NEXT)
    rem = '            <div style="border-radius:22px;background:#FFF8E6;border:1.5px solid #F2D9A6;padding:14px;display:flex;flex-direction:column;gap:12px">\n              <div style="display:flex;align-items:center;gap:10px">\n                <div style="width:42px;height:42px;border-radius:14px;background:#F2A93B;display:flex;align-items:center;justify-content:center;font-size:21px;flex:none">⏰</div>'
    h = sub(h, rem, PARENT_CARD + rem)
    h = sub(h, "\n        <!-- LESSON -->", CUSTOM + "\n        <!-- LESSON -->")
    # o anh bai hoc: bo chu "Keo anh minh hoa vao day" (chu thiet ke), thay bang Sen
    h = sub(h, '<div style="text-align:center;color:#9C8874;font-size:12px;padding:0 30px;line-height:1.5">{{ t.imgSlot }}</div>',
               '<img src="f37ca7cb-1419-41a5-be40-151490144349" alt="Sen" style="height:150px;width:150px;object-fit:contain;animation:senBob 3.2s ease-in-out infinite">')
    return h

def blank_variants(s):
    # file boi canh cu khong con dung (boi canh nam trong tung bai) -> thay bang noi dung rong
    m = re.search(r'(<script type="__bundler/manifest">)(.*?)(</script>)', s, re.S)
    mf = json.loads(m.group(2)); hit = 0
    for u, v in mf.items():
        d = base64.b64decode(v['data']); d = gzip.decompress(d) if v.get('compressed') else d
        if b'window.SEN_VARIANTS' in d:
            nd = b'window.SEN_VARIANTS = {};\n'
            v['data'] = base64.b64encode(gzip.compress(nd) if v.get('compressed') else nd).decode(); hit += 1
    assert hit == 1, hit
    return s[:m.start(2)] + json.dumps(mf).replace('</', '<\\/') + s[m.end(2):]

if __name__ == '__main__':
    path, d = sys.argv[1:3]
    s = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', s, re.S)
    t = json.loads(m.group(2))
    if 'effLessons' in t: print('da patch', path); sys.exit()
    t = app(t, d)
    s = s[:m.start(2)] + json.dumps(t, ensure_ascii=False).replace('</', '<\\/') + s[m.end(2):]
    s = blank_variants(s)
    open(path, 'w', encoding='utf-8').write(s); print('ok', path)
