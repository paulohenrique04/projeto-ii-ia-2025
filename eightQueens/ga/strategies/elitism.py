from abc import ABC, abstractmethod
from typing import List
from core.population import Population
from core.individual import Individual

class ElitismStrategy(ABC):
    """Abstract base class for elitism strategies."""
    @abstractmethod
    def select_elites(self, population: Population) -> List[Individual]:
        pass

class BestNElitism(ElitismStrategy):
    """
    Selects the top N fittest individuals from the population as elites.
    """
    def __init__(self, n: int):
        self.n = n
        self.name = f"BestN(n={n})"

    def select_elites(self, population: Population) -> List[Individual]:
        sorted_individuals = sorted(population.individuals, key=lambda ind: ind.fitness, reverse=True)
        return sorted_individuals[:self.n]

class PercentageElitism(ElitismStrategy):
    """
    Selects a top percentage of the fittest individuals as elites.
    """
    def __init__(self, percentage: float):
        if not 0.0 <= percentage <= 1.0:
            raise ValueError("Percentage must be between 0.0 and 1.0.")
        self.percentage = percentage
        self.name = f"Percentage(p={percentage*100:.0f}%)"

    def select_elites(self, population: Population) -> List[Individual]:
        num_elites = int(len(population) * self.percentage)
        sorted_individuals = sorted(population.individuals, key=lambda ind: ind.fitness, reverse=True)
        return sorted_individuals[:num_elites]