# Roteiro de Apresentação — 5 Integrantes

Defesa técnica do projeto **Controlador Fuzzy Mamdani + AG para Rastreamento de
Trajetória** (Opção A, trilha A1 — reprodução de Mancilla et al., 2022).
Duração-alvo: **12–15 min** (≈2–3 min por integrante) + arguição.

> **Atenção (lauda, Seção 6):** equipes de 5 integrantes devem cumprir uma
> **trilha de ampliação obrigatória**. A mais aderente ao que já temos é
> **"Comparação de modelos"** (Mamdani × TSK) ou **"Validação ampliada"**. Hoje
> a comparação Mamdani×TSK é **conceitual** (Seção 8 do artigo); para a ampliação
> seria preciso torná-la experimental ou ampliar a validação. Discutir com o
> professor. Cada integrante deve dominar o todo — o professor pode perguntar a
> qualquer um.

Convenção de sinais (todos devem saber): `e_lat>0` = robô à **direita** da pista;
`theta_e>0` = apontando à **esquerda**; `omega>0` = vira à **esquerda**.

---

## Integrante 1 — Problema, motivação e pesquisa bibliográfica

**Fala (abertura):**

"Bom dia. Nosso trabalho é um **sistema de controle fuzzy para rastreamento de
trajetória** de um robô autônomo — o problema de fazer um veículo seguir um
caminho de referência com o menor desvio possível. Escolhemos a **Opção A**:
reproduzir um artigo científico. O artigo principal é o de **Mancilla e colegas,
publicado na revista Symmetry em 2022**, que projeta um controlador fuzzy de path
tracking e otimiza seus parâmetros com metaheurísticas.

Por que **lógica fuzzy** é adequada aqui? Porque o conhecimento de pilotagem é
qualitativo — 'se estou um pouco à direita e apontando para fora, vire mais forte
à esquerda'. As fronteiras entre 'pouco' e 'muito' desviado são graduais, não
nítidas, e há tolerância à imprecisão do modelo. Esse é exatamente o perfil para
o qual a inferência fuzzy foi criada.

Sobre a **pesquisa bibliográfica**: buscamos em IEEE Xplore, ScienceDirect,
Scopus, MDPI e Google Scholar, com as palavras-chave *fuzzy logic control*,
*genetic algorithm*, *autonomous vehicle* e *path tracking*. Os critérios de
inclusão foram artigos recentes, com resultados quantitativos, que cruzassem
lógica fuzzy e otimização evolutiva para veículos autônomos. Selecionamos o
artigo de Mancilla et al. como principal por ser reprodutível — descreve modelo,
pistas, controlador e função objetivo — e montamos uma tabela com trabalhos
relacionados. Agora o [Integrante 2] explica a modelagem fuzzy."

**Perguntas que podem cair para mim:**
- *Por que fuzzy e não um PID?* → PID exige sintonia de ganhos e modelo preciso;
  fuzzy codifica regras interpretáveis e tolera imprecisão; e o artigo de
  referência usa fuzzy.
- *É reprodução (A1) ou adaptação (A2)?* → A1, reprodução mínima viável: mantemos
  a estrutura do artigo (variáveis, 25 regras, função objetivo) e adaptamos só as
  convenções do nosso simulador.
- *Quantos trabalhos relacionados e onde estão?* → Tabela em
  `docs/trabalhos_relacionados.md`, com bases, palavras-chave e critérios.

---

## Integrante 2 — Variáveis, universos e funções de pertinência

**Fala:**

"O controlador é do tipo **Mamdani**, com **duas entradas e uma saída**:
"Mamdani - Um controlador difuso tipo Mamdani é um sistema inteligente que imita o raciocínio humano para controlar processos complexos ou não-lineares sem a necessidade de um modelo matemático exato. Ele utiliza regras linguísticas baseadas na experiência (como "se o erro for grande, a ação deve ser forte") e é caracterizado por ter saídas que também são conjuntos difusos."

- **Erro lateral** `e_lat`, em metros — a distância perpendicular do robô à pista.
  Positivo significa que o robô está à direita do caminho.
- **Erro angular** `theta_e`, em radianos — a diferença entre a orientação do robô
  e a tangente da pista. Positivo significa apontando à esquerda.
- A saída é a **taxa de guinada** `omega`, em rad/s, que vira em ângulo de
  esterçamento.

