// Teste da página /espera: render, rolagem, telas, formulário com envio interceptado.
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const BASE = 'http://localhost:8765';
const SHOT = process.argv[2] || 'shots';
import fs from 'fs'; fs.mkdirSync(SHOT, { recursive: true });

const res = []; const ok = (n, c, info='') => { res.push([c ? 'OK ' : 'FALHOU', n, info]); };
const browser = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'] });

for (const vp of [{ w: 1440, h: 900, n: 'desk' }, { w: 390, h: 844, n: 'mob', mobile: true }]) {
  const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, isMobile: !!vp.mobile, hasTouch: !!vp.mobile, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|ERR_|net::/.test(m.text())) errs.push(m.text()) });
  let payload = null;
  await page.route('**/functions/v1/lead-espera', async r => {
    payload = JSON.parse(r.request().postData());
    await r.fulfill({ status: 200, contentType: 'application/json', headers: { 'Access-Control-Allow-Origin': '*' }, body: '{"ok":true}' });
  });
  await page.goto(BASE + '/espera/?utm_source=teste', { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${SHOT}/${vp.n}-1-hero.png` });

  // meio da impressão e preço final
  const heroH = await page.evaluate(() => document.getElementById('hero').offsetHeight - innerHeight);
  await page.evaluate(y => scrollTo(0, y), heroH * 0.45); await page.waitForTimeout(1600);
  await page.screenshot({ path: `${SHOT}/${vp.n}-2-imprimindo.png` });
  await page.evaluate(y => scrollTo(0, y), heroH * 0.99); await page.waitForTimeout(1600);
  await page.screenshot({ path: `${SHOT}/${vp.n}-3-preco.png` });
  const ov = await page.evaluate(() => {
    const R = s => { const e = document.querySelector(s); if (!e || e.hidden || getComputedStyle(e).display === 'none') return null; return e.getBoundingClientRect() };
    const hit = (a, b) => a && b && a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
    const v = R('#views'), t = R('#ticket'), hud = R('.hud'), nav = R('.nav .in'), cta = R('.hero .ctas');
    return { visivel: !!v, ticket: hit(v, t), hud: hit(v, hud), nav: hit(v, nav), cta: hit(v, cta) };
  });
  ok(`${vp.n}: seletor Malha/Camadas/Sólido não encosta em nada`, ov.visivel && !ov.ticket && !ov.hud && !ov.nav && !ov.cta, JSON.stringify(ov));
  const precoTxt = await page.$eval('#ttot', e => e.textContent.replace(/\s/g, ''));
  ok(`${vp.n}: ticket chega no preço`, /R\$\d+,\d{2}/.test(precoTxt) && !/R\$0,00/.test(precoTxt), precoTxt);

  // telas
  await page.$eval('#telas', e => e.scrollIntoView()); await page.waitForTimeout(1800);
  await page.screenshot({ path: `${SHOT}/${vp.n}-4-telas.png` });
  const foto = await page.$eval('#app img.view.on', e => ({ ok: e.complete && e.naturalWidth > 0, src: e.currentSrc }));
  ok(`${vp.n}: foto real do orçamento carregada`, foto.ok, foto.src);
  for (const t of ['funil','prod']) { await page.click(`#tabs button[data-v="${t}"]`); await page.waitForTimeout(450); await page.screenshot({ path: `${SHOT}/${vp.n}-5-telas-${t}.png` }); }
  ok(`${vp.n}: sem botão de zoom`, (await page.$('#zoomBtn')) === null);
  const fotos = await page.$$eval('#app img.view', l => l.map(e => e.dataset.v + ':' + (e.complete && e.naturalWidth > 0)));
  ok(`${vp.n}: as 4 fotos do app carregam`, fotos.length === 4 && fotos.every(f => f.endsWith(':true')), fotos.join(' '));
  await page.click('#tabs button[data-v="fin"]'); await page.waitForTimeout(500);
  ok(`${vp.n}: aba Financeiro troca a tela`, await page.$eval('.view[data-v="fin"]', e => e.classList.contains('on')));
  if (vp.n === 'desk') {
    await page.evaluate(() => scrollTo(0, document.getElementById('founders').offsetTop)); await page.waitForTimeout(700);
    const nv = await page.evaluate(() => { const n = document.querySelector('.nav .in').getBoundingClientRect(), w = document.querySelector('#founders .wrap'), cs = getComputedStyle(w), r = w.getBoundingClientRect();
      return { nav: [Math.round(n.left), Math.round(n.right)], conteudo: [Math.round(r.left + parseFloat(cs.paddingLeft)), Math.round(r.right - parseFloat(cs.paddingRight))], cap: document.getElementById('nav').classList.contains('cap') } });
    ok(`${vp.n}: menu flutuante na largura do conteúdo`, nv.cap && Math.abs(nv.nav[0] - nv.conteudo[0]) <= 1 && Math.abs(nv.nav[1] - nv.conteudo[1]) <= 1, JSON.stringify(nv));
    await page.screenshot({ path: `${SHOT}/${vp.n}-menu-flutuante.png` });
  }
  await page.screenshot({ path: `${SHOT}/${vp.n}-5-telas-fin.png` });

  // formulário
  await page.click('.nav .btn-p', { force: true }).catch(() => {});
  await page.$eval('#lista', e => e.scrollIntoView()); await page.waitForTimeout(900);
  await page.screenshot({ path: `${SHOT}/${vp.n}-6-founders.png`, fullPage: false });
  await page.$eval('#founders', e => e.scrollIntoView()); await page.waitForTimeout(900);
  await page.screenshot({ path: `${SHOT}/${vp.n}-6b-founders-topo.png` });

  // envio vazio: erros nos obrigatórios, nada sai
  await page.click('#enviar');
  const bads = await page.$$eval('.fm .f.bad', l => l.map(e => e.dataset.f));
  ok(`${vp.n}: envio vazio marca nome, e-mail, WhatsApp e aceite`, ['nome','email','whatsapp','consent'].every(k => bads.includes(k)), bads.join(','));
  ok(`${vp.n}: envio vazio não chama o servidor`, payload === null);
  await page.$eval('#lista', e => e.scrollIntoView()); await page.waitForTimeout(300);
  await page.screenshot({ path: `${SHOT}/${vp.n}-7-erros.png` });

  await page.fill('#nome', 'Teste da Silva');
  await page.fill('#email', 'teste@exemplo');
  await page.locator('#email').blur();
  ok(`${vp.n}: e-mail sem domínio fica marcado`, await page.$eval('[data-f="email"]', e => e.classList.contains('bad')));
  await page.fill('#email', 'Teste@Exemplo.com');
  await page.locator('#whatsapp').pressSequentially('21995551234');
  ok(`${vp.n}: máscara do WhatsApp`, (await page.inputValue('#whatsapp')) === '(21) 99555-1234', await page.inputValue('#whatsapp'));
  await page.selectOption('#qtd', '2');
  await page.selectOption('#precifica', 'sistema');
  ok(`${vp.n}: "Outro sistema" abre o campo qual`, await page.isVisible('#qual'));
  await page.fill('#qual', 'Planilha do fulano');

  const mi = page.locator('[data-tags="marcas"] input');
  await mi.click(); await mi.pressSequentially('bamb'); await page.waitForTimeout(150);
  await page.screenshot({ path: `${SHOT}/${vp.n}-8-sugestao.png` });
  await mi.press('ArrowDown'); await mi.press('Enter');
  await mi.pressSequentially('kingroon'); await mi.press('Enter');
  await mi.pressSequentially('creality'); await mi.press('Enter');
  await mi.pressSequentially('BAMBU LAB'); await mi.press('Enter'); // repetido, não entra
  await mi.press('Backspace'); // tira Creality
  const vi = page.locator('[data-tags="vende"] input');
  await vi.click(); await vi.pressSequentially('shop'); await vi.press('Enter');
  await vi.pressSequentially('insta'); await vi.press('ArrowDown'); await vi.press('Enter'); await vi.press('Escape');

  await page.check('#consent');
  await page.waitForTimeout(3100); // tempo mínimo da Edge Function
  await page.screenshot({ path: `${SHOT}/${vp.n}-9-preenchido.png` });
  await page.click('#enviar');
  await page.waitForSelector('#ok.on', { timeout: 4000 }).catch(() => {});
  ok(`${vp.n}: sucesso aparece`, await page.isVisible('#ok'));
  await page.waitForTimeout(600);
  await page.screenshot({ path: `${SHOT}/${vp.n}-10-sucesso.png` });
  const p = payload || {};
  ok(`${vp.n}: payload completo`,
    p.nome === 'Teste da Silva' && p.email === 'Teste@Exemplo.com' && p.whatsapp === '(21) 99555-1234' &&
    p.qtd_impressoras === '2' && JSON.stringify(p.marcas) === '["Bambu Lab","kingroon"]' &&
    JSON.stringify(p.vende_onde) === '["Shopee","Instagram"]' && p.precifica_hoje === 'sistema' && p.precifica_qual === 'Planilha do fulano' &&
    p.quer_founder === true && p.consentimento === true && p.empresa_site === '' && p.decorrido_ms >= 3000 && p.utm_source === 'teste',
    JSON.stringify(p));

  // sem horizontal, sem erro de console
  const hs = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  ok(`${vp.n}: sem rolagem horizontal`, hs <= 0, String(hs));
  ok(`${vp.n}: zero erro de console`, errs.length === 0, errs.join(' | '));
  await page.screenshot({ path: `${SHOT}/${vp.n}-full.png`, fullPage: true });
  await ctx.close();
}

// WhatsApp opcional sem Founders; servidor recusando mostra a mensagem dele
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  await page.route('**/functions/v1/lead-espera', r => r.fulfill({ status: 429, contentType: 'application/json', body: '{"erro":"limite","mensagem":"Muitos envios. Tente mais tarde."}' }));
  await page.goto(BASE + '/espera/');
  await page.$eval('#lista', e => e.scrollIntoView());
  await page.fill('#nome', 'Sem Zap'); await page.fill('#email', 'semzap@exemplo.com.br');
  await page.uncheck('#founder'); await page.check('#consent');
  ok('sem Founders: WhatsApp vira opcional', (await page.textContent('#wa-opt')) === 'opcional');
  await page.waitForTimeout(3100); await page.click('#enviar'); await page.waitForTimeout(500);
  ok('servidor recusando mostra a mensagem', (await page.textContent('#msg')) === 'Muitos envios. Tente mais tarde.');
  ok('botão volta a funcionar depois do erro', await page.isEnabled('#enviar'));
  await ctx.close();
}

// política de privacidade abre
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  const r = await page.goto(BASE + '/privacidade/');
  ok('/privacidade abre', r.status() === 200 && /Política de privacidade/.test(await page.title()));
  await page.screenshot({ path: `${SHOT}/privacidade-mob.png`, fullPage: true });
  await ctx.close();
}

// movimento reduzido
{
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage(); const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto(BASE + '/espera/'); await page.waitForTimeout(800);
  ok('movimento reduzido sem erro', errs.length === 0, errs.join('|'));
  await ctx.close();
}

await browser.close();
for (const r of res) console.log(r[0], r[1], r[2] ? '· ' + String(r[2]).slice(0, 300) : '');
console.log(`${res.filter(r => r[0] === 'OK ').length} de ${res.length}`);
