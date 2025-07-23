import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# --- CONFIGURAÇÕES GLOBAIS ---
RESULTS_DIR = "results"
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# Define um tema visual padrão para todos os gráficos, para consistência.
sns.set_theme(style="whitegrid")


# --- FUNÇÕES DE PLOTAGEM ---

def plot_convergence(exp_folder: str, title: str):
    """
    Plota a convergência da média de fitness ao longo das gerações
    para as diferentes configurações de um experimento.
    """
    plt.figure(figsize=(12, 7))
    path = os.path.join(RESULTS_DIR, exp_folder)

    summary_path = os.path.join(path, "summary.csv")
    if not os.path.exists(summary_path):
        print(f"Aviso: Arquivo de sumário não encontrado em {path}. Pulando gráfico de convergência.")
        return

    summary_df = pd.read_csv(summary_path)
    configs = summary_df['config_name'].unique()

    for config_name in configs:
        run_files_pattern = os.path.join(path, f"run_*_{config_name}*.csv")
        run_files = glob.glob(run_files_pattern)

        if not run_files:
            continue

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
    print(f"-> Gráfico de convergência salvo em: {plot_path}")
    plt.close()


def plot_experiment_summary(exp_folder: str, exp_name: str):
    """
    Gera um conjunto de gráficos de resumo para um experimento,
    analisando fitness e taxa de sucesso.
    """
    summary_path = os.path.join(RESULTS_DIR, exp_folder, "summary.csv")
    if not os.path.exists(summary_path):
        print(f"Aviso: Arquivo de sumário para '{exp_name}' não encontrado. Pulando gráficos de resumo.")
        return

    df = pd.read_csv(summary_path)

    # --- GRÁFICO 1: Violino + Enxame (Distribuição do Fitness) ---
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df, x='config_name', y='best_fitness', inner=None, color=".8")
    sns.swarmplot(data=df, x='config_name', y='best_fitness', size=5)
    plt.title(f"Distribuição do Fitness Final: {exp_name}", fontsize=16)
    plt.xlabel("Configuração", fontsize=12)
    plt.ylabel("Melhor Fitness Final", fontsize=12)
    plt.tight_layout()
    plot_path_violin = os.path.join(PLOTS_DIR, f"{exp_folder}_fitness_distribution.png")
    plt.savefig(plot_path_violin)
    print(f"-> Gráfico de distribuição de fitness salvo em: {plot_path_violin}")
    plt.close()

    # --- [BLOCO REMOVIDO] O código que gerava o boxplot de tempo de execução foi removido daqui. ---

    # --- GRÁFICO 2: Barras (Taxa de Sucesso) ---
    success_rate = df.groupby('config_name')['solution_found'].mean().reset_index()
    success_rate['solution_found'] *= 100

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(data=success_rate, x='config_name', y='solution_found')
    for p in barplot.patches:
        barplot.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 9), textcoords='offset points')
    plt.title(f"Taxa de Sucesso (Solução Ótima): {exp_name}", fontsize=16)
    plt.xlabel("Configuração", fontsize=12)
    plt.ylabel("Taxa de Sucesso (%)", fontsize=12)
    plt.ylim(0, 105)
    plt.tight_layout()
    plot_path_success = os.path.join(PLOTS_DIR, f"{exp_folder}_success_rate.png")
    plt.savefig(plot_path_success)
    print(f"-> Gráfico de taxa de sucesso salvo em: {plot_path_success}")
    plt.close()


def plot_scalability():
    """
    Plota o tempo de execução vs. tamanho do problema (N) para o experimento de escalabilidade.
    """
    exp_folder = "part_5_scalability"
    summary_path = os.path.join(RESULTS_DIR, exp_folder, "summary.csv")
    if not os.path.exists(summary_path):
        return

    df = pd.read_csv(summary_path)

    plt.figure(figsize=(12, 7))
    sns.lineplot(data=df, x='n_queens', y='execution_time', hue='config_name', marker='o', errorbar='sd')
    plt.title("Escalabilidade do AG: Tempo de Execução vs. Tamanho do Problema (N)", fontsize=16)
    plt.xlabel("Número de Rainhas (N)", fontsize=12)
    plt.ylabel("Tempo Médio de Execução (segundos)", fontsize=12)
    plt.grid(True)
    plt.legend(title='Variação Campeã')
    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, f"{exp_folder}_time_vs_n.png")
    plt.savefig(plot_path)
    print(f"-> Gráfico de escalabilidade salvo em: {plot_path}")
    plt.close()


def plot_total_execution_time():
    """
    Calcula e plota o tempo de execução total para cada estratégia campeã
    e o tempo total geral do experimento de escalabilidade.
    """
    exp_folder = "part_5_scalability"
    summary_path = os.path.join(RESULTS_DIR, exp_folder, "summary.csv")
    if not os.path.exists(summary_path):
        return

    df = pd.read_csv(summary_path)

    total_time_per_strategy = df.groupby('config_name')['execution_time'].sum()
    grand_total_time = total_time_per_strategy.sum()
    total_time_per_strategy['Total Geral'] = grand_total_time
    total_time_per_strategy_min = total_time_per_strategy / 60

    plot_data = total_time_per_strategy_min.reset_index()
    plot_data.columns = ['Estratégia', 'Tempo Total (minutos)']

    plt.figure(figsize=(12, 7))
    barplot = sns.barplot(data=plot_data, x='Estratégia', y='Tempo Total (minutos)')

    for p in barplot.patches:
        barplot.annotate(f"{p.get_height():.2f} min", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    plt.title("Tempo de Execução Total do Experimento de Escalabilidade", fontsize=16)
    plt.xlabel("Estratégia Campeã", fontsize=12)
    plt.ylabel("Tempo de Execução Total (minutos)", fontsize=12)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, f"{exp_folder}_total_time.png")
    plt.savefig(plot_path)
    print(f"-> Gráfico de tempo total de execução salvo em: {plot_path}")
    plt.close()


# --- PONTO DE ENTRADA DO SCRIPT ---
if __name__ == "__main__":
    print("--- Gerando Gráficos para os Experimentos ---")

    # Parte 1 - Seleção
    print("\nAnalisando Experimento 1: Estratégias de Seleção")
    plot_convergence("part_1_selection", "Convergência: Estratégias de Seleção")
    plot_experiment_summary("part_1_selection", "Estratégias de Seleção")

    # Parte 2 - Crossover
    print("\nAnalisando Experimento 2: Estratégias de Crossover")
    plot_convergence("part_2_crossover", "Convergência: Estratégias de Crossover")
    plot_experiment_summary("part_2_crossover", "Estratégias de Crossover")

    # Parte 3 - Elitismo
    print("\nAnalisando Experimento 3: Estratégias de Elitismo")
    plot_convergence("part_3_elitism", "Convergência: Estratégias de Elitismo")
    plot_experiment_summary("part_3_elitism", "Estratégias de Elitismo")

    # Parte 4 - Mutação
    print("\nAnalisando Experimento 4: Estratégias de Mutação")
    plot_convergence("part_4_mutation", "Convergência: Estratégias de Mutação")
    plot_experiment_summary("part_4_mutation", "Estratégias de Mutação")

    # Parte 5 - Escalabilidade
    print("\nAnalisando Experimento 5: Escalabilidade")
    plot_scalability()
    plot_total_execution_time()

    print("\nTodos os gráficos foram gerados. Verifique a pasta 'plots'.")