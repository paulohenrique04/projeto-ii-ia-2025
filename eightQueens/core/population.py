import random
from typing import List
from .individual import Individual

class Population:
    """
    Represents a population of individuals for the Genetic Algorithm.

    Attributes:
        individuals (List[Individual]): A list of Individual objects.
    """
    def __init__(self, individuals: List[Individual]):
        self.individuals = individuals

    @classmethod
    def generate_initial_population(cls, population_size: int, n_queens: int):
        """
        Creates a new population with random individuals.

        Args:
            population_size (int): The number of individuals in the population.
            n_queens (int): The size of the N-Queens problem (board size).

        Returns:
            Population: A new Population object.
        """
        individuals = []
        for _ in range(population_size):
            chromosome = [random.randint(0, n_queens - 1) for _ in range(n_queens)]
            individuals.append(Individual(chromosome))
        return cls(individuals)

    def get_best_individual(self) -> Individual:
        """Returns the individual with the highest fitness."""
        return max(self.individuals, key=lambda ind: ind.fitness)

    def __len__(self) -> int:
        return len(self.individuals)