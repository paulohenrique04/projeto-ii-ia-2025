# Algoritmo Genético para o Problema das N-Rainhas

Este projeto implementa um Algoritmo Genético (AG) configurável para resolver o problema das N-Rainhas, conforme especificado no "Trabalho 2 - Algoritmos Genéticos".

## Estrutura do Projeto

O projeto é organizado em vários módulos para garantir a separação de responsabilidades e a manutenibilidade:

-   `main.py`: O script principal para executar os experimentos.
-   `plotter.py`: Um script para gerar gráficos a partir dos resultados dos experimentos.
-   `core/`: Contém os blocos de construção básicos do AG (`Individual`, `Population`).
-   `problem/`: Define a lógica do problema das N-Rainhas, especificamente a função de fitness.
-   `ga/`: Contém o motor principal do AG e as implementações das estratégias.
    -   `ga/strategies/`: Armazena as diferentes implementações para seleção, cruzamento, mutação e elitismo.
-   `utils/`: Contém classes de utilidades, como o logger para arquivos CSV.
-   `results/`: Diretório onde todos os arquivos de saída CSV dos experimentos são armazenados.
-   `plots/`: Diretório onde todos os gráficos gerados são salvos.

## Pré-requisitos

Você precisa do Python 3.8+ e das bibliotecas listadas no arquivo `requirements.txt`.

## Instalação

1.  Clone o repositório ou baixe o código-fonte.
2.  Navegue até o diretório do projeto.
3.  Instale os pacotes necessários:
    ```bash
    pip install -r requirements.txt
    ```

## Como Executar

### 1. Executando os Experimentos

Para executar todos os experimentos conforme definido na especificação do trabalho, execute o script `main.py` a partir do seu terminal:

```bash
python main.py
```

Este comando irá:
- Rodar os experimentos para comparar os diferentes operadores do AG (Seleção, Crossover, etc.).
- Realizar múltiplas execuções para cada configuração, garantindo robustez estatística.
- Salvar logs detalhados para cada execução e um CSV de sumário para cada parte do experimento dentro do diretório `results/`.

### 2. Gerando os Gráficos

Após a conclusão dos experimentos e o preenchimento da pasta `results/` com os arquivos CSV, execute o script `plotter.py` para gerar as análises visuais:

```bash
python plotter.py
```

Este comando criará imagens `.png` dos gráficos e as salvará no diretório `plots/`. Estes gráficos são essenciais para a análise e são referenciados no relatório final.