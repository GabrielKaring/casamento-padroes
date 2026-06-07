"""
operadores.py
-----------------------------------------------------------------------------
Reune os OPERADORES GENETICOS exigidos no trabalho:

  - GERACAO INICIAL .... criar_individuo() / populacao_inicial()
  - SELECAO ............ selecao_torneio() e selecao_roleta()
  - CROSSOVER .......... crossover()  (um ponto)
  - MUTACAO ............ mutacao()

REPRESENTACAO DO CROMOSSOMO: [inicio, comprimento]
  - inicio       -> posicao inicial do trecho no texto (sugestao do enunciado)
  - comprimento  -> tamanho do trecho; deixa-lo variar permite tratar
                    insercoes e delecoes (o melhor trecho nem sempre tem o
                    mesmo tamanho do padrao).
-----------------------------------------------------------------------------
"""

import random
import config


# --------------------------- GERACAO INICIAL -------------------------------

def criar_individuo(n_texto, n_padrao):
    """Cria um individuo aleatorio [inicio, comprimento] valido."""
    comp = random.randint(max(1, n_padrao - config.FOLGA_TAMANHO),
                          n_padrao + config.FOLGA_TAMANHO)
    inicio = random.randint(0, max(0, n_texto - comp))
    return [inicio, comp]


def populacao_inicial(n_texto, n_padrao):
    """Populacao inicial totalmente aleatoria, espalhada pelo texto."""
    return [criar_individuo(n_texto, n_padrao)
            for _ in range(config.TAMANHO_POPULACAO)]


# ------------------------------- SELECAO -----------------------------------

def selecao_torneio(pop, fits):
    """Sorteia k individuos e devolve uma copia do melhor deles."""
    melhor_i = None
    for _ in range(config.TAMANHO_TORNEIO):
        i = random.randrange(len(pop))
        if melhor_i is None or fits[i] > fits[melhor_i]:
            melhor_i = i
    return list(pop[melhor_i])


def selecao_roleta(pop, fits):
    """Probabilidade de escolha proporcional ao fitness do individuo."""
    total = sum(fits)
    if total <= 0:
        return list(random.choice(pop))
    r = random.uniform(0, total)
    acumulado = 0.0
    for ind, f in zip(pop, fits):
        acumulado += f
        if acumulado >= r:
            return list(ind)
    return list(pop[-1])


def selecionar(pop, fits):
    """Dispara o metodo de selecao configurado em config.METODO_SELECAO."""
    if config.METODO_SELECAO == "roleta":
        return selecao_roleta(pop, fits)
    return selecao_torneio(pop, fits)


# ------------------------------ CROSSOVER ----------------------------------

def crossover(p1, p2):
    """
    Crossover de UM PONTO. O cromossomo tem 2 genes [inicio, comprimento];
    o ponto de corte fica entre eles, trocando os genes entre os pais.
    """
    if random.random() > config.TAXA_CROSSOVER:
        return list(p1), list(p2)
    filho1 = [p1[0], p2[1]]   # inicio do pai1 + comprimento do pai2
    filho2 = [p2[0], p1[1]]   # inicio do pai2 + comprimento do pai1
    return filho1, filho2


# ------------------------------- MUTACAO -----------------------------------

def mutacao(individuo, n_texto, n_padrao):
    """
    Mutacao:
      - posicao inicial: 70% ajuste fino local (+/- 15);
                         30% salto aleatorio (mantem diversidade);
      - comprimento:     +/- 1 ou 2 (trata insercoes/delecoes).
    No fim, garante que o individuo continua valido (dentro do texto).
    """
    novo = [individuo[0], individuo[1]]

    if random.random() < config.TAXA_MUTACAO:
        if random.random() < 0.7:
            novo[0] += random.randint(-15, 15)               # ajuste fino
        else:
            novo[0] = random.randint(0, max(0, n_texto - 1)) # salto

    if random.random() < config.TAXA_MUTACAO:
        novo[1] += random.choice([-2, -1, 1, 2])

    # Correcoes de validade
    novo[1] = max(1, min(novo[1], n_padrao + config.FOLGA_TAMANHO))
    if novo[0] < 0:
        novo[0] = 0
    if novo[0] + novo[1] > n_texto:
        novo[0] = max(0, n_texto - novo[1])
    return novo