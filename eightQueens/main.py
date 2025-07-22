# main.py

# --- Bloco de Importações ---
# Importa bibliotecas padrão do Python.
import os  # Usado para interagir com o sistema operacional, como criar diretórios.
import time  # Usado para medir o tempo de execução dos algoritmos.

# Importa bibliotecas de terceiros, essenciais para o projeto.
import \
    pandas as pd  # Poderosa biblioteca para manipulação e análise de dados, usada para criar e salvar os arquivos .csv.
from tqdm import tqdm  # Usada para criar barras de progresso visuais e amigáveis no terminal.

# Importa as classes principais do nosso projeto.
from ga.genetic_algorithm import GeneticAlgorithm  # O motor do nosso Algoritmo Genético.
from utils.logger import Logger  # A classe utilitária para registrar os resultados.

# Importa todas as estratégias que implementamos.
# Esta abordagem modular nos permite montar diferentes tipos de AGs facilmente.
from ga.strategies.selection import TournamentSelection, RouletteWheelSelection
from ga.strategies.crossover import SinglePointCrossover, TwoPointCrossover
from ga.strategies.mutation import SwapMutation, RandomResettingMutation
from ga.strategies.elitism import BestNElitism, PercentageElitism

# --- Configuração Base do Experimento ---
# Este dicionário define os parâmetros padrão que serão usados nos experimentos.
# É uma boa prática centralizar os parâmetros para facilitar o ajuste.
BASE_PARAMS = {
    "n_queens": 10,  # O tamanho do problema: um tabuleiro 10x10 com 10 rainhas.
    "population_size": 100,  # O número de indivíduos (soluções candidatas) em cada geração.
    "num_generations": 500,  # O critério de parada: o AG irá parar após 500 gerações.
    "mutation_rate": 0.05,  # A probabilidade (5%) de um novo indivíduo (filho) sofrer uma mutação.
    "elitism_n": 2,  # O número de "elites" (melhores indivíduos) a serem preservados na estratégia BestNElitism.
    "elitism_percentage": 0.1,  # A porcentagem (10%) de elites a serem preservadas na estratégia PercentageElitism.
    "tournament_k": 3,  # O número de "competidores" em cada torneio na estratégia TournamentSelection.
    "num_runs": 20,
    # O número de vezes que cada experimento será repetido para garantir resultados estatisticamente relevantes.
}

# --- Preparação do Diretório de Resultados ---
# Define o nome da pasta onde todos os arquivos de resultado serão salvos.
RESULTS_DIR = "results"
# Garante que esta pasta exista. Se não existir, o 'os.makedirs' a criará.
# 'exist_ok=True' previne um erro caso a pasta já tenha sido criada.
os.makedirs(RESULTS_DIR, exist_ok=True)


# --- Funções de Experimento (Parte 1 a 4) ---
# O padrão para as próximas 4 funções é o mesmo:
# 1. Definir duas configurações de AG que diferem em apenas UMA estratégia.
# 2. Executar cada configuração 'num_runs' vezes.
# 3. Salvar um sumário dos resultados finais em um arquivo .csv.

def experiment_part_1_selection():
    """Esta função executa a Parte 1 do trabalho: comparar duas estratégias de seleção."""
    # Imprime um cabeçalho no console para indicar qual experimento está rodando.
    print("\n--- Running Experiment Part 1: Selection Strategies ---")
    # Define o nome da subpasta onde os resultados desta parte serão salvos.
    folder = "part_1_selection"

    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)
    # 'configs' é uma lista de dicionários. Cada dicionário é uma "receita" para montar um AG completo.
    configs = [
        {
            "name": "Tournament",  # Um nome para identificar esta configuração.
            "folder": folder,  # A pasta de resultados.
            "params": BASE_PARAMS,  # Usa os parâmetros base definidos anteriormente.
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),  # A estratégia de seleção a ser testada.
            "crossover": SinglePointCrossover(),  # As outras estratégias são mantidas fixas (baseline).
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "RouletteWheel",  # A segunda configuração, que só difere na estratégia de seleção.
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": RouletteWheelSelection(),  # A única linha diferente da configuração acima.
            "crossover": SinglePointCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        }
    ]

    # Lista vazia para armazenar o resultado final de cada uma das 40 execuções (20 de cada config).
    summary_results = []
    # Loop sobre as configurações (primeiro 'Tournament', depois 'RouletteWheel').
    for config in configs:
        print(f"Testing configuration: {config['name']}")
        # Loop que executa o experimento 'num_runs' (20) vezes para obter robustez estatística.
        # 'tqdm' envolve o loop para mostrar uma barra de progresso.
        for i in tqdm(range(BASE_PARAMS["num_runs"]), desc=f"Runs for {config['name']}"):
            # Chama a função auxiliar para rodar uma única instância do AG.
            result = run_single_experiment(config, i)
            # Adiciona o dicionário de resultado (fitness final, tempo, etc.) à lista de sumários.
            summary_results.append(result)

    # Após todas as execuções, converte a lista de resultados em um DataFrame do pandas.
    df = pd.DataFrame(summary_results)
    # Salva o DataFrame em um arquivo 'summary.csv' na pasta correta.
    # 'index=False' evita que o pandas salve o índice das linhas no arquivo.
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 1 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


