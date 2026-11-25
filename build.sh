#!/usr/bin/env bash
# Build lai ban phat hanh vao public/ tu ma nguon trong src/.
# Can: python3, node >= 18. Lan dau: (cd src/tools && npm ci)
# Bien moi truong: SEN_NOMIN=1 -> khong thu gon/lam roi ma (de go loi / ban chay mau)
set -euo pipefail
cd "$(dirname "$0")"
OUT="${1:-public}"
[ -x src/tools/node_modules/.bin/terser ] || (cd src/tools && npm ci)
rm -rf "$OUT"; cp -r src/base-v13 "$OUT"
python3 src/v15.py "$OUT"     # tap trung tieu hoc, bo PDF
python3 src/v16.py "$OUT"     # 12 thang noi dung, danh muc cho ba me
python3 src/v17.py "$OUT"     # mien phi 100%, moi Sen ly Coffee, dong bo Bamedonghanh
python3 src/v14.py "$OUT"     # (c), Dieu khoan, thu gon & lam roi ma
python3 src/fonts.py "$OUT"   # nhung san font cho trang Dieu khoan (App & trang chu da co font trong tep)
cp src/legal/OFL-fonts.txt "$OUT/OFL-fonts.txt"
# tang so phien ban bo nho dem khi phat hanh ban moi, de may cac con tai lai App
sed -i -E "s/const CACHE = 'sen-v[0-9]+';/const CACHE = 'sen-v${SEN_VERSION:-17}';/" "$OUT/sw.js"
echo "Xong: $OUT"
