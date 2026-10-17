#!/usr/bin/env python3
"""Segunda etapa da /espera (10/10/2026): comentários do Pedro.
Telas atualizadas com o app publicado em 09/10, sem botão de zoom, título novo da seção de telas,
textos do Founders, rótulos do formulário, FAQ, seletor Malha/Camadas/Sólido sem sobrepor o ticket
no celular e rolagem do hero mais fluida no celular."""
import re, sys
p_in, p_out = sys.argv[1], sys.argv[2]
h = open(p_in, encoding='utf-8').read()

def sub1(s, a, b):
    n = s.count(a); assert n == 1, ('sub1', n, a[:80]); return s.replace(a, b)
def between(s, a, b, repl, keep_b=True):
    i = s.index(a); j = s.index(b, i); assert s.count(a) == 1, a[:60]
    return s[:i] + repl + (s[j:] if keep_b else s[j+len(b):])

# ================= TELAS: cabeçalho e abas =================
h = sub1(h, '<span class="mask"><span>Da bobina</span></span><span class="mask"><span>ao extrato.</span></span>',
            '<span class="mask"><span>Sem planilha.</span></span><span class="mask"><span>Sem chute.</span></span>')
h = sub1(h, '<p class="lede rv">Orçamento, produção, estoque e financeiro usam o mesmo custo. <b>O número que nasce no orçamento é o mesmo que chega no caixa.</b> Roda no navegador, no celular e no computador.</p>',
            '<p class="lede rv">Orçamento, funil de vendas, produção e financeiro no mesmo lugar, usando o mesmo custo. <b>O preço que você passa no orçamento é o lucro que aparece no caixa.</b> Roda no navegador, no celular e no computador.</p>')
TABS = '''<button role="tab" aria-selected="true" aria-controls="app" data-v="orc">Orçamento<i class="tp"></i></button>
        <button role="tab" aria-selected="false" aria-controls="app" data-v="funil" tabindex="-1">Funil de vendas<i class="tp"></i></button>
        <button role="tab" aria-selected="false" aria-controls="app" data-v="prod" tabindex="-1">Produção<i class="tp"></i></button>
        <button role="tab" aria-selected="false" aria-controls="app" data-v="fin" tabindex="-1">Financeiro<i class="tp"></i></button>'''
h = re.sub(r'<button role="tab" aria-selected="true" aria-controls="app" data-v="orc">.*?data-v="fin" tabindex="-1">Financeiro<i class="tp"></i></button>', TABS, h, count=1, flags=re.S)

