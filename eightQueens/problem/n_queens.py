# problem/n_queens.py

# Importa a classe Individual, pois a função de fitness opera sobre um indivíduo.
from core.individual import Individual


class NQueensFitness:
    """
    Esta classe encapsula a lógica para calcular o "fitness" (a "qualidade" ou "aptidão")
    de um indivíduo para o problema das N-Rainhas.
    O fitness aqui é definido como o número de pares de rainhas que NÃO se atacam.
    Quanto maior o fitness, melhor a solução.
    """

    def __init__(self, n: int):
        # O construtor da classe recebe 'n', o tamanho do tabuleiro.
        if n < 4:
            # Garante que o problema seja para um tabuleiro de tamanho razoável.
            raise ValueError("O Problema das N-Rainhas é tipicamente definido para N >= 4.")
        self.n = n

        # Pré-calcula o fitness máximo possível. Isso ocorre quando não há nenhum ataque.
        # O número total de pares únicos de rainhas em um tabuleiro n x n é n*(n-1)/2.
        # Este será o fitness de uma solução perfeita.
        self.max_fitness = n * (n - 1) / 2

    def calculate(self, individual: Individual):
        """
        Calcula o fitness de um dado indivíduo e atribui o valor a ele.
        A fórmula é: Fitness = (Total de Pares Possíveis) - (Pares em Conflito)
        """
        # Pega o cromossomo (a lista de posições das rainhas) do indivíduo.
        chromosome = individual.chromosome

        # Inicia um contador para os pares de rainhas que se atacam.
        attacking_pairs = 0

        # A representação usada (um vetor onde o índice é a coluna e o valor é a linha)
        # já impede ataques na vertical, pois só há uma rainha por coluna.
        # Portanto, precisamos verificar apenas ataques na horizontal e nas diagonais.

        # Itera por cada rainha (i) no tabuleiro.
        for i in range(self.n):
            # Compara a rainha 'i' com todas as rainhas à sua direita (j).
            # Isso evita contar o mesmo par duas vezes (ex: par i-j e j-i).
            for j in range(i + 1, self.n):
                # Verifica se há um ataque na horizontal (mesma linha).
                if chromosome[i] == chromosome[j]:
                    attacking_pairs += 1
                # Verifica se há um ataque na diagonal.
                # Duas rainhas estão na mesma diagonal se a distância vertical entre elas
                # for igual à distância horizontal.
                elif abs(i - j) == abs(chromosome[i] - chromosome[j]):
                    attacking_pairs += 1

        # O fitness final é o máximo possível menos o número de conflitos encontrados.
        individual.fitness = self.max_fitness - attacking_pairs