# AG × PSO × Busca Aleatória na Otimização de um Controlador Fuzzy de Rastreamento de Trajetória: Replicação Experimental de Mancilla et al. (2022)

**Disciplina:** Inteligência Artificial e Computacional (0700M8) — CESUPA
**Trabalho:** Parte 2 — IA Evolutiva e Computação Bioinspirada · **Opção 1: Pesquisa Científica**
**Turma:** `<PREENCHER: CC5MA ou CC5NA>`
**Equipe:** `<PREENCHER: nomes completos dos integrantes>`
**Pontuação extra solicitada:** Alternativa 3 — Otimização automática de parâmetros Fuzzy (comparação antes/depois na Seção 6.4)
**Repositório GitHub:** <https://github.com/brenda24070071-dotcom/fuzzy-ag-path-tracking-cesupa> — Parte 2 na pasta `parte2-evolutiva/`; Parte 1 (modelagem fuzzy) na raiz

---

## Resumo

Este trabalho executa um protocolo experimental controlado comparando três métodos de
busca — **Algoritmo Genético (AG)** real-coded, **Otimização por Enxame de Partículas
(PSO)** canônico e **Busca Aleatória** uniforme (baseline) — no problema de ajuste
automático dos 10 parâmetros das funções de pertinência de um controlador fuzzy Mamdani de
rastreamento de trajetória, replicando o cerne do artigo-base (Mancilla et al., *Symmetry*,
2022): avaliar metaheurísticas populacionais nesse problema. Com orçamento idêntico de
**220 avaliações** da função objetivo por execução e **5 execuções independentes** por
método (sementes 42–46), todos os métodos reduziram o RMSE de rastreamento em 16–21% sobre
a referência fixa (1,5601 m). O AG obteve a melhor média (**1,2926 m**) e o melhor
resultado global (**1,2319 m**); o PSO foi o mais estável (desvio-padrão 0,0156); e a
busca aleatória ficou surpreendentemente competitiva (média 1,3208 m) — um resultado
honesto que discutimos criticamente em termos de orçamento de busca, dimensionalidade e
geometria da paisagem de fitness.

## 1. Problema e abordagem escolhida

**Abordagem (Opção 1):** replicação experimental adaptada de artigo científico recente,
com protocolo próprio de comparação contra baseline.

**Problema concreto:** controladores fuzzy dependem fortemente da forma e posição das
funções de pertinência (MFs). O ajuste manual é trabalhoso e subótimo. O artigo-base
formula o ajuste como **problema de otimização contínua** resolvido por metaheurísticas
populacionais, avaliando cada candidato por simulação de um robô que segue pistas de
referência. Nós replicamos essa formulação e acrescentamos um baseline de busca aleatória
— exigência metodológica clássica para verificar se a "inteligência" do método agrega
valor sobre amostragem pura com o mesmo custo.

### 1.1 Formulação como busca/otimização

| Elemento | Definição |
|---|---|
| Variáveis de decisão | `p = (p0, …, p9) ∈ [0,1]^10` — parâmetros que definem larguras, centros e rampas das MFs das duas entradas do controlador (5 por variável) |
| Espaço de busca | Hipercubo contínuo `[0,1]^10` (parâmetros normalizados; desnormalização interna por escalas fixas) |
| Função objetivo | `f(p) = média do RMSE do erro lateral nas 3 pistas (M, A, S)` — **minimização** |
| Restrições | Caixa `[0,1]^10`, imposta por *clipping* nos três métodos |
| Factibilidade | Penalidade de **+2000** quando o robô não completa a pista em T_MAX = 50 s; **5000** quando a inferência fuzzy falha (cobertura nula) — soluções inviáveis são fortemente desfavorecidas, sem descarte |
| Métricas | Melhor/pior/média/desvio-padrão do fitness final (5 sementes); curva de convergência por avaliação; tempo médio; nº de avaliações |

## 2. Artigo-base e justificativa

**Referência completa:** MANCILLA, A.; GARCÍA-VALDEZ, M.; CASTILLO, O.; MERELO-GUERVÓS,
J. J. Optimal Fuzzy Controller Design for Autonomous Robot Path Tracking Using
Population-Based Metaheuristics. *Symmetry*, v. 14, n. 2, art. 202, 2022.
DOI: 10.3390/sym14020202.

