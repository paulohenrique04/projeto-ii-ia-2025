# ga/strategies/mutation.py

import random
from abc import ABC, abstractmethod
from core.individual import Individual


class MutationStrategy(ABC):
    """Classe base abstrata para estratégias de mutação."""

    @abstractmethod
    def mutate(self, individual: Individual):
        # Toda estratégia de mutação deve modificar um indivíduo "in-place" (diretamente).
        pass


class SwapMutation(MutationStrategy):
    """
    Implementa a Mutação por Troca (Swap).
    Dois genes (posições) do cromossomo são escolhidos aleatoriamente
    e seus valores são trocados.
    """

    def __init__(self):
        self.name = "Swap"

    def mutate(self, individual: Individual):
        size = len(individual.chromosome)
        if size < 2:
            return  # A troca não é possível.

        # Escolhe dois índices distintos aleatoriamente.
        idx1, idx2 = random.sample(range(size), 2)

        chromosome = individual.chromosome
        # Realiza a troca dos valores nos índices escolhidos.
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]


class RandomResettingMutation(MutationStrategy):
    """
    Implementa a Mutação por Reinicialização Aleatória.
    Um gene (posição) do cromossomo é escolhido aleatoriamente
    e seu valor é substituído por um novo valor aleatório.
    """

    def __init__(self):
        self.name = "RandomReset"

    def mutate(self, individual: Individual):
        size = len(individual.chromosome)
        # Escolhe um índice aleatório no cromossomo para sofrer mutação.
        gene_to_mutate = random.randint(0, size - 1)
        # Gera um novo valor aleatório para este gene.
        new_value = random.randint(0, size - 1)
        # Atribui o novo valor, modificando o cromossomo.
        individual.chromosome[gene_to_mutate] = new_value