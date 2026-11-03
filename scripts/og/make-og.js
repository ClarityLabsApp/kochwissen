const { chromium } = require('playwright');
const path = require("path"); const R = path.resolve(__dirname, "../.."), D = path.join(R, "public");
const T = {
  de: { h: 'Verstehen, warum es <em>funktioniert</em>', s: 'Kochen und Backen einfach erklärt und sichtbar gemacht', tag: 'KEIN REZEPTBUCH · DIE VORGÄNGE DAHINTER' },
  en: { h: 'Understand why it <em>works</em>', s: 'Cooking and baking simply explained and made visible', tag: 'NOT A RECIPE BOOK · THE PROCESSES BEHIND IT' },
};
const pics = ['g-carbonara','garum','g-zopf','w-eier'];
const html = (t) => `<html><head><style>
@font-face{font-family:F;src:url(file://${R}/node_modules/@fontsource-variable/fraunces/files/fraunces-latin-opsz-normal.woff2)}
@font-face{font-family:F;font-style:italic;src:url(file://${R}/node_modules/@fontsource-variable/fraunces/files/fraunces-latin-opsz-italic.woff2)}
@font-face{font-family:N;src:url(file://${R}/node_modules/@fontsource-variable/newsreader/files/newsreader-latin-opsz-normal.woff2)}
@font-face{font-family:M;src:url(file://${R}/node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2)}
body{margin:0;width:1200px;height:630px;background:#efe4cf;background-image:radial-gradient(#d9c9a8 1px,transparent 1px);background-size:14px 14px;font-family:N;color:#2b2118;overflow:hidden;position:relative}
.l{position:absolute;left:72px;top:64px;width:600px}
.brand{display:flex;align-items:center;gap:14px;font-family:F;font-size:40px;font-weight:600}
.brand img{width:56px;height:56px}.brand i{color:#b4542a;font-weight:500}
h1{font-family:F;font-weight:600;font-size:74px;line-height:1.02;margin:60px 0 22px;letter-spacing:-1px}
h1 em{color:#b4542a;font-weight:500}
p{font-size:29px;margin:0;line-height:1.3;max-width:540px}
.tag{position:absolute;left:72px;bottom:54px;font-family:M;font-size:16px;letter-spacing:2px;color:#7a5a3a}
.url{position:absolute;right:72px;bottom:54px;font-family:M;font-size:18px;letter-spacing:1px;color:#7a5a3a}
.g{position:absolute;right:50px;top:40px;width:470px;height:500px;display:grid;grid-template-columns:1fr 1fr;gap:6px}
.g img{width:100%;height:240px;object-fit:contain}
</style></head><body>
<div class="l"><div class="brand"><img src="file://${R}/public/logo.svg"><span>Gar<i>um</i></span></div><h1>${t.h}</h1><p>${t.s}</p></div>
<div class="g">${pics.map(p=>`<img src="file://${R}/public/illustrationen/${p}.webp">`).join('')}</div>
<div class="tag">${t.tag}</div><div class="url">garum.guide</div></body></html>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});
for(const l of ['de','en']){const tmp=require("os").tmpdir()+`/og-${l}.html`;require("fs").writeFileSync(tmp,html(T[l]));await p.goto(`file://${tmp}`,{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:`${D}/og-${l}.png`});}
await b.close();})();
