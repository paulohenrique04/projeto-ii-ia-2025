# Genetic Algorithm for the N-Queens Problem

This project implements a configurable Genetic Algorithm (GA) to solve the N-Queens problem, as specified in the "Trabalho 2 - Algoritmos Genéticos" assignment.

## Project Structure

The project is organized into several modules to ensure separation of concerns and maintainability:

-   `main.py`: The main script to run the experiments.
-   `plotter.py`: A script to generate plots from the experiment results.
-   `core/`: Contains the basic building blocks of the GA (Individual, Population).
-   `problem/`: Defines the N-Queens problem, specifically the fitness function.
-   `ga/`: Contains the main GA engine and the strategy implementations.
    -   `ga/strategies/`: Holds the different implementations for selection, crossover, mutation, and elitism.
-   `utils/`: Contains helper classes, such as the CSV logger.
-   `results/`: Directory where all CSV output files from the experiments are stored.
-   `plots/`: Directory where all generated plots are saved.

## Prerequisites

You need Python 3.8+ and the libraries listed in `requirements.txt`.

## Installation

1.  Clone the repository or download the source code.
2.  Navigate to the project directory.
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

### 1. Running the Experiments

To run all the experiments as defined in the assignment, execute the `main.py` script from your terminal:

```bash
python main.py
```

This will:
- Run experiments for comparing different GA operators (Selection, Crossover, etc.).
- Perform 20 runs for each configuration, as specified.
- Save detailed logs for each run and a summary CSV for each experiment part inside the `results/` directory.

### 2. Generating the Plots

After the experiments are finished and the `results/` folder is populated with CSV files, run the `plotter.py` script to generate visual analyses:

```bash
python plotter.py
```

This will create PNG images of the plots and save them in the `plots/` directory. These plots are referenced in the final report.