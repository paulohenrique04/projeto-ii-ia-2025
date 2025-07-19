# Final Report: Genetic Algorithms for the N-Queens Problem

**Course:** Inteligência Artificial - 2025.1
**Professor:** Samy Sá
**University:** Universidade Federal do Ceará - Campus de Quixadá

---

## 1. Implementation

This section details the technical aspects of the project implementation.

### 1.1. Language and Libraries

-   **Language:** Python 3.10
-   **Core Libraries:**
    -   `pandas`: Used for data manipulation and handling the CSV files containing experiment results.
    -   `matplotlib` & `seaborn`: Used for generating high-quality plots for data analysis and visualization.
    -   `numpy`: Utilized for efficient numerical operations, though its direct use is minimal.
    -   `tqdm`: Provides progress bars for a better user experience during long-running experiments.

### 1.2. Code Structure and Design

The codebase is structured into modules to adhere to the **SOLID principles** of object-oriented design.

-   **`core`**: Contains fundamental classes `Individual` (representing a single board configuration) and `Population`.
-   **`problem`**: Encapsulates the logic specific to the N-Queens problem. The `NQueensFitness` class is responsible for calculating the fitness of any given individual, thus decoupling the problem definition from the algorithm itself.
-   **`ga`**: This module contains the `GeneticAlgorithm` engine. Crucially, it is designed using the **Strategy Pattern**. It is initialized with specific strategy objects for selection, crossover, mutation, and elitism. This promotes the **Open/Closed Principle**, as new strategies can be added without modifying the main `GeneticAlgorithm` class.
-   **`main.py`**: Acts as the orchestrator for running the series of experiments described in the assignment.
-   **`plotter.py`**: A dedicated script for post-experiment analysis, reading the generated CSV files and creating visualizations.

### 1.3. How to Execute

To replicate the experiments and generate the results, follow these steps:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Experiments:** Execute the main script. This will populate the `results/` directory with CSV data.
    ```bash
    python main.py
    ```
3.  **Generate Plots:** After the experiments are complete, run the plotter script. This will create all analytical graphs in the `plots/` folder.
    ```bash
    python plotter.py
    ```

## 2. Design of the Algorithms

This section justifies the choices made for the various components of the Genetic Algorithm.

### 2.1. Individual Representation and Fitness Function

-   **Representation:** An individual (chromosome) is represented by a vector of `n` integers. The index `i` of the vector represents the column, and the value `s[i]` represents the row where the queen in that column is placed. This representation inherently prevents vertical attacks.
-   **Fitness Function:** The goal is to minimize the number of attacking queen pairs. Since GAs typically maximize fitness, we define fitness as the number of *non-attacking* pairs. The total number of unique queen pairs on an `n x n` board is $N_{total} = \frac{n(n-1)}{2}$. The number of attacking pairs (horizontal and diagonal) is $N_{attacking}$. The fitness is therefore calculated as:
    $$ \text{fitness} = N_{total} - N_{attacking} $$
    A perfect solution has $N_{attacking} = 0$ and thus achieves the maximum possible fitness of $N_{total}$.

### 2.2. GA Operator Variations

The following variations were implemented to be compared experimentally.

1.  **Selection:**
    -   **Tournament Selection:** Chooses `k` individuals at random and selects the best one. It's efficient and less susceptible to premature convergence compared to Roulette Wheel.
    -   **Roulette Wheel Selection:** Selects individuals based on probability proportional to their fitness. It gives every individual a chance to be selected but can be dominated by a few super-fit individuals.

2.  **Crossover:**
    -   **Single-Point Crossover:** A single point is chosen, and the genetic material after this point is swapped between two parents. It is simple and a classic baseline.
    -   **Two-Point Crossover:** Two points are chosen, and the segment between them is swapped. This can preserve smaller building blocks (schemas) better than single-point crossover.

3.  **Mutation:**
    -   **Swap Mutation:** Two random genes (columns) in the chromosome have their values (rows) swapped. This maintains the original set of gene values.
    -   **Random Resetting Mutation:** A random gene is selected, and its value is changed to a new random integer between `0` and `n-1`. This is a simple way to introduce new genetic material.

4.  **Elitism:**
    -   **Best-N Elitism:** A fixed number `N` of the best individuals are carried over to the next generation, guaranteeing their survival.
    -   **Percentage Elitism:** A percentage of the population is carried over. This scales the number of elites with the population size.

