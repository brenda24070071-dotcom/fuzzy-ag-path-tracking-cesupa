"""
Gera fuzzy_path_tracking.ipynb a partir do modulo CORRIGIDO fuzzy_path_tracking.py.
O notebook NAO duplica a logica: ele importa do modulo, garantindo coerencia total
entre codigo, relatorio e demonstracao. Rode: python scripts/build_notebook.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.splitlines(keepends=True)}


cells = [
    md("# Controlador Fuzzy Mamdani Otimizado por Algoritmo Genetico\n"
       "### Rastreamento de trajetoria de robo autonomo (modelo bicicleta)\n\n"
       "Reproducao/adaptacao de Mancilla et al., *Optimal Fuzzy Controller Design for "
       "Autonomous Robot Path Tracking Using Population-Based Metaheuristics*, Symmetry 2022.\n\n"
       "> Este notebook **importa** toda a logica de `fuzzy_path_tracking.py` (motor de "
       "inferencia, simulacao e AG) e de `experiments.py` (evidencias). Assim, codigo, "
       "relatorio e demonstracao permanecem 100% coerentes."),

    md("## 1. Imports e configuracao"),
    code("import numpy as np\n"
         "import matplotlib.pyplot as plt\n"
         "import fuzzy_path_tracking as F\n"
         "import experiments\n"
         "np.random.seed(42)\n"
         "print('Pistas:', [t.name for t in F.TRACKS])\n"
         "print('Saida omega in [%.1f, %.1f] rad/s' % (F.UNIV_FAST[0], F.UNIV_FAST[-1]))"),

    md("## 2. Trajetorias de referencia (pistas M, A, S)\n"
       "Cada pista e uma *cubic spline* por 7 pontos de controle (Tabela 4 do artigo)."),
    code("fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n"
         "for ax, t in zip(axes, F.TRACKS):\n"
         "    ax.plot(t.rx, t.ry, 'r--'); ax.plot(t.rx[0], t.ry[0], 'go', label='inicio')\n"
         "    ax.plot(t.rx[-1], t.ry[-1], 'ks', label='fim')\n"
         "    ax.set_title('Pista ' + t.name); ax.set_aspect('equal'); ax.grid(alpha=.3); ax.legend()\n"
         "plt.tight_layout(); plt.show()"),

    md("## 3. Modelo fuzzy: variaveis, funcoes de pertinencia e base de regras\n\n"
       "**Entradas:** erro lateral `e` (m) e erro angular `theta_e`. **Saida:** taxa de "
       "guinada `omega` (rad/s). 5 termos linguisticos por variavel "
       "(AN, MN, Z, MP, AP) -> **25 regras** (matriz 5x5).\n\n"
       "Operadores: E = `min`, implicacao = `min`, agregacao = `max`, "
       "defuzzificacao = **centroide**."),
    code("print('Matriz de regras (linha = theta_e, coluna = e), valor = indice do termo de omega):')\n"
         "for lab, row in zip(F.LABELS, F.RULE_MATRIX):\n"
         "    print(f'  {lab}: ' + '  '.join(F.LABELS[i] for i in row))\n"
         "\n"
         "# Funcoes de pertinencia (parametros baseline = 0.5)\n"
         "_, te, er, om = F.build_fuzzy(np.full(10, 0.5))\n"
         "fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n"
         "for ax, var, nm in zip(axes, [te, er, om], ['theta_e', 'e', 'omega']):\n"
         "    for L in F.LABELS: ax.plot(var.universe, var[L].mf, label=L)\n"
         "    ax.set_title(nm); ax.legend(); ax.grid(alpha=.3)\n"
         "    ax.set_xlim(-20, 20) if nm != 'omega' else ax.set_xlim(-2.2, 2.2)\n"
         "plt.tight_layout(); plt.show()"),

    md("### 3.1 Convencao de sinais (realimentacao negativa)\n"
       "`e>0` = veiculo a **direita** da rota; `omega>0` = estercar a **esquerda** "
       "(corretivo). O metodo `FastFuzzyController.control()` aplica essa convencao."),
    code("c = F.FastFuzzyController(np.full(10, 0.5))\n"
         "for e in (-8, -1, 0, 1, 8):\n"
         "    print(f'  e={e:+d} m, theta_e=0  ->  omega = {c.control(e, 0.0):+.3f} rad/s')"),

    md("## 4. Parte 1 - Fuzzy baseline (sem otimizacao)\n"
       "Parametros medios (0.5). Simulacao cinematica de Euler com terminacao ao atingir o fim."),
    code("base = F.FastFuzzyController(np.full(10, 0.5))\n"
         "fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n"
         "for ax, t in zip(axes, F.TRACKS):\n"
         "    rmse, hx, hy = F.simulate(base, t)\n"
         "    ax.plot(t.rx, t.ry, 'r--', label='ref'); ax.plot(hx, hy, 'b', label='robo')\n"
         "    ax.set_title(f'Pista {t.name} (RMSE={rmse:.3f})'); ax.set_aspect('equal')\n"
         "    ax.grid(alpha=.3); ax.legend()\n"
         "plt.tight_layout(); plt.show()\n"
         "print('RMSE medio baseline:', round(F.fitness(np.full(10, 0.5)), 4))"),

    md("## 5. Parte 2 - Otimizacao evolutiva (AG)\n"
       "Carrega os melhores parametros salvos em `resultados/best_params.npy` "
       "(gerados por `python main.py`). Caso nao existam, roda uma busca curta."),
    code("import os\n"
         "p = 'resultados/best_params.npy'\n"
         "if os.path.exists(p):\n"
         "    best = np.load(p); print('Parametros otimizados carregados de', p)\n"
         "else:\n"
         "    best, fit, hist = F.run_ga(pop_size=20, gens=10); print('AG executado, RMSE:', round(fit, 4))\n"
         "print('best =', np.round(best, 3))"),

    md("## 6. Resultados - Fuzzy otimizado"),
    code("opt = F.FastFuzzyController(best)\n"
         "fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n"
         "for ax, t in zip(axes, F.TRACKS):\n"
         "    rmse, hx, hy = F.simulate(opt, t)\n"
         "    ax.plot(t.rx, t.ry, 'r--', label='ref'); ax.plot(hx, hy, 'g', label='otimizado')\n"
         "    ax.set_title(f'Pista {t.name} (RMSE={rmse:.3f})'); ax.set_aspect('equal')\n"
         "    ax.grid(alpha=.3); ax.legend()\n"
         "plt.tight_layout(); plt.show()\n"
         "print('RMSE medio otimizado:', round(F.fitness(best), 4))"),

    md("### 6.1 Superficie de controle"),
    code("fsim, *_ = F.build_fuzzy(best)\n"
         "F.plot_surface(fsim)\n"
         "from matplotlib import image as mpimg\n"
         "plt.figure(figsize=(7, 5)); plt.imshow(mpimg.imread('resultados/superficie_controle.png'))\n"
         "plt.axis('off'); plt.show()"),

    md("## 7. Evidencias experimentais automaticas\n"
       "Gera `test_scenarios.csv`, `funcoes_pertinencia.png` e `analise_experimentos.md` "
       "(8 cenarios categorizados + verificacoes de coerencia)."),
    code("res = experiments.run()\n"
         "import csv\n"
         "with open('resultados/test_scenarios.csv', encoding='utf-8') as f:\n"
         "    for row in csv.reader(f): print(row[:6])"),

    md("## 8. Conclusao\n"
       "O controlador fuzzy Mamdani segue as 3 trajetorias com RMSE da ordem de 1-2 m; o AG "
       "reduz o RMSE medio em ~20-25% frente ao baseline. As verificacoes automaticas "
       "confirmam deadband, antissimetria, realimentacao negativa e estabilidade em malha "
       "fechada. Veja `resultados/analise_experimentos.md`."),
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.13"},
    },
    "nbformat": 4, "nbformat_minor": 5,
}

out = os.path.join(ROOT, "fuzzy_path_tracking.ipynb")
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Notebook regenerado:", out, "->", len(cells), "celulas")
