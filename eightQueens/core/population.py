# core/population.py

# Importa a biblioteca random para gerar indivíduos aleatórios.
import random
# Importa List para dicas de tipo.
from typing import List
# Importa a classe Individual, pois uma população é um conjunto de indivíduos.
from .individual import Individual

class Population:
    """
    Representa uma população, que é um conjunto de indivíduos.
    É nesta população que a evolução ocorre a cada geração.

    Atributos:
        individuals (List[Individual]): Uma lista de objetos da classe Individual.
    """
    def __init__(self, individuals: List[Individual]):
        # O construtor simplesmente armazena a lista de indivíduos fornecida.
        self.individuals = individuals

    @classmethod
    def generate_initial_population(cls, population_size: int, n_queens: int):
        """
        Um método de classe (classmethod) para criar a primeira geração da população
        com indivíduos gerados aleatoriamente.

        Args:
            population_size (int): Quantos indivíduos a população deve ter.
            n_queens (int): O tamanho do tabuleiro (e do cromossomo de cada indivíduo).

        Returns:
            Population: Um novo objeto Population com os indivíduos aleatórios.
        """
        # Lista para armazenar os novos indivíduos.
        individuals = []
        # Loop para criar o número desejado de indivíduos.
        for _ in range(population_size):
            # Para cada indivíduo, cria um cromossomo aleatório.
            # Cada gene (posição da rainha na coluna) recebe um valor de linha aleatório entre 0 e n-1.
            chromosome = [random.randint(0, n_queens - 1) for _ in range(n_queens)]
            # Cria um objeto Individual com o cromossomo aleatório e o adiciona à lista.
            individuals.append(Individual(chromosome))
        # Retorna uma nova instância da classe Population, contendo a lista de indivíduos criada.
        return cls(individuals)

    def get_best_individual(self) -> Individual:
        """Retorna o indivíduo com o maior fitness (o mais apto) da população atual."""
        # Usa a função max() para encontrar o indivíduo com o valor máximo no atributo 'fitness'.
        return max(self.individuals, key=lambda ind: ind.fitness)

    def __len__(self) -> int:
        # Permite usar a função len() em um objeto Population (ex: len(populacao)).
        # O tamanho da população é o número de indivíduos que ela contém.
        return len(self.individuals)