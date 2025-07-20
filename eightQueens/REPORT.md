# Relatório Técnico: Algoritmos Genéticos para o Problema das N-Rainhas

**Curso:** Inteligência Artificial - 2025.1
**Professor:** Samy Sá
**Universidade:** Universidade Federal do Ceará - Campus de Quixadá

---

## 1. Implementação

Esta seção detalha os aspectos técnicos da implementação do projeto, as ferramentas utilizadas e as decisões de design da arquitetura do software.

### 1.1. Linguagem e Bibliotecas

-   **Linguagem:** Python 3.10
-   **Bibliotecas Principais:**
    -   `pandas`: Essencial para a manipulação de dados, leitura e escrita dos arquivos `.csv` contendo os resultados dos experimentos.
    -   `matplotlib` & `seaborn`: Utilizadas para a geração de gráficos estatísticos de alta qualidade, como os de convergência e os boxplots, permitindo uma análise visual robusta.
    -   `tqdm`: Fornece barras de progresso interativas no terminal, melhorando a experiência do usuário durante as execuções, que podem ser demoradas.

### 1.2. Arquitetura do Código e Design

A base de código foi estruturada de forma modular, aderindo aos princípios **SOLID** de design orientado a objetos para promover flexibilidade e manutenibilidade.

-   **`core`**: Contém as classes fundamentais `Individual` (um cromossomo representando um tabuleiro) e `Population`.
-   **`problem`**: Isola a lógica específica do problema das N-Rainhas. A classe `NQueensFitness` é a única responsável por avaliar um indivíduo, desacoplando a definição do problema do algoritmo em si.
-   **`ga`**: Contém o motor `GeneticAlgorithm`. Sua arquitetura é baseada no **Padrão de Projeto Strategy**, sendo inicializado com objetos de estratégia para seleção, cruzamento, mutação и elitismo. Isso respeita o **Princípio Aberto/Fechado**, pois novas estratégias podem ser adicionadas sem modificar o motor principal do AG.
-   **`main.py`**: Serve como o orquestrador dos experimentos, configurando e executando as diferentes variações do AG conforme a especificação do trabalho.
-   **`plotter.py`**: Script dedicado à análise pós-experimento, responsável por ler os dados brutos dos arquivos `.csv` e gerar as visualizações gráficas.

---

## 2. Design dos Algoritmos

Esta seção justifica as escolhas de design para os componentes do Algoritmo Genético e como eles se aplicam ao problema das N-Rainhas.

### 2.1. Representação do Indivíduo e Função de Fitness

-   **Representação:** Um indivíduo (cromossomo) é representado por um vetor de `n` inteiros. O índice `i` do vetor representa a coluna, e o valor `s[i]` representa a linha onde a rainha daquela coluna está posicionada. Esta representação já previne ataques verticais, pois há apenas um valor por coluna.
-   **Função de Fitness:** O objetivo é minimizar o número de pares de rainhas em conflito. Como os AGs canonicamente maximizam o fitness, a função foi definida para **maximizar o número de pares de rainhas que não se atacam**. O número total de pares em um tabuleiro `n x n` é $N_{total} = \frac{n(n-1)}{2}$. A função de fitness calcula o número de ataques (horizontais e diagonais), $N_{ataques}$, e o fitness final é:
    $$ \text{fitness} = N_{total} - N_{ataques} $$
    Uma solução perfeita atinge o fitness máximo de $N_{total}$, que para N=10 é $10 \times 9 / 2 = 45$.

### 2.2. Variações de Operadores e Combinações

O design flexível permite 16 combinações de algoritmos distintas a partir dos operadores implementados.

-   **Seleção (2):** `TournamentSelection`, `RouletteWheelSelection`.
-   **Cruzamento (2):** `SinglePointCrossover`, `TwoPointCrossover`.
-   **Mutação (2):** `SwapMutation`, `RandomResettingMutation`.
-   **Elitismo (2):** `BestNElitism`, `PercentageElitism`.

