import os
import time
import pandas as pd
from tqdm import tqdm

from ga.genetic_algorithm import GeneticAlgorithm
from utils.logger import Logger

# Import Strategies
from ga.strategies.selection import TournamentSelection, RouletteWheelSelection
# A importação foi alterada aqui:
from ga.strategies.crossover import UniformCrossover, TwoPointCrossover
from ga.strategies.mutation import SwapMutation, RandomResettingMutation
from ga.strategies.elitism import BestNElitism, PercentageElitism

# --- BASE CONFIGURATION ---
BASE_PARAMS = {
    "n_queens": 10,
    "population_size": 100,
    "num_generations": 500,
    "mutation_rate": 0.05,
    "elitism_n": 2,
    "elitism_percentage": 0.1,  # 10%
    "tournament_k": 3,
    "num_runs": 20,
}

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def experiment_part_1_selection():
    """Compares two selection strategies."""
    print("\n--- Running Experiment Part 1: Selection Strategies ---")
    folder = "part_1_selection"
    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    configs = [
        {
            "name": "Tournament",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            # Alterado aqui para usar UniformCrossover como baseline
            "crossover": UniformCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "RouletteWheel",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": RouletteWheelSelection(),
            # Alterado aqui
            "crossover": UniformCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        }
    ]

    summary_results = []
    for config in configs:
        print(f"Testing configuration: {config['name']}")
        for i in tqdm(range(BASE_PARAMS["num_runs"]), desc=f"Runs for {config['name']}"):
            result = run_single_experiment(config, i)
            summary_results.append(result)

    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 1 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


def experiment_part_2_crossover():
    """Compares two crossover strategies."""
    print("\n--- Running Experiment Part 2: Crossover Strategies ---")
    folder = "part_2_crossover"
    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    configs = [
        {
            # A primeira configuração agora testa o UniformCrossover
            "name": "Uniform",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": UniformCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "TwoPoint",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": TwoPointCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        }
    ]

    summary_results = []
    for config in configs:
        print(f"Testing configuration: {config['name']}")
        for i in tqdm(range(BASE_PARAMS["num_runs"]), desc=f"Runs for {config['name']}"):
            result = run_single_experiment(config, i)
            summary_results.append(result)

    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 2 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


def experiment_part_3_elitism():
    """Compares two elitism strategies."""
    print("\n--- Running Experiment Part 3: Elitism Strategies ---")
    folder = "part_3_elitism"
    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    configs = [
        {
            "name": "BestN",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            # Alterado aqui
            "crossover": UniformCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "Percentage",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            # Alterado aqui
            "crossover": UniformCrossover(),
            "mutation": SwapMutation(),
            "elitism": PercentageElitism(BASE_PARAMS["elitism_percentage"]),
        }
    ]

    summary_results = []
    for config in configs:
        print(f"Testing configuration: {config['name']}")
        for i in tqdm(range(BASE_PARAMS["num_runs"]), desc=f"Runs for {config['name']}"):
            result = run_single_experiment(config, i)
            summary_results.append(result)

    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 3 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


def experiment_part_4_mutation():
    """Compares two mutation strategies."""
    print("\n--- Running Experiment Part 4: Mutation Strategies ---")
    folder = "part_4_mutation"
    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    configs = [
        {
            "name": "Swap",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            # Alterado aqui
            "crossover": UniformCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "RandomReset",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            # Alterado aqui
            "crossover": UniformCrossover(),
            "mutation": RandomResettingMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        }
    ]

    summary_results = []
    for config in configs:
        print(f"Testing configuration: {config['name']}")
        for i in tqdm(range(BASE_PARAMS["num_runs"]), desc=f"Runs for {config['name']}"):
            result = run_single_experiment(config, i)
            summary_results.append(result)

    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 4 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


def run_single_experiment(config: dict, run_id: int, show_progress=False):
    """Helper to run one instance of a GA configuration."""
    logger = Logger(
        os.path.join(
            RESULTS_DIR, config["folder"], f"run_{run_id}_{config['name']}_n{config['params']['n_queens']}.csv"
        )
    ) if not show_progress else None

    ga = GeneticAlgorithm(
        n_queens=config["params"]["n_queens"],
        selection_strategy=config["selection"],
        crossover_strategy=config["crossover"],
        mutation_strategy=config["mutation"],
        elitism_strategy=config["elitism"],
    )
    start_time = time.time()
    best_solution = ga.run(
        population_size=config["params"]["population_size"],
        num_generations=config["params"]["num_generations"],
        mutation_rate=config["params"]["mutation_rate"],
        logger=logger,
    )
    end_time = time.time()

    if logger:
        logger.save()

    return {
        "run_id": run_id,
        "config_name": config["name"],
        "best_fitness": best_solution.fitness,
        "execution_time": end_time - start_time,
        "solution_found": best_solution.fitness == ga.fitness_calculator.max_fitness
    }


def experiment_part_5_scalability():
    """
    Tests the four champion variations on increasing N to determine viable problem size
    and satisfy the 10+ minute execution time requirement.
    """
    print("\n--- Running Experiment Part 5: Scalability (Problem Size) ---")
    folder = "part_5_scalability"
    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    champion_configs = [
        {
            "name": "Champ_TournamentSel",
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            # Alterado aqui
            "crossover": UniformCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "Champ_TwoPointCross",
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": TwoPointCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "Champ_RandomResetMut",
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            # Alterado aqui
            "crossover": UniformCrossover(),
            "mutation": RandomResettingMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "Champ_PercentageElit",
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            # Alterado aqui
            "crossover": UniformCrossover(),
            "mutation": SwapMutation(),
            "elitism": PercentageElitism(BASE_PARAMS["elitism_percentage"]),
        }
    ]

    n_values = [10, 15, 20, 25, 30, 35, 40]
    summary_results = []
    total_execution_time = 0

    for n in n_values:
        print(f"\n----- Testing for N = {n} -----")
        current_params = BASE_PARAMS.copy()
        current_params["n_queens"] = n
        current_params["num_generations"] = 1000
        current_params["population_size"] = 200

        for config_template in champion_configs:
            config = config_template.copy()
            config["params"] = current_params
            config["folder"] = folder

            print(f"Running configuration: {config['name']} for N={n}")

            for i in tqdm(range(2), desc=f"Runs for {config['name']}"):
                result = run_single_experiment(config, i, show_progress=True)
                result["n_queens"] = n
                summary_results.append(result)
                total_execution_time += result["execution_time"]

    print(f"\nTotal execution time for Part 5: {total_execution_time / 60:.2f} minutes.")
    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 5 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


if __name__ == "__main__":
    experiment_part_1_selection()
    experiment_part_2_crossover()
    experiment_part_3_elitism()
    experiment_part_4_mutation()
    experiment_part_5_scalability()
    print("\nAll experiments complete. Check the 'results' folder.")
    print("Now run 'python plotter.py' to generate graphs.")