def experiment_part_2_crossover():
    """Executa a Parte 2: comparar duas estratégias de crossover. A lógica é idêntica à da Parte 1."""
    print("\n--- Running Experiment Part 2: Crossover Strategies ---")
    folder = "part_2_crossover"

    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    configs = [
        # A primeira configuração usa Crossover de Ponto Único.
        {
            "name": "SinglePoint",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": SinglePointCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        # A segunda configuração usa Crossover de Dois Pontos.
        {
            "name": "TwoPoint",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": TwoPointCrossover(),  # A única diferença está aqui.
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        }
    ]

    summary_results = []
    for config in configs:
        print(f"Testing configuration: {config['name']}")
        for i in tqdm(range(BASE_PARAMS["num_runs"]), desc=f"Runs for {config['name']}"):
            result = run_single_experiment(config, i)
            summary_results.append(result)

    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 2 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


def experiment_part_3_elitism():
    """Executa a Parte 3: comparar duas estratégias de elitismo."""
    print("\n--- Running Experiment Part 3: Elitism Strategies ---")
    folder = "part_3_elitism"

    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    configs = [
        # A primeira configuração usa Elitismo por 'N' melhores.
        {
            "name": "BestN",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": SinglePointCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        # A segunda configuração usa Elitismo por Porcentagem.
        {
            "name": "Percentage",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": SinglePointCrossover(),
            "mutation": SwapMutation(),
            "elitism": PercentageElitism(BASE_PARAMS["elitism_percentage"]),  # A única diferença está aqui.
        }
    ]

    summary_results = []
    for config in configs:
        print(f"Testing configuration: {config['name']}")
        for i in tqdm(range(BASE_PARAMS["num_runs"]), desc=f"Runs for {config['name']}"):
            result = run_single_experiment(config, i)
            summary_results.append(result)

    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 3 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


def experiment_part_4_mutation():
    """Executa a Parte 4: comparar duas estratégias de mutação."""
    print("\n--- Running Experiment Part 4: Mutation Strategies ---")
    folder = "part_4_mutation"

    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    configs = [
        # A primeira configuração usa Mutação por Troca (Swap).
        {
            "name": "Swap",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": SinglePointCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        # A segunda configuração usa Mutação por Reset Aleatório.
        {
            "name": "RandomReset",
            "folder": folder,
            "params": BASE_PARAMS,
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": SinglePointCrossover(),
            "mutation": RandomResettingMutation(),  # A única diferença está aqui.
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        }
    ]

    summary_results = []
    for config in configs:
        print(f"Testing configuration: {config['name']}")
        for i in tqdm(range(BASE_PARAMS["num_runs"]), desc=f"Runs for {config['name']}"):
            result = run_single_experiment(config, i)
            summary_results.append(result)

    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 4 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


def run_single_experiment(config: dict, run_id: int, show_progress=False):
    """Função auxiliar que executa uma única instância de uma configuração de AG."""

    # Cria um objeto Logger para registrar os dados da execução.
    # A expressão ternária (if/else em uma linha) desabilita o logger se 'show_progress' for True.
    # Isso é usado na Parte 5 para não gerar centenas de arquivos de log detalhados.
    logger = Logger(
        os.path.join(  # os.path.join monta o caminho do arquivo de forma segura para qualquer sistema operacional.
            RESULTS_DIR, config["folder"], f"run_{run_id}_{config['name']}_n{config['params']['n_queens']}.csv"
        )
    ) if not show_progress else None

    # Monta o objeto do Algoritmo Genético, passando as estratégias definidas no dicionário 'config'.
    # Este é o poder do Padrão de Projeto Strategy: montamos o algoritmo dinamicamente.
    ga = GeneticAlgorithm(
        n_queens=config["params"]["n_queens"],
        selection_strategy=config["selection"],
        crossover_strategy=config["crossover"],
        mutation_strategy=config["mutation"],
        elitism_strategy=config["elitism"],
    )

    # Marca o tempo de início da execução.
    start_time = time.time()
    # Roda o algoritmo genético com os parâmetros numéricos e o logger.
    best_solution = ga.run(
        population_size=config["params"]["population_size"],
        num_generations=config["params"]["num_generations"],
        mutation_rate=config["params"]["mutation_rate"],
        logger=logger,
    )
    # Marca o tempo de fim da execução.
    end_time = time.time()

    # Se um logger foi criado, chama o método para salvar os dados no arquivo .csv.
    if logger:
        logger.save()

    # Retorna um dicionário contendo as informações mais importantes sobre o resultado desta execução.
    return {
        "run_id": run_id,  # O ID desta execução (de 0 a 19).
        "config_name": config["name"],  # O nome da configuração testada.
        "best_fitness": best_solution.fitness,  # O fitness da melhor solução encontrada.
        "execution_time": end_time - start_time,  # O tempo total que a execução levou.
        "solution_found": best_solution.fitness == ga.fitness_calculator.max_fitness
        # Um booleano (True/False) indicando se a solução perfeita foi encontrada.
    }


def experiment_part_5_scalability():
    """
    Executa a Parte 5: testar as variações campeãs em problemas de tamanho crescente (N)
    para analisar a escalabilidade e o tempo de execução.
    """
    print("\n--- Running Experiment Part 5: Scalability (Problem Size) ---")
    folder = "part_5_scalability"

    # Define as 4 variações "campeãs", baseadas nos resultados prováveis das Partes 1-4.
    # Cada uma representa um algoritmo forte que se destacou em uma categoria.

    os.makedirs(os.path.join(RESULTS_DIR, folder), exist_ok=True)

    champion_configs = [
        {
            "name": "Champ_TournamentSel",  # Esta é a configuração base, considerada forte.
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": SinglePointCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "Champ_TwoPointCross",  # Variação com o crossover campeão.
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": TwoPointCrossover(),
            "mutation": SwapMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "Champ_RandomResetMut",  # Variação com a mutação campeã.
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": SinglePointCrossover(),
            "mutation": RandomResettingMutation(),
            "elitism": BestNElitism(BASE_PARAMS["elitism_n"]),
        },
        {
            "name": "Champ_PercentageElit",  # Variação com o elitismo campeão.
            "selection": TournamentSelection(BASE_PARAMS["tournament_k"]),
            "crossover": SinglePointCrossover(),
            "mutation": SwapMutation(),
            "elitism": PercentageElitism(BASE_PARAMS["elitism_percentage"]),
        }
    ]

    # Lista de tamanhos de problema (N) a serem testados.
    n_values = [10, 15, 20, 25, 30, 35]
    summary_results = []
    total_execution_time = 0

    # Loop principal que itera sobre os diferentes tamanhos de problema.
    for n in n_values:
        print(f"\n----- Testing for N = {n} -----")
        # Cria uma cópia dos parâmetros base e os ajusta para o N atual.
        # Problemas maiores podem precisar de mais gerações/população.
        current_params = BASE_PARAMS.copy()
        current_params["n_queens"] = n
        current_params["num_generations"] = 1000
        current_params["population_size"] = 200

        # Loop que itera sobre cada uma das 4 configurações campeãs.
        for config_template in champion_configs:
            config = config_template.copy()  # Cria uma cópia para não alterar o template original.
            config["params"] = current_params
            config["folder"] = folder

            print(f"Running configuration: {config['name']} for N={n}")

            # Executa o AG apenas 2 vezes para cada N e cada config, pois o objetivo aqui é medir o tempo.
            for i in tqdm(range(2), desc=f"Runs for {config['name']}"):
                # Chama 'run_single_experiment' com 'show_progress=True' para desativar a criação de logs detalhados.
                result = run_single_experiment(config, i, show_progress=True)
                result["n_queens"] = n  # Adiciona o valor de N aos resultados para a análise.
                summary_results.append(result)
                total_execution_time += result["execution_time"]  # Acumula o tempo de execução total.

    # Ao final de todas as execuções, imprime o tempo total em minutos.
    print(f"\nTotal execution time for Part 5: {total_execution_time / 60:.2f} minutes.")
    # Salva o sumário completo da Parte 5 em um arquivo .csv.
    df = pd.DataFrame(summary_results)
    df.to_csv(os.path.join(RESULTS_DIR, folder, "summary.csv"), index=False)
    print(f"Part 5 Summary saved to {os.path.join(RESULTS_DIR, folder, 'summary.csv')}")


# --- Ponto de Entrada Principal do Script ---
# O bloco 'if __name__ == "__main__"' é uma convenção em Python que garante que o código
# dentro dele só será executado quando o arquivo é rodado diretamente (e não quando é importado por outro arquivo).
if __name__ == "__main__":
    # Chama cada uma das funções de experimento em sequência.
    experiment_part_1_selection()
    experiment_part_2_crossover()
    experiment_part_3_elitism()
    experiment_part_4_mutation()
    experiment_part_5_scalability()

    # Imprime mensagens finais para guiar o usuário.
    print("\nAll experiments complete. Check the 'results' folder.")
    print("Now run 'python plotter.py' to generate graphs.")