# ================= TELAS: app novo =================
def ic(d): return '<svg viewBox="0 0 16 16">' + d + '</svg>'
I = {
 'casa': ic('<path d="M2.5 7.5 8 3l5.5 4.5V13h-11z"/><path d="M6.5 13V9.5h3V13"/>'),
 'cubo': ic('<path d="M8 2l5 3v6l-5 3-5-3V5z"/><path d="M3 5l5 3 5-3M8 8v6"/>'),
 'kit': ic('<rect x="2.5" y="5" width="11" height="8" rx="1"/><path d="M6 5V3.5h4V5M2.5 8.5h11"/>'),
 'users': ic('<circle cx="6" cy="6" r="2.3"/><path d="M2 13c.5-2.3 2-3.4 4-3.4s3.5 1.1 4 3.4"/><path d="M10.5 4a2 2 0 0 1 0 4M12 9.8c1 .5 1.7 1.6 2 3.2"/>'),
 'bobina': ic('<circle cx="8" cy="8" r="5.5"/><circle cx="8" cy="8" r="1.8"/>'),
 'caixa': ic('<path d="M2.5 5.5 8 3l5.5 2.5v6L8 14l-5.5-2.5z"/><path d="M2.5 5.5 8 8l5.5-2.5M8 8v6"/>'),
 'funil': ic('<path d="M2.5 3h11l-4.2 5v4.5l-2.6 1V8z"/>'),
 'calc': ic('<rect x="3.5" y="2" width="9" height="12" rx="1.2"/><path d="M5.5 4.5h5M5.5 8h.01M8 8h.01M10.5 8h.01M5.5 10.8h.01M8 10.8h.01M10.5 10.8h.01"/>'),
 'doc': ic('<path d="M4 2h6l3 3v9H4z"/><path d="M6 8h5M6 11h3"/>'),
 'tag': ic('<path d="M2.5 2.5h5.2l5.8 5.8-5.2 5.2-5.8-5.8z"/><circle cx="5.3" cy="5.3" r=".9"/>'),
 'loja': ic('<path d="M2.5 6 3.5 2.5h9L13.5 6"/><path d="M2.5 6h11v1a2 2 0 0 1-3.7 1 2 2 0 0 1-3.6 0A2 2 0 0 1 2.5 7z"/><path d="M3.5 9v4.5h9V9"/>'),
 'fila': ic('<rect x="2" y="3" width="12" height="9" rx="1"/><path d="M5 14h6M5 6.5h6M5 9h4"/>'),
 'caminhao': ic('<path d="M1.5 4h8v7h-8zM9.5 6.5h3l2 2.5V11h-5"/><circle cx="4.5" cy="12" r="1.3"/><circle cx="11.5" cy="12" r="1.3"/>'),
 'cal': ic('<rect x="2.5" y="3.5" width="11" height="10" rx="1.2"/><path d="M2.5 6.5h11M5.5 2v3M10.5 2v3"/>'),
 'grana': ic('<path d="M2 12l4-4 3 2 5-6"/><path d="M10 4h4v4"/>'),
 'graf': ic('<path d="M2.5 13.5h11M4.5 11V7.5M8 11V4.5M11.5 11V9"/>'),
 'eng': ic('<circle cx="8" cy="8" r="2"/><path d="M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2M3.4 3.4l1.4 1.4M11.2 11.2l1.4 1.4M3.4 12.6l1.4-1.4M11.2 4.8l1.4-1.4"/>'),
}
MENU = [('Início','casa',None), ('|Cadastros',), ('Produtos','cubo',None), ('Kits','kit',None), ('Clientes','users',None), ('Filamentos','bobina',None), ('Insumos','caixa',None),
        ('|Comercial',), ('Funil de vendas','funil','funil'), ('Simulador','calc',None), ('Orçamentos','doc','orc'), ('Vendas','tag',None), ('Consignação','loja',None),
        ('|Operação',), ('Fila de produção','fila','prod'), ('Entregas','caminhao',None), ('Calendário','cal',None),
        ('|Gestão',), ('Financeiro','grana','fin'), ('Relatórios','graf',None), ('|Sistema',), ('Configurações','eng',None)]
side = []
for m in MENU:
    if m[0].startswith('|'): side.append('<div class="grp">' + m[0][1:] + '</div>')
    else: side.append('<div class="it"' + (' data-n="' + m[2] + '"' if m[2] else '') + '>' + I[m[1]] + m[0] + '</div>')

