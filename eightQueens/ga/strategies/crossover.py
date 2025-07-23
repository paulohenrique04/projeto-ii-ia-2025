import random
from abc import ABC, abstractmethod
from typing import Tuple
from core.individual import Individual


class CrossoverStrategy(ABC):
    """Abstract base class for crossover strategies."""

    @abstractmethod
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        pass


class UniformCrossover(CrossoverStrategy):
    """
    Implementa o Crossover Uniforme.
    Para cada gene, uma escolha aleatória (como jogar uma moeda) é feita
    para decidir qual pai contribuirá com seu gene para cada filho.
    Isso resulta em uma mistura mais granular do material genético.
    """
    def __init__(self, mixing_ratio: float = 0.5):
        # mixing_ratio é a probabilidade de um gene vir do pai1. 0.5 significa 50% de chance.
        if not 0.0 <= mixing_ratio <= 1.0:
            raise ValueError("A taxa de mistura (mixing_ratio) deve estar entre 0.0 e 1.0.")
        self.mixing_ratio = mixing_ratio
        self.name = "Uniform"

    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        size = len(parent1)
        child1_chromosome = []
        child2_chromosome = []

        # Itera por cada gene do cromossomo.
        for i in range(size):
            # "Joga a moeda".
            if random.random() < self.mixing_ratio:
                # Se o resultado for menor que a taxa, o filho1 herda do pai1 e o filho2 do pai2.
                child1_chromosome.append(parent1.chromosome[i])
                child2_chromosome.append(parent2.chromosome[i])
            else:
                # Caso contrário, eles herdam dos pais opostos.
                child1_chromosome.append(parent2.chromosome[i])
                child2_chromosome.append(parent1.chromosome[i])

        # Retorna os dois novos indivíduos criados.
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