**Justificativa da escolha:** (i) publicado em **2022** — dentro da janela de 7 anos
exigida; (ii) periódico indexado (MDPI *Symmetry*, Scopus/JCR); (iii) metodologia clara e
replicável no escopo da disciplina: descreve o modelo cinemático, as pistas (pontos de
controle + spline), a estrutura do controlador (2 entradas × 5 termos, 25 regras Mamdani)
e a função objetivo (RMSE); (iv) o tema central do artigo — **comparar metaheurísticas
populacionais** no ajuste de MFs — é exatamente o objeto desta Parte 2; (v) continuidade
com a Parte 1 do trabalho, que reproduziu a modelagem fuzzy do mesmo artigo (lá o foco era
o sistema fuzzy; aqui é o experimento evolutivo).

**Leitura técnica (síntese):** problema = rastreamento de trajetória; objetivo = minimizar
erro lateral; variáveis de decisão = parâmetros das MFs de entrada; representação = vetor
real; aptidão = RMSE médio em múltiplas pistas; operadores = os de cada metaheurística;
protocolo = múltiplas execuções independentes por método; limitação = resultados
dependentes de orçamento e implementação.

## 3. Algoritmos implementados

### 3.1 Algoritmo Genético (AG) real-coded

| Componente | Escolha |
|---|---|
| Representação | Vetor real de 10 genes em `[0,1]` |
| População | 20 indivíduos, inicialização uniforme |
| Seleção | Torneio de 3 |
| Cruzamento | Aritmético por gene (`c1 = α·p1 + (1−α)·p2`, α ~ U(0,1) por gene), taxa 0,7 |
| Mutação | Gaussiana (σ = 0,2), taxa 0,3 por gene, com *clip* em `[0,1]` |
| Elitismo | 2 melhores preservados por geração |
| Parada | 10 gerações (orçamento: 20 + 10×20 = 220 avaliações) |

É **o mesmo AG da Parte 1** (mesmo código e parâmetros), o que permite verificação
cruzada: as 5 execuções reproduzem aqui exatamente os mesmos valores finais obtidos lá.

### 3.2 PSO (global best) canônico

| Componente | Escolha |
|---|---|
| Enxame | 20 partículas; posições U(0,1)^10; velocidades U(−0,1, 0,1) |
| Atualização | `v ← w·v + c1·r1·(pbest − x) + c2·r2·(gbest − x)`; `x ← x + v` |
| Coeficientes | w = 0,7298; c1 = c2 = 1,49618 (valores de constrição de Clerc–Kennedy) |
| Limites | Velocidade limitada a \|v\| ≤ 0,5; posição confinada em `[0,1]` por *clip* |
| Parada | 10 iterações (orçamento: 20 + 10×20 = 220 avaliações) |

### 3.3 Busca Aleatória (baseline)

220 amostras i.i.d. uniformes em `[0,1]^10`, guardando a melhor. Mesmo orçamento dos
demais — qualquer vantagem das metaheurísticas deve aparecer *acima* desse piso.

## 4. Metodologia experimental

- **5 execuções independentes por método**, sementes fixas **42–46** (exigência da lauda
  para métodos estocásticos; garante reprodutibilidade exata).
- **Orçamento idêntico**: 220 avaliações da função objetivo por execução, contadas por um
  invólucro (`AvaliadorFitness`) que também registra a curva de melhor-até-agora por
  avaliação — comparação justa por custo, não por "geração".
- **Mesma função objetivo** para todos: simulação determinística do robô (passo de Euler
  0,1 s) nas mesmas 3 pistas.
- **Referência fixa (antes da otimização):** controlador com todos os genes em 0,5 —
  RMSE = **1,5601 m**.
- **Ambiente:** Python 3.14, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.10.9, Windows 11;
  tempo total do experimento ≈ **1,3 min**.

## 5. Resultados

### 5.1 Tabela-resumo (RMSE final em metros, 5 sementes por método)

