# Checklist de Aderência à Rubrica (AV2 — Parte 1)

Autoavaliação da equipe. Legenda: ✅ **Atendido** · 🟡 **Parcial** · ⛔ **Pendente**.
Cada item aponta a **evidência no repositório** e, quando aplicável, a **ação restante**.

> Estrutura de referência: **Opção A — trilha A1 (Reprodução)** de Mancilla et al.
> (2022), modelo **Mamdani**, com extensão de **otimização por AG** (pontuação
> extra). Execução: `python fuzzy_path_tracking.py` (sementes 42–46).

## A. Requisitos técnicos obrigatórios (lauda, Seção 3)

| Requisito | Status | Evidência | Ação restante |
|---|:--:|---|---|
| Problema realista e delimitado | ✅ | Rastreamento de trajetória de robô (modelo bicicleta) — `docs/artigo.md`, `README.md` | — |
| ≥ 2 entradas e 1 saída | ✅ | `e_lat` (m) + `theta_e` (rad) → `omega` (rad/s) | — |
| ≥ 3 termos na entrada principal | ✅ | **5 termos** (AN, MN, Z, MP, AP) por variável — `docs/base_de_regras.md` | — |
| ≥ 3 termos na saída (Mamdani) | ✅ | **5 termos** na saída `omega` | — |
| Funções de pertinência (gráfico/fórmula/parâmetros) | ✅ | `docs/funcoes_de_pertinencia.md` + `resultados/mfs_otimizadas.png` | — |
| ≥ 12 regras efetivamente usadas | ✅ | **25 regras** (matriz 5×5) — `docs/base_de_regras.md` | — |
| Inferência explicada (operadores, agregação, defuzzificação) | ✅ | Mamdani min–max, defuzzificação por **centroide** — `docs/base_de_regras.md` + `docs/artigo.md` | — |
| ≥ 6 cenários de teste (baixo→crítico) | ✅ | **6 cenários** C1–C6 (nulo, alto, fronteiriço, conflito crítico) — `docs/cenarios_de_teste.md` | — |
| Validação (tabelas, gráficos, superfície, comparação) | ✅ | RMSE por pista, superfície de controle, trajetórias baseline×AG — `docs/cenarios_de_teste.md`, `resultados/` | — |
| Reprodução e consistência (código executa, manual reproduz) | ✅ | `docs/manual_de_execucao.md`, sementes fixas, números batem com a saída real | — |
| GitHub obrigatório | 🟡 | Repositório publicado com README, código, docs, resultados e slides | **Confirmar acesso do professor ao repositório** |

## B. Opção A — Pesquisa em artigos científicos (lauda, Seção 5.1)

| Item | Status | Evidência | Ação restante |
|---|:--:|---|---|
| Bases/mecanismos de busca declarados | ✅ | `docs/trabalhos_relacionados.md` | — |
| Palavras-chave declaradas | ✅ | `docs/trabalhos_relacionados.md` | — |
| Critérios de inclusão/exclusão | ✅ | `docs/trabalhos_relacionados.md` | — |
| Tabela com ≥ 5 trabalhos relacionados | ✅ | `docs/trabalhos_relacionados.md` | — |
| Justificativa do artigo principal | ✅ | Mancilla et al. (2022), justificado | — |
| A1 (reprodução) declarada | ✅ | **A1 — reprodução mínima viável** declarada no README/artigo | — |
| Comparação com a literatura | 🟡 | RMSE e comportamento comparados ao artigo no `docs/artigo.md` | **Reforçar no artigo a comparação quantitativa direta com Mancilla et al.** |
| Estrutura de artigo técnico/científico | ✅ | `docs/artigo.pdf` (documento principal) | — |

## C. Pontuação extra — Otimização com AG (lauda, Seção 7)

| Item | Status | Evidência | Ação restante |
|---|:--:|---|---|
| Função objetivo definida | ✅ | RMSE médio do erro lateral nas 3 pistas (M, A, S) | — |
| Representação da solução | ✅ | Cromossomo = 10 genes (parâmetros das MFs de entrada) | — |
| Operadores evolutivos | ✅ | Seleção, cruzamento, mutação, elitismo — `fuzzy_path_tracking.py` | — |
| Critério de parada | ✅ | Nº fixo de gerações × 5 execuções independentes (sementes 42–46) | — |
| Comparação antes/depois | ✅ | Baseline **1,560 m** → otimizado **1,232 m** (**−21,0%**) — `docs/cenarios_de_teste.md`, `resultados/ag_convergence.png` | — |
| Código da extensão no repositório | ✅ | AG em `fuzzy_path_tracking.py` | — |

## D. Entregáveis e GitHub (lauda, Seções 8 e 11)

| Entregável | Status | Evidência | Ação restante |
|---|:--:|---|---|
| Documento principal (PDF) | ✅ | `docs/artigo.pdf` | — |
| README completo | 🟡 | `README.md` (modalidade, instalação, execução, estrutura, resultados) | **Preencher turma e nomes dos integrantes** |
| Código-fonte organizado e comentado | ✅ | `fuzzy_path_tracking.py`, `fuzzy_path_tracking.ipynb` | — |
| Manual de execução | ✅ | `docs/manual_de_execucao.md` | — |
| Base de regras (tabela explícita) | ✅ | `docs/base_de_regras.md` | — |
| Funções de pertinência | ✅ | `docs/funcoes_de_pertinencia.md` + `resultados/*.png` | — |
| Cenários de teste (tabela + interpretação) | ✅ | `docs/cenarios_de_teste.md` | — |
| Evidências de execução | ✅ | Notebook executado + gráficos em `resultados/` | — |
| Slides | ✅ | `slides/slides.pdf` (12 slides) | **Revisar antes de apresentar** |
| Declaração de uso de IA | ✅ | `docs/declaracao_uso_ia.md` | — |
| Referências | ✅ | `docs/trabalhos_relacionados.md` | — |

## E. Pendências restantes (a cargo da equipe)

1. 🟡 **Preencher turma e integrantes** no README e na capa do artigo.
2. 🟡 **Confirmar o acesso do professor** ao repositório (público ou convite).
3. 🟡 **Revisar os slides** e ensaiar a defesa (ver perguntas prováveis no README).
4. 🟡 (Opcional) **Reforçar no artigo** a comparação quantitativa direta com o
   artigo de referência.

> Núcleo técnico (modelagem, código, experimentos, validação, reprodutibilidade,
> documento principal e slides) está ✅. As pendências são de **finalização
> administrativa** e dependem da equipe.
