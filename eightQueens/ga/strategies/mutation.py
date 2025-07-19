import random
from abc import ABC, abstractmethod
from core.individual import Individual


class MutationStrategy(ABC):
    """Abstract base class for mutation strategies."""

    @abstractmethod
    def mutate(self, individual: Individual):
        pass


class SwapMutation(MutationStrategy):
    """
    Performs swap mutation on an individual.
    Two genes (positions) are randomly selected and their values are swapped.
    """

    def __init__(self):
        self.name = "Swap"

    def mutate(self, individual: Individual):
        size = len(individual.chromosome)
        if size < 2:
            return

        idx1, idx2 = random.sample(range(size), 2)

        chromosome = individual.chromosome
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]


class RandomResettingMutation(MutationStrategy):
    """
    Performs random resetting mutation.
    A random gene is chosen and its value is changed to a new random value.
    """

    def __init__(self):
        self.name = "RandomReset"

    def mutate(self, individual: Individual):
        size = len(individual.chromosome)
        gene_to_mutate = random.randint(0, size - 1)
        new_value = random.randint(0, size - 1)
        individual.chromosome[gene_to_mutate] = new_value