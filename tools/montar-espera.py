#!/usr/bin/env python3
"""Monta espera/index.html a partir do index.html do site (branch parte-a-tempo-nf-pecas).
Mantém: nav, hero, telas, founders (vira founders + formulário), FAQ curto, rodapé.
Tira: capítulo do arquivo, cinco erros, número herói, galeria, calculadora."""
import re, sys

src = open(sys.argv[1], encoding='utf-8').read()
out_path = sys.argv[2]
h = src

def cut(s, a, b, keep_b=True, repl=''):
    i = s.index(a); j = s.index(b, i)
    assert s.count(a) == 1, a
    return s[:i] + repl + (s[j:] if keep_b else s[j+len(b):])

def sub1(s, a, b):
    assert s.count(a) == 1, ('sub1', a[:60], s.count(a))
    return s.replace(a, b)

# ---------- HEAD ----------
h = re.sub(r'<title>.*?</title>', '<title>Make3Lab · Lista de espera e 10 vagas Founders</title>', h, count=1)
h = re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="Gestão de produção para impressão 3D FDM. Entre na lista de espera do Make3Lab e concorra a uma das 10 vagas Founders: 6 meses grátis e depois R$ 19,90 por mês, para sempre.">', h, count=1)
h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Make3Lab · Lista de espera">', h, count=1)
h = re.sub(r'<meta property="og:description" content="[^"]*">',
  '<meta property="og:description" content="A conta da sua impressão 3D, fechada até o centavo. 10 vagas Founders com 6 meses grátis.">', h, count=1)
h = sub1(h, '<meta property="og:url" content="https://make3lab.com.br/">', '<meta property="og:url" content="https://make3lab.com.br/espera">')

# ---------- CSS ----------
h = cut(h, '/* DO ARQUIVO AO PRECO, capítulo preso */', '/* TELAS */')
h = cut(h, '/* GALERIA */', '/* toast */')
h = sub1(h, '.hero{position:relative;height:330vh;', '.hero{position:relative;height:240vh;')
h = sub1(h, '  .hero{height:280vh}', '  .hero{height:220vh}')