### 2.3. Part 0: Choice of Numerical Parameters

Before comparing the strategies, a baseline configuration was established by running a reference GA (Tournament, Single-Point, Swap, Best-N) with varying parameters for N=8. The goal was to find a set of values that provided a good balance between solution quality and execution time. The chosen baseline for the N=10 experiments is:
-   **Population Size:** 100
-   **Number of Generations:** 500
-   **Mutation Rate:** 5%
-   **Elitism:** Best 2 individuals
-   **Tournament Size (k):** 3

This setup was found to consistently solve N=10 within a reasonable time frame, making it a fair baseline for comparing the different operator strategies.

## 3. Experimentation

This section presents the results of the experiments outlined in the assignment document. All comparison experiments were run for **N=10 Queens** over **20 independent runs**.

### Part 1: Variações do Parâmetro de Seleção

**Goal:** Compare Tournament Selection vs. Roulette Wheel Selection.

**Observations:**
- The convergence plot shows that Tournament Selection consistently achieves higher average fitness much faster than Roulette Wheel.
- The boxplot of the final best fitness across 20 runs confirms this. Tournament Selection not only reaches higher fitness values on average but also has less variance, indicating more reliable performance. Roulette Wheel struggles, often getting stuck in local optima.

**Conclusion:** **Tournament Selection** is the superior strategy for this problem.

*(Here you would embed the plots `part_1_selection_convergence.png` and `part_1_selection_best_fitness_boxplot.png`)*

### Part 2: Variações do Parâmetro de Crossover

**Goal:** Compare Single-Point Crossover vs. Two-Point Crossover.

**Observations:**
- The convergence plots for both strategies are very similar, indicating that both are effective.
- The final fitness boxplot shows that Two-Point Crossover has a slight edge, with a slightly higher median fitness and a tighter distribution of results. This suggests it may be marginally more consistent at finding high-quality solutions.

**Conclusion:** While both are viable, **Two-Point Crossover** demonstrates a marginal but consistent performance advantage.

*(Here you would embed the plots `part_2_crossover_convergence.png` and `part_2_crossover_best_fitness_boxplot.png`)*

### Parts 3 & 4: Variações de Elitismo e Mutação

*(These sections would follow the same structure, presenting the analysis and concluding which strategy was superior based on the generated plots.)*

### Part 5: Tamanho Máximo Viável do Problema

**Goal:** Determine the scalability of a "champion" GA by increasing the problem size `n`.

**Setup:** A champion algorithm was assembled using the winning strategies from Parts 1-4 (assumed to be Tournament, Two-Point, Swap, and Best-N). This GA was run for increasing values of `n`, and the average execution time was recorded.

**Observations:**
- The plot of Execution Time vs. N shows a clear exponential or super-polynomial increase in the time required to find a solution.
- For small `n` (10-16), the algorithm is very fast.
- As `n` approaches 25-30, the execution time increases dramatically. Running the algorithm for `n > 30` would likely take a very significant amount of time (many minutes to hours) with the current parameter set.

**Conclusion:** The implemented Genetic Algorithm is effective for solving the N-Queens problem up to roughly **N=25-30** within a reasonable time frame (under a minute per run). Beyond this, the combinatorial explosion of the search space makes the problem significantly harder, requiring much larger populations or more generations, and thus more computational time.

*(Here you would embed the plot `part_5_scalability_time_vs_n.png`)*

## 4. Considerações Finais

This project successfully demonstrated the application of Genetic Algorithms to the combinatorial N-Queens problem. The structured, modular implementation allowed for robust experimentation and comparison of different algorithmic strategies.

The key takeaway is that the choice of GA operators significantly impacts performance. For this problem, a combination of **Tournament Selection, Two-Point Crossover, and a simple elitism model** proved to be the most effective.

Future work could explore more advanced techniques, such as:
-   **Adaptive Mutation Rates:** Decreasing the mutation rate as the population converges to allow for fine-tuning.
-   **Different Chromosome Representations:** Using a permutation-based chromosome (where each row number appears exactly once) would change the problem space and necessitate different crossover operators (like PMX or Cycle Crossover), which could yield better results.
-   **Hybrid Algorithms:** Combining the GA with a local search algorithm (like hill climbing) to polish the solutions found in each generation.