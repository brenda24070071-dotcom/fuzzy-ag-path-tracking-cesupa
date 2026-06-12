# Estrutura do Documento Principal (PDF)

Esqueleto do relatório/artigo técnico (Opção A — adaptação A2), alinhado à
Seção 10 da lauda e à rubrica (Seção 11). Cada parte indica **o que escrever** e
**qual artefato do repositório usar como evidência**.

---

## Parte 1 — Capa / Cabeçalho
- Título: *Controlador Fuzzy Mamdani Otimizado por Algoritmo Genético para
  Rastreamento de Trajetória de Robô Autônomo*.
- Turma, equipe, integrantes (até 4), **Opção A (A2 — adaptação)** + extra AG.
- **Link do repositório GitHub.**

## Parte 2 — Resumo, Introdução, Motivação e Justificativa
- Resumo (≈150 palavras): problema, abordagem fuzzy+AG, resultado (≈24% de
  redução de RMSE).
- Problema: seguir uma trajetória de referência minimizando o erro lateral, sob
  imprecisão de medição e julgamento de "correção suave vs forte" — justifica a
  lógica fuzzy (gradação de decisão, controle aproximado).
- Justificativa do uso de fuzzy: mapeamento linguístico erro→esterçamento mais
  interpretável que ganhos PID fixos.

## Parte 3 — Fundamentação Teórica e Trabalhos Relacionados
- Lógica fuzzy, sistemas Mamdani, fuzzificação/inferência/defuzzificação.
- Algoritmo Genético (representação, seleção, cruzamento, mutação, elitismo).
- **Evidência:** `docs/trabalhos_relacionados.md` (metodologia de busca, 5
  trabalhos relacionados, escolha de Mancilla et al. 2022).

## Parte 4 — Metodologia e Modelagem Fuzzy
- Variáveis e **universos de discurso** (com unidades):
  - Entrada `e` = erro lateral (m); `theta_e` = erro angular (graus).
  - Saída `omega` = taxa de guinada/esterçamento (rad/s), universo `[-2, 2]`
    (justificativa física: `V/L·tan(δ_max) ≈ 1,33 rad/s`).
- **5 termos linguísticos** por variável (AN, MN, Z, MP, AP) e funções de
  pertinência (triangulares/trapezoidais) — **figura:** `funcoes_pertinencia.png`.
- **Base de 25 regras** (matriz 5×5) com justificativa cinemática — **tabela:**
  `docs/base_de_regras.md`.
- Convenção de sinais e realimentação negativa (inversão do erro lateral em um
  único ponto).
- Operadores: E = min, implicação = min, agregação = max, defuzzificação =
  **centroide**.
- Modelagem do AG: cromossomo (10 genes = parâmetros das MFs de entrada), função
  objetivo `fitness` = média do RMSE lateral nas 3 pistas.

## Parte 5 — Implementação e Arquitetura
- Estrutura: `fuzzy_path_tracking.py` (motor Mamdani + simulação + AG),
  `experiments.py` (cenários/evidências), `main.py` (entrada única), notebook.
- Modelo cinemático bicicleta (Euler, `DT=0.1`), pistas via *cubic spline*.
- Dependências e execução — **evidência:** `docs/manual_execucao.md`.

## Parte 6 — Experimentos, Resultados e Análise Crítica
- **8 cenários de teste** (baixo/médio/alto/fronteiriço/conflitante/crítico) —
  **tabela:** `resultados/test_scenarios.csv` / `analise_experimentos.md`.
- Trajetórias: `baseline_trajectories.png` vs `optimized_trajectories.png`.
- Convergência do AG (5 execuções): `ag_convergence.png`.
- Superfície de controle: `superficie_controle.png`.
- Comparação quantitativa: **baseline RMSE ≈ 1,93 m → otimizado ≈ 1,47 m
  (≈24%)** — **log:** `resultados/execucao_resumo.txt`.
- Verificações de coerência (deadband, antissimetria, realimentação negativa,
  malha fechada estável): **4/4 PASS**.
- **Análise crítica:** quando funciona bem (erros moderados, curvas suaves),
  quando degrada (curvatura acentuada, velocidade alta), parâmetros sensíveis
  (largura do conjunto Zero ⇒ zona-morta), e limitações do modelo bicicleta.

## Parte 7 — Conclusão, Trabalhos Futuros, Declaração de IA e Referências
- Conclusão: AG melhora o RMSE preservando interpretabilidade do Mamdani.
- Trabalhos futuros: comparação Mamdani × TSK, ganhos independentes por variável,
  validação com ruído de sensor, PSO como alternativa ao AG.
- **Declaração de uso de IA:** `docs/declaracao_uso_ia.md`.
- Referências: `docs/trabalhos_relacionados.md` + PDFs em `Pesquisa/`.

---

### Mapa rubrica → seção do relatório
| Critério (peso) | Seção(ões) |
|---|---|
| 1. Problema e fundamentação (0,25) | Partes 2 e 3 |
| 2. Modelagem fuzzy (0,40) | Parte 4 |
| 3. Implementação e funcionamento (0,30) | Parte 5 |
| 4. Experimentos e análise (0,30) | Parte 6 |
| 5. Documento escrito (0,20) | Todo o PDF |
| 6. Apresentação e arguição (0,35) | Slides + defesa (ver README §arguição) |
| 7. GitHub, reprodutibilidade, IA (0,20) | Parte 5 + `docs/` + `resultados/` |
