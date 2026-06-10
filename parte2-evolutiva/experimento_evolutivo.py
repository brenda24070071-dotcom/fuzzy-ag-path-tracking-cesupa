"""
PARTE 2 - IA Evolutiva e Computacao Bioinspirada (CESUPA 0700M8)
Comparacao experimental AG x PSO x Busca Aleatoria no ajuste dos
parametros das funcoes de pertinencia de um controlador fuzzy Mamdani
de rastreamento de trajetoria.

Artigo-base: Mancilla et al., "Optimal Fuzzy Controller Design for
Autonomous Robot Path Tracking Using Population-Based Metaheuristics",
Symmetry 2022, 14, 202. DOI 10.3390/sym14020202.

Formulacao do problema de otimizacao:
  - Variaveis de decisao: p em [0,1]^10 (parametros das MFs de entrada)
  - Funcao objetivo: RMSE medio do erro lateral em 3 pistas (minimizar)
  - Restricoes: dominio em caixa [0,1]^10 (clip); factibilidade via
    penalidade (+2000 se o robo nao completa a pista; 5000 se a
    inferencia falha)
  - Protocolo: 5 execucoes independentes por metodo (sementes 42-46),
    orcamento identico de 220 avaliacoes da funcao objetivo por execucao.

O nucleo de simulacao (controlador Mamdani 5x5 + cinematica de bicicleta)
e compartilhado com a Parte 1 do trabalho (repositorio
fuzzy-ag-path-tracking-cesupa).
"""
import csv
import json
import os
import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree

os.makedirs("resultados", exist_ok=True)

# ============================================================
# 1. NUCLEO DE SIMULACAO (identico ao da Parte 1, ja corrigido)
# ============================================================
L = 2.5            # distancia entre eixos (m)
V_R = 10.0 / 3.0   # velocidade constante (~3.33 m/s)
DELTA_MAX = np.pi / 4
T_MAX, DT = 50.0, 0.1


class Track:
    """Pista de referencia via spline cubica + busca de ponto mais proximo."""
    def __init__(self, name, ax, ay):
        self.name = name
        t = np.linspace(0, 1, len(ax))
        self.cs_x, self.cs_y = CubicSpline(t, ax), CubicSpline(t, ay)
        td = np.linspace(0, 1, 500)
        self.rx, self.ry = self.cs_x(td), self.cs_y(td)
        self.rdx, self.rdy = self.cs_x(td, 1), self.cs_y(td, 1)
        self.tree = cKDTree(np.column_stack([self.rx, self.ry]))

    def closest(self, x, y):
        _, idx = self.tree.query([x, y])
        return self.rx[idx], self.ry[idx], self.rdx[idx], self.rdy[idx], idx


TRACKS = [
    Track("M", [0, 6, 12, 5, 7.5, 3, -1],   [0, 0, 5, 6.5, 3, 5, -2]),
    Track("A", [0, 1, 2.5, 5, 7.5, 3, -1],  [0, -4, 6, 6.5, 3, 5, -2]),
    Track("S", [0, 2, 2.5, 5, 7.5, -3, -1], [0, 3, 6, 6.5, 5, 5, -2]),
]

LABELS = ['AN', 'MN', 'Z', 'MP', 'AP']
# Convencao: e_lat > 0 = robo a direita; theta_e > 0 = apontando a esquerda;
# omega > 0 = guinada anti-horaria. Linhas = theta_e, colunas = e_lat.
RULE_MATRIX = [
    [2, 3, 4, 4, 4],  # theta_e = AN
    [2, 3, 3, 3, 3],  # theta_e = MN
    [0, 2, 2, 2, 4],  # theta_e = Z
    [1, 1, 1, 1, 2],  # theta_e = MP
    [0, 0, 0, 1, 2],  # theta_e = AP
]


def trimf(x, abc):
    a, b, c = abc
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    if x < b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)


def trapmf(x, abcd):
    a, b, c, d = abcd
    if x <= a or x >= d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if x < b:
        return (x - a) / (b - a)
    return (d - x) / (d - c)


