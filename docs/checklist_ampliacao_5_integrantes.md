# Checklist — Ampliação Obrigatória (Equipe de 5 Integrantes)

> Trilha escolhida: **Análise Experimental Ampliada** (Lauda Parte 2, Seção 5, opção 2 —
> *"realizar estudo de ablação ou sensibilidade, variando ao menos quatro parâmetros
> relevantes e discutindo impactos sobre convergência, qualidade da solução e custo
> computacional"*).
>
> Status: **ATENDIDO** / **PARCIAL** / **PENDENTE**. Evidências = arquivos reais gerados
> por execução (`python scripts/analise_experimental_ampliada.py --full`, 426 s).

## Exigências da lauda (Parte 2, Seção 5)

| # | Requisito | Status | Evidência |
|---|---|:---:|---|
| 1 | Estudo de ablação/sensibilidade | **ATENDIDO** | Método OFAT em [scripts/analise_experimental_ampliada.py](../scripts/analise_experimental_ampliada.py) |
| 2 | Variar **≥ 4 parâmetros** relevantes | **ATENDIDO** | `population_size`, `n_generations`, `mutation_rate`, `crossover_rate` (3 níveis cada) — ver `resumo_estatistico.csv` |
| 3 | Discutir impacto na **convergência** | **ATENDIDO** | §6.1 de [docs/analise_experimental_ampliada.md](analise_experimental_ampliada.md) + `convergencia_por_parametro.png` |
| 4 | Discutir impacto na **qualidade da solução** | **ATENDIDO** | §6.2 do doc + `comparacao_fitness_boxplot.png` (mais sensível: `population_size`, Δ0.0415 m) |
| 5 | Discutir impacto no **custo computacional** | **ATENDIDO** | §6.3 do doc + `tempo_medio_por_configuracao.png` (dominado por `n_generations`, 6.36×) |

## Requisitos metodológicos (Parte 2, Seções 4 e 9)

| # | Requisito | Status | Evidência |
|---|---|:---:|---|
| 6 | **≥ 5 execuções independentes** com sementes distintas (método estocástico) | **ATENDIDO** | Sementes 42–46; `resultados_sensibilidade.csv` (60 execuções no modo `--full`) |
| 7 | Métrica de **qualidade da solução** (melhor/média/pior/desvio) | **ATENDIDO** | Colunas `fitness_medio/min/max/std` em `resumo_estatistico.csv` |
| 8 | Métrica de **convergência** (gerações até estabilizar) | **ATENDIDO** | Coluna `geracoes_estab_media` (tolerância 1%) |
| 9 | Métrica de **estabilidade** (variação entre sementes) | **ATENDIDO** | Coluna `fitness_std`; baseline = 0.0317 m (robusto) |
| 10 | Métrica de **custo computacional** | **ATENDIDO** | Colunas `tempo_medio_s` e `n_avaliacoes_objetivo` = `pop_size×(gens+1)` |
| 11 | Tabelas e gráficos | **ATENDIDO** | 2 CSVs + 3 PNGs + `impacto_parametros_tabela.md` |
| 12 | Discussão técnica pronta para o relatório | **ATENDIDO** | [docs/analise_experimental_ampliada.md](analise_experimental_ampliada.md) (§1–8, paste-ready) |
| 13 | Reprodutibilidade (comando + dependências) | **ATENDIDO** | README §"Análise Experimental Ampliada"; usa as mesmas deps de `requirements.txt` |
| 14 | **Não quebrar** o sistema principal | **ATENDIDO** | Nenhuma linha de `fuzzy_path_tracking.py` alterada; `import` e `main()` intactos |
| 15 | Sem resultados inventados | **ATENDIDO** | Todos os números vêm de execução real; docs regeneráveis pelo script |
| 16 | Preparação para arguição individual | **ATENDIDO** | [docs/arguicao_analise_experimental.md](arguicao_analise_experimental.md) (7 perguntas-chave) |

## Arquivos gerados (evidências)

```
scripts/analise_experimental_ampliada.py                 # camada experimental isolada (NÃO altera o core)
resultados/analise_experimental_ampliada/
  resultados_sensibilidade.csv                           # 1 linha por (parâmetro, nível, semente)
  resumo_estatistico.csv                                 # 1 linha por configuração (agregado entre sementes)
  convergencia_por_parametro.png                         # curvas de convergência por nível
  comparacao_fitness_boxplot.png                         # distribuição do melhor fitness por nível
  tempo_medio_por_configuracao.png                       # custo médio por configuração
  impacto_parametros_tabela.md                           # tabela comparativa completa
  resumo_interpretativo.md                               # leitura automática dos números
docs/
  analise_experimental_ampliada.md                       # seção pronta para o relatório
  arguicao_analise_experimental.md                       # respostas curtas para a defesa
  checklist_ampliacao_5_integrantes.md                   # este arquivo
README.md                                                # seção de execução adicionada
```

## Observações

- **Nota:** esta ampliação é **obrigatória** para a equipe de 5 integrantes e é
  **distinta** da pontuação extra (otimização AG das MFs), que já existia no projeto.
- O modo `--quick` (3 sementes, níveis reduzidos) existe para validação rápida; os
  números deste checklist e dos docs vêm do modo `--full` (5 sementes).
- Limitação assumida (honestidade metodológica): OFAT não mede **interações** entre
  parâmetros; tempos absolutos dependem da máquina — por isso o custo é reportado também
  como nº de avaliações (métrica independente de hardware).
