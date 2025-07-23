# ga/genetic_algorithm.py

import random
from typing import List, Optional
from tqdm import tqdm  # Biblioteca para criar barras de progresso visuais.

# Importa todas as classes e estratégias necessárias.
from core.population import Population
from core.individual import Individual
from problem.n_queens import NQueensFitness
from ga.strategies.selection import SelectionStrategy
from ga.strategies.crossover import CrossoverStrategy
from ga.strategies.mutation import MutationStrategy
from ga.strategies.elitism import ElitismStrategy
from utils.logger import Logger


class GeneticAlgorithm:
    """
    O motor principal do Algoritmo Genético.
    Esta classe orquestra todo o processo evolutivo, utilizando as
    estratégias (seleção, crossover, etc.) que foram injetadas nela.
    """

    def __init__(self,
                 n_queens: int,
                 selection_strategy: SelectionStrategy,
                 crossover_strategy: CrossoverStrategy,
                 mutation_strategy: MutationStrategy,
                 elitism_strategy: ElitismStrategy):
        # O construtor recebe todas as estratégias como parâmetros (Injeção de Dependência).
        # Isso torna o AG flexível e fácil de configurar com diferentes combinações.
        self.fitness_calculator = NQueensFitness(n_queens)
        self.selection_strategy = selection_strategy
        self.crossover_strategy = crossover_strategy
        self.mutation_strategy = mutation_strategy
        self.elitism_strategy = elitism_strategy
        self.n_queens = n_queens

    def run(self,
            population_size: int,
            num_generations: int,
            mutation_rate: float,
            logger: Optional[Logger] = None) -> Individual:

        # --- 1. INICIALIZAÇÃO ---
        # Cria a população inicial com indivíduos aleatórios.
        population = Population.generate_initial_population(population_size, self.n_queens)
        # Variável para armazenar a melhor solução encontrada até agora em todas as gerações.
        best_solution_so_far = None

        # --- Laço Evolutivo Principal ---
        # O loop executa por um número definido de gerações.
        for gen in range(num_generations):

            # --- 2. AVALIAÇÃO DE FITNESS ---
            # Calcula o fitness de cada indivíduo na população atual.
            for individual in population.individuals:
                self.fitness_calculator.calculate(individual)

            # Encontra o melhor indivíduo da geração atual.
            best_in_gen = population.get_best_individual()

            # Atualiza a melhor solução geral se o melhor da geração atual for superior.
            if best_solution_so_far is None or best_in_gen.fitness > best_solution_so_far.fitness:
                best_solution_so_far = best_in_gen

            # Se um logger foi fornecido, registra as métricas da geração atual.
            if logger:
                avg_fitness = sum(ind.fitness for ind in population.individuals) / population_size
                worst_fitness = min(ind.fitness for ind in population.individuals)
                logger.log_generation(gen, best_in_gen.fitness, avg_fitness, worst_fitness)

            # --- 3. VERIFICAÇÃO DA CONDIÇÃO DE PARADA ---
            # Se a melhor solução encontrada atingiu o fitness máximo, o problema está resolvido.
            if best_solution_so_far.fitness == self.fitness_calculator.max_fitness:
                break  # Interrompe o loop de gerações.

            # --- 4. CRIAÇÃO DA PRÓXIMA GERAÇÃO ---
            # Lista para armazenar os indivíduos da nova geração.
            new_population_individuals: List[Individual] = []

            # 4a. Elitismo: Os melhores indivíduos passam diretamente para a próxima geração.
            elites = self.elitism_strategy.select_elites(population)
            new_population_individuals.extend(elites)

            # 4b. Seleção, Crossover e Mutação para preencher o resto da população.
            num_offspring = population_size - len(elites)  # Número de "filhos" a serem criados.

            # Garante um número par de filhos para formar pares de pais.
            if num_offspring % 2 != 0:
                num_offspring += 1

                # 4b.1. Seleção: Seleciona os pais da população atual.
            parents = self.selection_strategy.select(population, num_offspring)

            # Loop para criar os filhos em pares.
            for i in range(0, num_offspring, 2):
                parent1 = parents[i]
                parent2 = parents[i + 1]

                # 4b.2. Crossover: Gera dois filhos a partir dos dois pais.
                child1, child2 = self.crossover_strategy.crossover(parent1, parent2)

                # 4b.3. Mutação: Aplica a mutação nos filhos com base na taxa de mutação.
                # random.random gere numero decimal aleatorio entre 0 e 1 onde todos tem
                # a mesma chance de serem selecionados.
                if random.random() < mutation_rate:
                    self.mutation_strategy.mutate(child1)
                if random.random() < mutation_rate:
                    self.mutation_strategy.mutate(child2)

                # Adiciona os novos filhos à lista da nova geração.
                new_population_individuals.append(child1)
                new_population_individuals.append(child2)

            # Substitui a população antiga pela nova, garantindo o mesmo tamanho.
            population = Population(new_population_individuals[:population_size])

        # Ao final de todas as gerações, retorna a melhor solução encontrada.
        return best_solution_so_far