O conjunto completo dos 16 algoritmos é:
1.  (TournamentSelection, SinglePointCrossover, SwapMutation, BestNElitism)
2.  (TournamentSelection, SinglePointCrossover, SwapMutation, PercentageElitism)
3.  (TournamentSelection, SinglePointCrossover, RandomResettingMutation, BestNElitism)
4.  (TournamentSelection, SinglePointCrossover, RandomResettingMutation, PercentageElitism)
5.  (TournamentSelection, TwoPointCrossover, SwapMutation, BestNElitism)
6.  (TournamentSelection, TwoPointCrossover, SwapMutation, PercentageElitism)
7.  (TournamentSelection, TwoPointCrossover, RandomResettingMutation, BestNElitism)
8.  (TournamentSelection, TwoPointCrossover, RandomResettingMutation, PercentageElitism)
9.  (RouletteWheelSelection, SinglePointCrossover, SwapMutation, BestNElitism)
10. (RouletteWheelSelection, SinglePointCrossover, SwapMutation, PercentageElitism)
11. (RouletteWheelSelection, SinglePointCrossover, RandomResettingMutation, BestNElitism)
12. (RouletteWheelSelection, SinglePointCrossover, RandomResettingMutation, PercentageElitism)
13. (RouletteWheelSelection, TwoPointCrossover, SwapMutation, BestNElitism)
14. (RouletteWheelSelection, TwoPointCrossover, SwapMutation, PercentageElitism)
15. (RouletteWheelSelection, TwoPointCrossover, RandomResettingMutation, BestNElitism)
16. (RouletteWheelSelection, TwoPointCrossover, RandomResettingMutation, PercentageElitism)

### 2.3. Parte 0: Escolha de Parâmetros Numéricos

Antes dos experimentos comparativos, foi realizada uma etapa de ajuste para encontrar um conjunto de parâmetros numéricos de base que oferecesse um bom equilíbrio entre qualidade da solução e tempo de execução para N=10. Os parâmetros escolhidos para os experimentos seguintes foram:
-   **Tamanho da População:** 100
-   **Número de Gerações:** 500
-   **Taxa de Mutação:** 5%
-   **Elitismo:** `BestNElitism` com N=2 ou `PercentageElitism` com 10%.
-   **Tamanho do Torneio:** 3

---

## 3. Experimentação

Esta seção apresenta a análise dos resultados obtidos nos experimentos, com base nos gráficos e dados gerados. Todos os experimentos de comparação (Partes 1-4) foram executados 20 vezes para N=10.

### Parte 1: Variações do Parâmetro de Seleção

-   **Objetivo:** Comparar o desempenho da `TournamentSelection` contra a `RouletteWheelSelection`.
-   **Análise dos Resultados:**
    -   O gráfico de convergência demonstra claramente que a **Seleção por Torneio** atinge um fitness médio superior de forma muito mais rápida. A Seleção por Roleta apresenta uma convergência mais lenta e instável.
    -   O boxplot do fitness final revela que ambas as estratégias são consistentes em atingir um fitness de 44.0. No entanto, a `TournamentSelection` foi a única que conseguiu encontrar a solução ótima (fitness 45.0) em algumas execuções, que aparecem como outliers superiores. A análise do arquivo de sumário confirma que a solução ótima foi encontrada em 3 das 20 execuções (15%) com Torneio, e em 0% com Roleta.
-   **Conclusão:** A **`TournamentSelection` é superior**, pois converge mais rápido e é mais capaz de escapar de ótimos locais para encontrar a solução global.

### Parte 2: Variações do Parâmetro de Crossover

-   **Objetivo:** Comparar o desempenho do `SinglePointCrossover` contra o `TwoPointCrossover`.
-   **Análise dos Resultados:**
    -   O gráfico de convergência mostra trajetórias muito similares para ambas as estratégias, sugerindo eficácia parecida no processo de melhoria.
    -   O boxplot mostra que ambas as estratégias são extremamente consistentes, com quase todas as execuções terminando com fitness 44.0. Ambas encontraram a solução ótima (fitness 45.0) como um outlier. A análise do arquivo de sumário mostra que o `SinglePoint` encontrou a solução ótima em 2 das 20 execuções (10%) e o `TwoPoint` em 1 das 20 (5%).