APP = '''<div class="app" id="app" role="tabpanel" aria-label="Tela de exemplo do sistema">
            <aside>
              <div class="brand"><svg viewBox="0 0 723 114" fill="currentColor" aria-hidden="true"><use href="#wmp"/></svg></div>
              ''' + '\n              '.join(side) + '''
              <div class="who"><i>AE</i>Ateliê Exemplo</div>
            </aside>
            <main>
              <div class="top"><h4 id="appT">Orçamento ORC-0321</h4><div class="acts"><span class="b s" id="appS">Duplicar</span><span class="b p" id="appP">Enviar ao cliente</span></div></div>

              <div class="view on" data-v="orc">
                <div class="orc">
                  <div class="l">
                    <div class="card fields">
                      <div class="fld"><div class="lb">Cliente</div><div class="ip">Cliente de exemplo <em>loja de presentes</em></div></div>
                      <div class="fld"><div class="lb">Prazo de produção</div><div class="ip"><span class="mono">7</span><em>dias úteis</em></div></div>
                      <div class="fld"><div class="lb">Canal</div><div class="ip">Venda direta <em>0%</em></div></div>
                    </div>
                    <div class="card">
                      <div class="ch"><b>Produtos</b><span>o que o cliente recebe</span></div>
                      <table class="t">
                        <thead><tr><th>Produto</th><th class="r">Qtd</th><th class="r">Custo un.</th><th class="r">Preço un.</th><th class="r">Total</th></tr></thead>
                        <tbody id="orcRows"></tbody>
                      </table>
                    </div>
                    <div class="card">
                      <div class="ch"><b>Insumos</b><span>o que vai junto com a peça</span></div>
                      <table class="t">
                        <thead><tr><th>Insumo</th><th class="r">Qtd</th><th>Cobrança</th><th class="r">Custo un.</th><th class="r">Total</th></tr></thead>
                        <tbody id="insRows"></tbody>
                      </table>
                    </div>
                  </div>
                  <div class="card comp" id="compCard">
                    <div class="k">Total do orçamento</div>
                    <span class="big num" id="orcTot">R$ 0,00</span>
                    <div class="bar">
                      <i data-o="material" style="background:var(--azul-400)"></i><i data-o="energia" style="background:var(--azul-300)"></i><i data-o="maquina" style="background:var(--azul-600)"></i><i data-o="mao" style="background:var(--aco-400)"></i><i data-o="insumos" style="background:var(--aco-600)"></i><i data-o="refugo" class="hatch"></i><i data-o="lucro" style="background:var(--azul-100)"></i>
                    </div>
                    <div class="legend">
                      <div><b style="background:var(--azul-400)"></b>Filamento<span class="num" data-l="material"></span></div>
                      <div><b style="background:var(--azul-300)"></b>Energia<span class="num" data-l="energia"></span></div>
                      <div><b style="background:var(--azul-600)"></b>Máquina<span class="num" data-l="maquina"></span></div>
                      <div><b style="background:var(--aco-400)"></b>Mão de obra<span class="num" data-l="mao"></span></div>
                      <div><b style="background:var(--aco-600)"></b>Insumos<span class="num" data-l="insumos"></span></div>
                      <div><b class="hatch"></b><span>Refugo <small class="mono">5%</small></span><span class="num" data-l="refugo"></span></div>
                      <div><b style="background:var(--azul-100)"></b>Lucro<span class="num" data-l="lucro"></span></div>
                    </div>
                    <div class="sinal">
                      <div class="sr2"><span>Sinal para validar</span><span class="num" id="orcSinal"></span></div>
                      <div class="sr2 m"><span>Saldo na entrega</span><span class="num" id="orcSaldo"></span></div>
                      <div class="pg"><span class="pp">Pix</span><span class="pp">Cartão em até 3x</span></div>
                    </div>
                    <div class="snapb" id="snapb"><svg width="13" height="13" aria-hidden="true"><use href="#i-lock"/></svg>custo congelado em 09/10 10:14 · filamento a R$ 120,00/kg</div>
                  </div>
                </div>
              </div>

              <div class="view" data-v="funil">
                <div class="kpis k3">
                  <div class="card kpi"><div class="k">Em negociação</div><span class="num in">R$ 3.418,60</span><div class="s">7 cards</div></div>
                  <div class="card kpi"><div class="k">Fechado no mês</div><span class="num">R$ 6.842,30</span><div class="s">41 vendas</div></div>
                  <div class="card kpi"><div class="k">Conversão</div><span class="num">38%</span><div class="s">orçamentos que viraram venda</div></div>
                </div>
                <div class="kan fun">
                  <div class="col"><div class="ch2"><span>Contato</span><span class="num">2</span></div>
                    <div class="job"><div class="n">Loja de presentes</div><div class="m"><span>Chaveiros ×100</span><span>R$ 890,00</span></div></div>
                    <div class="job"><div class="n">Buffet infantil</div><div class="m"><span>Lembrancinhas</span><span>a orçar</span></div></div>
                  </div>
                  <div class="col"><div class="ch2"><span>Orçamento enviado</span><span class="num">3</span></div>
                    <div class="job"><div class="n">Cliente de exemplo</div><div class="m"><span>ORC-0321</span><span id="funOrc">R$ 0,00</span></div></div>
                    <div class="job"><div class="n">Escola de música</div><div class="m"><span>ORC-0319</span><span>R$ 412,00</span></div></div>
                    <div class="job"><div class="n">Café do bairro</div><div class="m"><span>ORC-0316</span><span class="tag er">vencido</span></div></div>
                  </div>
                  <div class="col"><div class="ch2"><span>Negociação</span><span class="num">2</span></div>
                    <div class="job"><div class="n">Casamento, 120 convidados</div><div class="m"><span>ORC-0318</span><span>R$ 1.140,00</span></div></div>
                    <div class="job"><div class="n">Pet shop</div><div class="m"><span>ORC-0314</span><span>R$ 286,60</span></div></div>
                  </div>
                  <div class="col win"><div class="ch2"><span>Fechado</span><span class="num">2</span></div>
                    <div class="job"><div class="n">Ateliê vizinho</div><div class="m"><span>VD-0151</span><span class="tag ok">sinal pago</span></div></div>
                    <div class="job"><div class="n">Loja de decoração</div><div class="m"><span>VD-0150</span><span class="tag ok">paga</span></div></div>
                  </div>
                </div>
                <p class="hint2">Mover para Fechado cria a venda, o a receber e as ordens na fila de produção.</p>
              </div>

              <div class="view" data-v="prod">
                <div class="kpis">
                  <div class="card kpi"><div class="k">Ordens abertas</div><span class="num">9</span><div class="s">de 6 vendas</div></div>
                  <div class="card kpi"><div class="k">Máquina na fila</div><span class="num">41 h 20 min</span><div class="s">só o que ainda vai imprimir</div></div>
                  <div class="card kpi"><div class="k">Atrasadas</div><span class="num" style="color:var(--erro)">1</span><div class="s">passaram da data de entrega</div></div>
                  <div class="card kpi"><div class="k">Prontas</div><span class="num">3</span><div class="s">esperando envio</div></div>
                </div>
                <div class="kan">
                  <div class="col"><div class="ch2"><span>A imprimir</span><span class="num">3</span></div>
                    <div class="job"><div class="n">Chaveiro com nome ×50</div><div class="m"><span>VD-0151</span><span class="tag at">aguardando arte</span></div></div>
                    <div class="job"><div class="n">Pião ×30</div><div class="m"><span>VD-0150</span><span>25 h</span></div></div>
                    <div class="job"><div class="n">Placa com logo ×4</div><div class="m"><span>VD-0149</span><span>19 h</span></div></div>
                  </div>
                  <div class="col"><div class="ch2"><span>Imprimindo</span><span class="num">2</span></div>
                    <div class="job live"><div class="n">Vaso espiral ×12</div><div class="m"><span>A1 · 01</span><span>lote 7/12</span></div><div class="pb"><i style="--w:.58"></i></div></div>
                    <div class="job live"><div class="n">Cachepô facetado ×2</div><div class="m"><span>A1 · 02</span><span>1 h 12 min</span></div><div class="pb"><i style="--w:.71"></i></div></div>
                  </div>
                  <div class="col"><div class="ch2"><span>Pós-processo</span><span class="num">2</span></div>
                    <div class="job"><div class="n">Luminária de lua</div><div class="m"><span>VD-0147</span><span class="tag at">prazo amanhã</span></div></div>
                    <div class="job"><div class="n">Cobra articulada ×1</div><div class="m"><span>VD-0146</span><span class="tag er">reimpressão</span></div></div>
                  </div>
                  <div class="col"><div class="ch2"><span>Pronto</span><span class="num">3</span></div>
                    <div class="job"><div class="n">Porta-velas ×3</div><div class="m"><span>CS-0012</span><span>consignado</span></div></div>
                    <div class="job"><div class="n">Cachepô facetado ×8</div><div class="m"><span>VD-0145</span><span class="tag ok">pronta para entrega</span></div></div>
                    <div class="job"><div class="n">Pião ×2</div><div class="m"><span>VD-0144</span><span class="tag ok">pronta para entrega</span></div></div>
                  </div>
                </div>
              </div>

              <div class="view" data-v="fin">
                <div class="subtabs"><span class="on">Dashboard</span><span>Entrada</span><span>Saída</span><span>Previsão</span></div>
                <div class="kpis">
                  <div class="card kpi"><div class="k">A receber</div><span class="num in">R$ 1.284,50</span><div class="s">6 em aberto</div></div>
                  <div class="card kpi"><div class="k">A pagar</div><span class="num">R$ 642,00</span><div class="s">custos fixos e variáveis</div></div>
                  <div class="card kpi"><div class="k">Resultado de outubro</div><span class="num">R$ 3.924,75</span><div class="s">já com estornos</div></div>
                  <div class="card kpi"><div class="k">Atrasados</div><span class="num" style="color:var(--erro)">R$ 210,00</span><div class="s">1 acerto de consignado</div></div>
                </div>
                <div class="fin">
                  <div class="card chart"><div class="k">Saldo projetado <span>por semana, a partir do que está em aberto</span></div>
                    <div class="bars"><div><i style="--h:42%"></i><span>13/10</span></div><div><i style="--h:55%"></i><span>20/10</span></div><div><i style="--h:49%"></i><span>27/10</span></div><div><i style="--h:63%"></i><span>03/11</span></div><div><i style="--h:71%"></i><span>10/11</span></div><div><i style="--h:84%"></i><span>17/11</span></div></div>
                  </div>
                  <div class="card">
                    <table class="t">
                      <thead><tr><th>Data</th><th>Lançamento</th><th class="r">Valor</th></tr></thead>
                      <tbody>
                        <tr><td class="num">09/10</td><td>Sinal VD-0151 · 50% <span class="tag ok">recebido</span></td><td class="r num v-in">R$ 451,50</td></tr>
                        <tr><td class="num">16/10</td><td>Saldo VD-0151 · na entrega <span class="tag">a receber</span></td><td class="r num">R$ 451,50</td></tr>
                        <tr><td class="num">08/10</td><td>Estorno VD-0139 · devolução</td><td class="r num v-er">− R$ 180,00</td></tr>
                        <tr><td class="num">07/10</td><td>Compra de PETG · 3 kg <span class="tag">variável</span></td><td class="r num">− R$ 297,00</td></tr>
                        <tr><td class="num">05/10</td><td>Energia elétrica <span class="tag">fixo</span></td><td class="r num">− R$ 184,00</td></tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </main>
          </div>'''
