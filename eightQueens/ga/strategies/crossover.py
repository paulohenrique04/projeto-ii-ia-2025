import random
from abc import ABC, abstractmethod
from typing import Tuple
from core.individual import Individual


class CrossoverStrategy(ABC):
    """Abstract base class for crossover strategies."""

    @abstractmethod
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        pass


class SinglePointCrossover(CrossoverStrategy):
    """
    Performs single-point crossover between two parents.
    """

    def __init__(self):
        self.name = "SinglePoint"

    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        size = len(parent1)
        if size < 2:
            return parent1, parent2

        crossover_point = random.randint(1, size - 1)
        child1_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
        child2_chromosome = parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:]

        return Individual(child1_chromosome), Individual(child2_chromosome)


class TwoPointCrossover(CrossoverStrategy):
    """
    Performs two-point crossover between two parents.
    """

    def __init__(self):
        self.name = "TwoPoint"

    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        size = len(parent1)
        if size < 3:
            return parent1, parent2

        point1, point2 = sorted(random.sample(range(1, size), 2))

        child1_chromosome = (parent1.chromosome[:point1] +
                             parent2.chromosome[point1:point2] +
                             parent1.chromosome[point2:])
        child2_chromosome = (parent2.chromosome[:point1] +
                             parent1.chromosome[point1:point2] +
                             parent2.chromosome[point2:])

        return Individual(child1_chromosome), Individual(child2_chromosome)