FORM_CSS = r'''
/* ESPERA: selo do hero */
.kick{display:inline-flex;align-items:center;gap:10px;align-self:flex-start;margin-bottom:22px;padding:7px 14px 7px 10px;border:1px solid var(--prussia-700);border-radius:99px;background:rgba(12,33,48,.9);font-size:13px;color:var(--nevoa-200);pointer-events:auto;text-decoration:none}
.kick i{width:8px;height:8px;border-radius:50%;background:var(--azul-400)}
.kick .num{color:var(--azul-300)}
@media (max-width:900px){.kick{margin-bottom:14px;font-size:12px}}

/* listrado do refugo (vinha do capítulo do arquivo) */
.hatch{background:repeating-linear-gradient(135deg,var(--aco-400) 0 2px,var(--prussia-950) 2px 5px)!important}
.fm .f>label.ck{display:flex;margin-bottom:0}

/* campo (vindo da calculadora do site) */
.inp{position:relative;display:flex;align-items:center;height:52px;background:var(--prussia-900);border:1px solid var(--prussia-700);border-radius:12px;transition:border-color var(--t-micro),background-color var(--t-micro)}
.inp::after{content:"";position:absolute;left:10px;right:10px;bottom:-1px;height:2px;border-radius:2px;background:var(--azul-400);transform:scaleX(0);transform-origin:0 50%;transition:transform var(--t-ui) var(--ease-out)}
.inp:hover{border-color:var(--aco-600)}
.inp:focus-within{border-color:var(--azul-400);background:var(--prussia-800)}
.inp:focus-within::after{transform:scaleX(1)}
.inp input{flex:1;min-width:0;width:100%;height:100%;background:transparent;border:0;outline:0;color:var(--nevoa-100);font:400 16px/1 var(--f-texto);padding:0 14px}
.inp input::placeholder{color:var(--aco-500)}
.f .err{font-size:13px;color:var(--atencao);margin-top:6px;display:none;line-height:1.4}

/* ESPERA: founders + formulário */
.fnd .fg2{align-items:start}
.fnd .ten{font-size:clamp(150px,18vw,260px)}
.fnd .terms li{grid-template-columns:130px 1fr}
.form-card{position:relative;background:var(--prussia-950);border:1px solid var(--prussia-700);border-radius:18px;padding:clamp(22px,3vw,34px)}
.form-card h3{font-size:clamp(30px,3vw,40px);text-transform:uppercase;line-height:.95}
.form-card .intro{font-size:15px;color:var(--aco-400);margin:12px 0 26px;max-width:46ch}
.fm{display:grid;gap:20px}
.fm .row2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.fm .f{min-width:0}
.fm .f>label,.fm .f>.lb2{display:block;font-size:14px;font-weight:500;color:var(--nevoa-200);margin-bottom:8px}
.fm .f>label small,.fm .f>.lb2 small{font-weight:400;color:var(--aco-500);margin-left:6px}
.fm .inp input,.fm .inp select{text-align:left;font-family:var(--f-texto);font-size:16px;padding:0 14px}
.fm .inp select{flex:1;width:100%;height:100%;background:transparent;border:0;outline:0;color:var(--nevoa-100);appearance:none;-webkit-appearance:none;cursor:pointer}
.fm .inp select option{background:var(--prussia-900);color:var(--nevoa-100)}
.fm .inp .chev{position:absolute;right:14px;top:50%;width:10px;height:10px;margin-top:-7px;border-right:1.5px solid var(--aco-400);border-bottom:1.5px solid var(--aco-400);transform:rotate(45deg);pointer-events:none}
.fm .f .err{color:var(--atencao)}
.fm .f.bad .inp,.fm .f.bad .tags{border-color:var(--atencao)}
.fm .f.bad .err{display:block}
.fm .hide{display:none}

/* campo de etiquetas com sugestão */
.tags{position:relative;display:flex;flex-wrap:wrap;align-items:center;gap:6px;min-height:52px;padding:7px 10px;background:var(--prussia-900);border:1px solid var(--prussia-700);border-radius:12px;cursor:text;transition:border-color var(--t-micro),background-color var(--t-micro)}
.tags:hover{border-color:var(--aco-600)}
.tags:focus-within{border-color:var(--azul-400);background:var(--prussia-800)}
.tags input{flex:1 1 120px;min-width:120px;height:36px;background:transparent;border:0;outline:0;color:var(--nevoa-100);font:400 16px/1 var(--f-texto);padding:0 4px}
.tags input::placeholder{color:var(--aco-500)}
.tag-p{display:inline-flex;align-items:center;gap:4px;height:32px;padding:0 4px 0 11px;border-radius:99px;background:rgba(37,161,239,.12);border:1px solid var(--azul-600);color:var(--azul-100);font-size:14px;white-space:nowrap}
.tag-p button{width:24px;height:24px;border:0;border-radius:50%;background:transparent;color:var(--azul-300);font-size:16px;line-height:1;cursor:pointer;display:grid;place-items:center}
.tag-p button:hover{background:rgba(37,161,239,.2);color:var(--nevoa-100)}
.sug{position:absolute;left:-1px;right:-1px;top:calc(100% + 6px);z-index:20;margin:0;padding:6px;list-style:none;background:var(--prussia-900);border:1px solid var(--prussia-700);border-radius:12px;max-height:248px;overflow:auto}
.sug li{padding:10px 12px;border-radius:8px;font-size:15px;color:var(--nevoa-200);cursor:pointer}
.sug li[aria-selected=true],.sug li:hover{background:var(--prussia-800);color:var(--nevoa-100)}
.sug li.novo{color:var(--azul-300)}
.sug li.novo b{font-weight:600}

/* compromisso e aceite */
.comp{border:1px solid var(--prussia-700);border-radius:14px;padding:16px;background:var(--prussia-900)}
.ck{display:flex;gap:12px;align-items:flex-start;cursor:pointer}
.ck input{flex:none;appearance:none;-webkit-appearance:none;width:22px;height:22px;margin:1px 0 0;border:1.5px solid var(--aco-500);border-radius:6px;background:var(--prussia-950);display:grid;place-items:center;cursor:pointer;transition:background-color var(--t-micro),border-color var(--t-micro)}
.ck input::after{content:"";width:6px;height:11px;border:solid var(--tinta);border-width:0 2px 2px 0;transform:rotate(45deg) translate(-1px,-1px) scale(0);transition:transform var(--t-micro) var(--ease-out)}
.ck input:checked{background:var(--azul-400);border-color:var(--azul-400)}
.ck input:checked::after{transform:rotate(45deg) translate(-1px,-1px) scale(1)}
.ck span{font-size:15px;color:var(--nevoa-200);line-height:1.45}
.ck span b{color:var(--nevoa-100);font-weight:600}
.comp .det{font-size:13.5px;color:var(--aco-400);margin:10px 0 0 34px;line-height:1.5}
.f.bad .ck input{border-color:var(--atencao)}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.fm .btn-p{width:100%;min-height:56px;font-size:17px}
.fm .btn-p[disabled]{opacity:.6;cursor:default}
.fm .msg{font-size:14.5px;color:var(--atencao);line-height:1.45;min-height:1px}
.fm .fine2{font-size:13px;color:var(--aco-500);text-align:center}
.ok-box{display:none}
.ok-box.on{display:block}
.ok-box .big{display:block;font-family:var(--f-titulo);font-weight:800;text-transform:uppercase;font-size:clamp(40px,4vw,56px);line-height:.92;color:var(--nevoa-100)}
.ok-box p{font-size:16px;color:var(--nevoa-200);margin-top:14px;max-width:44ch}
.ok-box ol{list-style:none;margin:26px 0 0;padding:0;border-top:1px solid var(--prussia-700)}
.ok-box li{display:grid;grid-template-columns:44px 1fr;gap:10px;padding:14px 0;border-bottom:1px solid var(--prussia-700);color:var(--nevoa-200);font-size:15px}
.ok-box li .num{color:var(--azul-300)}
.ok-box .wa-row{margin-top:24px}
@media (max-width:900px){.fnd .ten{font-size:clamp(120px,36vw,200px)}}
@media (max-width:620px){.fm .row2{grid-template-columns:1fr}.fnd .terms li{grid-template-columns:1fr}}
'''
h = sub1(h, '/* FAQ */', FORM_CSS + '\n/* FAQ */')

