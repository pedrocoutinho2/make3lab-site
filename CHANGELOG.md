---
chapeu: make3lab
status: ativo, pronto para revisão, sem deploy
atualizado: 2026-09-28
tags: [make3lab, site, changelog]
---

# Site make3lab.com.br, v2 (28/09/2026)

Base: site de 27/09 ("A conta fecha", hero com o 3 imprimindo). Arquivo único: `17-make3lab/site/index.html` (164 KB, 46 KB comprimido). Repo local: `Desktop/Projetos Claude/Make3Lab/site/`.

## O que mudou do base

**Seções novas**
- **Do arquivo ao preço**: capítulo preso em 5 passos (arquivo, leitura, máquina, custo em faixas, preço por canal). Arquivo marcado como exemplo; texto diz que sem fatiar vira estimativa com margem
- **Número herói**: R$ 1,18 a menos por peça (12% do lucro) quando a taxa de 20% entra multiplicando. Calculado pelo motor da página e reproduzível na calculadora. A sugestão original (float x numeric) foi recusada: o erro é de R$ 0,0000000188
- **Galeria**: 6 peças procedurais (suporte, gancho, caixa, engrenagem, porta-caneta, clipe) num único renderer com scissor. Hover, foco ou toque gira e mostra a malha. Preço pelo motor
- **FAQ**: 8 perguntas, todas com resposta no vault

**Evoluído**
- Hero: título por máscara, ticket com dígito rolando, controle Malha · Camadas · Sólido depois da impressão, arrastar para girar com inércia e retorno (setas no teclado), parallax leve da malha. Three.js carrega depois do primeiro paint, com o SVG do símbolo já na tela
- Nav vira cápsula depois do hero, com progresso da página e seção ativa
- Cinco erros: índice com barra de progresso por erro, demo atual acesa, spotlight de borda
- Telas: abas em controle segmentado com barra de avanço automático (para no toque, foco ou mouse) e zoom de câmera até o custo congelado do orçamento
- **Calculadora resumida**: 4 campos com stepper (peso, tempo, filamento, lucro) + canal (Venda direta, Shopee, ML Clássico, ML Premium com as taxas de referência). "Abrir a conta completa" mostra o resto no lugar, sem cadastro. Copiar preço com aviso. Barra fixa de preço no celular
- Founders com a oferta nova (6 meses)
- Copy reescrita em todas as seções, abrindo pelo erro do operador
- Mobile: hero, capítulo e calculadora com layout próprio; alvos de toque de 44 px

**Desvios do base corrigidos**: `#5FC99A` e `#F08A8A` (estado agora é ponto na cor do token + texto neutro), sombra e brilho do mockup, sombra da nav, degradê no trilho do slider e na dica "Role para imprimir", luz azul pontual no bico, frase "é o mesmo motor" (virou "calculado pelas mesmas regras do sistema").

## Testes (28/09)

- `tools/lint-marca.js`: zero hex fora dos tokens, travessão, sombra ou degradê de marca. O mesmo script acusa 7 desvios no base
- `tools/teste.js` (Playwright, 1440 e 390): 17 de 17. Calculadora em 3 casos feitos à mão (R$ 38,97; R$ 37,99; R$ 32,19), erro de campo, número herói, azul por tela (pior: 8,8% desktop, 9,4% celular), sem rolagem horizontal, zero erro de console, movimento reduzido, sem WebGL
- Desempenho com CPU 4x mais lenta: 58 a 60 fps em hero, capítulo, galeria e calculadora, nos dois tamanhos. LCP de 0,6 s com rede 4G simulada. Medido num M1, não num celular intermediário real
- Lighthouse **não rodou**: precisa baixar o pacote, aguardando autorização

## Pendências [CONFIRMAR]

1. Motor real: `motor-006.js` perdido, a página usa reimplementação das regras de 18/09
2. Refugo multiplicando ou dividindo (hoje multiplica)
3. Perda de 5% no peso digitado (padrão sem fonte)
4. Custo de hora de máquina (R$ 0,67 x R$ 0,85). A página não usa nenhum: calcula depreciação e energia separadas
5. Valores padrão da calculadora e do exemplo: impressora R$ 4.000, 5.000 h, R$ 0,95/kWh, canal 20% no exemplo
6. Termos de uso, política de privacidade, assinatura Crista Labs (links escondidos no rodapé)
7. Favicon definitivo (símbolo ainda é autotrace)
8. "Sem cartão" nos 6 meses: vinha do desenho de 30 dias
9. Regra para Founder que passar da capacidade do plano de entrada (no vault é recomendação)
10. Importação de G-code: o chip saiu, só 3MF está registrado
11. FAQ fora do ar: preço depois do lote, forma de pagamento, nota fiscal, cancelamento
12. `/espera` no vault ainda diz 30 dias grátis. Precisa mudar para 6 meses junto com o site

## Suposições

- O arquivo base é `~/Downloads/index_1.html` de 28/09 12:51 (confirmado pelo Pedro)
- Gramas e tempos da galeria são de exemplo, não de peças reais
- As taxas de canal são as de referência do vault; a taxa fixa do ML vale para qualquer preço na página (na regra real depende da faixa de preço)

## Antes do primeiro deploy (com o Pedro)

- Hospedagem agora é GitHub Pages, com o domínio da Hostinger apontando para o GitHub. Criar o arquivo `CNAME` com `make3lab.com.br` no repo e o `espera/index.html` no mesmo repo para `/espera` funcionar
- O `.htaccess` de `/app` não funciona no GitHub Pages. `app.make3lab.com.br` é subdomínio e continua apontando para a Hostinger
- Risco registrado: a decisão de 19/09 tirou o **sistema** do GitHub Pages por termo de uso. Página de venda estática costuma ser aceita, mas vale conferir
- 21st.dev CLI instalado, sem login: os componentes foram portados à mão. `npx @21st-dev/cli login` libera a busca no catálogo
