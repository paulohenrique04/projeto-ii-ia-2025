# ga/strategies/selection.py

import random
from abc import ABC, abstractmethod
from typing import List
from core.population import Population
from core.individual import Individual


class SelectionStrategy(ABC):
    """Classe base abstrata para todas as estratégias de seleção de pais."""

    @abstractmethod
    def select(self, population: Population, num_parents: int) -> List[Individual]:
        # Define a interface que todas as estratégias de seleção devem seguir.
        pass


class TournamentSelection(SelectionStrategy):
    """
    Implementa a Seleção por Torneio.
    Para cada pai a ser selecionado, um "torneio" é realizado:
    - k indivíduos são escolhidos aleatoriamente da população.
    - O indivíduo com o maior fitness entre eles é o vencedor e é selecionado como pai.
    """

    def __init__(self, tournament_size: int = 3):
        # Define 'k', o número de indivíduos que participam de cada torneio.
        self.tournament_size = tournament_size
        self.name = f"Tournament(k={tournament_size})"

    def select(self, population: Population, num_parents: int) -> List[Individual]:
        # Lista para armazenar os pais selecionados.
        selected_parents = []
        # Loop para selecionar a quantidade de pais necessária.
        for _ in range(num_parents):
            # Escolhe 'k' competidores aleatoriamente da população, sem repetição.
            # Amostragem sem reposição
            tournament_contenders = random.sample(population.individuals, self.tournament_size)
            # O vencedor do torneio é o que tem o maior fitness.
            winner = max(tournament_contenders, key=lambda ind: ind.fitness)
            # Adiciona o vencedor à lista de pais.
            selected_parents.append(winner)
        return selected_parents


class RouletteWheelSelection(SelectionStrategy):
    """
    Implementa a Seleção por Roleta (ou Fitness Proportionate Selection).
    Cada indivíduo recebe uma "fatia" da roleta proporcional ao seu fitness.
    Indivíduos mais aptos têm mais chances de serem selecionados.
    """

    def __init__(self):
        self.name = "RouletteWheel"

    def select(self, population: Population, num_parents: int) -> List[Individual]:
        # Calcula a soma total de todos os fitness da população.
        total_fitness = sum(ind.fitness for ind in population.individuals)

        # Caso especial: se todos os fitness forem 0, a divisão por zero ocorreria.
        # Nesse caso, todos têm a mesma chance de serem selecionados.
        if total_fitness == 0:
            return random.choices(population.individuals, k=num_parents)

        # Calcula a probabilidade de seleção de cada indivíduo (seu fitness / fitness total).
        selection_probs = [ind.fitness / total_fitness for ind in population.individuals]

        # Usa random.choices para selecionar 'num_parents' indivíduos.
        # O parâmetro 'weights' garante que a seleção seja feita com base nas probabilidades calculadas.
        selected_parents = random.choices(
            population.individuals,
            weights=selection_probs,
            k=num_parents
        )
        return selected_parents