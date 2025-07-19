import random
from typing import List, Optional
from tqdm import tqdm

from core.population import Population
from core.individual import Individual
from problem.n_queens import NQueensFitness
from ga.strategies.selection import SelectionStrategy
from ga.strategies.crossover import CrossoverStrategy
from ga.strategies.mutation import MutationStrategy
from ga.strategies.elitism import ElitismStrategy
from utils.logger import Logger


class GeneticAlgorithm:
    """
    The main Genetic Algorithm engine.
    It is configured with various strategies (selection, crossover, etc.)
    to solve an optimization problem.
    """

    def __init__(self,
                 n_queens: int,
                 selection_strategy: SelectionStrategy,
                 crossover_strategy: CrossoverStrategy,
                 mutation_strategy: MutationStrategy,
                 elitism_strategy: ElitismStrategy):
        self.fitness_calculator = NQueensFitness(n_queens)
        self.selection_strategy = selection_strategy
        self.crossover_strategy = crossover_strategy
        self.mutation_strategy = mutation_strategy
        self.elitism_strategy = elitism_strategy
        self.n_queens = n_queens

    def run(self,
            population_size: int,
            num_generations: int,
            mutation_rate: float,
            logger: Optional[Logger] = None) -> Individual:

        # 1. Initialization
        population = Population.generate_initial_population(population_size, self.n_queens)
        best_solution_so_far = None

        # Main generational loop
        for gen in range(num_generations):
            # 2. Fitness Evaluation
            for individual in population.individuals:
                self.fitness_calculator.calculate(individual)

            # Get stats for logging
            best_in_gen = population.get_best_individual()
            if best_solution_so_far is None or best_in_gen.fitness > best_solution_so_far.fitness:
                best_solution_so_far = best_in_gen

            # Log generation data
            if logger:
                avg_fitness = sum(ind.fitness for ind in population.individuals) / population_size
                worst_fitness = min(ind.fitness for ind in population.individuals)
                logger.log_generation(
                    gen, best_in_gen.fitness, avg_fitness, worst_fitness
                )

            # 3. Check for termination condition (solution found)
            if best_solution_so_far.fitness == self.fitness_calculator.max_fitness:
                # print(f"\nSolution found in generation {gen}!")
                break

            # 4. Create the next generation
            new_population_individuals: List[Individual] = []

            # 4a. Elitism
            elites = self.elitism_strategy.select_elites(population)
            new_population_individuals.extend(elites)

            # 4b. Crossover and Mutation
            num_offspring = population_size - len(elites)

            # Ensure an even number of parents are selected for crossover
            if num_offspring % 2 != 0:
                num_offspring += 1  # We will generate one extra and discard later if needed

            parents = self.selection_strategy.select(population, num_offspring)

            for i in range(0, num_offspring, 2):
                parent1 = parents[i]
                parent2 = parents[i + 1]

                child1, child2 = self.crossover_strategy.crossover(parent1, parent2)

                if random.random() < mutation_rate:
                    self.mutation_strategy.mutate(child1)
                if random.random() < mutation_rate:
                    self.mutation_strategy.mutate(child2)

                new_population_individuals.append(child1)
                new_population_individuals.append(child2)

            # Ensure population size is maintained
            population = Population(new_population_individuals[:population_size])

        return best_solution_so_far