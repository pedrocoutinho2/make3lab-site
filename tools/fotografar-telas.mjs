// Fotografa as telas reais do app (modo demonstração) para a seção "O sistema" da /founders.
// Uso: node tools/fotografar-telas.mjs <index.html do app> <pasta de saída>
// Monta dados de exemplo pela própria interface (orçamentos, vendas, fila, financeiro)
// e salva orc.png, funil.png, prod.png e fin.png em 1440x879 com densidade 2.
// Rodar de novo sempre que o layout do app mudar.
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PW || '/opt/npm-tools/node_modules/playwright');
import http from 'http';
import fs from 'fs';

const [APP, OUT] = process.argv.slice(2);
fs.mkdirSync(OUT, { recursive: true });
const html = fs.readFileSync(APP, 'utf8').replace(/window\.M3_CONFIG = \{[\s\S]*?\};/, 'window.M3_CONFIG = {};');
const srv = http.createServer((q, r) => { r.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); r.end(html); }).listen(0);
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 879 }, deviceScaleFactor: 2 })).newPage();
const erros = []; p.on('pageerror', e => erros.push(e.message));
const espera = ms => p.waitForTimeout(ms);
await p.goto(`http://localhost:${srv.address().port}/`); await espera(700);
await p.click('button[type=submit]'); await espera(900);

// a faixa "Modo demonstração" e a bolinha de notificação não aparecem na foto
const LIMPA = `.m3 [role=status]:has-text("Modo demonstração"){display:none!important}`;
async function semFaixa() {
  await p.evaluate(() => {
    for (const el of document.querySelectorAll('main *')) {
      if (el.children.length === 0 && /^Modo demonstração\./.test(el.textContent.trim())) {
        let box = el; while (box.parentElement && box.parentElement.tagName !== 'MAIN' && box.parentElement.children.length === 1) box = box.parentElement;
        box.style.display = 'none';
      }
    }
  });
}
const menu = async (nome) => {
  await p.locator('nav[aria-label="Menu"] button', { hasText: new RegExp(`^\\s*${nome}\\s*$`) }).first().click(); await espera(600);
};
async function cliente(nome) { await p.fill('#o-cli', nome); await espera(250); await p.locator('#o-cli ~ .lista button').first().click(); await espera(250); }
async function produto(busca, nome, qtd) {
  await p.fill('input[placeholder^="digite o nome do produto"]', busca); await espera(300);
  await p.locator('main button', { hasText: nome }).first().click(); await espera(350);
  const q = p.locator('main input[aria-label="Quantidade"]');
  await q.nth(await q.count() - 1).fill(String(qtd)); await espera(200);
}
async function insumo(busca, nome) {
  await p.fill('input[placeholder^="digite o nome do insumo"]', busca); await espera(300);
  await p.locator('main button', { hasText: nome }).first().click(); await espera(350);
}
async function salvar() { await p.getByRole('button', { name: /^\s*Salvar/ }).first().click(); await espera(800); }

// orçamento 1: o da foto
await menu('Orçamentos'); await p.getByRole('button', { name: 'Novo orçamento', exact: true }).last().click(); await espera(500);
await cliente('Cliente exemplo A');
await p.selectOption('#o-st', 'enviado');
await p.fill('#o-prazo', '7 dias úteis após aprovação');
await produto('Chaveiro', 'Chaveiro com logo do cliente', 50);
await produto('Porta', 'Porta-aliança', 4);
await produto('Plaquinha', 'Plaquinha de identificação pet', 10);
await insumo('Sílica', 'Sílica');
await p.getByText('Pedir sinal para validar o pedido').click(); await espera(300);
const sinal = p.locator("xpath=//*[contains(text(),\"Pedir sinal\")]/following::input[not(@type=\"checkbox\")][1]");
await sinal.first().fill('50').catch(() => {}); await espera(300);
await semFaixa();
// aviso de estoque da loja de demonstração (estoque de embalagem baixo) fica fora da foto
await p.evaluate(() => {
  const t = [...document.querySelectorAll('main *')].find(e => e.children.length === 0 && /^Estoque (ficando curto|insuficiente)/.test(e.textContent.trim()));
  if (t) { let box = t; while (box.parentElement && !/border-left/.test(box.parentElement.getAttribute('style') || '') && box.parentElement.textContent.length < 600) box = box.parentElement; box.style.display = 'none'; }
});
await p.evaluate(() => { const h = [...document.querySelectorAll('main h2, main h3, main div')].find(e => e.textContent.trim() === 'Produtos'); if (h) { const y = h.getBoundingClientRect().top + scrollY - 70; scrollTo(0, y); } });
await espera(400);
await p.screenshot({ path: `${OUT}/orc.png` });
await salvar();

// orçamentos 2 e 3 para o funil
for (const [cli, st, itens] of [
  ['Cliente exemplo B', 'rascunho', [['Porta', 'Porta-aliança', 20]]],
  ['Cliente exemplo B', 'enviado', [['Plaquinha', 'Plaquinha de identificação pet', 40], ['Chaveiro', 'Chaveiro com logo do cliente', 15]]],
]) {
  await menu('Orçamentos'); await p.getByRole('button', { name: 'Novo orçamento', exact: true }).last().click(); await espera(500);
  await cliente(cli); await p.selectOption('#o-st', st);
  for (const [bq, n, q] of itens) await produto(bq, n, q);
  await salvar();
}

// vendas: entram na fila de produção e no a receber
for (const [cli, pago, itens] of [
  ['Cliente exemplo A', false, [['Chaveiro', 'Chaveiro com logo do cliente', 25]]],
  ['Cliente exemplo B', true, [['Porta', 'Porta-aliança', 3]]],
  ['Cliente exemplo A', false, [['Plaquinha', 'Plaquinha de identificação pet', 10], ['Porta', 'Porta-aliança', 2]]],
  ['Cliente exemplo B', true, [['Chaveiro', 'Chaveiro com logo do cliente', 40]]],
]) {
  await menu('Início'); await p.getByRole('button', { name: 'Nova venda', exact: true }).first().click(); await espera(500);
  await cliente(cli);
  for (const [bq, n, q] of itens) await produto(bq, n, q);
  if (pago) {
    await p.fill('#v-forma', 'PIX'); await espera(300);
    await p.locator('#v-forma ~ .lista button', { hasText: 'PIX' }).first().click().catch(() => p.keyboard.press('Enter')); await espera(250);
    await p.getByText('Pagamento já efetuado', { exact: true }).first().click(); await espera(250);
  }
  await p.getByRole('button', { name: /Salvar venda/ }).click(); await espera(800);
  const aviso = await p.locator('main').innerText();
  if (/precisa|Escolha|Informe/.test(aviso.slice(0, 400))) throw new Error('venda não salvou: ' + aviso.slice(0, 200));
}

// fila: uma ordem imprimindo e uma no pós-processo
await menu('Fila de produção');
const setas = () => p.locator('main button[aria-label="Mover para a próxima etapa"]');
console.log('setas encontradas', await setas().count());
for (const n of [0, 0, 1]) { const s = setas(); if (await s.count() > n) { await s.nth(n).click(); await espera(500); } }

for (const [nome, arq] of [['Funil de vendas', 'funil'], ['Fila de produção', 'prod'], ['Financeiro', 'fin']]) {
  await menu(nome); await espera(400); await semFaixa(); await p.evaluate(() => scrollTo(0, 0)); await espera(300);
  await p.screenshot({ path: `${OUT}/${arq}.png` });
}
console.log('erros', JSON.stringify(erros));
await b.close(); srv.close();
process.exit(erros.length ? 1 : 0);