# ---------- HTML ----------
h = sub1(h, '<a class="sr" href="#calculadora">Pular para a calculadora</a>', '<a class="sr" href="#lista">Pular para o formulário</a>')
h = re.sub(r'<ul>\s*<li><a class="lk" href="#arquivo">.*?</ul>',
  '<ul>\n      <li><a class="lk" href="#telas">O sistema</a></li>\n      <li><a class="lk" href="#founders">Founders</a></li>\n      <li><a class="lk" href="#faq">Perguntas</a></li>\n    </ul>', h, count=1, flags=re.S)
h = sub1(h, '<a class="btn btn-p sm mag" href="/espera">Quero uma vaga</a>', '<a class="btn btn-p sm mag" href="#lista">Entrar na lista</a>')

# hero: selo + CTAs apontando para o formulário
h = sub1(h, '<div class="wrap">\n        <h1 class="display">',
  '<div class="wrap">\n        <a class="kick" href="#lista"><i aria-hidden="true"></i>Lista de espera aberta · <span class="num">10</span> vagas Founders</a>\n        <h1 class="display">')
h = sub1(h, '<a class="btn btn-p mag" href="/espera"><span>Quero uma vaga<span class="lg"> Founders</span></span>',
            '<a class="btn btn-p mag" href="#lista"><span>Entrar na lista<span class="lg"> de espera</span></span>')