Cada variável tem **cinco termos linguísticos**: Alto Negativo, Médio Negativo,
Zero, Médio Positivo e Alto Positivo — AN, MN, Z, MP, AP. Os **universos de
discurso** vão de −50 a +50, com a região de operação fina entre −5 e +5 para o
erro lateral.

As **funções de pertinência** são **triangulares** no centro e **trapezoidais**
nas extremidades — os 'ombros' longos garantem que qualquer valor de entrada,
mesmo extremo, tenha pertinência definida. Um ponto importante: as MFs das
**entradas** são justamente os parâmetros que o Algoritmo Genético otimiza; as MFs
da **saída** mantivemos fixas, para preservar o significado físico da ação de
controle e reduzir o espaço de busca. As funções não são nem estreitas demais (o
que eliminaria o caráter fuzzy) nem largas demais (o que deixaria o sistema
indiferente). Os gráficos estão em `resultados/mfs_otimizadas.png`. O
[Integrante 3] explica como as regras combinam essas variáveis."

**Perguntas que podem cair para mim:**
- *Por que 5 termos e não 3?* → 5 dão resolução suficiente para distinguir
  correção leve, moderada e forte, mantendo a base interpretável (25 regras).
- *Por que triangular/trapezoidal e não gaussiana?* → São as do artigo, simples de
  parametrizar e suficientes; trapezoidais nos extremos cobrem o universo todo.
- *O que cada gene do AG representa?* → 10 genes = 5 parâmetros de MF por entrada
  (posições e larguras dos conjuntos).

---

## Integrante 3 — Base de regras e inferência Mamdani

**Fala:**

"A base de conhecimento tem **25 regras**, organizadas numa matriz 5×5: para cada
combinação de erro angular (linha) e erro lateral (coluna), há uma ação de saída.
Todas têm a forma *SE theta_e é X E e_lat é Y ENTÃO omega é Z*.

As regras seguem uma lógica cinemática, que agrupamos:

- **Regime nominal:** centrado e alinhado → ação zero (ponto de equilíbrio).
- **Zona morta:** desvio lateral pequeno e alinhado → ação zero, para evitar
  oscilação (chattering) em torno da pista.
- **Retorno à pista:** alinhado mas muito afastado → guinada forte de volta.
- **Correção de rumo:** sobre a pista mas torto → corrige só o ângulo, com sinal
  oposto ao erro — isso é a **realimentação negativa**.
- **Convergência:** afastado mas já apontando de volta → ação nula, para não
  desfazer a aproximação (evita sobressinal).
- **Conflito:** afastado E apontando para fora → pior caso, correção máxima.

A matriz é **antissimétrica**: girá-la 180° troca os sinais — refletindo a
simetria física do problema.

Sobre a **inferência Mamdani**: o conectivo **E** é a t-norma **mínimo**; a
**implicação** também é por mínimo, truncando o conjunto de saída; a **agregação**
das 25 regras é por **máximo**; e a saída numérica vem da **defuzzificação pelo
centroide** — o centro de massa do conjunto agregado. A [Integrante 4] mostra como
o AG ajusta esse sistema."

**Perguntas que podem cair para mim:**
- *Por que omega = Zero no caso de conflito invertido (G3)?* → Porque o robô já
  está corrigindo sozinho (apontando de volta); agir mais causaria sobressinal.
- *O que é a realimentação negativa aqui?* → A ação tem sinal oposto ao erro;
  garante que o erro diminua. Foi justamente onde encontramos um defeito (a matriz
  estava espelhada) — o [Integrante 5] detalha.
- *Por que centroide e não máximo/média dos máximos?* → Centroide dá saída suave e
  contínua, considerando todas as regras ativas.

---

## Integrante 4 — Otimização por Algoritmo Genético e implementação

**Fala:**

"A nossa extensão (pontuação extra) é otimizar automaticamente as funções de
pertinência com um **Algoritmo Genético real-coded**.

- **Representação:** cada indivíduo é um vetor de **10 genes** entre 0 e 1 — os
  parâmetros das MFs das entradas.
- **Função objetivo (fitness):** rodamos o robô nas **3 pistas** de referência e
  medimos o **RMSE do erro lateral**; o AG **minimiza** essa média. Pistas geradas
  por spline cúbica; o ponto mais próximo é achado por árvore k-d.
- **Operadores:** seleção por **torneio de 3**, **cruzamento aritmético** (taxa
  0,7), **mutação gaussiana** (σ=0,2, taxa 0,3 por gene) e **elitismo** dos 2
  melhores.
