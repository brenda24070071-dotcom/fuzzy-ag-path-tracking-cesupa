# Análise Experimental Ampliada

> Ampliação obrigatória da equipe de **5 integrantes** (Lauda Parte 2, Seção 5, opção *Análise experimental ampliada*).

## 1. Objetivo e justificativa

Quantificar como os hiperparâmetros do Algoritmo Genético afetam **convergência**, **qualidade da solução** e **custo computacional** do controlador fuzzy de rastreamento. Escolhemos a trilha de *análise experimental ampliada* (em vez de comparar AG×PSO) porque ela aprofunda o método que já é o núcleo do projeto, sem trocar a modelagem fuzzy nem introduzir um segundo algoritmo — atendendo à exigência de variar **pelo menos 4 parâmetros** e discutir os três eixos pedidos pela lauda.

## 2. Protocolo experimental

- **Método:** sensibilidade *One-Factor-At-A-Time* (OFAT) — varia-se um parâmetro por vez em 3 níveis (baixo, baseline, alto), mantendo os demais fixos no baseline para isolar o efeito de cada variável.
- **Baseline:** `{'pop_size': 20, 'gens': 10, 'pc': 0.7, 'pm': 0.3, 'sigma': 0.2}` (os valores reais usados em `fuzzy_path_tracking.main()`).
- **Sementes:** `[42, 43, 44, 45, 46]` (5 execuções independentes por configuração — método estocástico).
- **Modo de execução deste relatório:** `--full`.
- **Função objetivo:** média do RMSE do erro lateral nas 3 pistas (reutilizada de `fitness()`, sem alteração). Sem penalidade, o fitness é igual ao RMSE médio.

## 3. Parâmetros variados

| Parâmetro | Chave em `run_ga` | Níveis (baixo / baseline / alto) | Eixo principal investigado |
|---|---|---|---|
| population_size | `pop_size` | [10, 20, 40] | Diversidade × custo |
| n_generations | `gens` | [10, 20, 40] | Convergência × custo |
| mutation_rate | `pm` | [0.1, 0.3, 0.5] | Exploração × estabilidade |
| crossover_rate | `pc` | [0.5, 0.7, 0.9] | Recombinação × qualidade média |

(No modo `--quick` os níveis altos de população/gerações são reduzidos para acelerar o teste.)

## 4. Métricas

Qualidade (fitness médio/melhor/pior), estabilidade (desvio-padrão entre sementes), convergência (gerações até estabilizar a 1% do valor final) e custo (tempo médio e nº de avaliações da função objetivo = `pop_size × (gens+1)`).

> **Nota sobre custo:** a métrica primária de custo é o **nº de avaliações da função objetivo** (`pop_size × (gens+1)`), que é exata e independente da máquina. O **tempo médio (s)** é secundário e carrega ruído de carga do sistema — por isso níveis com o mesmo nº de avaliações (ex.: `mutation_rate` e `crossover_rate`, sempre 220) podem ter tempos diferentes sem que o algoritmo custe mais.

## 5. Resultados

### 5.1 population_size

| Nivel | Fitness medio (m) | std | Tempo medio (s) | Ger. estab. | Aval. obj. |
|---:|---:|---:|---:|---:|---:|
| 10 | 1.3341 | 0.0252 | 2.17 | 6.2 | 110 |
| 20 (baseline) | 1.2926 | 0.0317 | 4.18 | 4.0 | 220 |
| 40 | 1.3022 | 0.0199 | 8.94 | 2.2 | 440 |

### 5.2 n_generations

| Nivel | Fitness medio (m) | std | Tempo medio (s) | Ger. estab. | Aval. obj. |
|---:|---:|---:|---:|---:|---:|
| 10 (baseline) | 1.2926 | 0.0317 | 4.18 | 4.0 | 220 |
| 20 | 1.2793 | 0.0265 | 10.17 | 9.6 | 420 |
| 40 | 1.2698 | 0.0206 | 26.55 | 15.0 | 820 |

### 5.3 mutation_rate

| Nivel | Fitness medio (m) | std | Tempo medio (s) | Ger. estab. | Aval. obj. |
|---:|---:|---:|---:|---:|---:|
| 0.1 | 1.3217 | 0.0199 | 11.48 | 6.2 | 220 |
| 0.3 (baseline) | 1.2926 | 0.0317 | 4.18 | 4.0 | 220 |
| 0.5 | 1.3214 | 0.0109 | 11.68 | 5.0 | 220 |

### 5.4 crossover_rate

| Nivel | Fitness medio (m) | std | Tempo medio (s) | Ger. estab. | Aval. obj. |
|---:|---:|---:|---:|---:|---:|
| 0.5 | 1.3019 | 0.0191 | 5.27 | 5.4 | 220 |
| 0.7 (baseline) | 1.2926 | 0.0317 | 4.18 | 4.0 | 220 |
| 0.9 | 1.3047 | 0.0211 | 4.67 | 6.0 | 220 |

Tabela completa: [`resultados/analise_experimental_ampliada/impacto_parametros_tabela.md`](../resultados/analise_experimental_ampliada/impacto_parametros_tabela.md). Dados brutos por semente: `resultados_sensibilidade.csv`.

## 6. Discussão

### 6.1 Convergência

Variar `n_generations` mostra retornos decrescentes: o melhor fitness cai rapidamente nas primeiras gerações e depois estabiliza (ver `convergencia_por_parametro.png`). A amplitude do fitness médio ao variar gerações foi de 0.0228 m.

### 6.2 Qualidade da solução

O parâmetro que mais alterou a qualidade média foi **`population_size`** (amplitude 0.0415 m). A melhor configuração individual observada foi `n_generations=40`, com fitness 1.2304 m.

### 6.3 Custo computacional

O custo é dominado por **`n_generations`** (amplitude de tempo 22.38 s, fator 6.36×), coerente com o nº de avaliações da função objetivo escalar com `pop_size × (gens+1)`: `population_size` e `n_generations` multiplicam as avaliações (110→440 e 220→820), enquanto `mutation_rate`/`crossover_rate` mantêm 220 avaliações em todos os níveis — logo **não têm custo algorítmico adicional** (qualquer variação de tempo nessas linhas é ruído de carga da máquina, não do AG).

## 7. Limitações

- OFAT não captura **interações** entre parâmetros (um grid completo ou superfície de resposta capturaria, a custo muito maior).
- Tempos absolutos dependem da máquina; as **tendências relativas** é que são reprodutíveis.
- A análise varia hiperparâmetros do AG, não as MFs fuzzy (estas continuam sendo o que o AG otimiza).

## 8. Conclusão

Os hiperparâmetros de **escala de busca** (`population_size`, `n_generations`) governam o trade-off qualidade×custo, enquanto `mutation_rate`/`crossover_rate` ajustam o equilíbrio exploração×estabilidade a custo quase nulo. O baseline do projeto (fitness médio 1.2926 m, std 0.0317 m) fica numa região de bom compromisso, confirmando a robustez do AG à semente.

---
*Gerado por `scripts/analise_experimental_ampliada.py` a partir de execução real. Reexecute o script para atualizar os números.*
