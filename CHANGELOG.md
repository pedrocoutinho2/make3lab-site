---
chapeu: make3lab
status: ativo, Parte A na branch parte-a-tempo-nf-pecas, sem deploy
atualizado: 2026-10-07
tags: [make3lab, site, changelog]
---

# Site make3lab.com.br, v2.1 Parte A (07/10/2026)

Repo: `github.com/pedrocoutinho2/make3lab-site` (privado). `main` tem o commit base de 28/09. A Parte A está na branch `parte-a-tempo-nf-pecas`. Sem merge e sem deploy. Decisões em `50-decisoes/2026-10-07-make3lab-site-motor-019-e-fonte-dos-numeros.md`.

## O que mudou

**Motor da página**
- Espelho do `fn_precificar` (SQL 019), lido no Supabase em 07/10. Mesma ordem de conta, conta inteira arredondada só no fim, preço arredondado para cima até o próximo ,90 (padrão do sistema, decisão do Pedro)
- Entrou a manutenção por hora da máquina (R$ 0,15/h, padrão do sistema). Tarifa padrão passou de R$ 0,95 para R$ 0,881/kWh, como em `fn_params_preco`
- Imposto da nota no denominador, com canal e pagamento: `preço = (custo + lucro + taxa fixa) ÷ (1 − canal − pagamento − imposto)`, igual ao 019
- Taxas somando 90% ou mais: sem preço, com a mensagem "As taxas somam X%. Revise canal, pagamento e imposto."

**Calculadora**
- Campos na ordem: peso, tempo (h e min), filamento, lucro, onde você vende, nota fiscal. Padrão `Sem nota`. `Com nota` abre "Imposto da nota", 4%
- Tempo em dois campos com sufixo. Minuto de 0 a 59, 75 vira 1 h 15 min ao sair do campo. Stepper do minuto de 10 em 10, transbordando para a hora. Stepper da hora de 1 em 1. Erro: "Informe o tempo de impressão, maior que zero."
- Resultado com Preço, Custo, Lucro, Taxas e, com nota, Imposto em linha própria. Conta completa ganhou o campo Manutenção
- Texto da seção: "Cinco números e onde você vende. Sem cadastro."

**Tempo em toda a página**: `3 h 20 min`, `45 min`, `4 h`. Hero, capítulo, galeria e telas do sistema.

**Peças de exemplo**: brinquedo e decoração no lugar das peças técnicas. Vaso espiral (85 g, 3 h 10 min) no hero, no capítulo (`vaso-espiral.3mf`) e no número herói. Galeria com vaso espiral, cachepô facetado, luminária de lua, cobra articulada, pião e porta-velas, no mesmo renderer procedural. Orçamento e produção das telas do sistema também trocados. Pesos e tempos marcados como exemplo.

**Número herói**: R$ 1,34 a menos por peça, 12% do lucro, no vaso espiral com canal de 20%. Os dois jeitos arredondam em ,90.

**Cinco erros**: saíram float e "margem com duas respostas". Novos: nota fiscal fora do preço (cachepô), perda cobrada duas vezes (luminária), refugo no chute (pião), orçamento que muda sozinho (porta-velas), devolução que some do caixa (cobra articulada). Todo valor pelo motor da página.

**Fonte dos números**: Archivo com algarismo tabular, como no sistema (v2.3). A B612 Mono saiu (decisão do Pedro, 07/10).

**Texto corrigido**: "refugo medido" e "vem das suas falhas reais" saíram. O `fn_precificar` lê o refugo de um parâmetro da org (`taxa_refugo`), não do histórico de produção.

## Testes (07/10)

- `tools/lint-marca.js`: zero hex fora dos tokens, zero travessão, zero sombra ou degradê de marca
- `tools/teste.js` (Playwright, 1440 e 390): 50 de 50. Seis casos da calculadora (três sem nota, três com nota) iguais centavo por centavo à conta à mão e ao `fn_precificar` em preço, custo, lucro, taxas e imposto (`tools/casos-calculadora.json`). Tempo (75 min, transbordo, zero), taxas em 89%, 90% e 94%, sem "float", "numeric" ou "ponto flutuante", sem peça técnica antiga, azul por tela (pior: 9,4% no hero a 390), sem rolagem horizontal, zero erro de console, movimento reduzido, sem WebGL
- Playwright agora instalado no repo (`npm install`, `npx playwright install chromium`). Rodar com o site em `http://localhost:8765`: `node tools/teste.js <pasta>`

## Divergências com o fn_precificar

- O 019 recusa o preço com taxas acima de 95%. A página recusa a partir de 90%, por regra de tela
- O canal do 019 aceita taxa por faixa de preço. A página usa uma taxa só por canal (ML com taxa fixa em qualquer preço)
- O refugo do 019 é parâmetro fixo da org, não histórico. As instruções v2.3 dizem que vem do histórico quando houver

## Pendências [CONFIRMAR]

1. **Novo.** 4% de imposto é referência da primeira faixa do Simples Nacional, Anexo I. Peça impressa pode cair no Anexo II. Validar com contador
2. **Novo.** O campo de imposto aceita só percentual inteiro, pelo padrão de campo do vault. Alíquota efetiva do Simples costuma ter casa decimal
3. **Novo.** Refugo do histórico de produção: o sistema não faz. Decidir se entra no 019 ou se a regra da v2.3 muda
4. Perda de 5% no peso digitado (padrão sem fonte)
5. Valores padrão da peça de exemplo: impressora R$ 4.000, 120 W, 5.000 h, canal de 20%
6. Termos de uso, política de privacidade, assinatura Crista Labs (links escondidos no rodapé)
7. Favicon definitivo (símbolo ainda é autotrace)
8. "Sem cartão" nos 6 meses: vinha do desenho de 30 dias
9. Regra para Founder que passar da capacidade do plano de entrada (no vault é recomendação)
10. Importação de G-code: o chip saiu, só 3MF está registrado
11. FAQ fora do ar: preço depois do lote, forma de pagamento, nota fiscal, cancelamento
12. `/espera` no vault ainda diz 30 dias grátis. Precisa mudar para 6 meses junto com o site

**Saíram das pendências** (resolvidas pelo motor 019): motor real da página, refugo multiplicando ou dividindo (o 019 multiplica), custo de hora de máquina R$ 0,67 x R$ 0,85 (o 019 usa depreciação mais manutenção por hora).

**Observação**: `50-decisoes/2026-10-05-make3lab-tempo-hmin-nf-e-pecas-de-exemplo.md` não existe no vault. As regras de tempo, nota e peças vieram do prompt da Parte A.

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

## Pendências [CONFIRMAR] em 28/09 (lista atual no topo)

3. Perda de 5% no peso digitado (padrão sem fonte)
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
