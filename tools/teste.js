// Teste de navegador do site. Precisa do site servido em http://localhost:8765 e do Playwright.
// Uso: node tools/teste.js <pasta de saída>   (PW=<caminho do playwright> se não estiver em node_modules)
const { chromium } = require(process.env.PW || 'playwright');
const OUT = process.argv[2] || '.';
const URL = process.env.URL || 'http://localhost:8765/';
const fs = require('fs');
const FIX = require('./casos-calculadora.json'), CASOS = FIX.casos, BORDAS = FIX.bordas;
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
async function center(p, sel){ await p.evaluate(s => { const el = document.querySelector(s), r = el.getBoundingClientRect(); window.scrollTo(0, r.top + scrollY - Math.max(0, (innerHeight - r.height)/2)) }, sel); await p.waitForTimeout(1100) }
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
async function shot(p, sel, path){ await p.waitForTimeout(900); const h = await p.addStyleTag({content:'#nav,.pbar{visibility:hidden!important}'}); await p.locator(sel).screenshot({path}); await h.evaluate(e => e.remove()) }
const txt = (p, s) => p.$eval(s, e => e.textContent.trim());
const money = (p, s) => p.$eval(s, e => (e.querySelector('.sr') || e).textContent.trim());
async function set(p, id, v){ await p.fill(id, String(v)); await p.dispatchEvent(id, 'input'); await p.waitForTimeout(120) }
async function canal(p, v){ await p.click(`#chan button[data-v="${v}"]`); await p.waitForTimeout(120) }
async function nota(p, com){ await p.click(`#nota button[data-v="${com ? 'com' : 'sem'}"]`); await p.waitForTimeout(120) }