h = between(h, '<div class="app" id="app" role="tabpanel"', '\n        </div></div></div>', APP)

# zoom fora
h = re.sub(r'\s*<div class="zoom-row">.*?</div>\n', '\n', h, count=1, flags=re.S)
assert 'zoomBtn' in h  # ainda no JS, sai abaixo
MODS = '''<div class="mods rv" aria-label="Módulos do sistema">
      <span>Produtos e kits</span><span>Clientes</span><span>Filamentos</span><span>Insumos</span><span>Funil de vendas</span><span>Simulador</span><span>Orçamentos</span><span>Vendas</span><span>Consignação</span><span>Fila de produção</span><span>Entregas</span><span>Calendário</span><span>Financeiro</span><span>Relatórios e metas</span><span>Personalização com aprovação de arte</span><span>Sinal e pagamento parcial</span><span>Importação de 3MF e G-code</span><span>Preço por canal</span><span>Usuários por convite</span>
      <span class="soon">Integração direta com marketplace, depois</span><span class="soon">Emissão fiscal, depois</span>
    </div>'''
h = re.sub(r'<div class="mods rv" aria-label="Módulos do sistema">.*?</div>', MODS, h, count=1, flags=re.S)

# ================= TELAS: CSS =================
APP_CSS = r'''
/* app: menu real com grupos, mais compacto */
.app aside{padding:14px 10px;gap:0;overflow:hidden}
.app aside .brand{padding:2px 8px 10px}
.app aside .grp{font-size:9.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--aco-500);padding:9px 10px 3px}
.app aside .it{padding:4.5px 10px;font-size:12px;gap:9px}
.app aside .it svg{width:14px;height:14px}
.app aside .who{padding:8px 10px 0}
.orc .l{gap:10px}
.card .ch{display:flex;align-items:baseline;gap:8px;padding:10px 12px 0}
.card .ch b{font-size:12.5px;color:var(--nevoa-100);font-weight:600}
.card .ch span{font-size:11px;color:var(--aco-500)}
table.t td .tag{margin-left:6px}
table.t td .pers{display:block;font-size:10.5px;color:var(--aco-500);margin-top:2px}
.comp .legend{gap:4px}
.sinal{margin-top:12px;padding-top:10px;border-top:1px solid var(--prussia-700);display:grid;gap:6px}
.sinal .sr2{display:flex;justify-content:space-between;font-size:12px;color:var(--nevoa-200)}
.sinal .sr2 .num{color:var(--azul-300);font-size:12.5px}
.sinal .sr2.m{color:var(--aco-400)}
.sinal .sr2.m .num{color:var(--nevoa-200)}
.sinal .pg{display:flex;gap:6px;margin-top:2px}
.sinal .pp{font-size:10.5px;color:var(--aco-400);border:1px solid var(--prussia-700);border-radius:99px;padding:2px 8px}
.snapb{margin-top:10px}
.kpis.k3{grid-template-columns:repeat(3,1fr)}
.kan{height:auto;margin-top:12px}
.kan.fun .col{min-height:300px}
.col.win{border-color:var(--azul-700)}
.hint2{margin:10px 2px 0;font-size:11.5px;color:var(--aco-500)}
.subtabs{display:inline-flex;gap:2px;padding:3px;border:1px solid var(--prussia-700);border-radius:9px;background:var(--prussia-900);margin-bottom:12px}
.subtabs span{font-size:11.5px;padding:5px 11px;border-radius:7px;color:var(--aco-400)}
.subtabs span.on{background:rgba(37,161,239,.12);color:var(--azul-300)}
.chart .k span{color:var(--aco-500);font-size:11px;margin-left:6px}
.bars{height:170px}
'''
h = sub1(h, '/* GALERIA */', APP_CSS + '\n/* GALERIA */') if '/* GALERIA */' in h else sub1(h, '/* FOUNDERS */', APP_CSS + '\n/* FOUNDERS */')