-   **Conclusão:** As duas estratégias apresentam **desempenho praticamente idêntico** e altamente consistente. Não há um vencedor claro, ambas são escolhas viáveis.

### Parte 3: Variações do Parâmetro de Elitismo

-   **Objetivo:** Comparar o `BestNElitism` (com N=2) contra o `PercentageElitism` (com 10%, resultando em 10 elites).
-   **Análise dos Resultados:**
    -   O gráfico de convergência indica que um elitismo maior (`Percentage`) leva a uma convergência inicial mais rápida.
    -   O boxplot é a visualização mais interessante. O `PercentageElitism` é extremamente consistente, convergindo quase sempre para um fitness de 44.0. Já o `BestNElitism` produziu resultados mais variados, com uma dispersão maior, mas foi o único que conseguiu encontrar a solução ótima (outlier em 45.0). O sumário confirma que `BestN` encontrou a solução em 1 de 20 execuções (5%).
-   **Conclusão:** Há um trade-off. O **`PercentageElitism` com mais elites é mais rápido e consistente** para atingir uma boa solução, mas o **`BestNElitism` com menos elites permitiu maior diversidade na população**, o que possibilitou encontrar a solução ótima. A escolha depende do objetivo: consistência ou chance de otimalidade.

### Parte 4: Variações do Parâmetro de Mutação

-   **Objetivo:** Comparar a `SwapMutation` contra a `RandomResettingMutation`.
-   **Análise dos Resultados:**
    -   O gráfico de convergência mostra que a `RandomResettingMutation` leva a uma melhora mais rápida nas gerações iniciais.
    -   O boxplot revela diferenças na consistência. A `SwapMutation` é muito consistente (linha em 44.0), enquanto a `RandomResettingMutation` produz resultados mais variados, com um fitness mediano superior. Nenhuma das duas encontrou a solução ótima de fitness 45 nas 20 execuções.
-   **Conclusão:** A **`RandomResettingMutation` parece superior**, pois, embora menos consistente, atinge em média soluções finais de melhor qualidade e converge mais rápido. A `SwapMutation` parece levar o algoritmo a um ótimo local específico de forma mais previsível.

### Parte 5: Tamanho Máximo Viável do Problema

-   **Objetivo:** Analisar a escalabilidade de quatro variações "campeãs" do AG, medindo o tempo de execução com o aumento de `N`.
-   **Análise dos Resultados:**
    -   O gráfico de escalabilidade plota o tempo de execução em função do número de rainhas (N) para as quatro variações.
    -   Observa-se um **crescimento exponencial no tempo de execução** para todas as variações, o que é esperado para um problema combinatório.
    -   A variação `Champ_TwoPointCross` demonstrou ser a mais rápida, enquanto a `Champ_RandomResetMut` foi a que mais sofreu com o aumento de N, tornando-se a mais lenta.
-   **Conclusão:** O framework implementado é eficaz para instâncias de até **N=25-30**, onde o tempo de execução ainda é gerenciável (na ordem de minutos). Acima disso, o tempo de execução cresce drasticamente, tornando o problema intratável para esta configuração de parâmetros. A escolha do operador de Crossover (`TwoPoint`) mostrou ter o maior impacto positivo na escalabilidade.

---

## 4. Considerações Finais

O projeto demonstrou com sucesso a aplicação de Algoritmos Genéticos para o problema das N-Rainhas. A arquitetura modular permitiu uma experimentação robusta e a comparação detalhada de diferentes estratégias.

A principal conclusão é que a escolha dos operadores tem um impacto significativo no desempenho. Uma combinação de **`TournamentSelection`** (pela sua capacidade de encontrar a solução ótima) e **`TwoPointCrossover`** (pela sua eficiência em problemas maiores) parece ser a mais promissora.

Como trabalhos futuros, poderiam ser exploradas técnicas mais avançadas, como taxas de mutação adaptativas (que diminuem à medida que a população converge), representações de cromossomos baseadas em permutação (evitando conflitos de linha e coluna por design) ou a hibridização do AG com um algoritmo de busca local para refinar as soluções encontradas a cada geração.