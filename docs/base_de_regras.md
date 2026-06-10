# Base de Regras — Controlador Fuzzy Mamdani de Rastreamento de Trajetória

## 1. Convenções de sinal

Antes de ler as regras, é essencial fixar as convenções geométricas usadas no simulador
(`fuzzy_path_tracking.py`, função `simulate`):

| Grandeza | Símbolo | Convenção |
|---|---|---|
| Erro lateral | `e_lat` (m) | `e_lat > 0` → robô à **direita** da trajetória de referência (em relação ao sentido de percurso); `e_lat < 0` → à esquerda. Calculado pelo produto vetorial entre o vetor de desvio e a tangente da pista. |
| Erro angular | `theta_e` (rad) | `theta_e = θ_robô − θ_pista`, normalizado para `[-π, π]`. `theta_e > 0` → robô apontando à **esquerda** da direção da pista. |
| Saída | `omega` (rad/s) | Taxa de guinada comandada. `omega > 0` → guinada anti-horária (vira à **esquerda**); `omega < 0` → vira à direita. Convertida em ângulo de esterçamento por `δ = arctan(L·ω/v)`, saturado em ±45°. |

**Termos linguísticos** (5 por variável): `AN` = Alto Negativo, `MN` = Médio Negativo,
`Z` = Zero, `MP` = Médio Positivo, `AP` = Alto Positivo.

## 2. Matriz de regras (5×5 = 25 regras)

Todas as regras têm a forma **SE** `theta_e` é X **E** `e_lat` é Y **ENTÃO** `omega` é Z,
com o conectivo **E** implementado pela t-norma **mínimo**.

| `theta_e` \ `e_lat` | **AN** (muito à esq.) | **MN** (pouco à esq.) | **Z** (no centro) | **MP** (pouco à dir.) | **AP** (muito à dir.) |
|---|---|---|---|---|---|
| **AN** (apontando muito à dir.) | Z | MP | AP | AP | AP |
| **MN** (apontando pouco à dir.) | Z | MP | MP | MP | MP |
| **Z** (alinhado) | AN | Z | Z | Z | AP |
| **MP** (apontando pouco à esq.) | MN | MN | MN | MN | Z |
| **AP** (apontando muito à esq.) | AN | AN | AN | MN | Z |

## 3. Lista completa das 25 regras

| # | SE `theta_e` é | E `e_lat` é | ENTÃO `omega` é | Grupo de justificativa |
|---|---|---|---|---|
| R1 | AN | AN | Z | G3 — convergência |
| R2 | AN | MN | MP | G2 — correção composta |
| R3 | AN | Z | AP | G1 — correção de rumo |
| R4 | AN | MP | AP | G4 — conflito |
| R5 | AN | AP | AP | G4 — conflito |
| R6 | MN | AN | Z | G3 — convergência |
| R7 | MN | MN | MP | G2 — correção composta |
| R8 | MN | Z | MP | G1 — correção de rumo |
| R9 | MN | MP | MP | G2 — correção composta |
| R10 | MN | AP | MP | G2 — correção composta |
| R11 | Z | AN | AN | G5 — retorno à pista |
| R12 | Z | MN | Z | G6 — zona morta |
| R13 | Z | Z | Z | G0 — regime nominal |
| R14 | Z | MP | Z | G6 — zona morta |
| R15 | Z | AP | AP | G5 — retorno à pista |
| R16 | MP | AN | MN | G2 — correção composta |
| R17 | MP | MN | MN | G2 — correção composta |
| R18 | MP | Z | MN | G1 — correção de rumo |
| R19 | MP | MP | MN | G2 — correção composta |
| R20 | MP | AP | Z | G3 — convergência |
| R21 | AP | AN | AN | G4 — conflito |
| R22 | AP | MN | AN | G4 — conflito |
| R23 | AP | Z | AN | G1 — correção de rumo |
| R24 | AP | MP | MN | G2 — correção composta |
| R25 | AP | AP | Z | G3 — convergência |

## 4. Justificativa dos grupos de regras

- **G0 — Regime nominal (R13).** Robô no centro da pista e alinhado: nenhuma ação
  (`omega = Z`). É o ponto de equilíbrio do controlador.

- **G1 — Correção de rumo (R3, R8, R18, R23).** Robô sobre a pista, mas com erro de
  orientação: a ação corrige apenas o rumo, com intensidade proporcional ao erro angular e
  sinal oposto a ele (realimentação negativa: apontou à esquerda → vira à direita).

- **G5 — Retorno à pista (R11, R15).** Robô alinhado mas muito afastado lateralmente: comanda
  guinada forte **em direção** à pista (à direita da pista → vira forte à esquerda, e
  vice-versa). É o caso clássico de captura da trajetória.

- **G6 — Zona morta deliberada (R12, R14).** Desvios laterais pequenos com robô alinhado não
  geram ação. Isso evita oscilação/chattering em torno da referência; a correção surge
  naturalmente quando o desvio cresce e ativa `AN`/`AP`, ou quando aparece erro angular.

- **G3 — Convergência (R1, R6, R20, R25).** Erro lateral e erro angular com **sinais
  opostos**: o robô está afastado, porém já apontando de volta para a pista. A ação é nula
  para não "desfazer" a aproximação em curso — evita sobressinal na captura.

- **G2 — Correção composta (R2, R7, R9, R10, R16, R17, R19, R24).** Combinações
  intermediárias: a saída é moderada (`MN`/`MP`), dominada pelo sinal do erro angular,
  ajustando o rumo sem saturar o esterçamento.

- **G4 — Conflito (R4, R5, R21, R22).** Erro lateral e angular com **mesmo sinal**
  (afastado e apontando para fora): pior caso, divergência ativa. A resposta é a máxima
  correção (`AN`/`AP`), priorizando trazer o robô de volta.

A estrutura é **antissimétrica** (girar a tabela 180° troca os sinais da saída), refletindo a
simetria física do problema — propriedade herdada do artigo de referência (Mancilla et al.,
2022), que explora exatamente essa simetria do controlador.

## 5. Origem e validação da base

A base reproduz a estrutura de 25 regras do artigo de referência (Mancilla et al., *Symmetry*
2022), adaptada à convenção de sinais do nosso simulador (ver Seção 1). Durante o
desenvolvimento, a versão inicial da matriz estava **espelhada** no eixo do erro lateral em
relação a essa convenção, o que invertia a realimentação lateral (o robô fugia da pista; RMSE
≈ 2085 m com penalidade). A correção do espelhamento foi validada por simulação: RMSE médio
baseline caiu para **1,56 m** e o robô passou a completar as três pistas. Esse episódio está
discutido na análise crítica do documento principal.
