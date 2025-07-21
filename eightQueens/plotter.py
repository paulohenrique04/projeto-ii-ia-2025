# plotter.py

# Importa as bibliotecas de visualização e manipulação de dados.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Importa bibliotecas para manipulação de arquivos e diretórios.
import os
import glob

# Define os nomes dos diretórios de resultados e de gráficos.
RESULTS_DIR = "results"
PLOTS_DIR = "plots"
# Garante que o diretório para salvar os gráficos exista.
os.makedirs(PLOTS_DIR, exist_ok=True)

# Define um tema visual padrão para todos os gráficos, para consistência.
sns.set_theme(style="whitegrid")


# --- FUNÇÕES DE PLOTAGEM ---
# Cada função é responsável por criar um tipo específico de gráfico.

def plot_convergence(exp_folder: str, title: str):
    """
    Plota o gráfico de convergência (Melhor Fitness Médio x Geração).
    Este gráfico mostra a velocidade com que cada estratégia melhora.
    """
    # Cria a figura e os eixos para o gráfico.
    plt.figure(figsize=(12, 7))
    # Monta o caminho para a pasta do experimento.
    path = os.path.join(RESULTS_DIR, exp_folder)

    # Lê o arquivo de sumário para obter os nomes das configurações testadas.
    summary_df = pd.read_csv(os.path.join(path, "summary.csv"))
    configs = summary_df['config_name'].unique()

    # Itera sobre cada configuração (ex: 'Tournament', 'RouletteWheel').
    for config_name in configs:
        # Encontra todos os arquivos de log detalhado para esta configuração.
        run_files = glob.glob(os.path.join(path, f"run_*_{config_name}*.csv"))

        # Se não houver arquivos de log, pula para a próxima configuração.
        if not run_files:
            continue

        # Lê todos os arquivos CSV e os concatena em um único DataFrame.
        df_all_runs = pd.concat([pd.read_csv(f) for f in run_files])
        # Agrupa os dados por geração e calcula a média do 'best_fitness' entre todas as execuções.
        mean_fitness = df_all_runs.groupby('generation')['best_fitness'].mean().reset_index()

        # Plota a linha de convergência para esta configuração.
        sns.lineplot(data=mean_fitness, x='generation', y='best_fitness', label=config_name)

    # Configura os títulos e rótulos do gráfico.
    plt.title(title, fontsize=16)
    plt.xlabel("Geração", fontsize=12)
    plt.ylabel("Melhor Fitness Médio", fontsize=12)
    plt.legend()
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição.
    # Salva o gráfico como um arquivo de imagem.
    plot_path = os.path.join(PLOTS_DIR, f"{exp_folder}_convergence.png")
    plt.savefig(plot_path)
    print(f"Gráfico de convergência salvo em: {plot_path}")
    plt.close()  # Fecha a figura para liberar memória.


def plot_summary_boxplot(exp_folder: str, metric: str, title: str):
    """
    Cria um boxplot para comparar a distribuição dos resultados finais.
    Este gráfico é excelente para analisar a consistência e a qualidade final das soluções.
    """
    summary_path = os.path.join(RESULTS_DIR, exp_folder, "summary.csv")
    if not os.path.exists(summary_path):
        return

    plt.figure(figsize=(10, 6))
    # Lê o arquivo de sumário.
    df = pd.read_csv(summary_path)
    # Cria o boxplot, comparando o 'metric' (ex: 'best_fitness') para cada 'config_name'.
    sns.boxplot(data=df, x='config_name', y=metric)

    plt.title(title, fontsize=16)
    plt.xlabel("Configuração", fontsize=12)
    plt.ylabel(metric.replace('_', ' ').title(), fontsize=12)
    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, f"{exp_folder}_{metric}_boxplot.png")
    plt.savefig(plot_path)
    print(f"Gráfico de boxplot salvo em: {plot_path}")
    plt.close()


def plot_scalability():
    """
    Plota o gráfico de escalabilidade (Tempo de Execução x Tamanho do Problema).
    Mostra como cada algoritmo campeão se comporta com o aumento da complexidade.
    """
    exp_folder = "part_5_scalability"
    summary_path = os.path.join(RESULTS_DIR, exp_folder, "summary.csv")
    if not os.path.exists(summary_path):
        return

    df = pd.read_csv(summary_path)

    plt.figure(figsize=(12, 7))
    # Cria um gráfico de linha. O parâmetro 'hue' cria uma linha de cor diferente
    # para cada 'config_name', permitindo a comparação direta.
    sns.lineplot(data=df, x='n_queens', y='execution_time', hue='config_name', marker='o', errorbar='sd')

    plt.title("Escalabilidade do AG: Tempo de Execução vs. Tamanho do Problema (N)", fontsize=16)
    plt.xlabel("Número de Rainhas (N)", fontsize=12)
    plt.ylabel("Tempo Médio de Execução (segundos)", fontsize=12)
    plt.grid(True)
    plt.legend(title='Variação Campeã')
    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, f"{exp_folder}_time_vs_n.png")
    plt.savefig(plot_path)
    print(f"Gráfico de escalabilidade salvo em: {plot_path}")
    plt.close()


# --- PONTO DE ENTRADA DO SCRIPT ---
if __name__ == "__main__":
    print("--- Gerando Gráficos para os Experimentos ---")

    # Chama cada função de plotagem para cada parte do experimento.
    # Plot Part 1 - Seleção
    plot_convergence("part_1_selection", "Convergência: Estratégias de Seleção")
    plot_summary_boxplot("part_1_selection", "best_fitness", "Fitness Final: Estratégias de Seleção (20 Execuções)")

    # Plot Part 2 - Crossover
    plot_convergence("part_2_crossover", "Convergência: Estratégias de Crossover")
    plot_summary_boxplot("part_2_crossover", "best_fitness", "Fitness Final: Estratégias de Crossover (20 Execuções)")

    # Plot Part 3 - Elitismo
    plot_convergence("part_3_elitism", "Convergência: Estratégias de Elitismo")
    plot_summary_boxplot("part_3_elitism", "best_fitness", "Fitness Final: Estratégias de Elitismo (20 Execuções)")

    # Plot Part 4 - Mutação
    plot_convergence("part_4_mutation", "Convergência: Estratégias de Mutação")
    plot_summary_boxplot("part_4_mutation", "best_fitness", "Fitness Final: Estratégias de Mutação (20 Execuções)")

    # Plot Part 5 - Escalabilidade
    plot_scalability()

    print("\nTodos os gráficos foram gerados. Verifique a pasta 'plots'.")