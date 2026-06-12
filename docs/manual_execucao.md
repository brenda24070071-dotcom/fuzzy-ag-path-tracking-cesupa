# Manual de Execução

Controlador Fuzzy Mamdani + Algoritmo Genético para rastreamento de trajetória.
Disciplina **Inteligência Artificial e Computacional (0700M8) — CESUPA**.

Este manual permite **reproduzir do zero** todos os resultados do relatório.

---

## 1. Pré-requisitos

- **Python 3.11+** (testado com Python 3.13).
- `pip` disponível no `PATH`.
- Sistema operacional indiferente (Windows, Linux ou macOS). O backend gráfico
  do matplotlib é forçado para `Agg` (sem janela), então funciona inclusive em
  servidores e notebooks headless.

Verifique a versão:

```bash
python --version
```

## 2. Instalação das dependências

A partir da raiz do repositório:

```bash
pip install -r requirements.txt
```

Isso instala `numpy`, `scipy`, `matplotlib`, `scikit-fuzzy` e `networkx`
(dependência transitiva do scikit-fuzzy). Recomenda-se um ambiente virtual:

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Execução completa (otimização AG + evidências)

```bash
python main.py
```

Tempo aproximado: **~1 minuto** (5 execuções do AG, 20 indivíduos × 11 gerações
cada, sobre 3 pistas). Ao final, a pasta `resultados/` é (re)gerada com todos os
artefatos descritos na seção 6.

Alternativa equivalente (mesma lógica, ponto de entrada do módulo principal):

```bash
python fuzzy_path_tracking.py
```

> Diferença: `fuzzy_path_tracking.py` treina o AG e gera os gráficos, mas **não
> persiste** `best_params.npy`; `main.py` treina, **salva** `best_params.npy` e
> em seguida gera as evidências experimentais (CSV + Markdown). Para a entrega,
> prefira `main.py`.

## 4. Execução rápida (sem re-treinar o AG)

Se `resultados/best_params.npy` já existe e você quer apenas regerar as
evidências experimentais (tabela de cenários, funções de pertinência, análise):

```bash
python main.py --fast
```

## 5. Reproduzir os testes / evidências isoladamente

```bash
python experiments.py
```

Gera `test_scenarios.csv`, `funcoes_pertinencia.png` e `analise_experimentos.md`
usando o controlador otimizado (se `best_params.npy` existir) ou o baseline.

## 6. Notebook interativo (opcional)

```bash
python -m nbconvert --to notebook --execute --inplace fuzzy_path_tracking.ipynb
```

O notebook importa a **mesma** lógica de `fuzzy_path_tracking.py` e
`experiments.py` — não há duplicação de implementação, garantindo coerência
entre código, notebook e relatório.

## 7. Artefatos gerados em `resultados/`

| Arquivo | Conteúdo |
|---|---|
| `baseline_trajectories.png` | Trajetórias seguidas pelo controlador baseline nas 3 pistas |
| `optimized_trajectories.png` | Trajetórias seguidas pelo controlador otimizado por AG |
| `ag_convergence.png` | Curvas de convergência das 5 execuções do AG |
| `funcoes_pertinencia.png` | Funções de pertinência das 3 variáveis (via skfuzzy) |
| `mfs_otimizadas.png` | Funções de pertinência com os parâmetros otimizados |
| `superficie_controle.png` | Superfície de controle `omega = f(e, theta_e)` |
| `test_scenarios.csv` | 8 cenários: entradas, `omega`, classificação e coerência |
| `analise_experimentos.md` | Relatório automático (deadband, antissimetria, malha fechada, RMSE) |
| `best_params.npy` | Melhores parâmetros (10 genes) encontrados pelo AG |
| `execucao_resumo.txt` | Log textual reproduzível da execução de `main.py` |

## 8. Reprodutibilidade

- As 5 execuções do AG usam sementes fixas (`np.random.seed(42..46)`), de modo
  que **os resultados numéricos são determinísticos** em uma mesma versão do
  NumPy. Valores de referência da nossa execução: baseline RMSE ≈ **1,93 m**,
  otimizado ≈ **1,47 m**, melhoria ≈ **24%**.
- Pequenas variações no terceiro/quarto decimal podem ocorrer entre versões de
  bibliotecas; a ordem de grandeza e a melhoria percentual permanecem estáveis.

## 9. Solução de problemas

| Sintoma | Causa provável | Correção |
|---|---|---|
| `ModuleNotFoundError: skfuzzy` | dependências não instaladas | `pip install -r requirements.txt` |
| `ModuleNotFoundError: networkx` | scikit-fuzzy sem dependência transitiva | já listada no `requirements.txt`; reinstale |
| Nenhuma janela de gráfico abre | backend `Agg` (esperado) | os gráficos são salvos em `resultados/`, não exibidos |
| RMSE diferente do relatório | versão distinta do NumPy | comportamento esperado; ver seção 8 |
