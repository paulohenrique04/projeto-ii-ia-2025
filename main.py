import random

# Função de fitness
def fitness_function(individual):
    
    """"
    A função de fitness vai avaliar a quantidade de peças que estão em ameaça,
    neste caso, o número de pares de rainhas que estão se ameaçando na mesma diagonal.
    Mas por que não na vertical ou na horizontal? Pois iremos gerar os indivíduos por
    meio de uma permutação de números, ou seja, nunca iremos se preocupar com a vertical
    e horizontal, apenas com a diagonal. Pois veja, um exemplo de indivíduo:
    [0, 2, 4, 1, 3]
    Isso significa que a rainha 0 está na posição 0 do tabuleiro, a rainha 1 está na posição 2 
    e assim sucessivamente. Nunca termos um exemplo do tipo [0, 0, 0, 0, 0], pois isso
    significaria que todas as rainhas estão na mesma coluna, o que não é permitido.
    """
    conflicts = 0
    for i in range(len(individual)):
        for j in range(i+1, len(individual)):
            if abs(i - j) == abs(individual[i] - individual[j]):
                conflicts += 1
    return conflicts

# Duas formas de seleção ============================================================================
def tournament_selection(population, fitnesses, tournament_size=3):
    """
    Seleção por torneio: seleciona k indivíduos aleatórios aleatoriamente e escolhe o melhor entre eles.
    """
    candidates = list(zip(population, fitnesses))

    # Selecionamos o primeiro pai
    tournament1 = random.sample(candidates, min(tournament_size, len(candidates)))
    parent1, _ = min(tournament1, key=lambda x: x[1])

    # Selecionamos o segundo pai
    candidates = [cand for cand in candidates if cand[0] != parent1]
    tournament2 = random.sample(candidates, min(tournament_size, len(candidates)))
    parent2, _ = min(tournament2, key=lambda x: x[1])

    return parent1, parent2

def roulette_wheel_selection(population, fitnesses):
    inverse_fitness = [1.0 / (1 + f) for f in fitnesses]
    total_inverse_fitness = sum(inverse_fitness)
    probabilities = [f / total_inverse_fitness for f in inverse_fitness]
    selected = random.choices(population, weights=probabilities, k=2)

    return selected[0], selected[1]

# =====================================================================================================

# Duas formas de crossover ============================================================================
def one_point_crossover(parent1, parent2):
    """
    Preserva uma parte de um pai e o resto do outro pai de forma que não haja repetição de genes. 
    Pois repetição de genes pode causar um problema de fitness.
    """
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + [gene for gene in parent2 if gene not in parent1[:point]]
    child2 = parent2[:point] + [gene for gene in parent1 if gene not in parent2[:point]]

    return child1, child2

def crossover_order(parent1, parent2):
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))

    child1, child2 = [-1] * n, [-1] * n

    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    def fill_child(child, parent):
        pos = end
        for gene in parent:
            if gene not in child:
                while child[pos % n] != -1:
                    pos += 1
                child[pos % n] = gene

    fill_child(child1, parent2)
    fill_child(child2, parent1)

    return child1, child2
# =====================================================================================================

# Duas formas de mutação ==============================================================================
def mutation_swap(child):
    """
    Mutação por troca: troca duas posições aleatórias
    """
    i, j = random.sample(range(len(child)), 2)
    child[i], child[j] = child[j], child[i]
    return child

def mutation_inversion(child):
    """
    Mutação por inversão: inverte uma subsequência aleatória
    """
    n = len(child)
    p1, p2 = sorted(random.sample(range(n), 2))
    child[p1:p2] = reversed(child[p1:p2])
    return child
# =====================================================================================================

# Duas formas de elitismo =============================================================================
def elitismo_simples(populacao, fitness, elitismo_n):
    """
    Seleciona os n melhores indivíduos
    """
    sorted_population = sorted(zip(populacao, fitness), key=lambda x: x[1])
    return [ind[0] for ind in sorted_population[:elitismo_n]]

def elitismo_diversificado_sem_repeticao(populacao, fitness, elitismo_n):
    """
    Seleciona os melhores únicos e adiciona um indivíduo aleatório para diversidade
    """
    sorted_population = sorted(zip(populacao, fitness), key=lambda x: x[1])
    elite = []
    
    # Seleciona indivíduos únicos
    for ind, _ in sorted_population:
        if ind not in elite:
            elite.append(ind)
        if len(elite) == elitismo_n - 1:
            break
    
    # Adiciona um indivíduo aleatório diversificado
    restante = [ind for ind in populacao if ind not in elite]
    if restante:
        elite.append(random.choice(restante))
    
    return elite
# ======================================================================================================