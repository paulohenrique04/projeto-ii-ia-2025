# utils/logger.py

# Importa a biblioteca pandas para trabalhar com DataFrames e salvar em CSV.
import pandas as pd
# Importa a biblioteca os para manipulação de caminhos de arquivos e diretórios.
import os

class Logger:
    """
    Uma classe de utilidade para registrar o progresso do Algoritmo Genético
    e salvar os dados em um arquivo no formato CSV (Comma-Separated Values).
    """
    def __init__(self, filepath: str):
        # O construtor recebe o caminho do arquivo onde o log será salvo.
        self.filepath = filepath
        # A lista 'log_data' armazenará os dados de cada geração em memória.
        self.log_data = []
        # Chama um método privado para garantir que o diretório do arquivo exista.
        self._prepare_directory()

    def _prepare_directory(self):
        """Garante que o diretório para o arquivo de log exista. Se não, ele é criado."""
        # Pega o nome do diretório a partir do caminho completo do arquivo.
        dir_name = os.path.dirname(self.filepath)
        # Se o caminho incluir um diretório (não for apenas um nome de arquivo)...
        if dir_name:
            # ...cria o diretório e todos os seus diretórios pais, se necessário.
            # 'exist_ok=True' evita um erro caso o diretório já exista.
            os.makedirs(dir_name, exist_ok=True)

    def log_generation(self, generation: int, best_fitness: float, avg_fitness: float, worst_fitness: float):
        """
        Registra as métricas de uma única geração.
        Este método é chamado a cada iteração do loop principal do AG.
        """
        # Adiciona um dicionário à lista 'log_data' com as informações da geração.
        self.log_data.append({
            'generation': generation,
            'best_fitness': best_fitness,
            'avg_fitness': avg_fitness,
            'worst_fitness': worst_fitness
        })

    def save(self):
        """Salva todos os dados registrados em memória para o arquivo CSV."""
        # Se não houver dados para salvar, não faz nada.
        if not self.log_data:
            return
        # Cria um DataFrame do pandas a partir da lista de dicionários.
        # O DataFrame é uma estrutura de dados tabular, como uma planilha.
        df = pd.DataFrame(self.log_data)
        # Salva o DataFrame no arquivo CSV especificado.
        # 'index=False' evita que o pandas escreva o índice da linha no arquivo.
        df.to_csv(self.filepath, index=False)

    def clear(self):
        """Limpa os dados registrados em memória. Útil para reutilizar o logger."""
        self.log_data = []