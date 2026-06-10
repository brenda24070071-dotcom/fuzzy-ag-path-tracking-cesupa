# Controlador Fuzzy Mamdani + AG para Rastreamento de Trajetória

> **Disciplina:** Inteligência Artificial e Computacional (0700M8) — CESUPA · Prof. Daniel Leal Souza
> **Turma:** `<PREENCHER: CC5MA ou CC5NA>`
> **Equipe:** `<PREENCHER: nomes completos dos integrantes>`
> **Modalidade:** Opção A (artigo científico) — trilha **A1: Reprodução**, com extensão opcional de **otimização por Algoritmo Genético** (pontuação extra, opção 2)

Sistema de controle **Fuzzy Mamdani** que comanda a guinada de um robô autônomo (modelo
cinemático *bicicleta*) para seguir trajetórias de referência, com **otimização das funções
de pertinência por Algoritmo Genético (AG)**.

Reprodução mínima viável de: Mancilla, A.; García-Valdez, M.; Castillo, O.; Merelo-Guervós,
J. J. *Optimal Fuzzy Controller Design for Autonomous Robot Path Tracking Using
Population-Based Metaheuristics*. **Symmetry** 2022, 14, 202. DOI:
[10.3390/sym14020202](https://doi.org/10.3390/sym14020202).

## Resumo da solução

| Item | Valor |
|---|---|
| Entradas | `e_lat` = erro lateral (m); `theta_e` = erro angular (rad) |
| Saída | `omega` = taxa de guinada (rad/s) → esterçamento `δ = arctan(L·ω/v)`, saturado em ±45° |
| Termos linguísticos | 5 por variável: AN, MN, Z, MP, AP |
| Base de regras | 25 regras (matriz 5×5 antissimétrica) — [docs/base_de_regras.md](docs/base_de_regras.md) |
| Inferência | Mamdani min–max, fuzzificação singleton, **defuzzificação por centroide** |
| Otimização | AG real-coded (10 genes = parâmetros das MFs de entrada), fitness = RMSE médio do erro lateral em 3 pistas (M, A, S), 5 execuções com sementes fixas |
| **Resultado** | RMSE médio **1,560 m (baseline) → 1,232 m (otimizado)** = **−21,0%**, completando as 3 pistas |

## Tecnologias

Python 3.10+ · NumPy · SciPy · Matplotlib · scikit-fuzzy · Jupyter (versões em
[requirements.txt](requirements.txt))

## Instalação

```bash
git clone https://github.com/brenda24070071-dotcom/fuzzy-ag-path-tracking-cesupa.git
cd fuzzy-ag-path-tracking-cesupa
pip install -r requirements.txt
```

## Execução

```bash
python fuzzy_path_tracking.py
```

Executa o pipeline completo (~1–2 min): baseline → 5 execuções do AG → comparação final.
Imprime no terminal o RMSE por etapa e a tabela dos **6 cenários de teste**, e salva os
gráficos em `resultados/`. Alternativa interativa (mesmo código, já executado e com saídas
visíveis no GitHub):

```bash
jupyter notebook fuzzy_path_tracking.ipynb
```

## Reprodução dos testes

As execuções usam **sementes fixas (42–46)** — os números do relatório são reproduzíveis
exatamente. Guia completo (incluindo solução de problemas):
[docs/manual_de_execucao.md](docs/manual_de_execucao.md). Tabela de cenários com
interpretação e análise: [docs/cenarios_de_teste.md](docs/cenarios_de_teste.md).

## Estrutura do repositório

```
fuzzy_path_tracking.py      # Código-fonte: motor Mamdani (NumPy), simulador, AG e gráficos
fuzzy_path_tracking.ipynb   # Notebook executado (mesmo código, com narrativa e saídas)
requirements.txt            # Dependências e versões validadas
docs/
  artigo.md / artigo.pdf            # DOCUMENTO PRINCIPAL (artigo técnico-científico)
  trabalhos_relacionados.md         # Levantamento bibliográfico (bases, critérios, 7 obras)
  base_de_regras.md                 # 25 regras + convenções de sinal + justificativas
  funcoes_de_pertinencia.md         # Universos, fórmulas e parâmetros das MFs
  cenarios_de_teste.md              # 6 cenários + validação por simulação + análise
  manual_de_execucao.md             # Manual de execução e reprodução
  declaracao_uso_ia.md              # Declaração obrigatória de uso de IA
slides/
  slides.html / slides.pdf          # Apresentação (12 slides)
resultados/
  baseline_trajectories.png         # Trajetórias com parâmetros baseline
  optimized_trajectories.png        # Trajetórias pós-AG
  ag_convergence.png                # Convergência das 5 execuções do AG
  mfs_otimizadas.png                # Funções de pertinência otimizadas
  superficie_controle.png           # Superfície de controle ω = f(e_lat, θe)
```

## Documento principal e declaração de IA

- **Artigo (documento principal):** [docs/artigo.md](docs/artigo.md) · [docs/artigo.pdf](docs/artigo.pdf)
- **Declaração de uso de IA:** [docs/declaracao_uso_ia.md](docs/declaracao_uso_ia.md)
