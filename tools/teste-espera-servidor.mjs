// Teste da /espera contra respostas reais da Edge Function: mensagem do servidor
// aparece no formulário, botão volta a funcionar e e-mail repetido mostra sucesso.
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const BASE = process.env.BASE || 'http://localhost:8765';

const res = []; const ok = (n, c, info = '') => res.push([c ? 'OK ' : 'FALHOU', n, info]);
const browser = await chromium.launch();

async function preenche(page) {
  await page.fill('#nome', 'Ana Teste');
  await page.fill('#email', 'ana@exemplo.com');
  await page.fill('#whatsapp', '21999998888');
  await page.check('#consent');
}

for (const vp of [{ w: 1440, h: 900, n: 'desk' }, { w: 390, h: 844, n: 'mob', mobile: true }]) {
  for (const caso of [
    { nome: 'limite', status: 429, body: { erro: 'limite', mensagem: 'Muitos envios deste aparelho. Tente de novo daqui a uma hora.' }, espera: 'erro' },
    { nome: 'servidor fora', status: 500, body: { erro: 'gravacao', mensagem: 'Não deu para salvar agora. Tente de novo em instantes.' }, espera: 'erro' },
    { nome: 'repetido', status: 200, body: { ok: true, repetido: true }, espera: 'sucesso' },
  ]) {
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, isMobile: !!vp.mobile, hasTouch: !!vp.mobile });
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    await page.route('**/functions/v1/lead-espera', r => r.fulfill({ status: caso.status, contentType: 'application/json', body: JSON.stringify(caso.body) }));
    await page.goto(BASE + '/espera/', { waitUntil: 'load' });
    await page.waitForTimeout(3200); // a função recusa envio em menos de 3 s
    await page.locator('#fm').scrollIntoViewIfNeeded();
    await preenche(page);
    await page.click('#enviar');
    await page.waitForTimeout(700);
    if (caso.espera === 'erro') {
      const m = (await page.textContent('#msg')).trim();
      ok(`${vp.n} ${caso.nome}: mensagem do servidor aparece`, m === caso.body.mensagem, m);
      ok(`${vp.n} ${caso.nome}: botão liberado para tentar de novo`, !(await page.isDisabled('#enviar')));
      ok(`${vp.n} ${caso.nome}: formulário continua na tela`, await page.isVisible('#fm'));
      const cor = await page.$eval('#msg', e => getComputedStyle(e).color);
      ok(`${vp.n} ${caso.nome}: mensagem na cor de erro`, cor === 'rgb(224, 85, 85)', cor);
    } else {
      ok(`${vp.n} ${caso.nome}: mostra sucesso`, await page.isVisible('#ok'));
    }
    ok(`${vp.n} ${caso.nome}: sem erro de JS`, errs.length === 0, errs.join(' | '));
    await ctx.close();
  }
}

// /privacidade existe e volta para a lista
const ctx = await browser.newContext(); const page = await ctx.newPage();
const r = await page.goto(BASE + '/privacidade/');
ok('privacidade: abre', r.status() === 200);
ok('privacidade: link de volta para /espera', await page.locator('a[href="/espera"]').count() > 0);
await browser.close();

for (const [s, n, i] of res) console.log(s, n, i ? '· ' + i : '');
const f = res.filter(x => x[0] === 'FALHOU').length;
console.log(`${res.length - f} de ${res.length}`);
process.exit(f ? 1 : 0);