- Rodamos **5 execuções independentes** com sementes fixas (42 a 46), o que torna
  os resultados **reprodutíveis** e mostra robustez à semente.

Sobre a **implementação**: é um arquivo único, `fuzzy_path_tracking.py`. O motor
Mamdani foi escrito em NumPy puro, cerca de 1500× mais rápido que a biblioteca
pronta — essencial porque o AG faz milhares de simulações. Validamos esse motor
rápido contra o `scikit-fuzzy`, que usamos para os gráficos. O modelo do robô é o
**cinemático de bicicleta**: entre-eixos 2,5 m, velocidade 3,33 m/s, integração de
Euler, e o esterçamento satura em ±45°. Para reproduzir, basta
`pip install -r requirements.txt` e `python fuzzy_path_tracking.py`. O
[Integrante 5] apresenta os resultados."

**Perguntas que podem cair para mim:**
- *Por que AG e não ajuste manual?* → O espaço de 10 parâmetros é grande e
  acoplado; o AG busca sem gradiente, guiado pela simulação.
- *Por que otimizar só as entradas?* → Fixar a saída preserva o significado físico
  da ação e reduz o espaço de busca; foi suficiente para −21%.
- *Como garantem reprodutibilidade?* → Sementes fixas 42–46; os números do
  relatório saem iguais. Manual em `docs/manual_de_execucao.md`.
- *Por que penalidade de +2000?* → Para o AG descartar controladores que não
  completam a pista; sem isso ele acharia mínimos que "cortam caminho".

---

## Integrante 5 — Experimentos, análise crítica e conclusão

**Fala:**

"Validamos o sistema de duas formas. Primeiro, **6 cenários pontuais**: caso nulo
(centrado e alinhado → ação zero, o equilíbrio); erro lateral alto à direita e à
esquerda (ação forte de volta, e perfeitamente **antissimétrica**); erro angular
alto (corrige o rumo); um caso fronteiriço de aproximação (à direita mas já
apontando de volta → não interfere); e o **conflito crítico** (afastado e
divergindo → correção máxima). Todos coerentes — tabela em
`docs/cenarios_de_teste.md`.

Segundo, **simulação completa** nas 3 pistas. O RMSE médio do erro lateral caiu de
**1,56 m no baseline para 1,23 m após o AG — uma melhoria de 21%** —, com o robô
completando as três pistas. A maior melhoria foi na pista com curvas mais severas
(−42%). As curvas de convergência e as trajetórias estão em `resultados/`.

Quero destacar um ponto de **honestidade metodológica**. Durante a validação
descobrimos **dois defeitos**: a matriz de regras estava espelhada em relação à
convenção de sinal — o robô divergia da pista, com RMSE de mais de 2000 m — e
faltava um critério de chegada ao fim da pista. Corrigimos os dois, e a melhoria do
AG saltou de 0,5% para 21%. A lição: em controle fuzzy, **convenções de sinal são
parte da modelagem**, e a validação de malha fechada é indispensável — os cenários
isolados não revelavam o problema.

**Limitações:** o controlador é puramente reativo, sem antecipar a curvatura; com
velocidade fixa, faz laços de recaptura em curvas fechadas. Como **trabalho
futuro**: uma terceira entrada com a curvatura da pista, velocidade variável, e uma
comparação experimental **Mamdani × TSK** — um TSK daria saída mais suave, mas
perderia a leitura linguística que facilita auditar as regras.

**Conclusão:** reproduzimos o controlador de Mancilla et al., validamos com análise
crítica e o otimizamos por computação evolutiva, cumprindo o ciclo completo da
disciplina. Obrigado — abrimos para perguntas."

**Perguntas que podem cair para mim:**
- *Quando o sistema falha?* → Curvas fechadas em velocidade fixa; é reativo, sem
  antecipação.
- *Como sabem que a melhora não é sorte?* → 5 execuções com sementes diferentes
  convergem para a mesma faixa (1,23–1,32 m).
- *Diferença Mamdani × TSK?* → TSK tem consequentes numéricos (média ponderada),
  saída mais suave; Mamdani tem consequentes linguísticos, mais interpretável.

---

## Encerramento (coletivo)

Todos devem saber responder, em uma frase, **por que escolhemos aquelas variáveis,
por que as MFs são adequadas, por que as regras fazem sentido e como interpretar os
resultados** — são as quatro perguntas que a lauda (Seção 14) sinaliza como certas.