UNIV_FAST = np.arange(-50.0, 50.1, 1.0)
OM_MFS_FAST = [
    np.array([trapmf(x, [-50, -5, -1, -0.5]) for x in UNIV_FAST]),
    np.array([trimf(x, [-1, -0.5, 0]) for x in UNIV_FAST]),
    np.array([trimf(x, [-0.5, 0, 0.5]) for x in UNIV_FAST]),
    np.array([trimf(x, [0, 0.5, 1]) for x in UNIV_FAST]),
    np.array([trapmf(x, [0.5, 1, 5, 50]) for x in UNIV_FAST]),
]


class FastFuzzyController:
    """Motor de inferencia Mamdani (min-max, centroide) em NumPy puro."""
    def __init__(self, params):
        self.a, self.f = params[0], params[5]
        self.b, self.g = 0.5 + params[1] * 1.5, 0.5 + params[6] * 1.5
        self.c, self.h = params[2] * 2.0, params[7] * 2.0
        self.d, self.i = 0.5 + params[3], 0.5 + params[8]
        self.e, self.j = params[4], params[9]

    def compute(self, err_val, te_val):
        te_deg = [
            trapmf(te_val, [-50, -5, -self.b, -self.b + self.c]),
            trimf(te_val, [-self.d - self.e, -self.d, -self.d + self.e]),
            trimf(te_val, [-self.a, 0, self.a]),
            trimf(te_val, [self.d - self.e, self.d, self.d + self.e]),
            trapmf(te_val, [self.b - self.c, self.b, 5, 50]),
        ]
        er_deg = [
            trapmf(err_val, [-50, -5, -self.g, -self.g + self.h]),
            trimf(err_val, [-self.i - self.j, -self.i, -self.i + self.j]),
            trimf(err_val, [-self.f, 0, self.f]),
            trimf(err_val, [self.i - self.j, self.i, self.i + self.j]),
            trapmf(err_val, [self.g - self.h, self.g, 5, 50]),
        ]

        om_deg = [0.0] * 5
        for r in range(5):
            for col in range(5):
                act = min(te_deg[r], er_deg[col])
                out_mf = RULE_MATRIX[r][col]
                if act > om_deg[out_mf]:
                    om_deg[out_mf] = act

        aggregated = np.zeros_like(UNIV_FAST)
        for idx in range(5):
            if om_deg[idx] > 0:
                aggregated = np.maximum(aggregated, np.minimum(om_deg[idx], OM_MFS_FAST[idx]))

        sum_agg = np.sum(aggregated)
        if sum_agg == 0:
            raise Exception("No rules")
        return np.sum(UNIV_FAST * aggregated) / sum_agg


def simulate(controller, track):
    """Simula ate o robo alcancar o fim da pista ou estourar T_MAX.
    Penaliza em +2000 controladores que nao completam o percurso."""
    xr, yr, th = 0.0, 0.0, 0.0
    hx, hy, ssq = [], [], 0.0
    steps = int(T_MAX / DT)
    last_idx = len(track.rx) - 1
    n_exec, reached = 0, False

    for _ in range(steps):
        hx.append(xr); hy.append(yr)
        rx, ry, rdx, rdy, idx = track.closest(xr, yr)

        n = np.hypot(rdx, rdy) + 1e-6
        e_lat = (xr - rx) * rdy / n - (yr - ry) * rdx / n
        e_ang = ((th - np.arctan2(rdy, rdx)) + np.pi) % (2 * np.pi) - np.pi

        try:
            w = controller.compute(np.clip(e_lat, -49.99, 49.99), np.clip(e_ang, -49.99, 49.99))
        except Exception:
            return 5000.0, hx, hy

        delta = np.clip(np.arctan(L * w / V_R), -DELTA_MAX, DELTA_MAX)
        xr += V_R * np.cos(th) * DT
        yr += V_R * np.sin(th) * DT
        th += (V_R / L) * np.tan(delta) * DT
        ssq += e_lat ** 2
        n_exec += 1

        if idx >= last_idx - 2 and np.hypot(xr - track.rx[-1], yr - track.ry[-1]) < 2.0:
            reached = True
            break

    rmse = np.sqrt(ssq / n_exec)
    if not reached:
        rmse += 2000.0
    return rmse, hx, hy


