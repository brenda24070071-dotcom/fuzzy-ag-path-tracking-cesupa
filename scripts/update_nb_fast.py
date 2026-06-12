import json

f = open(r'c:\Users\Kzar\Documents\Faculade\Fuzzy\fuzzy_path_tracking.ipynb', 'r', encoding='utf-8')
nb = json.load(f)
f.close()

# Encontrar o indice das celulas importantes
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    
    # Imports: Add time and cKDTree
    if 'import skfuzzy as fuzz' in src and 'cKDTree' not in src:
        new_lines = []
        for line in cell['source']:
            new_lines.append(line)
            if 'from scipy.interpolate import CubicSpline' in line:
                new_lines.append('from scipy.spatial import cKDTree\n')
            if 'import os' in line:
                new_lines.append('import time\n')
        cell['source'] = new_lines

    # Track class: add KDTree
    if 'class Track:' in src and 'cKDTree' not in src:
        new_lines = []
        for line in cell['source']:
            if 'np.linspace(0, 1, 1000)' in line:
                line = line.replace('1000', '500')
            if 'self.rdx, self.rdy' in line:
                new_lines.append(line)
                new_lines.append('        self.tree = cKDTree(np.column_stack([self.rx, self.ry]))\n')
                continue
            if 'np.argmin' in line:
                line = line.replace(
                    'idx = np.argmin((self.rx - x)**2 + (self.ry - y)**2)',
                    '_, idx = self.tree.query([x, y])'
                )
            new_lines.append(line)
        cell['source'] = new_lines

    # Build fuzzy: add FastFuzzyController
    if 'def build_fuzzy(params):' in src and 'FastFuzzyController' not in src:
        fast_code = """
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
        return np.sum(UNIV_FAST * aggregated) / sum_agg\n"""
        
        # we will append it
        cell['source'] = cell['source'] + [fast_code]

    # Simulate function
    if 'def simulate(' in src and 'controller.compute' not in src:
        new_lines = []
        for line in cell['source']:
            line = line.replace('def simulate(fsim, track):', 'def simulate(controller, track):')
            line = line.replace('fsim.input', '# fsim.input')
            line = line.replace('fsim.compute()', 'w = controller.compute(np.clip(e_lat, -49.99, 49.99), np.clip(e_ang, -49.99, 49.99))')
            line = line.replace("w = fsim.output['omega']", '# w = fsim.output')
            line = line.replace('def fitness(params):', 'def fitness(params):\n    controller = FastFuzzyController(params)\n    return np.mean([simulate(controller, t)[0] for t in TRACKS])\n')
            if 'fsim, *_ = build_fuzzy(params)' in line: continue
            if 'return np.mean([simulate(fsim, t)[0] for t in TRACKS])' in line: continue
            new_lines.append(line)
        cell['source'] = new_lines

    # Baseline exec
    if 'fsim_base, te_base, er_base, om_base = build_fuzzy(base_params)' in src and 'FastFuzzyController' not in src:
        new_lines = []
        for line in cell['source']:
            if 'fsim_base,' in line:
                new_lines.append('base_controller = FastFuzzyController(base_params)\n')
                new_lines.append(line)
            else:
                new_lines.append(line)
        cell['source'] = new_lines

    # plot_tracks baseline
    if 'simulate(fsim_base, track)' in src and 'FastFuzzyController' not in src:
        new_lines = []
        for line in cell['source']:
            line = line.replace('simulate(fsim_base, track)', 'simulate(base_controller, track)')
            new_lines.append(line)
        cell['source'] = new_lines

    # Final optimized plot
    if 'fsim_opt, te_opt, er_opt, om_opt = build_fuzzy(best_ind)' in src and 'FastFuzzyController' not in src:
        new_lines = []
        for line in cell['source']:
            if 'fsim_opt,' in line:
                new_lines.append('opt_controller = FastFuzzyController(best_ind)\n')
                new_lines.append(line)
            elif 'simulate(fsim_opt, track)' in line:
                line = line.replace('simulate(fsim_opt, track)', 'simulate(opt_controller, track)')
                new_lines.append(line)
            else:
                new_lines.append(line)
        cell['source'] = new_lines
        
    # fix RULE_MATRIX strings to ints
    if "RULE_MATRIX = [" in src and "'AP','AP'" in src:
        cell['source'] = [line.replace("['AP','AP','AP','MP','Z']", "[4, 4, 4, 3, 2]")
                          .replace("['MP','MP','MP','MP','Z']", "[3, 3, 3, 3, 2]")
                          .replace("['AP','Z', 'Z', 'Z', 'AN']", "[4, 2, 2, 2, 0]")
                          .replace("['Z', 'MN','MN','MN','MN']", "[2, 1, 1, 1, 1]")
                          .replace("['Z', 'MN','AN','AN','AN']", "[2, 1, 0, 0, 0]")
                          for line in cell['source']]
        # also need to rewrite build_fuzzy rules to use ints
        # we will just add str_rules
        new_lines2 = []
        for line in cell['source']:
            if 'rules.append(ctrl.Rule(te[te_label] & er[er_label], om[RULE_MATRIX[r][col]]))' in line:
                new_lines2.append("            str_rules = ['AN','MN','Z','MP','AP']\n")
                new_lines2.append("            om_label = str_rules[RULE_MATRIX[r][col]]\n")
                new_lines2.append("            rules.append(ctrl.Rule(te[te_label] & er[er_label], om[om_label]))\n")
            else:
                new_lines2.append(line)
        cell['source'] = new_lines2

f = open(r'c:\Users\Kzar\Documents\Faculade\Fuzzy\fuzzy_path_tracking.ipynb', 'w', encoding='utf-8')
json.dump(nb, f, ensure_ascii=False, indent=1)
f.close()
print('Notebook atualizado com sucesso para FastFuzzyController!')
