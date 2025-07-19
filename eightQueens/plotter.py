# plotter.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

RESULTS_DIR = "results"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# Define um estilo visual agradável para os gráficos
sns.set_theme(style="whitegrid")


def plot_convergence(exp_folder: str, title: str):
    """
    Plota a convergência da média de fitness ao longo das gerações
    para as diferentes configurações de um experimento.
    """
    plt.figure(figsize=(12, 7))
    path = os.path.join(RESULTS_DIR, exp_folder)

    # Verifica se o arquivo de sumário existe para obter os nomes das configurações
    summary_path = os.path.join(path, "summary.csv")
    if not os.path.exists(summary_path):
        print(f"Aviso: Arquivo de sumário não encontrado em {path}. Pulando gráfico de convergência.")
        return

    summary_df = pd.read_csv(summary_path)
    configs = summary_df['config_name'].unique()

    for config_name in configs:
        # Padrão de busca para os arquivos de log de cada execução
        run_files_pattern = os.path.join(path, f"run_*_{config_name}*.csv")
        run_files = glob.glob(run_files_pattern)

        if not run_files:
            continue

        # Concatena os dados de todas as execuções e calcula a média do fitness por geração
        df_all_runs = pd.concat([pd.read_csv(f) for f in run_files])
        mean_fitness = df_all_runs.groupby('generation')['best_fitness'].mean().reset_index()

        sns.lineplot(data=mean_fitness, x='generation', y='best_fitness', label=config_name)

    plt.title(title, fontsize=16)
    plt.xlabel("Geração", fontsize=12)
    plt.ylabel("Melhor Fitness Médio", fontsize=12)
    plt.legend()
    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, f"{exp_folder}_convergence.png")
    plt.savefig(plot_path)
    print(f"Gráfico de convergência salvo em: {plot_path}")
    plt.close()


def plot_summary_boxplot(exp_folder: str, metric: str, title: str):
    """
    Cria um boxplot para comparar os resultados finais (ex: melhor fitness)
    das diferentes configurações de um experimento.
    """
    summary_path = os.path.join(RESULTS_DIR, exp_folder, "summary.csv")
    if not os.path.exists(summary_path):
        print(f"Aviso: Arquivo de sumário não encontrado em {os.path.dirname(summary_path)}. Pulando boxplot.")
        return

    plt.figure(figsize=(10, 6))
    df = pd.read_csv(summary_path)
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
    Plota o tempo de execução vs. tamanho do problema (N) para o experimento de escalabilidade,
    mostrando uma linha para cada variação campeã.
    """
    exp_folder = "part_5_scalability"
    summary_path = os.path.join(RESULTS_DIR, exp_folder, "summary.csv")
    if not os.path.exists(summary_path):
        print(f"Aviso: Arquivo de sumário não encontrado para {exp_folder}. Pulando gráfico de escalabilidade.")
        return

    df = pd.read_csv(summary_path)

    plt.figure(figsize=(12, 7))
    # Usa o parâmetro 'hue' para criar uma linha para cada 'config_name'
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


if __name__ == "__main__":
    print("--- Gerando Gráficos para os Experimentos ---")

    # Plot Part 1 - Seleção
    plot_convergence("part_1_selection", "Convergência: Estratégias de Seleção")
    plot_summary_boxplot("part_1_selection", "best_fitness", "Fitness Final: Estratégias de Seleção (20 Execuções)")

    # Plot Part 2 - Crossover
    plot_convergence("part_2_crossover", "Convergência: Estratégias de Crossover")
    plot_summary_boxplot("part_2_crossover", "best_fitness", "Fitness Final: Estratégias de Crossover (20 Execuções)")

    # --- AJUSTE ADICIONADO AQUI ---
    # Plot Part 3 - Elitismo
    plot_convergence("part_3_elitism", "Convergência: Estratégias de Elitismo")
    plot_summary_boxplot("part_3_elitism", "best_fitness", "Fitness Final: Estratégias de Elitismo (20 Execuções)")

    # Plot Part 4 - Mutação
    plot_convergence("part_4_mutation", "Convergência: Estratégias de Mutação")
    plot_summary_boxplot("part_4_mutation", "best_fitness", "Fitness Final: Estratégias de Mutação (20 Execuções)")

    # Plot Part 5 - Escalabilidade
    plot_scalability()

    print("\nTodos os gráficos foram gerados. Verifique a pasta 'plots'.")