# tira capítulo, erros, número herói, galeria, calculadora
h = cut(h, '<!-- 2. DO ARQUIVO AO PREÇO -->', '<!-- 5. TELAS DO SISTEMA -->')
h = cut(h, '<!-- 6. GALERIA -->', '<!-- 8. FOUNDERS -->')
h = sub1(h, '<!-- 5. TELAS DO SISTEMA -->', '<!-- 2. TELAS DO SISTEMA -->')

FOUNDERS = r'''<!-- 3. FOUNDERS E FORMULÁRIO -->
<section class="fnd band" id="founders" aria-labelledby="fnd-t">
  <div class="wrap fg2">
    <div>
      <span class="eyebrow">Programa Founders</span>
      <h2 id="fnd-t" class="rv-t"><span class="mask"><span>Entre antes.</span></span><span class="mask"><span>Pague menos. Para sempre.</span></span></h2>
      <p class="lede rv" style="color:var(--nevoa-200)">O Make3Lab nasceu para rodar uma oficina de verdade e agora abre para as primeiras de fora. Quem entra no lote Founders <b>usa de graça por seis meses</b>, fala direto com quem constrói e ajuda a decidir o que vem depois.</p>
      <div class="rv" style="margin-top:34px;display:flex;align-items:flex-end;gap:22px;flex-wrap:wrap">
        <span class="ten num" aria-hidden="true">10</span>
        <span style="padding-bottom:14px"><span class="ten-l" style="margin-top:0">vagas Founders</span><span class="ten-s">Lote único. Vagas confirmadas por contato, não por ordem de chegada.</span></span>
      </div>
      <ul class="terms rv">
        <!-- [CONFIRMAR] "sem cartão" vinha do desenho de 30 dias; confirmar que vale para os 6 meses -->
        <li><span>Grátis</span><span><span class="num">6</span> meses, sem cartão</span></li>
        <li><span>Depois</span><span><span class="num">R$ 19,90</span> por mês, para sempre<small>Enquanto a assinatura estiver ativa, na capacidade do plano de entrada.</small></span></li>
        <li><span>Entrada</span><span>Uma call de <span class="num">30</span> minutos para montar o sistema com as suas máquinas e os seus filamentos</span></li>
        <li><span>Acompanhamento</span><span>Uma conversa de <span class="num">15</span> minutos a cada <span class="num">15</span> dias até o 3º mês, depois uma por mês no 4º e no 5º</span></li>
        <li><span>Para quem</span><span>Quem já imprime e já vende, mesmo que pouco</span></li>
      </ul>
    </div>

    <div class="form-card" id="lista" tabindex="-1">
      <form class="fm" id="fm" novalidate>
        <div>
          <h3>Entrar na lista</h3>
          <p class="intro">Abertura por convite. Quem se encaixa no perfil Founder é chamado no WhatsApp antes de todo mundo.</p>
        </div>

        <div class="f" data-f="nome">
          <label for="nome">Seu nome</label>
          <div class="inp"><input id="nome" name="nome" type="text" autocomplete="name" maxlength="120" required></div>
          <p class="err" id="e-nome">Escreva seu nome para a gente saber com quem fala.</p>
        </div>

        <div class="row2">
          <div class="f" data-f="email">
            <label for="email">E-mail</label>
            <div class="inp"><input id="email" name="email" type="email" inputmode="email" autocomplete="email" maxlength="160" required></div>
            <p class="err" id="e-email">Confira o e-mail. Ele precisa ter @ e domínio, como voce@exemplo.com.</p>
          </div>
          <div class="f" data-f="whatsapp">
            <label for="whatsapp">WhatsApp <small id="wa-opt">obrigatório para Founders</small></label>
            <div class="inp"><input id="whatsapp" name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" placeholder="(21) 90000-0000" maxlength="16"></div>
            <p class="err" id="e-whatsapp">Informe o WhatsApp com DDD. É por ele que chamamos quem entra nas vagas.</p>
          </div>
        </div>

        <div class="row2">
          <div class="f" data-f="qtd">
            <label for="qtd">Impressoras hoje</label>
            <div class="inp"><select id="qtd" name="qtd_impressoras">
              <option value="">Selecione</option>
              <option value="0">Ainda não tenho</option>
              <option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option>
              <option value="5+">5 ou mais</option>
            </select><i class="chev" aria-hidden="true"></i></div>
          </div>
          <div class="f" data-f="precifica">
            <label for="precifica">Como chega no preço</label>
            <div class="inp"><select id="precifica" name="precifica_hoje">
              <option value="">Selecione</option>
              <option value="chute">No olho, comparando com o mercado</option>
              <option value="planilha">Planilha própria</option>
              <option value="sistema">Outro sistema</option>
              <option value="nao_vendo">Ainda não vendo</option>
            </select><i class="chev" aria-hidden="true"></i></div>
          </div>
        </div>

        <div class="f hide" data-f="qual" id="qualWrap">
          <label for="qual">Qual sistema?</label>
          <div class="inp"><input id="qual" type="text" maxlength="80"></div>
        </div>

        <div class="f" data-f="marcas">
          <span class="lb2" id="l-marcas">Marcas das suas impressoras <small>escolha ou digite</small></span>
          <div class="tags" data-tags="marcas" data-max="10"></div>
        </div>

        <div class="f" data-f="vende">
          <span class="lb2" id="l-vende">Onde você vende hoje <small>escolha ou digite</small></span>
          <div class="tags" data-tags="vende" data-max="10"></div>
        </div>

        <div class="comp">
          <label class="ck"><input id="founder" type="checkbox" checked><span><b>Quero concorrer a uma das 10 vagas Founders</b></span></label>
          <p class="det">Ao marcar, você topa uma call de 30 minutos na entrada, uma conversa de 15 minutos a cada 15 dias nos 3 primeiros meses e uma por mês no 4º e no 5º. Em troca, 6 meses grátis e depois R$ 19,90 por mês para sempre.</p>
        </div>

        <div class="f" data-f="consent">
          <label class="ck"><input id="consent" type="checkbox"><span>Autorizo o contato por e-mail e WhatsApp sobre a abertura do Make3Lab e o programa Founders, conforme a <a class="lk" href="/privacidade" target="_blank" rel="noopener">política de privacidade</a>. Posso pedir a exclusão dos meus dados quando quiser.</span></label>
          <p class="err" id="e-consent" style="margin-left:34px">Marque a autorização para a gente poder te chamar.</p>
        </div>

        <div class="hp" aria-hidden="true"><label for="empresa_site">Deixe em branco</label><input id="empresa_site" type="text" tabindex="-1" autocomplete="off"></div>

        <button class="btn btn-p" type="submit" id="enviar"><span>Entrar na lista</span> <svg class="ar" aria-hidden="true"><use href="#i-ar"/></svg></button>
        <p class="msg" id="msg" role="alert"></p>
        <p class="fine2">Sem spam e sem lista vendida. Seus dados servem só para falar sobre a abertura.</p>
      </form>

      <div class="ok-box" id="ok" role="status" aria-live="polite">
        <span class="big">Você está<br>na lista.</span>
        <p id="okTxt">Seu cadastro entrou. Quem se encaixa no perfil Founder recebe uma mensagem no WhatsApp antes da abertura.</p>
        <ol>
          <li><span class="num">01</span><span>A gente lê cada cadastro, um por um</span></li>
          <li><span class="num">02</span><span>Quem se encaixa é chamado no WhatsApp para a call de entrada</span></li>
          <li><span class="num">03</span><span>Sistema montado com as suas máquinas e <span class="num">6</span> meses grátis</span></li>
        </ol>
        <div class="wa-row"><a class="btn btn-s" href="https://wa.me/5521995215332?text=Oi%2C%20acabei%20de%20entrar%20na%20lista%20do%20Make3Lab" target="_blank" rel="noopener"><svg class="wa" aria-hidden="true"><use href="#i-wa"/></svg> Mandar um oi no WhatsApp</a></div>
      </div>
    </div>
  </div>
</section>

'''
i = h.index('<!-- 8. FOUNDERS -->'); j = h.index('<!-- 9. FAQ')
h = h[:i] + FOUNDERS + h[j:]

