// Teste de navegador do site. Precisa do site servido em http://localhost:8765 e do Playwright.
// Uso: PW=<caminho do playwright> node tools/teste.js <pasta de saída>
const { chromium } = require(process.env.PW || 'playwright');
const OUT = process.argv[2] || '.';
const URL = process.env.URL || 'http://localhost:8765/';
const fs = require('fs');
const res = [];
function ok(name, pass, info){ res.push({name, pass, info}); console.log((pass ? 'PASSOU ' : 'FALHOU ') + name + (info ? '  ' + info : '')) }
async function page(b, o){
  const ctx = await b.newContext({viewport:{width:o.w,height:o.h}, deviceScaleFactor:1, reducedMotion:o.rm ? 'reduce' : 'no-preference', isMobile:o.w < 500, hasTouch:o.w < 500});
  const p = await ctx.newPage(); p.errs = [];
  p.on('console', m => { if (m.type() === 'error') p.errs.push(m.text()) });
  p.on('pageerror', e => p.errs.push(e.message));
  await p.goto(URL, {waitUntil:'networkidle'}); await p.waitForTimeout(1200);
  return p;
}
async function scrollTo(p, sel, frac){ await p.evaluate(([s,f]) => { const el = document.querySelector(s); const top = el.getBoundingClientRect().top + scrollY; window.scrollTo(0, top + Math.max(0, el.offsetHeight - innerHeight)*(f||0)) }, [sel, frac]); await p.waitForTimeout(900) }
// fração de pixels azuis (matiz de cianotipia, saturados) numa captura
async function blueShare(p){
  const buf = await p.screenshot();
  return await p.evaluate(async b64 => {
    const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
    const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const x = c.getContext('2d'); x.drawImage(img,0,0);
    const d = x.getImageData(0,0,c.width,c.height).data; let blue = 0, n = 0;
    for (let i=0;i<d.length;i+=16){ const r=d[i]/255,g=d[i+1]/255,bl=d[i+2]/255; const mx=Math.max(r,g,bl), mn=Math.min(r,g,bl), s = mx ? (mx-mn)/mx : 0; let h=0;
      if (mx !== mn){ if (mx===bl) h = 60*((r-g)/(mx-mn))+240; else if (mx===g) h = 60*((bl-r)/(mx-mn))+120; else h = (60*((g-bl)/(mx-mn))+360)%360 }
      n++; if (s > .55 && mx > .45 && h > 190 && h < 215) blue++ }
    return blue/n;
  }, buf.toString('base64'));
}
(async () => {
  const b = await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  // 1. calculadora, três casos feitos à mão
  const p = await page(b, {w:1440, h:900});
  async function price(){ await p.waitForTimeout(150); return p.$eval('#rPrice .sr', e => e.textContent) }
  async function set(id, v){ await p.fill(id, String(v)); await p.dispatchEvent(id, 'input') }
  ok('calc caso A: padrão Shopee 64 g, 200 min, R$ 120/kg, 50%', (await price()) === 'R$ 38,97', await price());
  await p.click('#chan button[data-v="direta"]'); await set('#c-g', 100); await set('#c-h', 300); await set('#c-kg', '15000'); await set('#c-luc', 30);
  ok('calc caso B: venda direta 100 g, 300 min, R$ 150/kg, 30%', (await price()) === 'R$ 37,99', await price());
  await p.click('#chan button[data-v="mlp"]'); await set('#c-g', 10); await set('#c-h', 30); await set('#c-kg', '10000'); await set('#c-luc', 100);
  ok('calc caso C: ML Premium 10 g, 30 min, R$ 100/kg, 100%', (await price()) === 'R$ 32,19', await price());
  await set('#c-g', 0); ok('calc: peso zero mostra erro com instrução', await p.$eval('[data-f="gramas"]', e => e.classList.contains('bad') && getComputedStyle(e.querySelector('.err')).display !== 'none'));
  // 2. número herói bate com a calculadora
  ok('número herói R$ 1,18 e 12%', (await p.$eval('#hnBig', e => e.textContent)) === 'R$ 1,18' && (await p.$eval('#hnPct', e => e.textContent)) === '12%');
  // 3. hero em 5 estágios, desktop e celular, com área azul
  for (const v of [{w:1440,h:900,t:'d'},{w:390,h:844,t:'m'}]){
    const q = v.t === 'd' ? p : await page(b, v);
    let maxBlue = 0;
    for (const f of [0, .25, .5, .78, 1]){ await scrollTo(q, '#hero', f); await q.waitForTimeout(700); await q.screenshot({path:`${OUT}/hero-${v.t}-${Math.round(f*100)}.png`}); maxBlue = Math.max(maxBlue, await blueShare(q)) }
    ok(`azul no hero ${v.w}px, pior momento`, maxBlue <= .10, (maxBlue*100).toFixed(1) + '%');
    const secs = ['#arquivo','#erros','#numero','#telas','#pecas','#calculadora','#founders','#faq','footer'];
    let worst = [0,''];
    for (const s of secs){ await scrollTo(q, s, s === '#arquivo' ? .5 : 0); await q.screenshot({path:`${OUT}/sec-${v.t}-${s.replace(/\W/g,'')}.png`}); const bs = await blueShare(q); if (bs > worst[0]) worst = [bs, s] }
    ok(`azul por seção ${v.w}px, pior seção`, worst[0] <= .10, (worst[0]*100).toFixed(1) + '% em ' + worst[1]);
    const ovf = await q.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    ok(`sem rolagem horizontal ${v.w}px`, ovf <= 0, ovf + 'px');
    ok(`zero erro de console ${v.w}px`, q.errs.length === 0, q.errs.join(' | '));
  }
  // 4. movimento reduzido: sem pin, capítulo empilhado, página inteira legível
  const r = await page(b, {w:390, h:844, rm:true});
  const rm = await r.evaluate(() => ({hero: document.querySelector('#hero').offsetHeight, ih: innerHeight, steps: [...document.querySelectorAll('.step')].every(s => getComputedStyle(s).opacity === '1'), pos: getComputedStyle(document.querySelector('.cap-stage')).position}));
  ok('reduced motion: hero sem pin, passos visíveis, capítulo sem sticky', rm.hero <= rm.ih + 2 && rm.steps && rm.pos !== 'sticky', JSON.stringify(rm));
  await r.screenshot({path:`${OUT}/rm-top.png`, fullPage:false});
  ok('reduced motion: zero erro de console', r.errs.length === 0, r.errs.join(' | '));
  await b.close();
  // 5. sem WebGL: fallback SVG aparece, página funciona
  const b2 = await chromium.launch({args:['--disable-gpu','--disable-webgl','--disable-3d-apis']});
  const n = await page(b2, {w:1440, h:900});
  await scrollTo(n, '#hero', .5);
  const nog = await n.evaluate(() => ({fb: getComputedStyle(document.querySelector('#fb3d')).display, gl: getComputedStyle(document.querySelector('#gl')).display, price: document.querySelector('#rPrice .sr').textContent}));
  await n.screenshot({path:`${OUT}/nogl-hero.png`});
  ok('sem WebGL: SVG do símbolo no lugar do canvas, calculadora viva', nog.fb === 'block' && nog.gl === 'none' && nog.price === 'R$ 38,97', JSON.stringify(nog));
  ok('sem WebGL: zero erro de console', n.errs.length === 0, n.errs.join(' | '));
  await b2.close();
  fs.writeFileSync(`${OUT}/resultado.json`, JSON.stringify(res, null, 1));
  const f = res.filter(x => !x.pass).length; console.log(f ? `\n${f} FALHA(S)` : '\nTUDO PASSOU'); process.exit(f ? 1 : 0);
})();
