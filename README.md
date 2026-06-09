# Controlador Fuzzy Mamdani + AG para Rastreamento de Trajetória

Sistema de controle **Fuzzy Mamdani** que comanda o esterçamento de um robô autônomo (modelo cinemático *bicicleta*) para seguir trajetórias de referência, com **otimização das funções de pertinência por Algoritmo Genético (AG)**.

Trabalho prático que unifica as disciplinas de **Sistemas de Controle Fuzzy** e **IA Evolutiva e Computação Bioinspirada**.

Reprodução/adaptação de: Mancilla et al., *Optimal Fuzzy Controller Design for Autonomous Robot Path Tracking Using Population-Based Metaheuristics*, Symmetry 2022, 14, 202.

- **Disciplina:** Inteligência Artificial e Computacional (0700M8) — CESUPA
- **Modalidade:** Opção A (artigo científico) com extensão de otimização (AG)
- **Modelo de inferência:** Mamdani (Max-Min, defuzzificação=centroide)

## Modelo Fuzzy (Resumo)

| Item | Valor |
|---|---|
| Entradas | `e_lat` = erro lateral (m); `theta_e` = erro angular (rad) |
| Saída | `omega` = taxa de guinada/esterçamento (rad/s) |
| Termos linguísticos | 5 por variável: AN, MN, Z, MP, AP |
| Regras | 25 (matriz 5×5) — justificada em [docs/base_de_regras.md](docs/base_de_regras.md) |
| Otimização | AG (10 genes = parâmetros das MFs de entrada), avaliado por minimização de RMSE ao longo de 3 pistas (M, A, S). |

## Instalação e Requisitos

Instale as dependências via gerenciador de pacotes:

```bash
pip install numpy scipy matplotlib scikit-fuzzy
```

*(O projeto foi testado em Python 3.10+)*.

## Execução

Toda a lógica e pipeline (Motor Mamdani rápido em NumPy, simulador cinemático, Algoritmo Genético de 5 execuções e avaliação via `skfuzzy` para os cenários pontuais e gráficos) está consolidada em um único script de fácil execução:

```bash
python fuzzy_path_tracking.py
```

Você também pode abrir o notebook interativo (que reflete o código exato do script) no Jupyter:
```bash
jupyter notebook fuzzy_path_tracking.ipynb
```

## Estrutura do Repositório (Essencial)

```
fuzzy_path_tracking.py     # Motor fuzzy otimizado (NumPy), AG e simulação
fuzzy_path_tracking.ipynb  # Versão iterativa do código em Notebook
docs/                      # Documentação teórica: Base de Regras, Trabalhos Relacionados e Plano
resultados/                # Imagens geradas após a execução do código
```

## Saídas Geradas (`resultados/`)

As seguintes evidências e análises visuais serão extraídas automaticamente ao rodar a simulação:

| Arquivo | Conteúdo |
|---|---|
| `baseline_trajectories.png` | Trajetórias seguidas pelo robô usando parâmetros originais |
| `optimized_trajectories.png` | Trajetórias seguidas pelo robô usando parâmetros evoluídos pelo AG |
| `ag_convergence.png` | Curvas de convergência do AG (Sobreposição das 5 execuções independentes) |
| `mfs_otimizadas.png` | Funções de pertinência antes e depois da otimização genética |
| `superficie_controle.png` | Superfície de controle (Malha 3D de `omega = f(e_lat, theta_e)`) |

> A tabela com os 6 cenários de teste manuais exigidos na rubrica é impressa diretamente no console/terminal durante a execução.
