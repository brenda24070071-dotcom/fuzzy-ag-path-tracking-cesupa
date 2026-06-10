# AG × PSO × Busca Aleatória — Otimização de Controlador Fuzzy de Rastreamento

> **Disciplina:** Inteligência Artificial e Computacional (0700M8) — CESUPA · Prof. Daniel Leal Souza
> **Trabalho:** Parte 2 — IA Evolutiva e Computação Bioinspirada · **Opção 1 (Pesquisa Científica)**
> **Turma:** CC5MA
> **Equipe (5 integrantes):** Brenda Nascimento, Cauê Jadão, Augusto Pereira, Fernando Mourão, César Ribeiro
> **Ampliação obrigatória (equipe de 5):** **Comparação ampliada** — duas abordagens distintas comparadas (AG × PSO, exemplo literal da Seção 5 da lauda), estendida com baseline de busca aleatória
> **Pontuação extra:** Alternativa 3 — Otimização automática de parâmetros Fuzzy (comparação antes/depois incluída)
> **Localização:** pasta `parte2-evolutiva/` do repositório [fuzzy-ag-path-tracking-cesupa](https://github.com/brenda24070071-dotcom/fuzzy-ag-path-tracking-cesupa) — a Parte 1 está na raiz

## Descrição do experimento

Comparação experimental controlada entre **Algoritmo Genético (AG)**, **Otimização por
Enxame de Partículas (PSO)** e **Busca Aleatória** (baseline) no ajuste dos **10 parâmetros
das funções de pertinência** de um controlador fuzzy Mamdani (5×5, 25 regras) que rastreia
trajetórias com um robô de cinemática de bicicleta.

- **Formulação:** minimizar o RMSE médio do erro lateral em 3 pistas; variáveis de decisão
  `p ∈ [0,1]^10`; restrição de caixa via *clip*; factibilidade via penalidade (+2000 quando
  o robô não completa a pista).
- **Protocolo:** 5 execuções independentes por método (sementes 42–46), **orçamento
  idêntico de 220 avaliações** da função objetivo por execução, mesmas pistas e mesma
  função objetivo para todos os métodos.
- **Métricas:** melhor/pior/média/desvio-padrão do RMSE final, curvas de convergência por
  avaliação, tempo de execução e número de avaliações.

### Artigo de referência

Mancilla, A.; García-Valdez, M.; Castillo, O.; Merelo-Guervós, J. J. *Optimal Fuzzy
Controller Design for Autonomous Robot Path Tracking Using Population-Based
Metaheuristics*. **Symmetry** 2022, 14, 202. DOI:
[10.3390/sym14020202](https://doi.org/10.3390/sym14020202) — artigo de 2022 (últimos 7
anos), indexado (Scopus/JCR), cujo cerne é exatamente a comparação de metaheurísticas
populacionais nesse problema.

> Esta pasta contém a **Parte 2** do trabalho da disciplina. O núcleo de simulação
> (controlador Mamdani + cinemática) é compartilhado com a **Parte 1, na raiz deste
> repositório**, onde a modelagem fuzzy está documentada em detalhe
> ([../docs/base_de_regras.md](../docs/base_de_regras.md),
> [../docs/funcoes_de_pertinencia.md](../docs/funcoes_de_pertinencia.md)). Os resultados do
> AG aqui reproduzem exatamente os da Parte 1 (mesmas sementes → mesmos números).

## Resultados (reprodutíveis com as sementes fixas)

| Método | Melhor | Pior | Média | Desv. padrão | Tempo médio/execução |
|---|---|---|---|---|---|
| **AG** | **1,2319** | 1,3193 | **1,2926** | 0,0354 | 6,0 s |
| **PSO** | 1,2966 | 1,3349 | 1,3126 | **0,0156** | 5,9 s |
| Busca Aleatória | 1,2866 | 1,3487 | 1,3208 | 0,0246 | 3,0 s |
| Referência fixa (sem otimização) | 1,5601 | — | — | — | — |

(RMSE em metros; 5 sementes × 220 avaliações por método.) Todos os métodos melhoram
16–21% sobre a referência fixa; o AG obteve a melhor média e o melhor resultado global, o
PSO foi o mais estável, e a Busca Aleatória ficou surpreendentemente competitiva neste
orçamento — discussão completa no relatório técnico.

## Tecnologias

Python 3.10+ · NumPy · SciPy · Matplotlib (versões em [requirements.txt](requirements.txt))

## Instalação

```bash
git clone https://github.com/brenda24070071-dotcom/fuzzy-ag-path-tracking-cesupa.git
cd fuzzy-ag-path-tracking-cesupa/parte2-evolutiva
pip install -r requirements.txt
```

## Execução

```bash
python experimento_evolutivo.py
```

Tempo total: ~1,5 min. O script imprime a tabela de resultados no terminal e gera em
`resultados/`:

| Arquivo | Conteúdo |
|---|---|
| `estatisticas_execucoes.csv` | Uma linha por execução (método, semente, melhor fitness, tempo, nº de avaliações) |
| `melhores_individuos.json` | Melhor vetor de genes por método (reprodutibilidade) |
| `convergencia_metodos.png` | Curvas de convergência (média ± faixa min–max, 5 sementes) |
| `boxplot_metodos.png` | Distribuição do RMSE final por método |
| `antes_depois_trajetorias.png` | Trajetórias antes/depois da otimização (pontuação extra — Alternativa 3) |

## Estrutura da pasta (`parte2-evolutiva/`)

```
experimento_evolutivo.py    # Código-fonte completo (simulação + AG + PSO + busca aleatória + protocolo)
requirements.txt            # Dependências
docs/
  relatorio_tecnico.md/.pdf # PDF TÉCNICO (documento principal)
  declaracao_uso_ia.md      # Declaração obrigatória de uso de IA
slides/
  slides.html / slides.pdf  # Apresentação
resultados/                 # Saídas geradas (CSV, JSON e gráficos)
```

## Dados

Não há dados externos: as pistas de referência são geradas proceduralmente (spline cúbica
sobre pontos de controle do artigo-base) pelo próprio script.

## Documento principal e declaração de IA

- **Relatório técnico (PDF):** [docs/relatorio_tecnico.pdf](docs/relatorio_tecnico.pdf)
- **Declaração de uso de IA:** [docs/declaracao_uso_ia.md](docs/declaracao_uso_ia.md)