# ============================================================
# 2. FUNCAO OBJETIVO COM CONTADOR DE AVALIACOES
# ============================================================
class AvaliadorFitness:
    """Encapsula a funcao objetivo: conta avaliacoes e registra a curva
    de melhor-ate-agora (uma entrada por avaliacao)."""
    def __init__(self):
        self.n_avaliacoes = 0
        self.melhor = float('inf')
        self.curva = []

    def __call__(self, params):
        controller = FastFuzzyController(params)
        f = float(np.mean([simulate(controller, t)[0] for t in TRACKS]))
        self.n_avaliacoes += 1
        if f < self.melhor:
            self.melhor = f
        self.curva.append(self.melhor)
        return f


# ============================================================
# 3. METAHEURISTICAS (mesmo orcamento: 220 avaliacoes cada)
# ============================================================
def run_ga(avaliador, pop_size=20, gens=10, pc=0.7, pm=0.3, sigma=0.2):
    """AG real-coded: torneio k=3, cruzamento aritmetico, mutacao gaussiana,
    elitismo de 2. Identico ao usado na Parte 1 do trabalho."""
    pop = np.random.rand(pop_size, 10)
    fit = np.array([avaliador(ind) for ind in pop])
    best_i = np.argmin(fit)
    gbest, gbest_f = pop[best_i].copy(), fit[best_i]

    for _ in range(gens):
        new = list(pop[np.argsort(fit)[:2]])  # elitismo (2)
        while len(new) < pop_size:
            p1 = pop[min(np.random.choice(pop_size, 3, replace=False), key=lambda x: fit[x])]
            p2 = pop[min(np.random.choice(pop_size, 3, replace=False), key=lambda x: fit[x])]
            if np.random.rand() < pc:
                al = np.random.rand(10)
                c1, c2 = al * p1 + (1 - al) * p2, al * p2 + (1 - al) * p1
            else:
                c1, c2 = p1.copy(), p2.copy()
            for c in (c1, c2):
                m = np.random.rand(10) < pm
                c[m] += np.random.normal(0, sigma, m.sum())
                np.clip(c, 0, 1, out=c)
                if len(new) < pop_size:
                    new.append(c)
        pop = np.array(new)
        fit = np.array([avaliador(ind) for ind in pop])
        bi = np.argmin(fit)
        if fit[bi] < gbest_f:
            gbest, gbest_f = pop[bi].copy(), fit[bi]
    return gbest, gbest_f


def run_pso(avaliador, n_particulas=20, iteracoes=10, w=0.7298, c1=1.49618, c2=1.49618):
    """PSO global-best canonico com coeficientes de constricao de Clerc,
    velocidade limitada a |v| <= 0.5 e posicoes confinadas em [0,1]."""
    x = np.random.rand(n_particulas, 10)
    v = np.random.uniform(-0.1, 0.1, (n_particulas, 10))
    fit = np.array([avaliador(xi) for xi in x])

    pbest, pbest_f = x.copy(), fit.copy()
    g = np.argmin(fit)
    gbest, gbest_f = x[g].copy(), fit[g]

    for _ in range(iteracoes):
        r1 = np.random.rand(n_particulas, 10)
        r2 = np.random.rand(n_particulas, 10)
        v = w * v + c1 * r1 * (pbest - x) + c2 * r2 * (gbest - x)
        np.clip(v, -0.5, 0.5, out=v)
        x = np.clip(x + v, 0.0, 1.0)
        fit = np.array([avaliador(xi) for xi in x])

        melhorou = fit < pbest_f
        pbest[melhorou] = x[melhorou]
        pbest_f[melhorou] = fit[melhorou]
        g = np.argmin(pbest_f)
        if pbest_f[g] < gbest_f:
            gbest, gbest_f = pbest[g].copy(), pbest_f[g]
    return gbest, gbest_f


def run_busca_aleatoria(avaliador, orcamento=220):
    """Baseline: amostragem uniforme i.i.d. em [0,1]^10 com o mesmo
    orcamento de avaliacoes dos demais metodos."""
    gbest, gbest_f = None, float('inf')
    for _ in range(orcamento):
        x = np.random.rand(10)
        f = avaliador(x)
        if f < gbest_f:
            gbest, gbest_f = x.copy(), f
    return gbest, gbest_f


