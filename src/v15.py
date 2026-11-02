"""Senapp v15 (ap dung tren v13, truoc buoc v14): tap trung ba me co con tieu hoc (6-11 tuoi),
nhom 12-15 thanh "ban thu"; bo PDF (so + to huy hieu), chi ban Webapp.
Dung: python3 v15.py <thu muc ban build>"""
import json, re, sys, os, glob

def sub(h, a, b, n=1):
    c = h.count(a); assert c == n, (a[:120], c); return h.replace(a, b)

def landing(t):
    t = sub(t, '>Kỹ năng mềm cho trẻ 6–15 tuổi</span>', '>Kỹ năng sống cho con tiểu học · 6–11 tuổi</span>')
    t = sub(t, 'Mỗi 50 sao là một huy hiệu có Sen để in ra, dán vào sổ “Cùng Sen khôn lớn”.', 'Mỗi 50 sao là một huy hiệu có Sen, cất trong bộ sưu tập để con khoe với cả nhà.')
    t = sub(t, '<li>Cả 9 kỹ năng, 135 bài, 2 bài theo dịp mỗi tháng</li>', '<li>Cả 9 kỹ năng, 45 bài đúng tuổi của con, 2 bài theo dịp mỗi tháng</li>')
    t = sub(t, "'Mỗi bài học đều có nút “Nghe Sen đọc” bằng tiếng Việt hoặc tiếng Anh. Lộ trình 6–8 tuổi câu ngắn, chữ to, mỗi bài 5–6 phút, và nhiệm vụ mức 1 luôn là làm cùng ba mẹ.'",
               "'Lộ trình 6–8 tuổi được viết để ba mẹ đọc cùng con: câu ngắn, mỗi bài 5–7 phút, có nút “Nghe Sen đọc”, và nhiệm vụ mức 1 luôn là làm cùng ba mẹ. Khi con đọc tốt hơn, con tự đọc dần.'")
    return t

def app(t):
    t = sub(t, '>Sen · Kỹ năng mềm cho trẻ 6–15</div>', '>Sen · Kỹ năng sống cho con tiểu học</div>')
    t = sub(t, 'Kỹ năng sống cho trẻ 6–15,', 'Kỹ năng sống cho con tiểu học (6–11 tuổi),')
    t = sub(t, "'Life skills for ages 6–15,", "'Life skills for primary-school children (6–11),")
    t = sub(t, "obBands:[['Bé 6–8 tuổi','Nghe & xem, ít chữ'],['Bạn 9–11 tuổi','Tình huống & câu đố'],['Bạn 12–15 tuổi','Phản biện & tài chính'],",
               "obBands:[['Bé 6–8 tuổi','Ba mẹ đọc cùng con'],['Bạn 9–11 tuổi','Tình huống & câu đố'],['Bạn 12–15 tuổi','Bản thử · phản biện & tài chính'],")
    t = sub(t, "obBands:[['Ages 6–8','Listen & watch, few words'],['Ages 9–11','Scenarios & quizzes'],['Ages 12–15','Critical thinking & money'],",
               "obBands:[['Ages 6–8','Read together with a parent'],['Ages 9–11','Scenarios & quizzes'],['Ages 12–15','Beta · critical thinking & money'],")
    t = sub(t, "rgKicker: i?'For kids 6–15 · 7 minutes a day':'Cho trẻ 6–15 tuổi · 7 phút mỗi ngày'",
               "rgKicker: i?'For primary-school kids 6–11 · 7 minutes a day':'Cho con tiểu học 6–11 tuổi · 7 phút mỗi ngày'")
    t = sub(t, "bandChips: ['6–8','9–11','12–15'].map(", "bandChips: ['6–8','9–11','12–15 · thử'].map(")
    t = sub(t, "const bandTxt = (b) => (b==='5-8'?'6–8':b==='9-12'?'9–11':'12–15') + (i?' yrs':' tuổi');",
               "const bandTxt = (b) => (b==='5-8'?'6–8':b==='9-12'?'9–11':'12–15') + (i?' yrs':' tuổi') + (b==='13-16' ? (i?' · beta':' · bản thử') : '');")
    # 6-8 tuoi: nhac ba me doc cung con o buoc doc chuyen
    t = sub(t, "      variantHint: !vset ?", "      variantHint: (band==='5-8' ? (i?'👨‍👩‍👧 Read this one together with a parent. ':'👨‍👩‍👧 Ba mẹ đọc cùng con nhé. ') : '') + (!vset ?")
    t = sub(t, "        : (i?'Out in the world: shops, the street, the neighbourhood.':'Ra ngoài đời: cửa hàng, đường phố, khu mình sống.')),",
               "        : (i?'Out in the world: shops, the street, the neighbourhood.':'Ra ngoài đời: cửa hàng, đường phố, khu mình sống.'))),")
    # bo PDF: the "So Cung Sen khon lon" -> bo suu tap huy hieu cua cac con
    a = t.index('<a href="so-sen/so-cung-sen-khon-lon.pdf"'); a = t.rindex('<div style="display:flex;gap:8px;flex-wrap:wrap">', 0, a)
    b = t.index('</div>', t.index('to-huy-hieu-60-tuan.pdf', a)) + len('</div>')
    t = t[:a] + t[b:].lstrip(' \n')
    t = sub(t, 'font-size:21px;flex:none">📘</div>', 'font-size:21px;flex:none">🏅</div>')
    t = sub(t, "bookTitle: i?'“Growing up with Sen” sticker book':'Sổ “Cùng Sen khôn lớn”',", "bookTitle: i?'Your children’s badges':'Huy hiệu của các con',")
    t = re.sub(r"bookSub: i\?`[^`]*`:`[^`]*`,", "bookSub: i?`Every ${per} stars = one Sen badge, kept in your child’s collection.`:`Mỗi ${per} sao = 1 huy hiệu có Sen, cất trong bộ sưu tập của con.`,", t, count=1)
    a = t.index('bookNote: i?'); b = t.index('\n', t.index("'In trên giấy decal", a)) + 1
    t = t[:a] + "bookNote: i?'Tap a badge to see it full size.':'Bấm vào huy hiệu để xem cỡ lớn.',\n" + t[b:]
    t = re.sub(r"nbHint: i\?'[^']*':'Nhờ ba mẹ in huy hiệu để con dán vào sổ “Cùng Sen khôn lớn” nhé!',",
               "nbHint: i?'It’s in your collection now. Go and show your parents!':'Huy hiệu đã vào bộ sưu tập của con. Khoe với ba mẹ ngay nhé!',", t, count=1)
    t = t.replace(' download="{{ x.file }}"', '')
    assert '.pdf' not in t and 'decal' not in t and 'Nhờ ba mẹ in' not in t
    return t

def patch(path, fn):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', s, re.S)
    t = fn(json.loads(m.group(2)))
    s = s[:m.start(2)] + json.dumps(t, ensure_ascii=False).replace('</', '<\\/') + s[m.end(2):]
    open(path, 'w', encoding='utf-8').write(s); print('ok', path)

if __name__ == '__main__':
    d = sys.argv[1]
    patch(os.path.join(d, 'trang-chu', 'index.html'), landing)
    patch(os.path.join(d, 'index.html'), app)
    for f in glob.glob(os.path.join(d, 'so-sen', '*.pdf')): os.remove(f); print('xoa', f)