# ================= TELAS: JS =================
ORC_JS = r'''/* orçamento de exemplo das telas: preço unitário pelo motor, venda direta */
(function(){
  var rows = [
    [PECAS.vaso, 12, null],
    [PECAS.piao, 30, null],
    [{n:'Chaveiro com nome, 2 cores', g:7, min:32}, 50, ['nome em cada peça', 'aguardando arte']],
    [{n:'Placa de mesa com logo', g:96, min:285}, 4, ['logo e cores da marca', 'arte aprovada']]
  ];
  var ins = [ ['Argola de chaveiro', 50, true, 18, 100], ['Embalagem kraft P', 1, false, 120, 0] ]; // centavos de custo, margem %
  var tot = 0, comp = {material:0, energia:0, maquina:0, mao:0, insumos:0, refugo:0, lucro:0};
  $('#orcRows').innerHTML = rows.map(function(x){
    var P = x[0], q = x[1], r = MOTOR.precificar(withP({gramas:P.g, minutos:P.min, origem:'fatiador', taxaCanalPct:0, taxaFixa:0}));
    tot += r.preco*q;
    comp.material += r.material*q; comp.energia += r.energia*q; comp.maquina += r.maquina*q; comp.mao += (r.setup + r.pos)*q;
    comp.insumos += r.insumos*q; comp.refugo += r.refugo*q; comp.lucro += r.lucro*q;
    var pers = x[2] ? '<span class="pers">' + x[2][0] + '</span>' : '';
    var tg = x[2] ? '<span class="tag ' + (x[2][1] === 'arte aprovada' ? 'ok' : 'at') + '">' + x[2][1] + '</span>' : '';
    return '<tr><td>' + P.n + tg + pers + '</td><td class="r num">' + q + '</td><td class="r num">' + brl(r.custo) + '</td><td class="r num">' + brl(r.preco) + '</td><td class="r num">' + brl(r.preco*q) + '</td></tr>';
  }).join('');
  $('#insRows').innerHTML = ins.map(function(x){
    var custo = x[3], q = x[1], cobra = x[2], preco = Math.round(custo*(1 + x[4]/100));
    comp.insumos += custo*q;
    if (cobra){ tot += preco*q; comp.lucro += (preco - custo)*q }
    return '<tr><td>' + x[0] + '</td><td class="r num">' + q + '</td><td>' + (cobra ? '<span class="tag az">cobra do cliente</span>' : '<span class="tag">custo do pedido</span>') + '</td><td class="r num">' + brl(custo) + '</td><td class="r num">' + brl((cobra ? preco : custo)*q) + '</td></tr>';
  }).join('');
  /* o custo do insumo que não é cobrado sai do lucro */
  ins.forEach(function(x){ if (!x[2]) comp.lucro -= x[3]*x[1] });
  var sinal = Math.round(tot/2);
  $('#orcTot').textContent = brl(tot);
  $('#orcSinal').textContent = brl(sinal) + ' · 50%';
  $('#orcSaldo').textContent = brl(tot - sinal);
  $('#funOrc').textContent = brl(tot);
  $$('#compCard .bar i').forEach(function(i){ i.style.flex = String(Math.max(0, comp[i.dataset.o])) });
  $$('#compCard [data-l]').forEach(function(e){ e.textContent = brl(comp[e.dataset.l]) });
})();

'''
h = between(h, '/* orçamento de exemplo das telas: preço unitário pelo motor, venda direta */', '/* ============ TELAS ============ */', ORC_JS)
h = sub1(h, "function fitApp(){ appScale = fit.clientWidth/1180; app.style.transform = 'scale(' + appScale + ')'; if (zoomed) applyZoom() }",
            "function fitApp(){ appScale = fit.clientWidth/1180; app.style.transform = 'scale(' + appScale + ')' }")
