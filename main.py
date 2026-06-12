"""
main.py - Ponto de entrada unico do projeto.

Uso:
    python main.py            # pipeline completo: AG (otimizacao) + evidencias
    python main.py --fast     # apenas evidencias experimentais (sem re-treinar o AG)

Gera todos os artefatos em ./resultados:
    baseline_trajectories.png, optimized_trajectories.png, ag_convergence.png,
    mfs_otimizadas.png, superficie_controle.png, funcoes_pertinencia.png,
    test_scenarios.csv, analise_experimentos.md, best_params.npy
"""
import sys
import os
import numpy as np

import fuzzy_path_tracking as F
import experiments


def run_optimization_and_save():
    """Otimizacao reproducivel (5 execucoes) salvando best_params.npy."""
    print("=" * 60)
    print("OTIMIZACAO EVOLUTIVA (AG) - 5 execucoes independentes")
    print("=" * 60)
    best_ind, best_fit, histories = None, float("inf"), []
    for run in range(5):
        seed = 42 + run
        np.random.seed(seed)
        print(f"\n--- Execucao {run+1}/5 (seed={seed}) ---")
        ind, fit, hist = F.run_ga(pop_size=20, gens=10)
        histories.append(hist)
        if fit < best_fit:
            best_fit, best_ind = fit, ind

    os.makedirs(F"{experiments.RESULTS_DIR}", exist_ok=True)
    np.save(os.path.join(experiments.RESULTS_DIR, "best_params.npy"), best_ind)
    print(f"\n  Melhor RMSE global: {best_fit:.4f}")
    print(f"  Parametros salvos em resultados/best_params.npy")

    # Graficos dependentes do AG
    F.plot_convergence(histories)
    opt = F.FastFuzzyController(best_ind)
    F.plot_tracks_fast(opt, "Fuzzy Otimizado (Pos-AG)",
                       "optimized_trajectories.png", "g", "Otimizado")
    fsim_opt, te, er, om = F.build_fuzzy(best_ind)
    F.plot_mfs(te, er, om)
    F.plot_surface(fsim_opt)

    # Baseline para comparacao
    base = F.FastFuzzyController(np.full(10, 0.5))
    F.plot_tracks_fast(base, "Baseline Fuzzy (Sem Otimizacao)",
                       "baseline_trajectories.png")
    base_rmse = F.fitness(np.full(10, 0.5))
    print(f"\n  Baseline RMSE:  {base_rmse:.4f}")
    print(f"  Otimizado RMSE: {best_fit:.4f}")
    print(f"  Melhoria:       {(1 - best_fit/base_rmse)*100:.1f}%")
    return best_ind


def main():
    fast = "--fast" in sys.argv
    if fast:
        print(">> Modo rapido: gerando evidencias experimentais (sem re-treinar o AG).")
        # Garante que a superficie/baseline existam mesmo sem rodar o AG.
        surf = os.path.join(experiments.RESULTS_DIR, "superficie_controle.png")
        if not os.path.exists(surf):
            params = np.full(10, 0.5)
            fsim, *_ = F.build_fuzzy(params)
            F.plot_surface(fsim)
            base = F.FastFuzzyController(params)
            F.plot_tracks_fast(base, "Baseline Fuzzy", "baseline_trajectories.png")
    else:
        run_optimization_and_save()

    # Evidencias experimentais (CSV + MD + funcoes_pertinencia.png)
    experiments.run()
    print("\nConcluido. Veja a pasta ./resultados/")


if __name__ == "__main__":
    main()