# ============================================================
# 4. PROTOCOLO EXPERIMENTAL
# ============================================================
SEMENTES = [42, 43, 44, 45, 46]
ORCAMENTO = 220  # avaliacoes da funcao objetivo por execucao

METODOS = {
    "AG":               lambda av: run_ga(av, pop_size=20, gens=10),
    "PSO":              lambda av: run_pso(av, n_particulas=20, iteracoes=10),
    "Busca Aleatoria":  lambda av: run_busca_aleatoria(av, orcamento=ORCAMENTO),
}


def main():
    t_ini = time.time()
    print("=" * 70)
    print("PARTE 2 - Comparacao experimental: AG x PSO x Busca Aleatoria")
    print("Problema: ajuste de 10 parametros de MFs de controlador fuzzy")
    print(f"Protocolo: {len(SEMENTES)} sementes x {ORCAMENTO} avaliacoes por metodo")
    print("=" * 70)

    # Referencia fixa (sem otimizacao): genes = 0.5
    base_av = AvaliadorFitness()
    base_f = base_av(np.full(10, 0.5))
    print(f"\nReferencia fixa (genes=0.5, sem otimizacao): RMSE = {base_f:.4f} m")

    resultados = {nome: [] for nome in METODOS}   # lista de dicts por execucao
    curvas = {nome: [] for nome in METODOS}       # curvas melhor-ate-agora
    melhores = {}                                 # melhor individuo global por metodo

    for nome, metodo in METODOS.items():
        print(f"\n--- {nome} ---")
        for seed in SEMENTES:
            np.random.seed(seed)
            av = AvaliadorFitness()
            t0 = time.perf_counter()
            ind, f = metodo(av)
            dt = time.perf_counter() - t0
            resultados[nome].append({
                "metodo": nome, "semente": seed, "melhor_fitness": f,
                "tempo_s": dt, "n_avaliacoes": av.n_avaliacoes,
            })
            curvas[nome].append(av.curva)
            if nome not in melhores or f < melhores[nome][1]:
                melhores[nome] = (ind.copy(), f, seed)
            print(f"  semente {seed}: melhor RMSE = {f:.4f} | "
                  f"{av.n_avaliacoes} avals | {dt:.1f} s")

    # ----- Estatisticas agregadas -----
    print("\n" + "=" * 70)
    print(f"{'Metodo':<18} | {'Melhor':>8} | {'Pior':>8} | {'Media':>8} | "
          f"{'DesvPad':>8} | {'Tempo medio':>11}")
    print("-" * 70)
    estatisticas = {}
    for nome in METODOS:
        finais = np.array([r["melhor_fitness"] for r in resultados[nome]])
        tempos = np.array([r["tempo_s"] for r in resultados[nome]])
        estatisticas[nome] = {
            "melhor": finais.min(), "pior": finais.max(),
            "media": finais.mean(), "desvio": finais.std(ddof=1),
            "tempo_medio_s": tempos.mean(),
        }
        e = estatisticas[nome]
        print(f"{nome:<18} | {e['melhor']:>8.4f} | {e['pior']:>8.4f} | "
              f"{e['media']:>8.4f} | {e['desvio']:>8.4f} | {e['tempo_medio_s']:>9.1f} s")
    print(f"{'Referencia fixa':<18} | {base_f:>8.4f} | {'-':>8} | {'-':>8} | "
          f"{'-':>8} | {'-':>11}")

    # ----- CSV com todas as execucoes -----
    with open("resultados/estatisticas_execucoes.csv", "w", newline="", encoding="utf-8") as fcsv:
        wr = csv.DictWriter(fcsv, fieldnames=["metodo", "semente", "melhor_fitness",
                                              "tempo_s", "n_avaliacoes"])
        wr.writeheader()
        for nome in METODOS:
            wr.writerows(resultados[nome])

    # ----- Melhores individuos (reprodutibilidade) -----
    with open("resultados/melhores_individuos.json", "w", encoding="utf-8") as fjson:
        json.dump({nome: {"genes": list(np.round(ind, 6)), "fitness": float(f),
                          "semente": s}
                   for nome, (ind, f, s) in melhores.items()}, fjson, indent=2)

    # ----- Curvas de convergencia (melhor-ate-agora x avaliacoes) -----
    fig, ax = plt.subplots(figsize=(10, 6))
    cores = {"AG": "tab:blue", "PSO": "tab:green", "Busca Aleatoria": "tab:orange"}
    x_av = np.arange(1, ORCAMENTO + 1)
    for nome in METODOS:
        m = np.array(curvas[nome])           # 5 x 220
        ax.plot(x_av, m.mean(axis=0), color=cores[nome], lw=2, label=f"{nome} (media)")
        ax.fill_between(x_av, m.min(axis=0), m.max(axis=0), color=cores[nome], alpha=0.18)
    ax.axhline(base_f, color="k", ls="--", lw=1, label=f"Referencia fixa ({base_f:.3f})")
    ax.set(title="Convergencia: melhor fitness ate a avaliacao n (5 sementes, faixa min-max)",
           xlabel="Numero de avaliacoes da funcao objetivo", ylabel="Melhor RMSE (m)")
    # Recorte na regiao de interesse: as primeiras avaliacoes (com penalidade
    # de nao-conclusao, RMSE > 2000) ficam fora da escala de proposito.
    ax.set_xlim(0, ORCAMENTO)
    ax.set_ylim(1.15, 1.65)
    ax.legend(); ax.grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig("resultados/convergencia_metodos.png", dpi=150)
    plt.close(fig)

    # ----- Boxplot dos resultados finais -----
    fig, ax = plt.subplots(figsize=(8, 5))
    dados = [[r["melhor_fitness"] for r in resultados[nome]] for nome in METODOS]
    ax.boxplot(dados, tick_labels=list(METODOS.keys()))
    ax.axhline(base_f, color="k", ls="--", lw=1, label=f"Referencia fixa ({base_f:.3f})")
    ax.set(title="Distribuicao do melhor RMSE final (5 sementes por metodo)",
           ylabel="Melhor RMSE (m)")
    ax.legend(); ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout(); fig.savefig("resultados/boxplot_metodos.png", dpi=150)
    plt.close(fig)

    # ----- Antes/depois: referencia fixa x melhor solucao global -----
    melhor_global = min(melhores.items(), key=lambda kv: kv[1][1])
    nome_mg, (ind_mg, f_mg, seed_mg) = melhor_global
    print(f"\nMelhor solucao global: {nome_mg} (semente {seed_mg}) "
          f"com RMSE = {f_mg:.4f} m")
    print(f"Genes: {np.round(ind_mg, 3)}")

    ctrl_base = FastFuzzyController(np.full(10, 0.5))
    ctrl_otim = FastFuzzyController(ind_mg)
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for linha, (ctrl, rotulo, cor) in enumerate(
            [(ctrl_base, "Antes (referencia fixa)", "b"),
             (ctrl_otim, f"Depois ({nome_mg} otimizado)", "g")]):
        for ax, track in zip(axes[linha], TRACKS):
            rmse, hx, hy = simulate(ctrl, track)
            ax.plot(track.rx, track.ry, "r--", lw=1.5, label="Referencia")
            ax.plot(hx, hy, cor, lw=1, label=rotulo)
            ax.set_title(f"Pista {track.name} - {rotulo} (RMSE {rmse:.3f})", fontsize=10)
            ax.legend(fontsize=8); ax.set_aspect("equal"); ax.grid(True, alpha=0.3)
    fig.suptitle("Comparacao antes/depois da otimizacao (pontuacao extra - Alternativa 3)")
    fig.tight_layout(); fig.savefig("resultados/antes_depois_trajetorias.png", dpi=150)
    plt.close(fig)

    print(f"\nTempo total do experimento: {(time.time() - t_ini) / 60:.2f} min")
    print("Saidas em ./resultados/: estatisticas_execucoes.csv, "
          "melhores_individuos.json, convergencia_metodos.png, "
          "boxplot_metodos.png, antes_depois_trajetorias.png")


if __name__ == "__main__":
    main()