h = re.sub(r"var HEAD = \{orc:.*?\};", "var HEAD = {orc:['Orçamento ORC-0321','Duplicar','Enviar ao cliente'], funil:['Funil de vendas','Colunas','Nova negociação'], prod:['Fila de produção','Tentativas','Novo pedido'], fin:['Financeiro','Exportar','Novo lançamento']};", h, count=1, flags=re.S)
h = sub1(h, "var ORDER = ['orc','prod','est','fin'], curTab = 'orc', autoTab = !RM, tabAnim = null, telasVis = false, zoomed = false;",
            "var ORDER = ['orc','funil','prod','fin'], curTab = 'orc', autoTab = !RM, tabAnim = null, telasVis = false;")
h = sub1(h, "  if (v !== 'orc' && zoomed) setZoom(false);\n", "")
h = between(h, '/* zoom de câmera: do app inteiro até o custo congelado do orçamento */', 'var tiltX = 0', '')
h = sub1(h, "  var z = zoomed ? 0 : 1;\n", "  var z = 1;\n")
assert 'zoomBtn' not in h and 'zoomed' not in h.split('<script>')[1], 'sobrou zoom no JS'

# ================= FOUNDERS =================
h = sub1(h, 'O Make3Lab nasceu para rodar uma oficina de verdade e agora abre para as primeiras de fora. Quem entra no lote Founders',
            'O Make3Lab foi criado dentro de uma operação de impressão 3D que produz e vende todos os dias. Agora ele abre para outros operadores. Quem entra no lote Founders')
