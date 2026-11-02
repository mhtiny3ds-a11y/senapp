"""Tao ban in A5 cua sach "Cung Sen khon lon" (3 tap) -> print-<band>.html, sau do pdf.mjs xuat PDF."""
import json, base64, html, os
H = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(H, 'book.json'), encoding='utf-8'))
FONTS = open(os.path.join(H, '..', 'sticker', 'fonts.css'), encoding='utf-8').read()
MASCOT = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(H, '..', 'sticker', 'mascot.png'), 'rb').read()).decode()
COLORS = ['#C8102E', '#2E8F72', '#7C6BD6', '#E08A2B', '#3B82C4', '#B5487D', '#4C8C2B', '#D2691E', '#1F7A8C']
CTX = ['Ở nhà', 'Trên lớp', 'Ngoài đời']
e = lambda s: html.escape(str(s))

CSS = """
@page { size: A5; margin: 14mm 13mm 16mm; }
* { box-sizing: border-box; }
body { margin: 0; font: 10.2pt/1.6 'Be Vietnam Pro', sans-serif; color: #2A1F18; }
h1, h2, h3 { font-family: 'Baloo 2', sans-serif; line-height: 1.12; margin: 0; }
h2 { font-size: 21pt; font-weight: 800; }
h3 { font-size: 12.5pt; font-weight: 700; }
p { margin: 0; }
.pg { break-before: page; }
.run { font-size: 7.5pt; letter-spacing: .1em; text-transform: uppercase; color: #8A7462; font-weight: 600; margin-bottom: 4mm; }
.cover { height: 178mm; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 5mm;
  background: radial-gradient(circle at 50% 38%, #FFE3EA 0 30%, #FFF6EA 31%); border-radius: 6mm; padding: 8mm; }
.cover img { width: 70mm; }
.cover h1 { font-size: 34pt; color: #C8102E; font-weight: 800; }
.tag { background: #C8102E; color: #FFF; border-radius: 99px; padding: 1mm 4mm; font-weight: 700; font-size: 10pt; }
.verse { font-family: 'Baloo 2'; font-weight: 700; color: #C8102E; font-size: 12.5pt; line-height: 1.5; margin: 3mm 0; }
.stack > * + * { margin-top: 3mm; }
ol.steps { padding-left: 5mm; margin: 0; } ol.steps li + li { margin-top: 1.5mm; }
.skills { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm; }
.skill { border: 0.3mm solid #EBDCC8; border-radius: 3mm; padding: 2.5mm 3mm; display: flex; gap: 2.5mm; align-items: center; }
.dot { width: 6.5mm; height: 6.5mm; border-radius: 2mm; color: #FFF; display: inline-flex; align-items: center; justify-content: center; font: 800 9pt 'Baloo 2'; flex: none; }
.toc-w { margin-top: 3mm; break-inside: avoid; }
.toc-w h3 { color: #C8102E; font-size: 11pt; }
.toc-r { display: flex; gap: 2mm; font-size: 9.3pt; padding: .6mm 0; border-bottom: 0.2mm dotted #D9C7AF; }
.toc-r .t { flex: 1; } .toc-r .s { color: #8A7462; font-size: 8pt; }
.wk { text-align: center; display: flex; flex-direction: column; align-items: center; gap: 4mm; padding-top: 10mm; }
.wk .n { font: 800 64pt/1 'Baloo 2'; color: #E8A33A; }
.wk ul { list-style: none; padding: 0; margin: 0; text-align: left; width: 100%; }
.wk li { padding: 1.2mm 0; display: flex; gap: 2.5mm; align-items: center; }
.slot { width: 56mm; height: 56mm; border-radius: 50%; border: 0.8mm dashed #E8A33A; display: flex; align-items: center; justify-content: center; text-align: center; color: #8A7462; font-size: 8.5pt; padding: 8mm; margin-top: 4mm; }
.lh { display: flex; gap: 2mm; margin-bottom: 2mm; }
.chip { font-size: 7.8pt; font-weight: 700; padding: .6mm 2.5mm; border-radius: 99px; background: #FBE3E7; color: #C8102E; }
.chip.g { background: #FFF1D6; color: #2A1F18; }
.scene { margin-top: 4mm; padding-top: 3mm; border-top: 0.3mm dashed #E3D2BC; break-inside: avoid; }
.st { font: 700 8.5pt 'Baloo 2'; letter-spacing: .05em; text-transform: uppercase; color: #2E8F72; margin-bottom: 1.5mm; }
.st b { display: inline-flex; width: 5mm; height: 5mm; background: #2E8F72; color: #FFF; border-radius: 1.5mm; align-items: center; justify-content: center; margin-right: 1.5mm; }
.story { font-size: 10.6pt; }
.q { font-weight: 700; margin-top: 1.5mm; }
.opt { display: flex; gap: 2mm; margin-top: 1.2mm; }
.box { width: 4mm; height: 4mm; border: 0.35mm solid #8A7462; border-radius: 1mm; flex: none; margin-top: .9mm; }
.tips { margin-top: 2mm; background: #F8F1E4; border-radius: 2.5mm; padding: 2mm 3mm; font-size: 8.6pt; color: #5C4B3C; }
.tips b { color: #2A1F18; }
.quiz { margin-top: 4mm; background: #FFF1D6; border-radius: 3mm; padding: 3mm; break-inside: avoid; }
.mis { margin-top: 4mm; border: 0.5mm solid #C8102E; border-radius: 3.5mm; padding: 3.5mm; break-inside: avoid; }
.mis .eb { font: 800 8.5pt 'Baloo 2'; letter-spacing: .08em; text-transform: uppercase; color: #C8102E; }
.lv { display: flex; gap: 2mm; margin-top: 1.5mm; font-size: 9.4pt; }
.lv .n { font-weight: 700; color: #C8102E; }
.rw { margin-top: 2.5mm; border: 0.35mm dashed #E8A33A; background: #FFF6E4; border-radius: 2.5mm; padding: 1.8mm 3mm; font-size: 9.4pt; }
.sign { display: flex; gap: 5mm; margin-top: 3mm; font-size: 8.2pt; color: #8A7462; }
.sign span { flex: 1; border-bottom: 0.3mm dotted #8A7462; padding-bottom: 5mm; }
.keys { columns: 2; column-gap: 6mm; font-size: 8.6pt; }
.keys div { break-inside: avoid; padding: .5mm 0; }
.cert { border: 1.2mm double #E8A33A; border-radius: 5mm; padding: 10mm 8mm; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 4mm; margin-top: 6mm; }
.cert .nm { width: 80%; border-bottom: 0.4mm dotted #8A7462; height: 10mm; }
.legal { font-size: 7.6pt; color: #8A7462; }
"""

