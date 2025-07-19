from typing import List

class Individual:
    """
    Represents an individual in the population.
    An individual is a potential solution to the N-Queens problem.

    Attributes:
        chromosome (List[int]): A list of integers representing the board state.
                                The index represents the column, and the value
                                represents the row where a queen is placed.
        fitness (float): The fitness score of the individual. Initialized to -1.
    """
    def __init__(self, chromosome: List[int]):
        if not all(isinstance(gene, int) for gene in chromosome):
            raise ValueError("Chromosome must contain only integers.")
        self.chromosome = chromosome
        self.fitness = -1.0

    def __len__(self) -> int:
        return len(self.chromosome)

    def __repr__(self) -> str:
        return f"Individual(chromosome={self.chromosome}, fitness={self.fitness:.2f})"