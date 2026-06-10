# Levantamento Bibliográfico e Trabalhos Relacionados

Modalidade **Opção A (A1 — Reprodução)**: reprodução mínima viável do artigo principal, com
adaptações declaradas (ver Seção 5).

## 1. Bases e mecanismos de busca utilizados

- **Google Scholar** (busca ampla e por citações)
- **IEEE Xplore** (controle fuzzy e robótica móvel)
- **MDPI** (acesso aberto — artigo principal)
- **ScienceDirect / SpringerLink** (fundamentos e surveys)

## 2. Palavras-chave

- `"fuzzy logic controller" AND "path tracking" AND "mobile robot"`
- `"fuzzy controller" AND ("genetic algorithm" OR "particle swarm") AND optimization`
- `"genetic fuzzy systems"`
- `controle fuzzy rastreamento de trajetória robô móvel`

## 3. Critérios de inclusão e exclusão

**Inclusão:**
1. Publicação revisada por pares (periódico ou conferência) ou livro de referência;
2. Descrição explícita da estrutura do controlador fuzzy (variáveis, termos linguísticos,
   funções de pertinência e/ou base de regras) — condição necessária para reprodução;
3. Aplicação em rastreamento de trajetória/robótica móvel **ou** fundamento teórico
   indispensável (lógica fuzzy, inferência Mamdani/TSK, sistemas genético-fuzzy);
4. Texto completo acessível (acesso aberto ou via instituição).

**Exclusão:**
1. Trabalhos sem detalhamento suficiente do modelo fuzzy para reprodução;
2. Abordagens fora do escopo da Parte 1 (fuzzy tipo-2 intervalar, deep learning end-to-end);
3. Aplicações distantes de controle de movimento quando não fundacionais;
4. Texto completo indisponível.

## 4. Tabela de trabalhos relacionados (≥ 5)

| # | Trabalho | Problema tratado | Abordagem | Relação com este projeto |
|---|---|---|---|---|
| 1 | **Mancilla, A.; García-Valdez, M.; Castillo, O.; Merelo-Guervós, J.J. (2022).** *Optimal Fuzzy Controller Design for Autonomous Robot Path Tracking Using Population-Based Metaheuristics.* Symmetry, 14(2), 202. | Rastreamento de trajetória por robô autônomo | Controlador Mamdani 5×5 (erro lateral + erro angular → guinada) com MFs otimizadas por metaheurísticas populacionais | **Artigo principal (reproduzido)** — estrutura do controlador, pistas via spline, fitness por RMSE |
| 2 | **Antonelli, G.; Chiaverini, S.; Fusco, G. (2007).** *A fuzzy-logic-based approach for mobile robot path tracking.* IEEE Trans. on Fuzzy Systems, 15(2), 211–221. | Path tracking de robô móvel | Fuzzy Mamdani sobre erros geométricos de seguimento | Confirma a escolha das variáveis de entrada (erros lateral/angular) como padrão da área |
| 3 | **Mamdani, E.H.; Assilian, S. (1975).** *An experiment in linguistic synthesis with a fuzzy logic controller.* Int. J. Man-Machine Studies, 7(1), 1–13. | Controle de planta (motor a vapor) | Primeira formulação do controlador fuzzy Mamdani | Fundamenta o mecanismo de inferência usado (min-max + centroide) |
| 4 | **Takagi, T.; Sugeno, M. (1985).** *Fuzzy identification of systems and its applications to modeling and control.* IEEE Trans. SMC, 15(1), 116–132. | Identificação e controle de sistemas | Modelo TSK (consequentes funcionais) | Base da comparação conceitual Mamdani × TSK feita na discussão |
| 5 | **Cordón, O.; Herrera, F.; Hoffmann, F.; Magdalena, L. (2001).** *Genetic Fuzzy Systems: Evolutionary Tuning and Learning of Fuzzy Knowledge Bases.* World Scientific. | Ajuste evolutivo de sistemas fuzzy | Taxonomia e métodos de tuning de MFs/regras por AG | Enquadra teoricamente a extensão de otimização (AG ajustando MFs) |
| 6 | **Precup, R.-E.; Hellendoorn, H. (2011).** *A survey on industrial applications of fuzzy control.* Computers in Industry, 62(3), 213–226. | Survey de aplicações industriais | Levantamento de controle fuzzy aplicado | Justifica a relevância prática do controle fuzzy no domínio escolhido |
| 7 | **Zadeh, L.A. (1965).** *Fuzzy sets.* Information and Control, 8(3), 338–353. | Fundamento matemático | Teoria de conjuntos fuzzy | Base conceitual de todo o trabalho |

## 5. Justificativa da escolha do artigo principal

O artigo de **Mancilla et al. (2022)** foi escolhido como referência principal por quatro
razões:

1. **Reprodutibilidade:** descreve explicitamente o modelo cinemático (bicicleta), as pistas
   de referência (pontos de controle interpolados por spline cúbica), a estrutura do
   controlador (2 entradas × 5 termos, 25 regras, inferência Mamdani) e a função objetivo
   (RMSE médio do erro lateral) — tudo o que é necessário para uma reprodução mínima viável;
2. **Aderência dupla à disciplina:** une Sistemas de Controle Fuzzy e Computação
   Evolutiva/Bioinspirada (otimização de MFs por metaheurísticas populacionais), permitindo
   integrar a pontuação extra (AG) organicamente ao trabalho principal;
3. **Atualidade e acesso:** publicado em 2022 em periódico de acesso aberto (MDPI,
   indexado no JCR/Scopus), com DOI: 10.3390/sym14020202;
4. **Problema realista:** rastreamento de trajetória é um problema clássico e atual de
   robótica móvel/veículos autônomos, citado na própria lauda como exemplo aceitável.

## 6. Limitações de reprodução declaradas (exigência A1)

A reprodução é **mínima viável**, com as seguintes adaptações em relação ao artigo:

| Aspecto | Artigo original | Esta reprodução | Motivo |
|---|---|---|---|
| Metaheurísticas | GA, PSO e outras variantes comparadas | Apenas **AG** (real-coded) | Escopo da Parte 1 + tempo disponível |
| Orçamento de busca | Populações/gerações maiores | Pop. 20, 10 gerações, 5 execuções | Custo computacional; convergência já observável |
| Convenção de sinais | Convenção própria do artigo | Convenção explícita (docs/base_de_regras.md), matriz espelhada de forma equivalente | Compatibilidade com o simulador implementado |
| Critério de término | Percurso da pista | Chegada detectada (abeam do fim + raio de 2 m) com T_MAX = 50 s | Penalizar controladores que não completam o percurso |
| Resultados numéricos | RMSE reportados no artigo | Comparação qualitativa (ordem de grandeza e tendência) | Implementações e orçamentos distintos |