# FAQ: tira a da calculadora (ela não está nesta página), troca "nesta página"
h = re.sub(r'\s*<details><summary>A calculadora é paga ou pede cadastro\?.*?</details>', '', h, count=1, flags=re.S)
h = sub1(h, '<!-- 9. FAQ: só perguntas com resposta confirmada no vault -->', '<!-- 4. FAQ: só perguntas com resposta confirmada no vault -->')
h = sub1(h, '<span class="mask"><span>pedir a vaga.</span></span>', '<span class="mask"><span>entrar na lista.</span></span>')

# rodapé: política de privacidade visível; termos e Crista Labs seguem escondidos
h = sub1(h, '<span hidden><a href="/termos">Termos de uso</a> · <a href="/privacidade">Privacidade</a> · Um produto Crista Labs</span>',
            '<span><a href="/privacidade">Política de privacidade</a></span>\n      <span hidden><a href="/termos">Termos de uso</a> · Um produto Crista Labs</span>')
h = sub1(h, '<span>Todos os dados desta página são de exemplo.</span>', '<span>Telas e peças desta página usam dados de exemplo.</span>')

# barra de preço da calculadora
h = re.sub(r'<div class="pbar" id="pbar"[^\n]*\n', '', h, count=1)
assert '<div class="pbar"' not in h

