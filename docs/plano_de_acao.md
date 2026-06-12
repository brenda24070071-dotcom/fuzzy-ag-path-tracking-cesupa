# Plano de Ação: Sistema Fuzzy Otimizado por Computação Evolutiva

Este plano de ação foi desenhado para unificar a **Parte 1** (Sistemas de Controle Fuzzy) e a **Parte 2** (IA Evolutiva e Computação Bioinspirada) do seu trabalho, focando na **Opção A** da Parte 1 e garantindo a pontuação extra de ambas as rubricas.

## 🎯 1. Visão Geral do Projeto Unificado

A estratégia para juntar ambos os trabalhos é criar um **Sistema Neuro-Fuzzy ou um Sistema Fuzzy Otimizado**. 

*   **O que será feito:** Você vai pesquisar e implementar um Sistema de Controle Fuzzy para um problema específico baseado em um artigo científico (cumprindo a Opção A da Parte 1). Em seguida, você usará um algoritmo evolutivo (como Algoritmo Genético - AG ou Otimização por Enxame de Partículas - PSO) para otimizar os parâmetros deste sistema Fuzzy (cumprindo a Parte 2 e as pontuações extras).
*   **Vantagem Estratégica:**
    *   **Atende Parte 1 (Opção A):** Reprodução/adaptação de um artigo científico de Fuzzy.
    *   **Atende Parte 1 (Pontuação Extra):** Opção 2 (Otimização de Hiperparâmetros com AG ou PSO).
    *   **Atende Parte 2:** Aplicação de Computação Evolutiva em um experimento.
    *   **Atende Parte 2 (Pontuação Extra):** Alternativa 3 (Otimização automática de parâmetros Fuzzy).

---

## 🔍 2. Como buscar os Artigos Científicos

Para a Opção A, você precisa de um artigo principal e alguns relacionados. O ideal é buscar um artigo que proponha um sistema Fuzzy claro e que tenha resultados mensuráveis.

**Bases de Busca Recomendadas:**
*   IEEE Xplore, ScienceDirect, Scopus, Web of Science, Google Scholar. *(Dica: Se você usar artigos de revistas de alto impacto - Qualis A1 a A4 -, pode garantir também a pontuação extra 3 da Parte 1).*

**Termos de Busca (Keywords):**
Combine termos de Fuzzy, Evolutiva e o seu domínio de interesse (ex: controle de robôs, diagnóstico médico, finanças).
*   *Fuzzy:* `"Fuzzy Logic Control"`, `"Fuzzy Inference System"`, `"Mamdani"`, `"Takagi-Sugeno"`.
*   *Evolutiva:* `"Genetic Algorithm"`, `"PSO"`, `"Evolutionary Computation"`, `"Parameter Optimization"`.
*   *Exemplos de strings de busca:* 
    *   `"Fuzzy Logic Control" AND "Genetic Algorithm" AND "Autonomous Vehicle"`
    *   `"Fuzzy Inference System" AND "PSO" AND "Medical Diagnosis"`

**Critério de Escolha do Artigo Principal:**
Escolha um artigo (preferencialmente dos últimos 7 anos) onde os autores descrevam claramente:
1.  As **variáveis de entrada e saída** (mínimo de 2 entradas e 1 saída).
2.  As **funções de pertinência** utilizadas.
3.  A **base de regras** (mínimo de 12 regras).
4.  Um **método de avaliação** (ex: o erro médio quadrático do sistema, a precisão, etc.) para que você tenha como medir o *fitness* (aptidão) na Parte 2.

---

## 🔗 3. Como conectar os dois projetos (Parte 1 + Parte 2)

A conexão ocorre na **Fase de Otimização**. O sistema Fuzzy (Parte 1) será a função a ser avaliada pelo Algoritmo Evolutivo (Parte 2).

1.  **A Base (Parte 1):** Você implementará o sistema Fuzzy com os parâmetros manuais definidos no artigo (ou definidos por você a partir da adaptação do artigo). Esse será o seu *baseline* (modelo de referência).
2.  **O Algoritmo Evolutivo (Parte 2):** Escolha o AG ou o PSO.
    *   **Representação (Cromossomo/Partícula):** Os genes do AG (ou dimensões da partícula do PSO) serão os parâmetros numéricos das funções de pertinência do seu sistema Fuzzy (ex: as coordenadas $a, b, c$ de um triângulo) ou os pesos das regras.
    *   **Função Objetivo/Aptidão (Fitness):** Para calcular o quão bom é um indivíduo, o algoritmo vai injetar os parâmetros dele no sistema Fuzzy, rodar os dados de teste e calcular o erro (ou desempenho). O objetivo do AG/PSO será **minimizar esse erro**.
3.  **O Resultado Final:** Após rodar várias gerações, o AG/PSO entregará os parâmetros otimizados. Você então comparará o desempenho do "Fuzzy Original/Manual" contra o "Fuzzy Otimizado por AG/PSO".

---

## 🚀 4. Plano de Execução (Como prosseguir)

Divida o desenvolvimento em 4 fases lógicas:

### Fase 1: Levantamento e Modelagem (Foco Teórico)
*   [ ] Definir o problema e buscar artigos usando as palavras-chave sugeridas.
*   [ ] Selecionar o artigo principal e montar a tabela com 5 trabalhos relacionados.
*   [ ] Documentar as variáveis, os universos de discurso, as funções de pertinência e as regras (mínimo 12).
*   [ ] Definir qual algoritmo evolutivo será usado (AG ou PSO) e como será a função de aptidão.

### Fase 2: Implementação do Fuzzy Base (Parte 1)
*   [ ] Codificar o sistema Fuzzy básico (sugestão: usar Python com bibliotecas como `scikit-fuzzy`).
*   [ ] Criar os **6 cenários de teste** exigidos na Parte 1.
*   [ ] Validar se o sistema produz as saídas esperadas (reprodução mínima do artigo).

### Fase 3: Implementação da Otimização Evolutiva (Parte 2)
*   [ ] Codificar o AG ou PSO (pode-se criar do zero ou usar bibliotecas de apoio).
*   [ ] Conectar o algoritmo ao sistema Fuzzy: a cada iteração do AG/PSO, os parâmetros do Fuzzy devem ser atualizados e testados.
*   [ ] Executar o processo de otimização (realizando pelo menos **5 execuções independentes** com sementes distintas, conforme exigido na Parte 2).

### Fase 4: Análise de Resultados e Documentação
*   [ ] Gerar as **curvas de convergência** do AG/PSO.
*   [ ] Criar tabelas e gráficos comparando o **Fuzzy Base** vs **Fuzzy Otimizado** (Comparação exigida na Parte 2 e na pontuação extra).
*   [ ] Consolidar tudo em um único repositório GitHub organizado (com código executável e instruções).
*   [ ] Redigir o PDF Técnico unificado seguindo a estrutura recomendada (Introdução, Fundamentação, Metodologia, Implementação, Experimentos, Conclusão).
*   [ ] Preparar os slides para a apresentação conjunta (5 a 15 minutos).

> [!TIP]
> **Dica de Engenharia:** Não tente otimizar *todos* os parâmetros de uma vez se o modelo ficar muito pesado. Comece otimizando apenas os picos das funções de pertinência ou os pesos das regras. Isso já configurará a integração exigida sem tornar o custo computacional proibitivo.
