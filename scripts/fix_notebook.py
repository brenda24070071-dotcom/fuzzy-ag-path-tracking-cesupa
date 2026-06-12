"""
Fix all bugs in the notebook:
1. Cell 6: build_fuzzy universe should be 0.1 for skfuzzy (visualization)
2. Cell 8: simulate must use np.clip(-49.99, 49.99) on inputs
3. Cell 8: dead code in fitness function
4. Cell 25: broken indentation and wrong function call in 8.1
"""
import json

nb = json.load(open('fuzzy_path_tracking.ipynb', encoding='utf-8'))

# === Fix Cell 6: build_fuzzy universe resolution ===
cell6 = nb['cells'][6]
src6 = ''.join(cell6['source'])
src6 = src6.replace(
    "univ = np.arange(-50.0, 50.1, 1.0)  # resolucao 1.0 (10x mais rapido)",
    "univ = np.arange(-50.0, 50.1, 0.1)  # resolucao 0.1 para plotagem"
)
cell6['source'] = [src6]

# === Fix Cell 8: simulate + fitness ===
new_cell8 = """def simulate(controller, track):
    \"\"\"Simula o robo na pista usando Euler discreto e retorna RMSE.\"\"\"
    xr, yr, th = 0.0, 0.0, 0.0
    hx, hy, ssq = [], [], 0.0
    steps = int(T_MAX / DT)

    for _ in range(steps):
        hx.append(xr); hy.append(yr)
        rx, ry, rdx, rdy = track.closest(xr, yr)

        # Erro lateral (produto vetorial) e angular
        n = np.hypot(rdx, rdy) + 1e-6
        e_lat = (xr-rx)*rdy/n - (yr-ry)*rdx/n
        e_ang = ((th - np.arctan2(rdy, rdx)) + np.pi) % (2*np.pi) - np.pi

        try:
            w = controller.compute(np.clip(e_lat, -49.99, 49.99), np.clip(e_ang, -49.99, 49.99))
        except Exception:
            return 5000.0, hx, hy  # penalidade

        delta = np.clip(np.arctan(L*w/V_R), -DELTA_MAX, DELTA_MAX)
        xr += V_R * np.cos(th) * DT
        yr += V_R * np.sin(th) * DT
        th += (V_R/L) * np.tan(delta) * DT
        ssq += e_lat**2

    rmse = np.sqrt(ssq / steps)
    if np.hypot(xr - track.rx[-1], yr - track.ry[-1]) > 5.0:
        rmse += 2000.0
    return rmse, hx, hy

def fitness(params):
    \"\"\"RMSE medio nas 3 pistas (Eq. 12 do artigo).\"\"\"
    controller = FastFuzzyController(params)
    return np.mean([simulate(controller, t)[0] for t in TRACKS])

print('Funcoes de simulacao e fitness definidas.')
"""
nb['cells'][8]['source'] = [new_cell8]
nb['cells'][8]['outputs'] = []

# === Fix Cell 25: 8.1 optimized trajectories ===
new_cell25 = """opt_controller = FastFuzzyController(best_ind)
fsim_opt, te_opt, er_opt, om_opt = build_fuzzy(best_ind)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, track in zip(axes, TRACKS):
    rmse, hx, hy = simulate(opt_controller, track)
    ax.plot(track.rx, track.ry, 'r--', lw=1.5, label='Referencia')
    ax.plot(hx, hy, 'g-', lw=1, label='Otimizado')
    ax.set_title(f'Pista {track.name} (RMSE: {rmse:.3f})')
    ax.legend(); ax.set_aspect('equal'); ax.grid(True, alpha=0.3)
fig.suptitle('Fuzzy Otimizado (Pos-AG)', fontsize=14)
plt.tight_layout()
fig.savefig('resultados/optimized_trajectories.png', dpi=150)
plt.show()
"""
nb['cells'][25]['source'] = [new_cell25]
nb['cells'][25]['outputs'] = []

# Clear all outputs so the notebook is clean for re-execution
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

json.dump(nb, open('fuzzy_path_tracking.ipynb', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("Notebook corrigido com sucesso!")
print()
print("Bugs corrigidos:")
print("  1. Cell 6: build_fuzzy universe 1.0 -> 0.1 (para graficos corretos via skfuzzy)")
print("  2. Cell 8: np.clip(-49.99, 49.99) adicionado no simulate (evita 'No rules' exception)")
print("  3. Cell 8: dead code removido da funcao fitness")
print("  4. Cell 25: indentacao e chamada simulate(opt_controller, track) corrigidas")