# ---------- JS ----------
h = sub1(h, "['arquivo','erros','calculadora','founders'].forEach", "['telas','founders','faq'].forEach")
h = cut(h, '/* ============ DO ARQUIVO AO PREÇO ============ */', '/* orçamento de exemplo das telas: preço unitário pelo motor, venda direta */')
h = cut(h, '/* ============ GALERIA: um renderer, recortado por card ============ */', '/* pílulas depois das fontes */')

FORM_JS = r'''/* ============ LISTA DE ESPERA ============ */
var ENDPOINT = 'https://lvnavmtyselveozllcuy.supabase.co/functions/v1/lead-espera';
var T0 = Date.now(), PRM = new URLSearchParams(location.search);
var fm = $('#fm'), btnEnviar = $('#enviar'), msg = $('#msg');
var SUG = {
  marcas: ['Bambu Lab','Creality','Elegoo','Prusa','Anycubic','Flashforge','Sovol','Qidi','Artillery','Snapmaker','Anker','Voron','3D Cloner','GTMax3D'],
  vende: ['Shopee','Mercado Livre','Instagram','WhatsApp','Elo7','TikTok Shop','Amazon','Site próprio','Encomenda direta','Feira','Loja física','Ainda não vendo']
};
var TAGS = {};
function norm(s){ return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().trim() }
function esc(s){ return s.replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c] }) }

$$('[data-tags]').forEach(function(box){
  var key = box.dataset.tags, max = +box.dataset.max || 10, vals = [], act = -1, opts = [];
  var lid = 'sug-' + key, lbl = $('#l-' + key);
  box.innerHTML = '<input type="text" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="' + lid + '" aria-labelledby="l-' + key + '" placeholder="' + (key === 'marcas' ? 'Bambu Lab, Creality...' : 'Shopee, Instagram...') + '" maxlength="60" autocomplete="off"><ul class="sug" id="' + lid + '" role="listbox" hidden></ul>';
  var inp = $('input', box), ul = $('ul', box);
  function render(){
    $$('.tag-p', box).forEach(function(t){ t.remove() });
    vals.forEach(function(v, i){
      var t = D.createElement('span'); t.className = 'tag-p';
      t.innerHTML = esc(v) + '<button type="button" aria-label="Tirar ' + esc(v) + '">×</button>';
      $('button', t).addEventListener('click', function(e){ e.stopPropagation(); vals.splice(i,1); render(); inp.focus() });
      box.insertBefore(t, inp);
    });
    inp.placeholder = vals.length ? '' : (key === 'marcas' ? 'Bambu Lab, Creality...' : 'Shopee, Instagram...');
  }
  function add(v){
    v = v.trim().replace(/\s+/g,' ').slice(0,60); if (!v) return;
    if (vals.length >= max || vals.some(function(x){ return norm(x) === norm(v) })){ inp.value = ''; close(); return }
    var canon = SUG[key].filter(function(s){ return norm(s) === norm(v) })[0];
    vals.push(canon || v); render(); inp.value = ''; close();
  }
  function close(){ ul.hidden = true; inp.setAttribute('aria-expanded','false'); inp.removeAttribute('aria-activedescendant'); act = -1 }
  function open(){
    var q = norm(inp.value);
    opts = SUG[key].filter(function(s){ return vals.indexOf(s) < 0 && (!q || norm(s).indexOf(q) >= 0) });
    var exact = SUG[key].some(function(s){ return norm(s) === q }) || vals.some(function(s){ return norm(s) === q });
    if (q && !exact) opts.push({novo: inp.value.trim()});
    if (!opts.length){ close(); return }
    ul.innerHTML = opts.map(function(o, i){
      return '<li role="option" id="' + lid + '-' + i + '" aria-selected="false"' + (o.novo ? ' class="novo">Adicionar <b>' + esc(o.novo) + '</b>' : '>' + esc(o)) + '</li>';
    }).join('');
    $$('li', ul).forEach(function(li, i){ li.addEventListener('mousedown', function(e){ e.preventDefault(); pick(i) }) });
    ul.hidden = false; inp.setAttribute('aria-expanded','true'); act = -1;
  }
  function pick(i){ var o = opts[i]; add(o.novo ? o.novo : o); inp.focus(); open() }
  function move(d){
    if (ul.hidden) open(); if (!opts.length) return;
    act = (act + d + opts.length) % opts.length;
    $$('li', ul).forEach(function(li, i){ li.setAttribute('aria-selected', i === act) });
    var li = $('#' + lid + '-' + act); inp.setAttribute('aria-activedescendant', li.id); li.scrollIntoView({block:'nearest'});
  }
  inp.addEventListener('input', open);
  inp.addEventListener('focus', open);
  inp.addEventListener('blur', function(){ if (inp.value.trim()) add(inp.value); close() });
  inp.addEventListener('keydown', function(e){
    if (e.key === 'ArrowDown'){ move(1); e.preventDefault() }
    else if (e.key === 'ArrowUp'){ move(-1); e.preventDefault() }
    else if (e.key === 'Enter' || e.key === ','){
      if (act >= 0 && !ul.hidden) pick(act);
      else if (inp.value.trim()){ open(); if (opts.length && !opts[0].novo) pick(0); else add(inp.value) }
      else return;
      e.preventDefault()
    }
    else if (e.key === 'Escape'){ close() }
    else if (e.key === 'Backspace' && !inp.value && vals.length){ vals.pop(); render() }
  });
  box.addEventListener('click', function(e){ if (e.target === box) inp.focus() });
  TAGS[key] = function(){ if (inp.value.trim()) add(inp.value); return vals.slice() };
});

/* WhatsApp: máscara (21) 99999-9999 */
var wa = $('#whatsapp');
function waDig(){ return wa.value.replace(/\D/g,'').replace(/^55(?=\d{10,11}$)/,'') }
wa.addEventListener('input', function(){
  var d = wa.value.replace(/\D/g,'').slice(0,11), r = d;
  if (d.length > 2) r = '(' + d.slice(0,2) + ') ' + d.slice(2);
  if (d.length > 6) r = '(' + d.slice(0,2) + ') ' + d.slice(2, d.length === 11 ? 7 : 6) + '-' + d.slice(d.length === 11 ? 7 : 6);
  wa.value = r;
});
var founder = $('#founder'), waOpt = $('#wa-opt');
function syncFounder(){ waOpt.textContent = founder.checked ? 'obrigatório para Founders' : 'opcional' }
founder.addEventListener('change', function(){ syncFounder(); if (!founder.checked) bad('whatsapp', false) });
syncFounder();

var prec = $('#precifica');
prec.addEventListener('change', function(){ $('#qualWrap').classList.toggle('hide', prec.value !== 'sistema') });

function bad(k, on){
  var f = $('[data-f="' + k + '"]'); f.classList.toggle('bad', on);
  var el = $('input', f); if (el) { if (on) { el.setAttribute('aria-invalid','true'); el.setAttribute('aria-describedby','e-' + k) } else { el.removeAttribute('aria-invalid'); el.removeAttribute('aria-describedby') } }
}
var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
function check(k){
  if (k === 'nome') return $('#nome').value.trim().length >= 2;
  if (k === 'email') return EMAIL_RE.test($('#email').value.trim());
  if (k === 'whatsapp'){ var n = waDig().length; return founder.checked ? (n === 10 || n === 11) : (n === 0 || n === 10 || n === 11) }
  if (k === 'consent') return $('#consent').checked;
  return true;
}
['nome','email','whatsapp'].forEach(function(k){
  var el = $('#' + k);
  el.addEventListener('blur', function(){ if (el.value.trim()) bad(k, !check(k)) });
  el.addEventListener('input', function(){ if ($('[data-f="' + k + '"]').classList.contains('bad')){ bad(k, !check(k)); clearMsg() } });
});
function clearMsg(){ if (!$('.fm .f.bad')) msg.textContent = '' }
$('#consent').addEventListener('change', function(){ bad('consent', !check('consent')); clearMsg() });

fm.addEventListener('submit', function(e){
  e.preventDefault();
  msg.textContent = '';
  var first = null;
  ['nome','email','whatsapp','consent'].forEach(function(k){ var ok = check(k); bad(k, !ok); if (!ok && !first) first = k });
  if (first){ var el = $('#' + first); el.focus(); msg.textContent = 'Falta ajustar o campo marcado em amarelo.'; return }

  var dados = {
    nome: $('#nome').value.trim(),
    email: $('#email').value.trim(),
    whatsapp: wa.value.trim() || null,
    qtd_impressoras: $('#qtd').value || null,
    marcas: TAGS.marcas(),
    vende_onde: TAGS.vende(),
    precifica_hoje: prec.value || null,
    precifica_qual: prec.value === 'sistema' ? ($('#qual').value.trim() || null) : null,
    quer_founder: founder.checked,
    consentimento: true,
    empresa_site: $('#empresa_site').value,
    decorrido_ms: Date.now() - T0,
    utm_source: PRM.get('utm_source'),
    utm_medium: PRM.get('utm_medium'),
    utm_campaign: PRM.get('utm_campaign'),
    referrer: D.referrer || null
  };

  btnEnviar.disabled = true; btnEnviar.firstChild.textContent = 'Enviando';
  fetch(ENDPOINT, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(dados)})
    .then(function(r){ return r.json().catch(function(){ return {} }).then(function(c){ return {ok:r.ok, c:c} }) })
    .then(function(x){
      if (!x.ok) throw new Error(x.c.mensagem || 'Não deu para enviar agora. Tente de novo em instantes.');
      if (!founder.checked) $('#okTxt').textContent = 'Seu cadastro entrou. Você recebe o convite por e-mail quando as contas abrirem.';
      fm.hidden = true; $('#ok').classList.add('on');
      var card = $('#lista'); card.focus({preventScroll:true}); card.scrollIntoView({block:'start', behavior: RM ? 'auto' : 'smooth'});
      if (W.dataLayer) W.dataLayer.push({event:'lead_espera', founder: dados.quer_founder});
    })
    .catch(function(err){
      msg.textContent = (err && err.message && !/fetch|network/i.test(err.message)) ? err.message : 'Sem conexão com o servidor. Confira a internet e tente de novo.';
      btnEnviar.disabled = false; btnEnviar.firstChild.textContent = 'Entrar na lista';
    });
});

'''
h = sub1(h, '/* pílulas depois das fontes */', FORM_JS + '/* pílulas depois das fontes */')

open(out_path, 'w', encoding='utf-8').write(h)
print('ok', len(h))
