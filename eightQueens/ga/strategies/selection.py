import random
from abc import ABC, abstractmethod
from typing import List
from core.population import Population
from core.individual import Individual

class SelectionStrategy(ABC):
    """Abstract base class for selection strategies."""
    @abstractmethod
    def select(self, population: Population, num_parents: int) -> List[Individual]:
        pass

class TournamentSelection(SelectionStrategy):
    """
    Selects parents using tournament selection.
    In each tournament, k individuals are chosen randomly, and the fittest is selected.
    """
    def __init__(self, tournament_size: int = 3):
        self.tournament_size = tournament_size
        self.name = f"Tournament(k={tournament_size})"

    def select(self, population: Population, num_parents: int) -> List[Individual]:
        selected_parents = []
        for _ in range(num_parents):
            tournament_contenders = random.sample(population.individuals, self.tournament_size)
            winner = max(tournament_contenders, key=lambda ind: ind.fitness)
            selected_parents.append(winner)
        return selected_parents

class RouletteWheelSelection(SelectionStrategy):
    """
    Selects parents using roulette wheel selection (fitness proportionate selection).
    """
    def __init__(self):
        self.name = "RouletteWheel"

    def select(self, population: Population, num_parents: int) -> List[Individual]:
        total_fitness = sum(ind.fitness for ind in population.individuals)
        if total_fitness == 0:
            # If all fitnesses are 0, select randomly
            return random.choices(population.individuals, k=num_parents)

        selection_probs = [ind.fitness / total_fitness for ind in population.individuals]
        selected_parents = random.choices(
            population.individuals,
            weights=selection_probs,
            k=num_parents
        )
        return selected_parents