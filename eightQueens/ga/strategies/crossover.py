# ga/strategies/crossover.py

import random
from abc import ABC, abstractmethod
from typing import Tuple
from core.individual import Individual


class CrossoverStrategy(ABC):
    """Classe base abstrata para estratégias de cruzamento (reprodução)."""

    @abstractmethod
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        # Toda estratégia de crossover deve receber dois pais e retornar dois filhos.
        pass


class SinglePointCrossover(CrossoverStrategy):
    """
    Implementa o Crossover de Ponto Único.
    1. Um ponto de corte é escolhido aleatoriamente no cromossomo.
    2. O primeiro filho recebe a primeira parte do pai1 e a segunda parte do pai2.
    3. O segundo filho recebe a primeira parte do pai2 e a segunda parte do pai1.
    """

    def __init__(self):
        self.name = "SinglePoint"

    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        size = len(parent1)
        # Se o cromossomo for muito pequeno, o crossover não faz sentido.
        if size < 2:
            return parent1, parent2

        # Escolhe um ponto de corte aleatório (evitando as extremidades 0 e size).
        crossover_point = random.randint(1, size - 1)

        # Cria o cromossomo do primeiro filho.
        child1_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
        # Cria o cromossomo do segundo filho.
        child2_chromosome = parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:]

        # Retorna dois novos objetos Individual.
        return Individual(child1_chromosome), Individual(child2_chromosome)


class TwoPointCrossover(CrossoverStrategy):
    """
    Implementa o Crossover de Dois Pontos.
    1. Dois pontos de corte são escolhidos aleatoriamente.
    2. O material genético ENTRE os dois pontos é trocado entre os pais.
    """

    def __init__(self):
        self.name = "TwoPoint"

    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        size = len(parent1)
        # Requer um cromossomo de tamanho mínimo 3 para ter um segmento entre dois pontos.
        if size < 3:
            return parent1, parent2

        # Escolhe dois pontos de corte distintos e os ordena.
        point1, point2 = sorted(random.sample(range(1, size), 2))

        # Cria o cromossomo do primeiro filho trocando o segmento do meio.
        child1_chromosome = (parent1.chromosome[:point1] +
                             parent2.chromosome[point1:point2] +
                             parent1.chromosome[point2:])
        # Cria o cromossomo do segundo filho.
        child2_chromosome = (parent2.chromosome[:point1] +
                             parent1.chromosome[point1:point2] +
                             parent2.chromosome[point2:])

        # Retorna dois novos objetos Individual.
        return Individual(child1_chromosome), Individual(child2_chromosome)