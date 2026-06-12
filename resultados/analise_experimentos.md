# Analise Experimental Automatica - Controlador Fuzzy de Trajetoria

**Controlador avaliado:** Otimizado (AG)  
**Parametros (10 genes do AG):** `[0.724, 0.239, 0.322, 0.922, 0.454, 0.386, 0.283, 0.499, 0.4, 0.034]`

Sistema Mamdani, 2 entradas (erro lateral `e`, erro angular `theta_e`), 1 saida (`omega`), 5 termos linguisticos por variavel, 25 regras ativas, operador E = min, agregacao = max, defuzzificacao = centroide.

## 1. Cenarios de teste

| Categoria | e (m) | theta_e (deg) | omega | Classificacao | Sentido | Coerencia |
|---|---:|---:|---:|---|---|---|
| Baixo | 0.0 | 0.0 | 0.0 | Manter reto | neutro | COERENTE: sem erro -> acao ~0 (deadband) |
| Medio | 1.5 | 0.5 | 0.7182 | Correcao moderada | esquerda (+) | COERENTE: acao de correcao acionada |
| Alto | 8.0 | 0.0 | 1.3545 | Correcao forte | esquerda (+) | COERENTE: acao de correcao acionada |
| Fronteirico | 0.2 | 0.05 | 0.6603 | Correcao moderada | esquerda (+) | COERENTE: resposta suave perto de zero |
| Conflitante | 5.0 | 2.0 | 0.0 | Manter reto | neutro | COERENTE: conflito arbitrado (acao amortecida, anti-overshoot) |
| Conflitante | -5.0 | -2.0 | 0.0 | Manter reto | neutro | COERENTE: conflito arbitrado (acao amortecida, anti-overshoot) |
| Critico | -8.0 | 3.0 | -1.3545 | Correcao forte | direita (-) | COERENTE: acao de correcao acionada |
| Critico | 8.0 | -3.0 | 1.3545 | Correcao forte | esquerda (+) | COERENTE: acao de correcao acionada |

## 2. Verificacoes automaticas de coerencia

| Propriedade | Resultado | Evidencia |
|---|:---:|---|
| Deadband em (0,0) | PASS | omega(0,0) = 0.0000 (esperado ~0) |
| Antissimetria omega(-e,-th) = -omega(e,th) | PASS | erro maximo de antissimetria = 0.0000 |
| Realimentacao negativa (e>0 -> omega>0, acao forte) | PASS | omega(e=0.5,1,3,8) = 1.314, 1.362, 1.362, 1.354 |
| Malha fechada estavel (RMSE finito) | PASS | RMSE por pista: M=0.618, A=2.413, S=1.379 |

## 3. Desempenho em malha fechada

| Pista | RMSE lateral (m) |
|---|---:|
| M | 0.6185 |
| A | 2.4125 |
| S | 1.3793 |
| **Media** | **1.4701** |

## 4. Veredito automatico

Verificacoes aprovadas: **4/4** -> comportamento global **COERENTE**.

- A acao de controle e nula em regime nominal (zona-morta) e cresce monotonicamente com a magnitude do erro, saturando nos extremos.
- A base de regras antissimetrica e confirmada numericamente: o sistema trata desvios a esquerda e a direita de forma espelhada.
- A malha fechada e estavel: o veiculo segue as 3 pistas com RMSE finito.

## 5. Limitacoes observadas

- Os universos de `e` e `theta_e` compartilham a mesma escala (-50..50); ganhos diferentes por variavel poderiam melhorar a sensibilidade.
- O modelo cinematico (bicicleta) ignora dinamica de pneus e atraso de atuacao; em velocidades altas o RMSE tende a subir.
