# Arguição — Análise Experimental Ampliada (respostas curtas)

**Por que a equipe escolheu análise experimental ampliada?**  
Porque aprofunda o algoritmo que já é o núcleo do projeto (o AG), atendendo à ampliação obrigatória sem trocar a modelagem fuzzy nem introduzir um segundo algoritmo. Variamos 4 hiperparâmetros e medimos impacto em convergência, qualidade e custo.

**Quais 4 parâmetros foram variados?**  
`population_size`, `n_generations`, `mutation_rate` (taxa de mutação por gene) e `crossover_rate`, cada um em 3 níveis (baixo/baseline/alto), método OFAT.

**Por que usar múltiplas sementes?**  
O AG é estocástico; rodamos 5 sementes ([42, 43, 44, 45, 46]) por configuração para separar efeito real do parâmetro do ruído de inicialização. O desvio-padrão entre sementes mede a robustez.

**Qual parâmetro mais afetou a convergência/qualidade?**  
`population_size` — maior variação do fitness médio entre níveis (0.0415 m).

**Qual parâmetro mais afetou o custo computacional?**  
`n_generations` — fator de 6.36× no tempo entre o nível baixo e o alto. Custo escala com `pop_size × (gens+1)`.

**O que os resultados mostram sobre a robustez do AG?**  
No baseline, o melhor fitness varia pouco entre sementes (std 0.0317 m em torno de 1.2926 m), indicando convergência consistente e baixa dependência da semente.

**Quais limitações ainda existem?**  
OFAT não mede interações entre parâmetros; tempos absolutos dependem da máquina; e a análise cobre os hiperparâmetros do AG, não a dinâmica do controlador fuzzy em si.
