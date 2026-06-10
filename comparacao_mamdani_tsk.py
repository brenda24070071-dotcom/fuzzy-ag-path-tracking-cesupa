"""
Comparacao experimental Mamdani x TSK (ordem zero) - Trilha de ampliacao
para equipe de 5 integrantes (lauda Parte 1, Secao 6: "Comparacao de modelos").

O controlador TSK reutiliza os MESMOS antecedentes (MFs de entrada) e a mesma
base de 25 regras do controlador Mamdani. A diferenca esta no consequente e na
saida:
  - Mamdani: consequentes fuzzy (AN..AP), implicacao/agregacao min-max e
    defuzzificacao por centroide do conjunto agregado;
  - TSK ordem zero: cada regra produz uma CONSTANTE c_k (tomada como o
    centroide do conjunto de saida correspondente, para comparacao justa) e a
    saida e a MEDIA PONDERADA  omega = sum(w_r * c_r) / sum(w_r), onde o peso
    w_r = min(mu_theta, mu_err) e o grau de ativacao da regra.

Execucao:  python comparacao_mamdani_tsk.py   (~5 s)
Saidas: tabela comparativa no terminal + resultados/comparacao_mamdani_tsk.png
"""
import numpy as np
import matplotlib.pyplot as plt

from fuzzy_path_tracking import (
    FastFuzzyController, TRACKS, simulate, build_fuzzy,
    RULE_MATRIX, trimf, trapmf,
)

# Consequentes constantes do TSK: centroide de cada conjunto de saida Mamdani
# (AN, MN, Z, MP, AP) avaliado em pertinencia plena -> comparacao justa.
# Grade fina (0.01) para nao zerar os triangulos estreitos MN/MP.
_FINE = np.arange(-50.0, 50.0001, 0.01)
_OM_PARAMS = [
    ("trap", [-50, -5, -1, -0.5]),   # AN
    ("tri",  [-1, -0.5, 0]),         # MN
    ("tri",  [-0.5, 0, 0.5]),        # Z
    ("tri",  [0, 0.5, 1]),           # MP
    ("trap", [0.5, 1, 5, 50]),       # AP
]


def _centroide(tipo, p):
    mf = np.array([trimf(x, p) if tipo == "tri" else trapmf(x, p) for x in _FINE])
    return float(np.sum(_FINE * mf) / np.sum(mf))


TSK_CONSTS = [_centroide(t, p) for t, p in _OM_PARAMS]

# Parametros otimizados pelo AG (melhor individuo global, semente 44)
GENES_OTIMIZADOS = np.array([0.826, 0.19, 0.827, 0.844, 0.655,
                             0.642, 0.662, 0.756, 0.563, 0.255])


class FastTSKController(FastFuzzyController):
    """TSK ordem zero com os mesmos antecedentes do Mamdani."""

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

        num, den = 0.0, 0.0
        for r in range(5):
            for col in range(5):
                w = min(te_deg[r], er_deg[col])      # grau de ativacao da regra
                if w > 0:
                    num += w * TSK_CONSTS[RULE_MATRIX[r][col]]
                    den += w
        if den == 0:
            raise Exception("No rules")
        return num / den


CENARIOS = [
    (0.0, 0.0, "Centro, alinhado (caso nulo)"),
    (5.0, 0.0, "Direita, alinhado (erro lateral alto)"),
    (-5.0, 0.0, "Esquerda, alinhado (erro lateral alto)"),
    (0.0, 2.0, "Centro, apontando a esquerda (erro angular alto)"),
    (5.0, 2.0, "Direita, apontando a esquerda (aproximacao)"),
    (-5.0, 2.0, "Esquerda, apontando a esquerda (conflito critico)"),
]


def main():
    print("=" * 72)
    print("COMPARACAO MAMDANI x TSK (trilha de ampliacao - equipe de 5)")
    print("Mesmos antecedentes e 25 regras; muda o consequente e o calculo da saida")
    print("=" * 72)
    print("\nConsequentes TSK (centroides dos conjuntos de saida AN..AP):")
    print("  " + ", ".join(f"{c:+.4f}" for c in TSK_CONSTS))

    for nome, params in [("PARAMETROS BASELINE (genes=0.5)", np.full(10, 0.5)),
                         ("PARAMETROS OTIMIZADOS PELO AG", GENES_OTIMIZADOS)]:
        mam = FastFuzzyController(params)
        tsk = FastTSKController(params)
        print(f"\n--- {nome} ---")
        print(f"  {'Pista':<8} | {'RMSE Mamdani (m)':>17} | {'RMSE TSK (m)':>13}")
        rmses_m, rmses_t = [], []
        for t in TRACKS:
            rm, *_ = simulate(mam, t)
            rt, *_ = simulate(tsk, t)
            rmses_m.append(rm); rmses_t.append(rt)
            print(f"  {t.name:<8} | {rm:>17.4f} | {rt:>13.4f}")
        print(f"  {'MEDIA':<8} | {np.mean(rmses_m):>17.4f} | {np.mean(rmses_t):>13.4f}")

    # Cenarios pontuais com parametros otimizados
    mam = FastFuzzyController(GENES_OTIMIZADOS)
    tsk = FastTSKController(GENES_OTIMIZADOS)
    print(f"\n  {'Cenario (parametros otimizados)':<52} | {'Mamdani':>9} | {'TSK':>9}")
    print("  " + "-" * 76)
    for e_val, th_val, desc in CENARIOS:
        wm = mam.compute(e_val, th_val)
        wt = tsk.compute(e_val, th_val)
        print(f"  {desc:<52} | {wm:>9.4f} | {wt:>9.4f}")

    # Figura: trajetorias Mamdani x TSK (otimizados) nas 3 pistas
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, track in zip(axes, TRACKS):
        rm, hxm, hym = simulate(mam, track)
        rt, hxt, hyt = simulate(tsk, track)
        ax.plot(track.rx, track.ry, "r--", lw=1.5, label="Referencia")
        ax.plot(hxm, hym, "g", lw=1.2, label=f"Mamdani (RMSE {rm:.3f})")
        ax.plot(hxt, hyt, "b:", lw=1.5, label=f"TSK (RMSE {rt:.3f})")
        ax.set_title(f"Pista {track.name}")
        ax.legend(fontsize=8); ax.set_aspect("equal"); ax.grid(True, alpha=0.3)
    fig.suptitle("Mamdani x TSK ordem zero (mesmos antecedentes e regras, parametros otimizados)")
    fig.tight_layout()
    fig.savefig("resultados/comparacao_mamdani_tsk.png", dpi=150)
    plt.close(fig)
    print("\nFigura salva em resultados/comparacao_mamdani_tsk.png")


if __name__ == "__main__":
    main()
