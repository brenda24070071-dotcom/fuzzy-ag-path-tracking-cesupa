import numpy as np
import time

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

univ = np.arange(-50.0, 50.1, 5.0)
om_mfs = [
    np.maximum(0, np.minimum(1, np.minimum((univ - (-50))/45, (-0.5 - univ)/0.5))), # AN trapmf[-50,-5,-1,-0.5]
    np.maximum(0, np.minimum((univ - (-1))/0.5, (0 - univ)/0.5)),                   # MN trimf[-1,-0.5,0]
    np.maximum(0, np.minimum((univ - (-0.5))/0.5, (0.5 - univ)/0.5)),               # Z  trimf[-0.5,0,0.5]
    np.maximum(0, np.minimum((univ - 0)/0.5, (1 - univ)/0.5)),                      # MP trimf[0,0.5,1]
    np.maximum(0, np.minimum(1, np.minimum((univ - 0.5)/0.5, (50 - univ)/45)))      # AP trapmf[0.5,1,5,50]
]

# Fix trapmf boundaries manually for exact match:
def get_om_mfs():
    return [
        np.array([trapmf(x, [-50,-5,-1,-0.5]) for x in univ]),
        np.array([trimf(x, [-1,-0.5,0]) for x in univ]),
        np.array([trimf(x, [-0.5,0,0.5]) for x in univ]),
        np.array([trimf(x, [0,0.5,1]) for x in univ]),
        np.array([trapmf(x, [0.5,1,5,50]) for x in univ])
    ]
om_mfs = get_om_mfs()

RULE_MATRIX = [
    [4, 4, 4, 3, 2],
    [3, 3, 3, 3, 2],
    [4, 2, 2, 2, 0],
    [2, 1, 1, 1, 1],
    [2, 1, 0, 0, 0],
]

def fast_compute(te_val, err_val, params):
    a, f = params[0], params[5]
    b, g = 0.5 + params[1]*1.5, 0.5 + params[6]*1.5
    c, h = params[2]*2.0, params[7]*2.0
    d, i = 0.5 + params[3], 0.5 + params[8]
    e, j = params[4], params[9]

    te_deg = [
        trapmf(te_val, [-50, -5, -b, -b+c]),
        trimf(te_val, [-d-e, -d, -d+e]),
        trimf(te_val, [-a, 0, a]),
        trimf(te_val, [d-e, d, d+e]),
        trapmf(te_val, [b-c, b, 5, 50])
    ]
    er_deg = [
        trapmf(err_val, [-50, -5, -g, -g+h]),
        trimf(err_val, [-i-j, -i, -i+j]),
        trimf(err_val, [-f, 0, f]),
        trimf(err_val, [i-j, i, i+j]),
        trapmf(err_val, [g-h, g, 5, 50])
    ]

    om_deg = [0.0]*5
    for r in range(5):
        for col in range(5):
            act = min(te_deg[r], er_deg[col])
            out_mf = RULE_MATRIX[r][col]
            if act > om_deg[out_mf]:
                om_deg[out_mf] = act

    aggregated = np.zeros_like(univ)
    for idx in range(5):
        if om_deg[idx] > 0:
            aggregated = np.maximum(aggregated, np.minimum(om_deg[idx], om_mfs[idx]))

    sum_agg = np.sum(aggregated)
    if sum_agg == 0:
        raise Exception("No rules")
    return np.sum(univ * aggregated) / sum_agg

t0 = time.time()
for _ in range(1500):
    fast_compute(0.5, -0.2, np.full(10, 0.5))
t1 = time.time()
print(f"Time for 1500 inferences: {t1-t0:.4f}s")
