# Cenários de Teste e Validação Experimental

Todos os valores abaixo são saídas **reais** do sistema (`python fuzzy_path_tracking.py`,
sementes fixas 42–46) e podem ser reproduzidos seguindo `docs/manual_de_execucao.md`.

## 1. Cenários pontuais de inferência (6 cenários)

Entradas: `e_lat` em metros (+ = robô à direita da pista), `theta_e` em radianos
(+ = apontando à esquerda). Saída: `omega` em rad/s (+ = vira à esquerda). Inferência via
`scikit-fuzzy` (Mamdani min-max, defuzzificação por centroide).

| # | Tipo de caso | `e_lat` | `theta_e` | ω Baseline | ω Otimizado | Interpretação | Coerência |
|---|---|---|---|---|---|---|---|
| C1 | Nulo (equilíbrio) | 0.0 | 0.0 | 0.0000 | 0.0000 | Robô no centro e alinhado → nenhuma ação | ✔ Ponto de equilíbrio exato |
| C2 | Erro lateral alto | +5.0 | 0.0 | +17.2788 | +17.0322 | Muito à direita, alinhado → guinada forte à esquerda, de volta à pista | ✔ Sinal e magnitude corretos (satura o esterçamento em +45°) |
| C3 | Erro lateral alto (simétrico) | −5.0 | 0.0 | −17.2788 | −17.0322 | Muito à esquerda → guinada forte à direita | ✔ Antissimetria perfeita em relação a C2 |
| C4 | Erro angular alto | 0.0 | +2.0 | −17.2788 | −17.2707 | Sobre a pista mas apontando muito à esquerda → corrige rumo virando à direita | ✔ Realimentação negativa do rumo |
| C5 | Aproximação (fronteiriço) | +5.0 | +2.0 | 0.0000 | 0.0000 | À direita, mas já apontando para a pista → não interfere na convergência | ✔ Evita sobressinal (grupo G3 das regras) |
| C6 | Conflito crítico | −5.0 | +2.0 | −17.2788 | −17.2788 | À esquerda E apontando para fora (divergindo) → correção máxima à direita | ✔ Pior caso tratado com ação máxima |

**Comentário geral:** a tabela cobre caso nulo, casos altos (C2–C4), caso fronteiriço de
conflito de objetivos (C5) e caso crítico (C6), como exige a lauda. Os valores ±17.28 rad/s
correspondem ao centroide dos conjuntos de saída `AN`/`AP` (ombros longos até ±50); na
prática, o esterçamento satura em ±45° via `δ = arctan(L·ω/v)` — o que torna o controlador
"agressivo" fora da região fina e suave dentro dela.

## 2. Validação por simulação completa (3 pistas)

RMSE do erro lateral ao longo do percurso (robô parte de (0,0,0°) e deve completar a pista):

| Pista | RMSE Baseline (m) | RMSE Otimizado AG (m) | Completa o percurso? |
|---|---|---|---|
| M | 0.8020 | 0.7050 | Sim (ambos) |
| A | 2.2314 | 2.0440 | Sim (ambos) |
| S | 1.6468 | 0.9470 | Sim (ambos) |
| **Média** | **1.5601** | **1.2319** | **Melhoria: 21,0%** |

Evidências visuais: `resultados/baseline_trajectories.png` e
`resultados/optimized_trajectories.png`.

## 3. Análise do comportamento (não apenas listagem)

- **Onde o sistema vai bem:** trechos suaves e retas — erro lateral fica < 1 m; a captura da
  pista após desvio é rápida e sem oscilação sustentada (efeito do grupo de regras de
  convergência e da zona morta).
- **Onde o sistema sofre:** curvas fechadas das pistas (laços), pois a velocidade é fixa
  (3,33 m/s) e não há termo de antecipação de curvatura: o robô faz pequenos laços de
  recaptura (visíveis na pista A, pior RMSE). O AG mitiga, mas não elimina — limitação
  estrutural do controlador puramente reativo de 2 entradas.
- **Efeito do AG:** maior ganho na pista S (−42% de RMSE); o AG alargou a zona morta angular
  e estreitou os termos médios do erro lateral (ver `docs/funcoes_de_pertinencia.md`),
  reduzindo a oscilação de recaptura.
- **Superfície de controle** (`resultados/superficie_controle.png`): mostra transição suave
  na região central (caráter fuzzy preservado) e platôs saturados nas bordas — coerente com
  os cenários C2/C6.
- **Convergência do AG** (`resultados/ag_convergence.png`): as 5 execuções convergem para
  RMSE ≈ 1.23–1.32 m, indicando robustez do resultado à semente aleatória.

## 4. Caso degenerado documentado (robustez)

Durante o desenvolvimento, a matriz de regras espelhada (defeito de convenção de sinal)
produzia RMSE ≈ 2085 m — o robô seguia a pista por alguns metros e divergia. Esse caso ficou
registrado como evidência de que a métrica de fitness (RMSE + penalidade de não-chegada)
detecta corretamente controladores inválidos, e de que a validação por simulação é
indispensável (a tabela de cenários pontuais sozinha não revelava o problema com clareza).