def band_html(vi, B):
    L = B['lessons']; out = []
    out.append(f'''<section class="cover"><span class="tag">Tập {vi + 1} · {e(B["label"])}</span><img src="{MASCOT}" alt=""><h1>Cùng Sen khôn lớn</h1>
      <p>45 bài kỹ năng sống · 9 tuần<br>Mỗi bài 3 tình huống và một nhiệm vụ đời thực</p><p>Bạn đồng hành: <b>{e(B["hero"])}</b></p>
      <p class="legal">Sách phát triển từ Senapp · senapp.com · © 2026 Senapp</p></section>''')
    out.append(f'''<section class="pg stack"><div class="run">Lời ngỏ gửi ba mẹ</div><h2>Vì sao là Sen?</h2>
      <div class="verse">Trong đầm gì đẹp bằng sen,<br>Lá xanh bông trắng lại chen nhị vàng.<br>Nhị vàng bông trắng lá xanh,<br>Gần bùn mà chẳng hôi tanh mùi bùn.</div>
      <p>Hạt sen nằm dưới lớp bùn, kiên nhẫn qua nhiều ngày, rồi vươn lên khỏi mặt nước và nở thật thanh khiết. Mỗi đứa trẻ cũng lớn lên như thế: từng chút một, mỗi ngày một chút.</p>
      <p>Cuốn sách gom toàn bộ lộ trình học của Senapp cho lứa tuổi {e(B["label"])}. Ba mẹ đọc cùng con mỗi ngày một bài, rồi cùng con làm một việc thật ngoài đời.</p>
      <p>Senapp tin rằng không có đứa trẻ nào sinh ra để bị gọi là hư hay khó bảo. Các con chỉ cần có người đi cùng đủ lâu.</p>
      <h3 style="margin-top:6mm">Dùng sách thế nào?</h3>
      <ol class="steps"><li><b>Mỗi ngày một bài</b>, mỗi tuần 5 bài thuộc 5 kỹ năng khác nhau.</li>
        <li><b>Đi qua cả 3 tình huống</b> ở nhà, trên lớp, ngoài đời. Để con tự chọn rồi mới đọc mẹo của Sen.</li>
        <li><b>Làm câu đố cuối bài.</b> Đáp án ở cuối sách.</li>
        <li><b>Nhận nhiệm vụ đời thực</b>, chọn mức khó: làm cùng ba mẹ, làm có nhắc hoặc tự làm.</li>
        <li><b>Ba mẹ xác nhận</b> khi con làm thật, ký vào ô cuối bài và trao phần thưởng nhỏ đã hẹn.</li>
        <li><b>Cuối tuần</b>, dán huy hiệu tuần vào ô tròn ở trang mở đầu mỗi tuần.</li></ol></section>''')
    out.append('<section class="pg stack"><div class="run">Lộ trình</div><h2>9 kỹ năng con mang theo cả đời</h2><div class="skills">' +
               ''.join(f'<div class="skill"><span class="dot" style="background:{COLORS[k]}">{k + 1}</span><span><b>{e(s)}</b><br><span class="legal">{sum(1 for l in L if l["sk"] == k)} bài</span></span></div>' for k, s in enumerate(D['skills'])) +
               '</div><h2 style="margin-top:7mm">Mục lục</h2>' +
               ''.join(f'<div class="toc-w"><h3>Tuần {w + 1}</h3>' + ''.join(f'<div class="toc-r"><span class="t">{j + 1}. {e(l["t"])}</span><span class="s">{e(D["skills"][l["sk"]])}</span></div>' for j, l in enumerate(L[w * 5:w * 5 + 5])) + '</div>' for w in range(9)) +
               '</section>')
    for w in range(9):
        ls = L[w * 5:w * 5 + 5]
        out.append(f'<section class="pg wk"><div class="run">Tuần</div><div class="n">{w + 1}</div><ul>' +
                   ''.join(f'<li><span class="dot" style="background:{COLORS[l["sk"]]}">{j + 1}</span><span>{e(l["t"])} <span class="legal">· {e(D["skills"][l["sk"]])}</span></span></li>' for j, l in enumerate(ls)) +
                   f'</ul><div class="slot">Dán huy hiệu tuần {w + 1} vào đây khi con xong 5 bài</div></section>')
        for j, l in enumerate(ls):
            sc = ''.join(f'''<div class="scene"><div class="st"><b>{n + 1}</b>Tình huống {n + 1} · {CTX[c["k"]]}</div><p class="story">{e(c["s"])}</p><p class="q">{e(c["q"])}</p>
              {''.join(f'<div class="opt"><span class="box"></span><span><b>{"ABC"[m]}.</b> {e(o[0])}</span></div>' for m, o in enumerate(c["o"]))}
              <div class="tips"><b>Mẹo của Sen</b> (đọc sau khi con chọn): {' '.join(f'<b>{"ABC"[m]}</b>{" ✓" if o[1] else ""} {e(o[2])}' for m, o in enumerate(c["o"]))}</div></div>''' for n, c in enumerate(l['cx']))
            mi = l['mi']
            out.append(f'''<section class="pg"><div class="run">Tuần {w + 1} · Bài {j + 1}/5</div><div class="lh"><span class="chip">{e(D["skills"][l["sk"]])}</span><span class="chip g">{e(l["m"])}</span></div>
              <h2>{e(l["t"])}</h2>{sc}
              <div class="quiz"><div class="st" style="color:#2A1F18"><b style="background:#E8A33A">?</b>Câu đố cuối bài</div><p class="q">{e(l["qq"])}</p>
                {''.join(f'<div class="opt"><span class="box"></span><span><b>{"ABC"[m]}.</b> {e(o)}</span></div>' for m, o in enumerate(l["qo"]))}</div>
              <div class="mis"><div class="eb">Nhiệm vụ đời thực</div><h3>{e(mi["t"])}</h3><p>{e(mi["s"])}</p>
                {''.join(f'<div class="lv"><span class="box"></span><span><span class="n">Mức {n + 1} · {["Làm cùng ba mẹ", "Làm có nhắc", "Tự làm"][n]}.</span> {e(x)}</span></div>' for n, x in enumerate(mi["lv"]))}
                <div class="rw">🎁 <b>Phần thưởng:</b> {e(mi["rw"])}</div><div class="sign"><span>Ngày con làm:</span><span>Ba mẹ xác nhận:</span></div></div></section>''')
    out.append('<section class="pg"><div class="run">Phụ lục</div><h2>Đáp án câu đố</h2><p class="legal" style="margin:2mm 0 3mm">Dành cho ba mẹ.</p><div class="keys">' +
               ''.join(f'<div><b>T{i // 5 + 1}.{i % 5 + 1} · {"ABC"[l["qa"]]}</b> {e(l["t"])}</div>' for i, l in enumerate(L)) + '</div></section>')
    out.append(f'''<section class="pg"><div class="cert"><img src="{MASCOT}" alt="" style="width:34mm"><div class="run" style="margin:0">Giấy khen</div><h2 style="color:#C8102E">Cùng Sen khôn lớn</h2>
      <p>Chứng nhận bạn nhỏ</p><div class="nm"></div><p>đã hoàn thành 45 bài và các nhiệm vụ đời thực của Tập {vi + 1} ({e(B["label"])}).</p>
      <div class="sign" style="width:100%"><span>Ngày:</span><span>Ba mẹ ký tên:</span></div></div>
      <div class="stack" style="margin-top:8mm"><h3>Về Senapp</h3><p>Sách được phát triển từ Senapp, chương trình học kỹ năng mềm cho trẻ 6–15 tuổi. Trong App Sen, con còn được nhận sao, huy hiệu tuần, nhắc giờ học; ba mẹ có thể tự sửa bài học, nhiệm vụ, phần thưởng cho riêng gia đình.</p>
      <p>senapp.com · admin.senapp@gmail.com · Zalo/Viber hỗ trợ 0975 860 488</p>
      <p class="legal">© 2026 Senapp. Bảo lưu mọi quyền. Nội dung, bài học, nhiệm vụ, hình ảnh và linh vật Sen được bảo hộ quyền tác giả. Nghiêm cấm sao chép, in lại để bán, đăng tải lại hoặc dùng để huấn luyện trí tuệ nhân tạo khi chưa có văn bản đồng ý của Senapp. Gia đình được in để dùng riêng trong nhà.</p></div></section>''')
    return f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Cùng Sen khôn lớn · Tập {vi + 1}</title><style>{FONTS}{CSS}</style></head><body>' + ''.join(out) + '</body></html>'

for vi, B in enumerate(D['bands']):
    open(os.path.join(H, f'print-{vi + 1}.html'), 'w', encoding='utf-8').write(band_html(vi, B))
print('ok')
