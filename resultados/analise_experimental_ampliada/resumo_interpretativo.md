# Resumo Interpretativo — Analise de Sensibilidade do AG

Baseline: `{'pop_size': 20, 'gens': 10, 'pc': 0.7, 'pm': 0.3, 'sigma': 0.2}` · Sementes: `[42, 43, 44, 45, 46]`.

## Sensibilidade por parametro

| Parametro | Amplitude do fitness medio | Amplitude do tempo (s) | Fator de tempo (alto/baixo) |
|---|---:|---:|---:|
| population_size | 0.0415 | 6.77 | 4.12x |
| n_generations | 0.0228 | 22.38 | 6.36x |
| mutation_rate | 0.0291 | 7.51 | 2.80x |
| crossover_rate | 0.0121 | 1.10 | 1.26x |

## Leitura dos numeros

- **Parametro mais sensivel para a QUALIDADE da solucao:** `population_size` (maior variacao do fitness medio entre niveis: 0.0415 m).
- **Parametro mais sensivel para o CUSTO computacional:** `n_generations` (maior variacao de tempo: 22.38 s; fator 6.36x).
- **Estabilidade no baseline (robustez a semente):** desvio-padrao do melhor fitness = 0.0317 m em torno de 1.2926 m.
- **Melhor configuracao observada:** `n_generations=40` atingiu o melhor fitness individual de 1.2304 m.

## Interpretacao tecnica

- **Convergencia:** aumentar `n_generations` e `population_size` tende a reduzir o melhor fitness ate um plato — alem dele, ganham-se avaliacoes (custo) sem ganho proporcional de qualidade (retornos decrescentes).
- **Qualidade:** o efeito de `mutation_rate` e `crossover_rate` aparece na exploracao do espaco de 10 genes; mutacao alta demais adiciona ruido e aumenta o desvio entre sementes, mutacao baixa demais arrisca estagnacao.
- **Custo:** o tempo escala diretamente com o numero de avaliacoes da funcao objetivo = `pop_size x (gens + 1)`; por isso `population_size` e `n_generations` dominam o custo, enquanto `pm`/`pc` praticamente nao o alteram.
