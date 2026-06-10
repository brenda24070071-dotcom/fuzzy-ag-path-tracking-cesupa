# Declaração de Uso de IA — Parte 2 (IA Evolutiva e Computação Bioinspirada)

Conforme exigido na lauda (Seção 7), a equipe declara com transparência o uso de ferramentas
de IA, as finalidades, a revisão humana realizada e assume integral responsabilidade pelo
conteúdo final entregue.

| Ferramenta | Finalidade | Principais usos | Revisão humana |
|---|---|---|---|
| Claude Code (Anthropic) | Implementação do experimento comparativo | Escrita do script `experimento_evolutivo.py` (PSO canônico, busca aleatória e protocolo experimental com contador de avaliações), reutilizando o núcleo de simulação fuzzy e o AG já desenvolvidos e validados na Parte 1 do trabalho | Código lido e executado pela equipe; PSO conferido contra a formulação canônica (inércia + termos cognitivo/social com coeficientes de Clerc); contagem de avaliações verificada (220 por execução em todos os métodos); resultados reproduzidos com as sementes fixas |
| Claude Code (Anthropic) | Documentação | Rascunho do relatório técnico, README e slides, preenchidos com os números reais produzidos pela execução do experimento | Textos revisados pela equipe; todos os valores conferidos contra `resultados/estatisticas_execucoes.csv` e a saída do terminal; estrutura conferida contra os entregáveis da lauda |
| Claude Code (Anthropic) | Revisão de qualidade | Verificação de coerência entre formulação, código, resultados e relatório (checklist da Seção 9 da lauda) | A equipe validou cada item do checklist antes da submissão |

## Revisão crítica e responsabilidade

- **O que foi aceito:** implementação dos três métodos e protocolo experimental — após
  execução completa e conferência das métricas (melhor/pior/média/desvio, curvas de
  convergência, tempo e número de avaliações).
- **O que foi corrigido/ajustado pela equipe:** identificação da equipe, textos da
  documentação e interpretação dos resultados na análise crítica.
- **O que foi testado:** todo o código do repositório foi executado pela equipe
  (`python experimento_evolutivo.py`), e os resultados do relatório correspondem à saída
  real (sementes fixas 42–46 garantem reprodutibilidade exata).
- **Compreensão:** cada integrante estudou a formulação do problema (variáveis de decisão,
  espaço de busca, função objetivo, restrições e penalidades) e os operadores de cada
  método (seleção/cruzamento/mutação/elitismo no AG; inércia e termos cognitivo/social no
  PSO), e está preparado para a arguição sem depender da IA.

> O artigo-base e demais fontes estão citados no relatório técnico. Nenhum trecho de
> terceiros foi utilizado sem citação. O núcleo de simulação compartilhado com a Parte 1
> está declarado no cabeçalho do código e no relatório.
