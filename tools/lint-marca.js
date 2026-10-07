// Varre o index.html e falha se achar desvio do design system do Make3Lab.
// Uso: node tools/lint-marca.js [caminho]
const fs = require('fs');
const file = process.argv[2] || require('path').join(__dirname, '..', 'index.html');
const src = fs.readFileSync(file, 'utf8');
const TOKENS = ['061620','0C2130','12303F','1B4256','C6E7FB','5EBAF3','25A1EF','1087D1','0C68A1','094972','41627A','6B7F8E','8FA3B0','D8E4EC','EBF1F5','F7FAFC','2E9E6B','F2C200','E05555','04121A','FFFFFF'];
const BRAND = ['azul-100','azul-300','azul-400','azul-500','azul-600','azul-700','C6E7FB','5EBAF3','25A1EF','1087D1','0C68A1','094972','37,161,239','94,186,243','16,135,209','198,231,251'];
const fails = [];
const lines = src.split('\n');
lines.forEach((ln, i) => {
  const n = i + 1;
  // hex fora da lista (ignora as máscaras #000, que não são cor visível, e o path do favicon em data URI)
  (ln.match(/#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b/g) || []).forEach(h => {
    const v = h.slice(1).toUpperCase();
    if (v === '000' && /mask/.test(ln)) return;
    if (!TOKENS.includes(v)) fails.push(`${n}: hex fora dos tokens ${h}`);
  });
  (ln.match(/%23([0-9A-Fa-f]{6})/g) || []).forEach(h => { if (!TOKENS.includes(h.slice(3).toUpperCase())) fails.push(`${n}: hex fora dos tokens ${h}`) });
  // cores do Three.js
  (ln.match(/0x[0-9A-Fa-f]{6}\b/g) || []).forEach(h => { const v = h.slice(2).toUpperCase(); if (!TOKENS.includes(v) && v !== '000000') fails.push(`${n}: cor 3D fora dos tokens ${h}`) });
  if (/[—–]/.test(ln)) fails.push(`${n}: travessão`);
  if (/box-shadow/.test(ln) && !/focus/.test(ln)) fails.push(`${n}: box-shadow fora de foco`);
  const grads = ln.match(/(repeating-)?(linear|radial|conic)-gradient\([^;]*/g) || [];
  grads.forEach(g => {
    if (/--malha|rgba\(110,200,255/.test(ln)) return;           // a malha é o elemento assinatura
    if (BRAND.some(b => g.includes(b))) fails.push(`${n}: degradê com cor de marca`);
  });
  if (/rgba\(0,\s*0,\s*0/.test(ln)) fails.push(`${n}: preto puro em rgba`);
});
if (fails.length) { console.log('FALHOU\n' + fails.join('\n')); process.exit(1) }
console.log('OK: nenhum hex fora dos tokens, nenhum travessão, nenhuma sombra, nenhum degradê de marca');
