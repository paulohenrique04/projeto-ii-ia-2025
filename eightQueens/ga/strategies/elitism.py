# ga/strategies/elitism.py

# Importa ferramentas para criar classes abstratas e definir métodos abstratos.
# Isso força que qualquer estratégia de elitismo tenha o mesmo método 'select_elites'.
from abc import ABC, abstractmethod
# Importa tipos para legibilidade.
from typing import List
from core.population import Population
from core.individual import Individual

class ElitismStrategy(ABC):
    """Classe base abstrata para todas as estratégias de elitismo."""
    @abstractmethod
    def select_elites(self, population: Population) -> List[Individual]:
        # Toda classe filha DEVE implementar este método.
        pass

class BestNElitism(ElitismStrategy):
    """
    Implementa uma estratégia de elitismo simples: os 'N' melhores indivíduos
    da geração atual são garantidos na próxima geração, imunes a crossover e mutação.
    """
    def __init__(self, n: int):
        # O construtor define quantos indivíduos de elite (N) serão selecionados.
        self.n = n
        self.name = f"BestN(n={n})"  # Nome para identificação nos logs.

    def select_elites(self, population: Population) -> List[Individual]:
        # Ordena todos os indivíduos da população em ordem decrescente de fitness.
        sorted_individuals = sorted(population.individuals, key=lambda ind: ind.fitness, reverse=True)
        # Retorna uma lista contendo os 'n' primeiros indivíduos da lista ordenada.
        return sorted_individuals[:self.n]

class PercentageElitism(ElitismStrategy):
    """
    Implementa o elitismo com base em uma porcentagem da população.
    Por exemplo, os 10% melhores indivíduos sobrevivem para a próxima geração.
    """
    def __init__(self, percentage: float):
        # Valida se a porcentagem está entre 0 e 1.
        if not 0.0 <= percentage <= 1.0:
            raise ValueError("A porcentagem deve estar entre 0.0 e 1.0.")
        self.percentage = percentage
        self.name = f"Percentage(p={percentage*100:.0f}%)" # Nome para logs.

    def select_elites(self, population: Population) -> List[Individual]:
        # Calcula o número de elites com base na porcentagem do tamanho da população.
        num_elites = int(len(population) * self.percentage)
        # Ordena os indivíduos em ordem decrescente de fitness.
        sorted_individuals = sorted(population.individuals, key=lambda ind: ind.fitness, reverse=True)
        # Retorna os 'num_elites' melhores indivíduos.
        return sorted_individuals[:num_elites]