h = sub1(h, '<small>Enquanto a assinatura estiver ativa, na capacidade do plano de entrada.</small>',
            '<small>Enquanto a assinatura estiver ativa, no plano de entrada. Nos planos maiores, o Founder também tem condição especial.</small>')
h = sub1(h, '<li><span>Para quem</span><span>Quem já imprime e já vende, mesmo que pouco</span></li>',
            '<li><span>Para quem</span><span>Quem já imprime e vende, mesmo que pouco, e quer controlar os custos e vender com mais margem</span></li>')

# ================= FORMULÁRIO =================
h = sub1(h, '<label for="qtd">Impressoras hoje</label>', '<label for="qtd">Quantas impressoras você tem hoje?</label>')
h = sub1(h, '<label for="precifica">Como chega no preço</label>', '<label for="precifica">Como você calcula o preço hoje?</label>')

# ================= FAQ =================
FEAT = [
 ('Orçamento', 'produtos, insumos e personalização no mesmo pedido, com sinal e custo congelado no dia'),
 ('Funil de vendas', 'cada negociação numa etapa. Ao fechar, vira venda, conta a receber e ordem de produção'),
 ('Simulador', 'custo e preço de uma peça em segundos, sem salvar nada'),
 ('Fila de produção', 'a venda entra sozinha. Falhas e reimpressões ficam registradas'),
 ('Entregas e calendário', 'o que está pronto, o que está a caminho e os prazos da semana'),
 ('Consignação', 'peças deixadas em pontos de venda e o acerto de cada um'),
 ('Cadastros', 'produtos, kits, clientes, filamentos e insumos, com custo por grama'),
 ('Importação de 3MF e G‑code', 'peso e tempo lidos direto do arquivo do fatiador'),
 ('Financeiro', 'dashboard, entradas, saídas fixas e variáveis e previsão de saldo por semana'),
 ('Relatórios', 'vendas, ganho por canal, metas, produtos e clientes'),
 ('Preço por canal', 'a taxa da Shopee, do Mercado Livre e da venda direta já entra no preço. Nada é publicado automaticamente'),
 ('Usuários', 'convite por link para quem trabalha com você'),
]
feat_html = '<ul class="feat">' + ''.join('<li><b>' + a + '</b><span>' + b + '</span></li>' for a, b in FEAT) + '</ul>'
h = re.sub(r'(<details><summary>O que o sistema faz hoje\?<span class="pl" aria-hidden="true">\+</span></summary><div class="an"><div>)<p>.*?</p>(</div></div></details>)',
           lambda m: m.group(1) + feat_html + m.group(2), h, count=1, flags=re.S)
h = re.sub(r'(<summary>Por que a vaga não é por ordem de chegada\?.*?<div class="an"><div>)<p>.*?</p>',
           lambda m: m.group(1) + '<p>São só 10 vagas, e o programa depende de uso real. <b>Por isso escolhemos quem já imprime e vende hoje</b>: é essa operação que testa o sistema de verdade e mostra o que precisa melhorar. Você entra na lista, a gente lê cada cadastro e chama pelo WhatsApp quem tem esse perfil.</p>', h, count=1, flags=re.S)
