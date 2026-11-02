import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const H='/tmp/claude-0/-home-user-notebooklm-py/2645776a-48d7-5467-8bed-0fcf75c00226/scratchpad/ebook/';
const names = ['cung-sen-khon-lon-tap-1-6-8-tuoi','cung-sen-khon-lon-tap-2-9-11-tuoi','cung-sen-khon-lon-tap-3-12-15-tuoi'];
const b = await chromium.launch();
for (let v=1; v<=3; v++) {
  const pg = await b.newPage(); await pg.goto('file://'+H+`print-${v}.html`); await pg.waitForTimeout(800);
  await pg.pdf({ path: H+names[v-1]+'.pdf', format:'A5', printBackground:true, displayHeaderFooter:true,
    headerTemplate:'<div></div>',
    footerTemplate:`<div style="width:100%;font-size:7px;color:#8A7462;font-family:sans-serif;display:flex;justify-content:space-between;padding:0 13mm"><span>Cùng Sen khôn lớn · Tập ${v} · © 2026 Senapp</span><span class="pageNumber"></span></div>`,
    margin:{top:'14mm',bottom:'16mm',left:'13mm',right:'13mm'} });
  if (v===2) { await pg.setViewportSize({width:560,height:794}); }
  await pg.close();
}
await b.close();
