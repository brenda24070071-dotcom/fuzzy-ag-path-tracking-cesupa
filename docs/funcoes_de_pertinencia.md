# Funções de Pertinência — Universos de Discurso, Fórmulas e Parâmetros

## 1. Variáveis e universos de discurso

| Variável | Papel | Unidade | Universo de discurso | Faixa de operação típica |
|---|---|---|---|---|
| `e_lat` (erro lateral) | Entrada 1 | metros (m) | `[-50, 50]` | `[-5, 5]` |
| `theta_e` (erro angular) | Entrada 2 | radianos (rad) | `[-50, 50]` | `[-π, π]` (normalizado) |
| `omega` (taxa de guinada) | Saída | rad/s | `[-50, 50]` | `[-1.5, 1.5]` após defuzzificação típica; valores extremos saturam o esterçamento em ±45° |

O universo amplo `[-50, 50]` segue a parametrização do artigo de referência: os conjuntos
`AN`/`AP` têm ombros longos que garantem pertinência não-nula para qualquer erro fisicamente
alcançável, enquanto a "região de trabalho fina" do controlador fica em `[-5, 5]`. As
entradas são saturadas em `±49.99` antes da fuzzificação para garantir cobertura.

## 2. Formas das funções

São usadas funções **triangulares** e **trapezoidais**:

- Triangular `trimf(x; a, b, c)`: `μ(x) = max(0, min((x−a)/(b−a), (c−x)/(c−b)))`
- Trapezoidal `trapmf(x; a, b, c, d)`: `μ(x) = max(0, min((x−a)/(b−a), 1, (d−x)/(d−c)))`

A escolha (triangular no centro, trapezoidal nas extremidades) segue o artigo de referência e
é o padrão em controle fuzzy embarcado: avaliação barata, interpretação direta e suporte
compacto na região de precisão.

## 3. Parametrização pelo vetor de genes (entradas otimizáveis pelo AG)

As MFs das **entradas** são definidas por 10 parâmetros derivados do vetor de genes
`p ∈ [0,1]^10` (5 para `theta_e`, 5 para `e_lat`):

| Parâmetro | Derivação | Papel |
|---|---|---|
| `a = p0` | direto | meia-largura do `Z` de `theta_e` |
| `b = 0.5 + 1.5·p1` | escala `[0.5, 2.0]` | ombro interno de `AN`/`AP` de `theta_e` |
| `c = 2·p2` | escala `[0, 2]` | largura da rampa de `AN`/`AP` de `theta_e` |
| `d = 0.5 + p3` | escala `[0.5, 1.5]` | centro de `MN`/`MP` de `theta_e` |
| `e = p4` | direto | meia-largura de `MN`/`MP` de `theta_e` |
| `f = p5` | direto | meia-largura do `Z` de `e_lat` |
| `g = 0.5 + 1.5·p6` | escala `[0.5, 2.0]` | ombro interno de `AN`/`AP` de `e_lat` |
| `h = 2·p7` | escala `[0, 2]` | largura da rampa de `AN`/`AP` de `e_lat` |
| `i = 0.5 + p8` | escala `[0.5, 1.5]` | centro de `MN`/`MP` de `e_lat` |
| `j = p9` | direto | meia-largura de `MN`/`MP` de `e_lat` |

### MFs de `theta_e` (idem para `e_lat`, trocando `a,b,c,d,e` por `f,g,h,i,j`)

| Termo | Função | Parâmetros |
|---|---|---|
| AN | trapezoidal | `[-50, -5, -b, -b+c]` |
| MN | triangular | `[-d-e, -d, -d+e]` |
| Z | triangular | `[-a, 0, a]` |
| MP | triangular | `[d-e, d, d+e]` |
| AP | trapezoidal | `[b-c, b, 5, 50]` |

### MFs de `omega` (saída — fixas, não otimizadas)

| Termo | Função | Parâmetros (rad/s) |
|---|---|---|
| AN | trapezoidal | `[-50, -5, -1, -0.5]` |
| MN | triangular | `[-1, -0.5, 0]` |
| Z | triangular | `[-0.5, 0, 0.5]` |
| MP | triangular | `[0, 0.5, 1]` |
| AP | trapezoidal | `[0.5, 1, 5, 50]` |

Manter a saída fixa reduz o espaço de busca do AG para 10 dimensões e preserva a
interpretabilidade da ação de controle (a "força" de cada termo de saída não muda).

## 4. Valores concretos

### Baseline (todos os genes = 0.5)

`a=0.5, b=1.25, c=1.0, d=1.0, e=0.5` (theta_e) — `f=0.5, g=1.25, h=1.0, i=1.0, j=0.5` (e_lat)

### Otimizado pelo AG (melhor indivíduo, RMSE = 1.2319 m)

Genes: `[0.826, 0.190, 0.827, 0.844, 0.655, 0.642, 0.662, 0.756, 0.563, 0.255]`

| | `theta_e` | `e_lat` |
|---|---|---|
| Meia-largura do Z | `a = 0.826` | `f = 0.642` |
| Ombro AN/AP | `b = 0.785` | `g = 1.493` |
| Rampa AN/AP | `c = 1.654` | `h = 1.512` |
| Centro MN/MP | `d = 1.344` | `i = 1.063` |
| Meia-largura MN/MP | `e = 0.655` | `j = 0.255` |

Leitura: o AG **alargou** a zona morta angular (`a`: 0.5 → 0.83) e **estreitou** os termos
médios do erro lateral (`j`: 0.5 → 0.26), reduzindo oscilações sem perder capacidade de
captura. Os gráficos antes/depois estão em `resultados/mfs_otimizadas.png`.

## 5. Critérios de qualidade

- **Cobertura:** para qualquer valor saturado das entradas existe ao menos um termo com
  pertinência > 0 (os ombros de `AN`/`AP` se estendem até ±50).
- **Sobreposição:** termos vizinhos se cruzam (caráter gradual preservado — o sistema não
  vira uma tabela de decisão crisp).
- **Nem estreitas, nem indiferentes:** a região fina `[-5, 5]` concentra 5 termos; os limites
  do AG (`b ∈ [0.5,2]`, `d ∈ [0.5,1.5]` etc.) impedem que a otimização degenere as funções
  (colapso de suporte ou sobreposição total).