| Método | Melhor | Pior | Média | Desv. padrão | Tempo médio/execução | Avaliações |
|---|---|---|---|---|---|---|
| **AG** | **1,2319** | 1,3193 | **1,2926** | 0,0354 | 6,0 s | 220 |
| **PSO** | 1,2966 | 1,3349 | 1,3126 | **0,0156** | 5,9 s | 220 |
| Busca Aleatória | 1,2866 | 1,3487 | 1,3208 | 0,0246 | **3,0 s** | 220 |
| Referência fixa | 1,5601 | — | — | — | — | 1 |

Resultados por execução em `resultados/estatisticas_execucoes.csv`; melhores vetores de
genes em `resultados/melhores_individuos.json`.

### 5.2 Convergência

`resultados/convergencia_metodos.png` mostra o melhor fitness até a n-ésima avaliação
(média e faixa min–max das 5 sementes). Leitura: (i) todos os métodos encontram soluções
factíveis (que completam as 3 pistas) nas primeiras ~10 avaliações; (ii) o grosso do ganho
ocorre até ~60 avaliações; (iii) depois disso o AG segue melhorando lentamente (mutação +
elitismo), o PSO estabiliza cedo (convergência do enxame para o gbest) e a busca aleatória
melhora apenas por sorte decrescente — padrão coerente com a teoria.

### 5.3 Estabilidade

Boxplot em `resultados/boxplot_metodos.png`. O PSO apresentou a menor variância entre
sementes (0,0156) — o enxame converge consistentemente para soluções de qualidade
semelhante. O AG tem variância maior, porém com cauda *boa*: foi o único a atingir 1,2319
(semente 44). A busca aleatória varia mais e tem a pior média, como esperado.

### 5.4 Antes × depois (pontuação extra — Alternativa 3)

A otimização automática de parâmetros fuzzy reduziu o RMSE de **1,5601 m → 1,2319 m
(−21,0%)** na melhor solução global (AG, semente 44). As trajetórias antes/depois nas 3
pistas estão em `resultados/antes_depois_trajetorias.png` — visivelmente menos sobressinal
nas curvas fechadas. A leitura dos genes otimizados (zona morta angular alargada de 0,5
para 0,83; termos médios do erro lateral estreitados) está documentada na Parte 1
(`docs/funcoes_de_pertinencia.md` daquele repositório).

### 5.5 Custo computacional

AG e PSO: ≈ 6 s por execução (220 avaliações + sobrecarga dos operadores, desprezível
frente ao custo da simulação). Busca aleatória: ≈ 3 s — *mais rápida por avaliação* porque
amostras aleatórias ruins frequentemente divergem cedo ou falham na inferência,
encerrando a simulação antes; já AG/PSO concentram avaliações em controladores bons, que
completam as pistas inteiras (mais passos simulados por avaliação). O custo é dominado
pelo número de passos de simulação, não pelos operadores dos métodos.

## 6. Análise crítica e comparação

**Semelhanças com o artigo-base:** replicamos a tendência central reportada —
metaheurísticas populacionais ajustam MFs com ganho consistente sobre a configuração
não otimizada (−16% a −21% de RMSE), com AG e PSO chegando a soluções de qualidade
comparável entre si.

**Diferenças e causas prováveis de divergência:** não comparamos valores absolutos de
RMSE com o artigo porque (i) nosso orçamento é deliberadamente pequeno (220 avaliações
contra populações/iterações maiores no artigo); (ii) detalhes de implementação diferem
(integração de Euler, critério de chegada, discretização do centroide, convenção de
sinais documentada na Parte 1); (iii) o artigo avalia mais metaheurísticas e variantes.
Com orçamentos diferentes, comparação absoluta seria metodologicamente inválida — por
isso ancoramos a comparação no baseline interno (busca aleatória e referência fixa).