h = re.sub(r'(<summary>O R\$ 19,90 vale para sempre mesmo\?.*?<div class="an"><div>)<p>.*?</p>',
           lambda m: m.group(1) + '<p>Vale <b>enquanto a assinatura estiver ativa, sem interrupção</b>, no plano de entrada. Se a sua operação crescer e precisar de um plano maior, o Founder também tem condição especial nos outros planos. <!-- [CONFIRMAR] qual é a condição especial dos Founders nos planos maiores --></p>', h, count=1, flags=re.S)
FAQ_CSS = '''
.qa .feat{list-style:none;margin:0;padding:0 0 22px;display:grid;gap:10px;max-width:62ch}
.qa .feat li{display:grid;grid-template-columns:minmax(150px,200px) 1fr;gap:14px;padding-top:10px;border-top:1px solid var(--prussia-800);color:var(--aco-400);font-size:15.5px;line-height:1.5}
.qa .feat li:first-child{border-top:0;padding-top:0}
.qa .feat b{color:var(--nevoa-100);font-weight:600}
@media (max-width:620px){.qa .feat li{grid-template-columns:1fr;gap:2px}}
'''
h = sub1(h, '/* rodapé */', FAQ_CSS + '\n/* rodapé */')

h = sub1(h, '<p>Lê o 3MF. <b>', '<p>Lê o 3MF e o G‑code. <b>')

# ================= HERO: seletor sem sobrepor e rolagem fluida =================
h = sub1(h, '  .views{top:auto;right:auto;left:var(--gut);bottom:calc(env(safe-area-inset-bottom,0px) + 92px)}',
            '  .views{top:auto;right:auto;left:var(--gut);bottom:calc(env(safe-area-inset-bottom,0px) + 26px + var(--tkh,84px))}')
# no desktop, o seletor fica colado acima do ticket, alinhado à direita
h = sub1(h, '.views{position:absolute;right:var(--gut);top:calc(var(--nav-h) + 96px + env(safe-area-inset-top,0px));pointer-events:auto}',
            '.views{position:absolute;right:var(--gut);bottom:calc(clamp(20px,5vh,56px) + 12px + var(--tkh,420px));pointer-events:auto}')
h = sub1(h, "renderer.setPixelRatio(Math.min(W.devicePixelRatio||1, 2));", "renderer.setPixelRatio(Math.min(W.devicePixelRatio||1, FINE ? 2 : 1.5));")
h = sub1(h, "    var w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;\n",
            "    var w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;\n    if (w === size.w && Math.abs(h - (size.h||0)) < (FINE ? 1 : 140)) return; size.w = w; size.h = h;\n")
# progresso pelo palco fixo (100svh), não por innerHeight, que muda quando a barra do navegador some no celular
h = sub1(h, "  var r = heroEl.getBoundingClientRect(), tot = heroEl.offsetHeight - innerHeight;",
            "  var r = heroEl.getBoundingClientRect(), tot = heroEl.offsetHeight - heroStage.offsetHeight;")
h = sub1(h, "function heroProgress(){", "var heroStage = $('.stage', heroEl);\nfunction heroProgress(){")
h = sub1(h, "  hCur += (hTarget - hCur) * (RM ? 1 : 0.12);", "  hCur += (hTarget - hCur) * (RM ? 1 : (FINE ? 0.12 : 0.24));")
h = sub1(h, "var PRINT_END = 0.78, lastNow = null, lastDone = null;",
            "var PRINT_END = 0.78, lastNow = null, lastDone = null;\nfunction tkh(){ heroEl.style.setProperty('--tkh', ticket.offsetHeight + 'px') }")
h = sub1(h, "addEventListener('resize', relayout);", "addEventListener('resize', relayout); addEventListener('resize', tkh); tkh();\nif (D.fonts && D.fonts.ready) D.fonts.ready.then(tkh);")
# o ticket muda de altura quando acaba a impressão (linhas ligam): reposiciona o seletor
h = sub1(h, "  if (done !== lastDone){ lastDone = done;", "  if (done !== lastDone){ lastDone = done; tkh();")

open(p_out, 'w', encoding='utf-8').write(h)
print('ok', len(h))