(async () => {
  const b = await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});

  for (const v of [{w:1440,h:900,t:'d'},{w:390,h:844,t:'m'}]){
    const p = await page(b, v);
    const W = v.w + 'px';

    // 1. calculadora: casos sem nota e com nota, feitos à mão e conferidos no fn_precificar
    await center(p, '#calculadora');
    let aberta = false;
    for (const c of CASOS){
      await canal(p, c.canal); await nota(p, c.nota);
      if (c.nota) await set(p, '#c-imp', c.imposto);
      if (c.pag !== '0' && !aberta){ await p.click('#more summary'); aberta = true; await p.waitForTimeout(300) }
      if (aberta) await set(p, '#c-pag', c.pag);
      await set(p, '#c-g', c.g); await set(p, '#c-th', c.h); await set(p, '#c-tm', c.min); await set(p, '#c-kg', c.kg.replace(',','')); await set(p, '#c-luc', c.lucro);
      const got = {preco: await money(p, '#rPrice'), custo: await money(p, '#rCost'), lucroR: await money(p, '#rProfit'), taxas: await money(p, '#rFees'), impostoR: await money(p, '#rTax')};
      const impVis = await p.$eval('#rTaxW', e => !e.hidden);
      const pass = ['preco','custo','lucroR','taxas','impostoR'].every(k => got[k] === c[k]) && impVis === c.nota;
      ok(`${W} calc caso ${c.id}${c._obs ? ' (' + c._obs + ')' : ''} ${c.nota ? 'com nota ' + c.imposto + '%' : 'sem nota'}${c.pag !== '0' ? ', pagamento ' + c.pag + '%' : ''}: ${c.canal}, ${c.g} g, ${c.h} h ${c.min} min, R$ ${c.kg}/kg, ${c.lucro}%`, pass, JSON.stringify(got) + (impVis ? ' imposto visível' : ''));
    }
    if (aberta){ await set(p, '#c-pag', 0); await p.click('#more summary'); await p.waitForTimeout(300) }
    // percentual fiscal com até duas casas: ponto e vírgula são separador decimal, terceira casa arredonda
    const MASC = [['6.725','6,73'],['6.72','6,72'],['6,72','6,72'],['6,725','6,73'],['4.994','4,99'],['9.995','10,00']];
    for (const id of ['#c-imp','#c-pag']){
      if (id === '#c-pag'){ await p.click('#more summary'); await p.waitForTimeout(300) }
      const got = []; for (const [inp] of MASC){ await set(p, id, inp); got.push(await p.inputValue(id)) }
      ok(`${W} ${id === '#c-imp' ? 'imposto' : 'taxa de pagamento'}: ${MASC.map(m => m[0] + ' vira ' + m[1]).join(', ')}`, got.every((g, i) => g === MASC[i][1]), got.join(' / '));
      if (id === '#c-pag'){ await set(p, id, 0); await p.click('#more summary'); await p.waitForTimeout(300) }
    }
    if (v.t === 'd'){ await center(p, '#res'); }
    await p.screenshot({path:`${OUT}/calculadora-${v.w}-com-nota.png`});
    await shot(p, '#calculadora', `${OUT}/calculadora-${v.w}-secao.png`);

    // 2. tempo em horas e minutos
    await set(p, '#c-th', 0); await set(p, '#c-tm', 75); await p.dispatchEvent('#c-tm', 'blur'); await p.waitForTimeout(150);
    ok(`${W} tempo: 0 h 75 min normaliza para 1 h 15 min`, (await p.inputValue('#c-th')) === '1' && (await p.inputValue('#c-tm')) === '15', (await p.inputValue('#c-th')) + ' h ' + (await p.inputValue('#c-tm')) + ' min');
    await set(p, '#c-th', 1); await set(p, '#c-tm', 50); await p.click('#c-tm ~ .stp[data-step="10"]'); await p.waitForTimeout(150);
    ok(`${W} tempo: 1 h 50 min + 10 dá 2 h 0 min`, (await p.inputValue('#c-th')) === '2' && (await p.inputValue('#c-tm')) === '0', (await p.inputValue('#c-th')) + ' h ' + (await p.inputValue('#c-tm')) + ' min');
    await set(p, '#c-th', 0); await set(p, '#c-tm', 0);
    const zero = await p.$eval('[data-f="minutos"]', e => ({bad: e.classList.contains('bad'), vis: getComputedStyle(e.querySelector('.err')).display !== 'none', t: e.querySelector('.err').textContent}));
    ok(`${W} tempo: zero dá erro`, zero.bad && zero.vis && zero.t === 'Informe o tempo de impressão, maior que zero.', JSON.stringify(zero));
    await set(p, '#c-th', 3); await set(p, '#c-tm', 10);
    if (v.w < 1024){ const fs16 = await p.$$eval('#cf input', a => a.every(i => getComputedStyle(i).fontSize === '16px')); ok(`${W} input com 16 px abaixo de 1024 px`, fs16) }

    // 3. limite de taxas igual ao fn_precificar com ,90: sem corte por percentual, recusa só se o preço não fechar em 20.000 passos
    await set(p, '#c-g', 85); await set(p, '#c-th', 3); await set(p, '#c-tm', 10); await set(p, '#c-kg', '12000'); await set(p, '#c-luc', 50); await nota(p, true);
    for (const t of BORDAS){
      await canal(p, t.canal); await set(p, '#c-imp', t.imposto);
      const e = await p.evaluate(() => ({err: document.querySelector('#rErr').textContent, errVis: !document.querySelector('#rErr').hidden, price: getComputedStyle(document.querySelector('#rPrice')).display, v: document.querySelector('#rPrice .sr').textContent}));
      const pass = t.erro ? (e.errVis && e.err === t.erro && e.price === 'none') : (!e.errVis && e.price !== 'none' && e.v === t.preco);
      ok(`${W} taxas em ${t.soma}: ${t.erro ? 'erro e sem preço' : 'calcula ' + t.preco + ', igual ao sistema'}`, pass, JSON.stringify(e));
    }
    await set(p, '#c-imp', 4); await nota(p, false); await canal(p, 'shopee'); await set(p, '#c-g', 85);

    if (v.t === 'd'){
      // 4. número herói e peças, tudo do motor da página
      ok('número herói: 12% grande, R$ 1,34 a menos em cada vaso espiral', (await txt(p, '#hnBig')) === '12%' && (await txt(p, '.hn .per')) === 'R$ 1,34 a menos em cada vaso espiral.', (await txt(p, '#hnBig')) + ' · ' + (await txt(p, '.hn .per')));
      const hnFont = await p.$eval('#hnBig', e => getComputedStyle(e).fontFamily + ' ' + getComputedStyle(e).fontVariantNumeric);
      ok('número herói na fonte de número, tabular', /Archivo/.test(hnFont) && /tabular-nums/.test(hnFont), hnFont);
      const gal = await p.$$eval('.pc', a => a.map(e => e.querySelector('.meta b').textContent + ' ' + e.querySelector('.pr').textContent).join(' | '));
      ok('galeria: seis peças novas com preço', gal === 'Vaso espiral R$ 42,90 | Cachepô facetado R$ 61,90 | Luminária de lua R$ 52,90 | Cobra articulada R$ 29,90 | Pião R$ 21,90 | Porta-velas R$ 35,90', gal);
      ok('capítulo: vaso-espiral.3mf, 85 g, 3 h 10 min', (await txt(p, '.file b')) === 'vaso-espiral.3mf' && (await txt(p, '#c2g')) === '85 g' && (await txt(p, '#c2t')) === '3 h 10 min');
      ok('ticket do hero: vaso espiral', (await txt(p, '#ticket header strong')) === 'Vaso espiral');
      // 5. demos dos cinco erros
      ok('erro 01: imposto fora do preço tira R$ 2,48 do lucro do cachepô', (await txt(p, '#n1w')) === 'Somem R$ 2,48 do lucro. É 15% dele.', await txt(p, '#n1w'));
      ok('erro 02: luminária com perda de 15% fica R$ 4,00 mais cara', (await txt(p, '#p2w')) === 'A mesma luminária fica R$ 4,00 mais cara.', await txt(p, '#p2w'));
      ok('erro 03: pião sai a R$ 20,90 sem refugo e R$ 21,90 com 8%', (await money(p, '#r1p')) === 'R$ 20,90' && (await money(p, '#r2p')) === 'R$ 21,90' && (await txt(p, '#r1w')) === '4 falhas em 50 piões. R$ 28,84 em material e máquina que ninguém cobrou.', (await money(p, '#r1p')) + ' / ' + (await money(p, '#r2p')) + ' · ' + (await txt(p, '#r1w')));
      await p.fill('#fil', '160'); await p.dispatchEvent('#fil', 'input'); await p.waitForTimeout(200);
      ok('erro 04: orçamento de ontem fica congelado', (await money(p, '#o1c')) !== (await money(p, '#o2c')) && (await txt(p, '#o2w')).includes('continua em ' + (await money(p, '#o1c'))), await txt(p, '#o2w'));
      await p.fill('#fil', '120'); await p.dispatchEvent('#fil', 'input');
      await center(p, '#e5'); await p.click('#ledBtn'); await p.waitForTimeout(400);
      const ex = await p.$$eval('#led .r', a => a.map(r => r.innerText.replace(/\s+/g,' ')));
      ok('erro 05: devolução vira estorno, a venda continua', ex.length === 3 && /Venda VD-0152/.test(ex[1]) && /Estorno VD-0152/.test(ex[2]), ex.join(' | '));
      await p.click('#ledBtn'); await p.click('#ledBtn');
      // 6. palavras que saíram da página
      const body = (await p.evaluate(() => document.body.innerText)).toLowerCase();
      ok('nenhum "float", "numeric" ou "ponto flutuante" no texto', !/float|numeric|ponto flutuante/.test(body));
      ok('nenhum travessão no texto', !/[—–]/.test(body));
      ok('nenhuma peça técnica antiga no texto', !/headset|suporte em l|gancho de parede|engrenagem|porta-caneta|clipe de cabo|organizador de cabos|dock de fones/.test(body));
      const fonte = await p.$eval('#rPrice', e => getComputedStyle(e).fontFamily + ' ' + getComputedStyle(e).fontVariantNumeric);
      ok('números em Archivo com algarismo tabular', /Archivo/.test(fonte) && /tabular-nums/.test(fonte), fonte);
    }

    // 7. prints: hero, número herói, calculadora, galeria e cinco erros
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(900); await p.screenshot({path:`${OUT}/hero-${v.w}.png`});
    await center(p, '#numero'); await p.waitForTimeout(600); await p.screenshot({path:`${OUT}/numero-heroi-${v.w}.png`});
    for (const s of ['#e1','#e2','#e3','#e4','#e5']){ await center(p, s); await p.waitForTimeout(700); await p.screenshot({path:`${OUT}/erros-${v.w}-${s.slice(1)}.png`}) }
    await center(p, '#pecas'); await p.waitForTimeout(600); await p.screenshot({path:`${OUT}/galeria-${v.w}.png`});
    await shot(p, '#pecas', `${OUT}/galeria-${v.w}-secao.png`);

    // 8. azul por tela, rolagem horizontal, console
    let maxBlue = 0;
    for (const f of [0, .25, .5, .78, 1]){ await scrollTo(p, '#hero', f); await p.waitForTimeout(700); maxBlue = Math.max(maxBlue, await blueShare(p)) }
    ok(`${W} azul no hero, pior momento`, maxBlue <= .10, (maxBlue*100).toFixed(1) + '%');
    const secs = ['#arquivo','#e1','#e2','#e3','#e4','#e5','#numero','#telas','#pecas','#calculadora','#founders','#faq','footer'];
    let worst = [0,''];
    for (const s of secs){ if (/^#e\d/.test(s)) await center(p, s); else await scrollTo(p, s, s === '#arquivo' ? .5 : 0); const bs = await blueShare(p); if (bs > worst[0]) worst = [bs, s] }
    ok(`${W} azul por tela, pior tela`, worst[0] <= .10, (worst[0]*100).toFixed(1) + '% em ' + worst[1]);
    const ovf = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    ok(`${W} sem rolagem horizontal`, ovf <= 0, ovf + 'px');
    ok(`${W} zero erro de console`, p.errs.length === 0, p.errs.join(' | '));
    await p.context().close();
  }

  // 9. número herói sai do motor: filamento a R$ 200/kg no código da peça de exemplo muda os dois números
  const ctxH = await b.newContext({viewport:{width:1440,height:900}});
  await ctxH.route(URL, async r => { const resp = await r.fetch(); const body = (await resp.text()).replace("precoKg:120,minutos:190", "precoKg:200,minutos:190"); await r.fulfill({response: resp, body}) });
  const h = await ctxH.newPage(); await h.goto(URL, {waitUntil:'networkidle'}); await h.waitForTimeout(800);
  const hv = await h.evaluate(() => [document.querySelector('#hnBig').textContent, document.querySelector('.hn .per').textContent]);
  ok('número herói com filamento a R$ 200/kg: 8% e R$ 1,16, os dois mudam juntos', hv[0] === '8%' && hv[1] === 'R$ 1,16 a menos em cada vaso espiral.', hv.join(' · '));
  await ctxH.close();

  // 10. movimento reduzido: sem pin, capítulo empilhado, página inteira legível
  const r = await page(b, {w:390, h:844, rm:true});
  const rm = await r.evaluate(() => ({hero: document.querySelector('#hero').offsetHeight, ih: innerHeight, steps: [...document.querySelectorAll('.step')].every(s => getComputedStyle(s).opacity === '1'), pos: getComputedStyle(document.querySelector('.cap-stage')).position}));
  ok('reduced motion: hero sem pin, passos visíveis, capítulo sem sticky', rm.hero <= rm.ih + 2 && rm.steps && rm.pos !== 'sticky', JSON.stringify(rm));
  ok('reduced motion: zero erro de console', r.errs.length === 0, r.errs.join(' | '));
  await b.close();

  // 11. sem WebGL: fallback SVG aparece, página funciona
  const b2 = await chromium.launch({args:['--disable-gpu','--disable-webgl','--disable-3d-apis']});
  const n = await page(b2, {w:1440, h:900});
  await scrollTo(n, '#hero', .5);
  const nog = await n.evaluate(() => ({fb: getComputedStyle(document.querySelector('#fb3d')).display, gl: getComputedStyle(document.querySelector('#gl')).display, price: document.querySelector('#rPrice .sr').textContent}));
  ok('sem WebGL: SVG do símbolo no lugar do canvas, calculadora viva', nog.fb === 'block' && nog.gl === 'none' && nog.price === 'R$ 44,90', JSON.stringify(nog));
  ok('sem WebGL: zero erro de console', n.errs.length === 0, n.errs.join(' | '));
  await b2.close();
  fs.writeFileSync(`${OUT}/resultado.json`, JSON.stringify(res, null, 1));
  const f = res.filter(x => !x.pass).length; console.log(f ? `\n${f} FALHA(S)` : `\nTUDO PASSOU (${res.length})`); process.exit(f ? 1 : 0);
})();