**O achado mais interessante (e honesto):** a busca aleatória ficou a apenas ~2% da média
do AG. Três fatores explicam: (1) **orçamento pequeno** — 220 avaliações dão às
metaheurísticas pouco tempo para explorar *e* explotar; (2) **paisagem benigna na região
central** — a parametrização `[0,1]^10` foi desenhada (no artigo-base) para que qualquer
ponto razoável gere um controlador funcional; amostras uniformes caem com frequência em
bacias boas; (3) **dimensionalidade moderada** (10-D). A vantagem das metaheurísticas
aparece na *cauda da qualidade*: nenhuma execução da busca aleatória alcançou o 1,2319 do
AG, e a média do AG é a melhor com significância prática. Lição metodológica: **sem o
baseline de busca aleatória, seria fácil superestimar o mérito dos métodos** — exatamente
o motivo de a lauda exigir comparação.

**AG × PSO:** o AG explorou melhor (mutação gaussiana mantém diversidade; elitismo protege
o melhor), enquanto o PSO explotou mais rápido e estagnou (todas as partículas atraídas
para o gbest em 10 iterações). Com orçamento maior, espera-se o PSO recuperar terreno —
hipótese verificável em trabalho futuro.

**Limitações do experimento:** orçamento pequeno (decisão consciente para viabilizar 15
execuções completas no escopo da disciplina); 5 sementes permitem estatística descritiva,
mas não testes de hipótese robustos (n pequeno); apenas três métodos (o artigo-base inclui
outros); função objetivo determinística dada a semente (sem ruído de medição).

## 7. Conclusão

O protocolo experimental comparou AG, PSO e busca aleatória sob orçamento idêntico no
ajuste de parâmetros de um controlador fuzzy de rastreamento, replicando o núcleo
metodológico de Mancilla et al. (2022). O AG apresentou a melhor média (1,2926 m) e o
melhor resultado global (1,2319 m; −21,0% sobre a referência fixa), o PSO a maior
estabilidade, e o baseline aleatório revelou que, neste orçamento e paisagem, parte do
ganho vem da amostragem em si — análise crítica que consideramos o principal aprendizado
científico do trabalho. Trabalhos futuros: orçamentos maiores, mais sementes com teste
estatístico (Wilcoxon), DE e variantes de PSO com reinicialização, e co-otimização das MFs
de saída.

## Declaração de uso de IA

A equipe utilizou IA agêntica (Claude Code, Anthropic) para implementação do script
experimental (reutilizando o núcleo validado na Parte 1), rascunho da documentação e
revisão de coerência. Todo o material foi revisado, executado e validado pelos
integrantes, que assumem integral responsabilidade pelo conteúdo. Declaração completa:
`docs/declaracao_uso_ia.md`.

## Referências

[1] MANCILLA, A.; GARCÍA-VALDEZ, M.; CASTILLO, O.; MERELO-GUERVÓS, J. J. Optimal Fuzzy
Controller Design for Autonomous Robot Path Tracking Using Population-Based
Metaheuristics. *Symmetry*, v. 14, n. 2, art. 202, 2022. DOI: 10.3390/sym14020202.

[2] HOLLAND, J. H. *Adaptation in Natural and Artificial Systems*. Ann Arbor: University
of Michigan Press, 1975.

[3] KENNEDY, J.; EBERHART, R. Particle swarm optimization. In: *Proceedings of the IEEE
International Conference on Neural Networks*, Perth, 1995. p. 1942–1948.

[4] CLERC, M.; KENNEDY, J. The particle swarm — explosion, stability, and convergence in
a multidimensional complex space. *IEEE Transactions on Evolutionary Computation*, v. 6,
n. 1, p. 58–73, 2002.

[5] CORDÓN, O.; HERRERA, F.; HOFFMANN, F.; MAGDALENA, L. *Genetic Fuzzy Systems:
Evolutionary Tuning and Learning of Fuzzy Knowledge Bases*. Singapore: World Scientific,
2001.

[6] BERGSTRA, J.; BENGIO, Y. Random search for hyper-parameter optimization. *Journal of
Machine Learning Research*, v. 13, p. 281–305, 2012.

[7] MAMDANI, E. H.; ASSILIAN, S. An experiment in linguistic synthesis with a fuzzy logic
controller. *International Journal of Man-Machine Studies*, v. 7, n. 1, p. 1–13, 1975.

**Ferramentas:** Python, NumPy, SciPy, Matplotlib, Git/GitHub.
