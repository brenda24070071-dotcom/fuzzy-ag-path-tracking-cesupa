"""
Controlador Fuzzy Mamdani otimizado por Algoritmo Genetico (AG)
para rastreamento de trajetoria de robo autonomo tipo bicicleta.
Baseado em: Mancilla et al., "Optimal Fuzzy Controller Design for
Autonomous Robot Path Tracking Using Population-Based Metaheuristics",
Symmetry 2022, 14, 202.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os
import time

os.makedirs("resultados", exist_ok=True)

# --- Parametros do modelo cinematico (Tabela 6 do artigo) ---
L = 2.5            # wheelbase
V_R = 10.0 / 3.0   # velocidade alvo (~3.33 m/s)
DELTA_MAX = np.pi / 4
T_MAX, DT = 50.0, 0.1

# --- Trajetorias de referencia via cubic spline (Tabela 4) ---
class Track:
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
        return self.rx[idx], self.ry[idx], self.rdx[idx], self.rdy[idx]

TRACKS = [
    Track("M", [0,6,12,5,7.5,3,-1],   [0,0,5,6.5,3,5,-2]),
    Track("A", [0,1,2.5,5,7.5,3,-1],  [0,-4,6,6.5,3,5,-2]),
    Track("S", [0,2,2.5,5,7.5,-3,-1], [0,3,6,6.5,5,5,-2]),
]

LABELS = ['AN','MN','Z','MP','AP']
RULE_MATRIX = [
    [4, 4, 4, 3, 2],  # theta_e = AN (AP, AP, AP, MP, Z)
    [3, 3, 3, 3, 2],  # theta_e = MN (MP, MP, MP, MP, Z)
    [4, 2, 2, 2, 0],  # theta_e = Z  (AP, Z, Z, Z, AN)
    [2, 1, 1, 1, 1],  # theta_e = MP (Z, MN, MN, MN, MN)
    [2, 1, 0, 0, 0],  # theta_e = AP (Z, MN, AN, AN, AN)
]

# --- Construcao do controlador Fuzzy (skfuzzy) ---
def build_fuzzy(params):
    """Constrói o sistema via biblioteca skfuzzy para plotagem e cenários manuais."""
    a, f = params[0], params[5]
    b, g = 0.5 + params[1]*1.5, 0.5 + params[6]*1.5
    c, h = params[2]*2.0, params[7]*2.0
    d, i = 0.5 + params[3], 0.5 + params[8]
    e, j = params[4], params[9]

    univ = np.arange(-50.0, 50.1, 0.1)
    te = ctrl.Antecedent(univ, 'theta_e')
    er = ctrl.Antecedent(univ, 'err')
    om = ctrl.Consequent(univ, 'omega')

    te['AN'] = fuzz.trapmf(univ, [-50,-5,-b,-b+c])
    te['MN'] = fuzz.trimf(univ, [-d-e,-d,-d+e])
    te['Z']  = fuzz.trimf(univ, [-a,0,a])
    te['MP'] = fuzz.trimf(univ, [d-e,d,d+e])
    te['AP'] = fuzz.trapmf(univ, [b-c,b,5,50])

    er['AN'] = fuzz.trapmf(univ, [-50,-5,-g,-g+h])
    er['MN'] = fuzz.trimf(univ, [-i-j,-i,-i+j])
    er['Z']  = fuzz.trimf(univ, [-f,0,f])
    er['MP'] = fuzz.trimf(univ, [i-j,i,i+j])
    er['AP'] = fuzz.trapmf(univ, [g-h,g,5,50])

    om['AN'] = fuzz.trapmf(univ, [-50,-5,-1,-0.5])
    om['MN'] = fuzz.trimf(univ, [-1,-0.5,0])
    om['Z']  = fuzz.trimf(univ, [-0.5,0,0.5])
    om['MP'] = fuzz.trimf(univ, [0,0.5,1])
    om['AP'] = fuzz.trapmf(univ, [0.5,1,5,50])

    rules = []
    str_rules = [['AN','MN','Z','MP','AP'][idx] for idx in range(5)]
    for r, te_label in enumerate(LABELS):
        for col, er_label in enumerate(LABELS):
            om_label = str_rules[RULE_MATRIX[r][col]]
            rules.append(ctrl.Rule(te[te_label] & er[er_label], om[om_label]))

    sim = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
    return sim, te, er, om

# --- Motor de Inferencia Mamdani Otimizado em NumPy (~1500x mais rapido que skfuzzy) ---
def trimf(x, abc):
    a, b, c = abc
    if x <= a or x >= c: return 0.0
    if x == b: return 1.0
    if x < b: return (x - a) / (b - a)
    return (c - x) / (c - b)

def trapmf(x, abcd):
    a, b, c, d = abcd
    if x <= a or x >= d: return 0.0
    if b <= x <= c: return 1.0
    if x < b: return (x - a) / (b - a)
    return (d - x) / (d - c)

UNIV_FAST = np.arange(-50.0, 50.1, 1.0)
OM_MFS_FAST = [
    np.array([trapmf(x, [-50,-5,-1,-0.5]) for x in UNIV_FAST]),
    np.array([trimf(x, [-1,-0.5,0]) for x in UNIV_FAST]),
    np.array([trimf(x, [-0.5,0,0.5]) for x in UNIV_FAST]),
    np.array([trimf(x, [0,0.5,1]) for x in UNIV_FAST]),
    np.array([trapmf(x, [0.5,1,5,50]) for x in UNIV_FAST])
]

class FastFuzzyController:
    def __init__(self, params):
        self.a, self.f = params[0], params[5]
        self.b, self.g = 0.5 + params[1]*1.5, 0.5 + params[6]*1.5
        self.c, self.h = params[2]*2.0, params[7]*2.0
        self.d, self.i = 0.5 + params[3], 0.5 + params[8]
        self.e, self.j = params[4], params[9]

    def compute(self, err_val, te_val):
        te_deg = [
            trapmf(te_val, [-50, -5, -self.b, -self.b+self.c]),
            trimf(te_val, [-self.d-self.e, -self.d, -self.d+self.e]),
            trimf(te_val, [-self.a, 0, self.a]),
            trimf(te_val, [self.d-self.e, self.d, self.d+self.e]),
            trapmf(te_val, [self.b-self.c, self.b, 5, 50])
        ]
        er_deg = [
            trapmf(err_val, [-50, -5, -self.g, -self.g+self.h]),
            trimf(err_val, [-self.i-self.j, -self.i, -self.i+self.j]),
            trimf(err_val, [-self.f, 0, self.f]),
            trimf(err_val, [self.i-self.j, self.i, self.i+self.j]),
            trapmf(err_val, [self.g-self.h, self.g, 5, 50])
        ]

        om_deg = [0.0]*5
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

# --- Simulacao cinematica (Euler discreto) usando FastFuzzy ---
def simulate(controller, track):
    xr, yr, th = 0.0, 0.0, 0.0
    hx, hy, ssq = [], [], 0.0
    steps = int(T_MAX / DT)

    for _ in range(steps):
        hx.append(xr); hy.append(yr)
        rx, ry, rdx, rdy = track.closest(xr, yr)

        n = np.hypot(rdx, rdy) + 1e-6
        e_lat = (xr-rx)*rdy/n - (yr-ry)*rdx/n
        e_ang = ((th - np.arctan2(rdy, rdx)) + np.pi) % (2*np.pi) - np.pi

        try:
            w = controller.compute(np.clip(e_lat, -49.99, 49.99), np.clip(e_ang, -49.99, 49.99))
        except Exception:
            return 5000.0, hx, hy

        delta = np.clip(np.arctan(L*w/V_R), -DELTA_MAX, DELTA_MAX)
        xr += V_R * np.cos(th) * DT
        yr += V_R * np.sin(th) * DT
        th += (V_R/L) * np.tan(delta) * DT
        ssq += e_lat**2

    rmse = np.sqrt(ssq / steps)
    if np.hypot(xr - track.rx[-1], yr - track.ry[-1]) > 5.0:
        rmse += 2000.0
    return rmse, hx, hy

# --- Fitness: media do RMSE nas 3 pistas (Eq. 12 do artigo) ---
def fitness(params):
    controller = FastFuzzyController(params)
    return np.mean([simulate(controller, t)[0] for t in TRACKS])

# --- Algoritmo Genetico Real ---
def run_ga(pop_size=30, gens=20, pc=0.7, pm=0.3, sigma=0.2):
    pop = np.random.rand(pop_size, 10)
    fit = np.array([fitness(ind) for ind in pop])
    best_i = np.argmin(fit)
    gbest, gbest_f = pop[best_i].copy(), fit[best_i]
    hist = [gbest_f]
    print(f"  Gen 0 | Best: {gbest_f:.4f}")

    for g in range(1, gens+1):
        new = list(pop[np.argsort(fit)[:2]])  # elitismo (2)
        while len(new) < pop_size:
            p1 = pop[min(np.random.choice(pop_size, 3, replace=False), key=lambda x: fit[x])]
            p2 = pop[min(np.random.choice(pop_size, 3, replace=False), key=lambda x: fit[x])]
            if np.random.rand() < pc:
                al = np.random.rand(10)
                c1, c2 = al*p1 + (1-al)*p2, al*p2 + (1-al)*p1
            else:
                c1, c2 = p1.copy(), p2.copy()
            for c in (c1, c2):
                m = np.random.rand(10) < pm
                c[m] += np.random.normal(0, sigma, m.sum())
                np.clip(c, 0, 1, out=c)
                if len(new) < pop_size:
                    new.append(c)
        pop = np.array(new)
        fit = np.array([fitness(ind) for ind in pop])
        bi = np.argmin(fit)
        if fit[bi] < gbest_f:
            gbest, gbest_f = pop[bi].copy(), fit[bi]
        print(f"  Gen {g} | Best: {gbest_f:.4f} | Mean: {np.mean(fit):.4f}")
        hist.append(gbest_f)
    return gbest, gbest_f, hist

# --- Avaliacao pontual do controlador (6 cenarios) via Skfuzzy ---
def eval_scenarios(fsim, label):
    scenarios = [
        (0.0, 0.0, "Centro, alinhado"),
        (5.0, 0.0, "Direita, alinhado"),
        (-5.0, 0.0, "Esquerda, alinhado"),
        (0.0, 2.0, "Centro, apontando direita"),
        (5.0, 2.0, "Direita + apontando direita (conflito)"),
        (-5.0, 2.0, "Esquerda, apontando centro (aproximacao)"),
    ]
    print(f"\n  {'Cenario':<50} | {label+' (omega)':>20}")
    print("  " + "-"*75)
    for e_val, th_val, desc in scenarios:
        fsim.input['err'], fsim.input['theta_e'] = e_val, th_val
        try:
            fsim.compute()
            out = fsim.output['omega']
        except Exception:
            out = float('nan')
        print(f"  {desc:<50} | {out:>20.4f}")

# --- Visualizacoes ---
def plot_tracks_fast(controller, title, filename, color='b', label_rob='Robo'):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, track in zip(axes, TRACKS):
        rmse, hx, hy = simulate(controller, track)
        ax.plot(track.rx, track.ry, 'r--', lw=1.5, label='Referencia')
        ax.plot(hx, hy, color, lw=1, label=label_rob)
        ax.set_title(f"Pista {track.name} (RMSE: {rmse:.3f})")
        ax.legend(); ax.set_aspect('equal'); ax.grid(True, alpha=0.3)
    fig.suptitle(title, fontsize=14); fig.tight_layout()
    fig.savefig(f"resultados/{filename}", dpi=150); plt.close(fig)

def plot_convergence(histories):
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, h in enumerate(histories):
        ax.plot(h, marker='o', ms=3, label=f"Exec {i+1}")
    ax.set(title="Curvas de Convergencia do AG", xlabel="Geracao", ylabel="Melhor RMSE")
    ax.legend(); ax.grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig("resultados/ag_convergence.png", dpi=150); plt.close(fig)

def plot_mfs(te, er, om):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, var, name in zip(axes, [te, er, om], ['Erro Angular', 'Erro Lateral', 'Omega']):
        for label in ['AN','MN','Z','MP','AP']:
            ax.plot(var.universe, var[label].mf, label=label)
        ax.set_title(name); ax.legend(); ax.grid(True, alpha=0.3)
    fig.suptitle("Funcoes de Pertinencia Otimizadas"); fig.tight_layout()
    fig.savefig("resultados/mfs_otimizadas.png", dpi=150); plt.close(fig)

def plot_surface(fsim):
    """Superficie de controle omega = f(err, theta_e) via skfuzzy."""
    n = 50
    e_range = np.linspace(-5, 5, n)
    t_range = np.linspace(-3, 3, n)
    Z = np.zeros((n, n))
    for i, ev in enumerate(e_range):
        for j, tv in enumerate(t_range):
            fsim.input['err'], fsim.input['theta_e'] = ev, tv
            try:
                fsim.compute()
                Z[j, i] = fsim.output['omega']
            except Exception:
                Z[j, i] = 0
    fig, ax = plt.subplots(figsize=(8, 6))
    cs = ax.contourf(e_range, t_range, Z, levels=20, cmap='RdBu_r')
    fig.colorbar(cs, ax=ax, label='omega')
    ax.set(title="Superficie de Controle", xlabel="Erro Lateral (e)", ylabel="Erro Angular (theta_e)")
    fig.tight_layout(); fig.savefig("resultados/superficie_controle.png", dpi=150); plt.close(fig)

# === MAIN ===
def main():
    t_start = time.time()
    # Parte 1: Baseline Fuzzy (parametros medios)
    print("=" * 60)
    print("PARTE 1: Controlador Fuzzy Baseline")
    print("=" * 60)
    base_params = np.full(10, 0.5)
    base_controller = FastFuzzyController(base_params)
    plot_tracks_fast(base_controller, "Baseline Fuzzy (Sem Otimizacao)", "baseline_trajectories.png")
    base_rmse = fitness(base_params)
    print(f"  RMSE medio baseline: {base_rmse:.4f}")
    
    # Avaliacoes e Graficos via skfuzzy
    fsim_base, *_ = build_fuzzy(base_params)
    eval_scenarios(fsim_base, "Baseline")

    # Parte 2: Otimizacao via AG (5 execucoes independentes)
    print(f"\n{'=' * 60}")
    print("PARTE 2: Otimizacao Evolutiva (AG)")
    print("=" * 60)
    best_ind, best_fit = None, float('inf')
    histories = []
    for run in range(5):
        seed = 42 + run
        np.random.seed(seed)
        print(f"\n--- Execucao {run+1}/5 (seed={seed}) ---")
        ind, fit, hist = run_ga(pop_size=20, gens=10)
        histories.append(hist)
        if fit < best_fit:
            best_fit, best_ind = fit, ind

    print(f"\n  Melhor RMSE global: {best_fit:.4f}")
    print(f"  Parametros: {np.round(best_ind, 3)}")

    # Graficos finais
    plot_convergence(histories)
    
    opt_controller = FastFuzzyController(best_ind)
    plot_tracks_fast(opt_controller, "Fuzzy Otimizado (Pos-AG)", "optimized_trajectories.png", 'g', 'Otimizado')
    
    fsim_opt, te, er, om = build_fuzzy(best_ind)
    plot_mfs(te, er, om)
    plot_surface(fsim_opt)
    eval_scenarios(fsim_opt, "Otimizado")

    # Comparacao final
    print(f"\n{'=' * 60}")
    print("COMPARACAO FINAL")
    print("=" * 60)
    print(f"  Baseline RMSE:   {base_rmse:.4f}")
    print(f"  Otimizado RMSE:  {best_fit:.4f}")
    print(f"  Melhoria:        {(1 - best_fit/base_rmse)*100:.1f}%")
    print(f"  Tempo total:     {(time.time()-t_start)/60:.2f} min")
    print(f"\nGraficos salvos em ./resultados/")

if __name__ == "__main__":
    main()
