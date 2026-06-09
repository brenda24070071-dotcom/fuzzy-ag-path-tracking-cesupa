# Controlador Fuzzy Mamdani + AG para Rastreamento de Trajetória

Sistema de controle **Fuzzy Mamdani** que comanda o esterçamento de um robô
autônomo (modelo cinemático *bicicleta*) para seguir trajetórias de referência,
com **otimização das funções de pertinência por Algoritmo Genético (AG)**.

Reprodução/adaptação de: Mancilla et al., *Optimal Fuzzy Controller Design for
Autonomous Robot Path Tracking Using Population-Based Metaheuristics*, Symmetry 2022, 14, 202.

- **Disciplina:** Inteligência Artificial e Computacional (0700M8) — CESUPA
- **Modalidade:** Opção A (artigo científico) com extensão de otimização (AG)
- **Modelo de inferência:** Mamdani (E=min, agregação=max, defuzzificação=centroide)

## Modelo fuzzy (resumo)

| Item | Valor |
|---|---|
| Entradas | `e` = erro lateral (m); `theta_e` = erro angular |
| Saída | `omega` = taxa de guinada (rad/s), universo `[-2, 2]` |
| Termos linguísticos | 5 por variável: AN, MN, Z, MP, AP |
| Regras | 25 (matriz 5×5) — ver [docs/base_de_regras.md](docs/base_de_regras.md) |
| Otimização | AG (10 genes = parâmetros das MFs de entrada), 5 execuções |

**Convenção de sinais (realimentação negativa):** `e>0` = veículo à direita da
rota → `omega>0` = esterça à esquerda (corretivo). Aplicada em
`FastFuzzyController.control()`.

## Instalação

```bash
pip install -r requirements.txt
```

Dependências: `numpy`, `scipy`, `matplotlib`, `scikit-fuzzy` (+ `networkx`).
Testado com **Python 3.13**.

## Execução (um comando)

```bash
python main.py            # pipeline completo: AG + todas as evidências (~1-2 min)
python main.py --fast     # apenas evidências experimentais (sem re-treinar o AG)
```

Notebook equivalente (importa a mesma lógica do módulo):

```bash
python -m nbconvert --to notebook --execute --inplace fuzzy_path_tracking.ipynb
```

## Saídas geradas (`resultados/`)

| Arquivo | Conteúdo |
|---|---|
| `baseline_trajectories.png` / `optimized_trajectories.png` | Trajetórias seguidas nas 3 pistas |
| `ag_convergence.png` | Curvas de convergência do AG (5 execuções) |
| `funcoes_pertinencia.png` / `mfs_otimizadas.png` | Funções de pertinência |
| `superficie_controle.png` | Superfície de controle `omega = f(e, theta_e)` |
| `test_scenarios.csv` | 8 cenários: entradas, `omega`, classificação, coerência |
| `analise_experimentos.md` | Análise automática de coerência + RMSE em malha fechada |
| `best_params.npy` | Melhores parâmetros encontrados pelo AG |

## Estrutura dos arquivos

```
fuzzy_path_tracking.py   # motor fuzzy (Mamdani), simulação cinemática e AG
experiments.py           # cenários de teste, CSV, análise de coerência, MD
main.py                  # ponto de entrada único (AG + evidências)
fuzzy_path_tracking.ipynb# notebook (importa do módulo; executado com saídas)
requirements.txt
docs/                    # base de regras, trabalhos relacionados, plano
resultados/              # gráficos, tabelas e relatório gerados
Pesquisa/                # PDFs das referências
```

## Resultados de referência

RMSE lateral médio nas 3 pistas: **baseline ≈ 1,9 m → otimizado ≈ 1,5 m**
(melhoria de ~20–25%). Todas as verificações automáticas de coerência passam
(deadband, antissimetria, realimentação negativa, estabilidade em malha fechada).
