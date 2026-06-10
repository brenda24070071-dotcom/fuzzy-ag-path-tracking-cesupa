# Manual de Execução

## 1. Pré-requisitos

- **Python 3.10 ou superior** (testado em 3.10 e 3.14)
- `pip` disponível no PATH

## 2. Instalação das dependências

Na raiz do repositório:

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install numpy scipy matplotlib scikit-fuzzy networkx
```

> `networkx` é dependência do `scikit-fuzzy`. As versões exatas validadas estão em
> `requirements.txt`.

## 3. Execução do sistema completo (script)

```bash
python fuzzy_path_tracking.py
```

O script executa, nesta ordem:

1. **Parte 1 — Baseline:** simula o controlador Mamdani com parâmetros médios (genes = 0.5)
   nas 3 pistas (M, A, S), imprime o RMSE médio e a tabela dos 6 cenários de teste;
2. **Parte 2 — Otimização:** roda o AG 5 vezes (sementes 42–46; população 20, 10 gerações),
   imprime a convergência geração a geração;
3. **Comparação final:** RMSE baseline × otimizado e percentual de melhoria.

**Tempo total esperado:** ~1 a 2 minutos em um notebook comum.

### Saídas geradas em `resultados/`

| Arquivo | Conteúdo |
|---|---|
| `baseline_trajectories.png` | Trajetórias do robô com parâmetros baseline |
| `optimized_trajectories.png` | Trajetórias com parâmetros otimizados pelo AG |
| `ag_convergence.png` | Curvas de convergência das 5 execuções do AG |
| `mfs_otimizadas.png` | Funções de pertinência após a otimização |
| `superficie_controle.png` | Superfície de controle `omega = f(e_lat, theta_e)` |

A tabela dos 6 cenários de teste é impressa no terminal (e está documentada em
`docs/cenarios_de_teste.md`).

## 4. Execução via notebook

```bash
jupyter notebook fuzzy_path_tracking.ipynb
```

O notebook contém o mesmo código do script, organizado em seções com explicações
(Kernel → Restart & Run All para reproduzir tudo). O notebook do repositório já está
executado, com todas as saídas e gráficos visíveis no próprio GitHub.

## 5. Reprodutibilidade dos resultados

- As 5 execuções do AG usam **sementes fixas** (42 a 46): os números do relatório
  (baseline RMSE = 1.5601 m; otimizado = 1.2319 m; melhoria de 21,0%) são reproduzíveis
  exatamente.
- Pequenas variações podem ocorrer entre versões muito diferentes do NumPy.

## 6. Solução de problemas

| Sintoma | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: skfuzzy` | Dependência ausente | `pip install scikit-fuzzy networkx` |
| Gráficos não aparecem | Backend não interativo | Os PNGs são salvos em `resultados/` de qualquer forma |
| Execução lenta (> 5 min) | Máquina limitada | Reduzir `pop_size`/`gens` na chamada `run_ga` em `main()` |
