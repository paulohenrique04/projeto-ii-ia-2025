from core.individual import Individual


class NQueensFitness:
    """
    Calculates the fitness for an individual in the N-Queens problem.
    The fitness is defined as the number of non-attacking pairs of queens.
    A perfect solution has zero attacking pairs.
    """

    def __init__(self, n: int):
        if n < 4:
            raise ValueError("The N-Queens problem is typically defined for N >= 4.")
        self.n = n
        # The maximum number of non-attacking pairs, which is the total number of pairs.
        # This is the fitness of a perfect solution.
        self.max_fitness = n * (n - 1) / 2

    def calculate(self, individual: Individual):
        """
        Calculates and assigns the fitness to the individual.
        Fitness = Total Pairs - Attacking Pairs
        """
        chromosome = individual.chromosome
        attacking_pairs = 0

        # Horizontal and diagonal attacks. The representation already prevents vertical attacks.
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Horizontal attack
                if chromosome[i] == chromosome[j]:
                    attacking_pairs += 1
                # Diagonal attack
                elif abs(i - j) == abs(chromosome[i] - chromosome[j]):
                    attacking_pairs += 1

        individual.fitness = self.max_fitness - attacking_pairs