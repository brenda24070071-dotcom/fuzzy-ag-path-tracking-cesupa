# Impacto dos Parametros — Tabela Comparativa

Cada linha agrega as execucoes (sementes) de uma configuracao. O **fitness** e o RMSE medio do erro lateral nas 3 pistas (menor = melhor). `base` marca o nivel baseline.

| Parametro | Nivel | base | Fitness medio | Melhor | Pior | Desvio (std) | Tempo medio (s) | Ger. ate estab. | Aval. objetivo |
|---|---:|:---:|---:|---:|---:|---:|---:|---:|---:|
| population_size | 10 |  | 1.3341 | 1.3156 | 1.3837 | 0.0252 | 2.17 | 6.2 | 110 |
| population_size | 20 | X | 1.2926 | 1.2319 | 1.3193 | 0.0317 | 4.18 | 4.0 | 220 |
| population_size | 40 |  | 1.3022 | 1.2633 | 1.3171 | 0.0199 | 8.94 | 2.2 | 440 |
| n_generations | 10 | X | 1.2926 | 1.2319 | 1.3193 | 0.0317 | 4.18 | 4.0 | 220 |
| n_generations | 20 |  | 1.2793 | 1.2319 | 1.3025 | 0.0265 | 10.17 | 9.6 | 420 |
| n_generations | 40 |  | 1.2698 | 1.2304 | 1.2882 | 0.0206 | 26.55 | 15.0 | 820 |
| mutation_rate | 0.1 |  | 1.3217 | 1.2980 | 1.3467 | 0.0199 | 11.48 | 6.2 | 220 |
| mutation_rate | 0.3 | X | 1.2926 | 1.2319 | 1.3193 | 0.0317 | 4.18 | 4.0 | 220 |
| mutation_rate | 0.5 |  | 1.3214 | 1.3046 | 1.3384 | 0.0109 | 11.68 | 5.0 | 220 |
| crossover_rate | 0.5 |  | 1.3019 | 1.2662 | 1.3236 | 0.0191 | 5.27 | 5.4 | 220 |
| crossover_rate | 0.7 | X | 1.2926 | 1.2319 | 1.3193 | 0.0317 | 4.18 | 4.0 | 220 |
| crossover_rate | 0.9 |  | 1.3047 | 1.2724 | 1.3341 | 0.0211 | 4.67 | 6.0 | 220 |
