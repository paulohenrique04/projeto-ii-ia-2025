# core/individual.py

# Importa List da biblioteca typing para adicionar dicas de tipo, melhorando a legibilidade.
from typing import List


class Individual:
    """
    Representa um "indivíduo" ou uma "solução candidata" no nosso universo genético.
    No problema das N-Rainhas, um indivíduo é uma configuração específica do tabuleiro.

    Atributos:
        chromosome (List[int]): O "DNA" do indivíduo. É uma lista de inteiros onde
                                o índice representa a coluna e o valor representa a
                                linha em que a rainha está posicionada.
        fitness (float): A pontuação de qualidade do indivíduo, calculada pela
                         função de fitness. É inicializada com -1 para indicar
                         que ainda não foi avaliada.
    """

    def __init__(self, chromosome: List[int]):
        # O construtor recebe um cromossomo para criar um novo indivíduo.
        # Validação para garantir que o cromossomo contém apenas inteiros.
        if not all(isinstance(gene, int) for gene in chromosome):
            raise ValueError("O cromossomo deve conter apenas inteiros.")

        self.chromosome = chromosome
        self.fitness = -1.0  # Fitness inicial indefinido.

    def __len__(self) -> int:
        # Permite usar a função len() em um objeto Individual (ex: len(individuo)).
        # O "tamanho" de um indivíduo é o tamanho do seu cromossomo (o número de rainhas).
        return len(self.chromosome)

    def __repr__(self) -> str:
        # Define como o objeto Individual será representado como texto.
        # Útil para depuração e impressão de informações.
        return f"Indivíduo(cromossomo={self.chromosome}, fitness={self.fitness:.2f})"