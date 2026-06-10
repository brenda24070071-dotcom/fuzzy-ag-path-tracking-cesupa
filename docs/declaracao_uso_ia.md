# Declaração de Uso de IA

Conforme exigido na lauda da atividade (Seção 9), a equipe declara o uso de ferramentas de
IA no desenvolvimento deste trabalho, com transparência sobre finalidade, comandos utilizados
e revisão humana realizada.

| Ferramenta | Finalidade | Prompt/comando resumido | Revisão crítica da equipe |
|---|---|---|---|
| Claude Code (Anthropic) | Esboço inicial do código do controlador (motor Mamdani em NumPy, simulador cinemático e AG) a partir da estrutura descrita no artigo de referência | "Implementar controlador fuzzy Mamdani 5×5 com erro lateral/angular e otimização de MFs por AG, conforme Mancilla et al. 2022" | Código lido linha a linha pela equipe; estrutura do controlador conferida contra o artigo; executado e validado por simulação |
| Claude Code (Anthropic) | Revisão final do projeto: auditoria do código, depuração e correção de defeitos | "Verificar se o trabalho atende a lauda, revisar e implementar o que faltar" | A revisão por IA encontrou **dois defeitos reais**, confirmados pela equipe nas evidências de simulação: (1) matriz de regras espelhada em relação à convenção de sinal do erro lateral, que fazia o robô divergir da pista (RMSE ≈ 2085 m com penalidade); (2) ausência de critério de chegada ao fim da pista, que disparava a penalidade mesmo com bom rastreamento. As correções foram testadas: RMSE baseline caiu para 1,56 m e a melhoria do AG passou de 0,5% para 21,0%. A equipe validou os sinais das regras manualmente (tabela de cenários) e os gráficos de trajetória |
| Claude Code (Anthropic) | Geração dos rascunhos da documentação técnica (base de regras, funções de pertinência, manual, cenários de teste, artigo e slides) a partir do código e dos resultados reais de execução | "Documentar base de regras, MFs, cenários e estrutura do artigo conforme os entregáveis da lauda" | Textos revisados e ajustados pela equipe; números conferidos contra a saída real do programa; tabelas de regras e parâmetros validadas contra o código-fonte |

## O que foi aceito, corrigido, rejeitado, testado e validado

- **Aceito após teste:** correção da matriz de regras e critério de chegada — validados por
  execução completa (resultados em `resultados/` e no notebook executado).
- **Corrigido pela equipe:** convenções de nomenclatura, identificação da equipe e ajustes
  de texto na documentação gerada.
- **Testado:** todo o código presente no repositório foi executado pela equipe
  (`python fuzzy_path_tracking.py` e notebook completo) e os resultados do relatório
  correspondem à saída real do programa.
- **Compreensão:** cada integrante estudou a modelagem fuzzy (variáveis, universos, MFs,
  regras, inferência Mamdani e defuzzificação por centroide) e o fluxo do AG, e está
  preparado para a arguição sem depender da IA.

> Nenhum trecho de texto ou código foi copiado de terceiros sem citação. O artigo de
> referência e demais fontes estão citados em `docs/trabalhos_relacionados.md` e no
> documento principal.
