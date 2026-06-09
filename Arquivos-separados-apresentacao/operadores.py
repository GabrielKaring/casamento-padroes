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


def semear_com_trigramas(texto, padrao, n_sementes):
    """Gera individuos 'inteligentes' ancorados em substrings do padrao."""
    sementes  = []
    n_padrao  = len(padrao)
    n_texto   = len(texto)
    tam_grama = max(3, n_padrao // 4)

    for i in range(0, n_padrao - tam_grama + 1, max(1, tam_grama // 2)):
        grama = padrao[i: i + tam_grama]
        pos   = texto.find(grama)
        while pos != -1 and len(sementes) < n_sementes:
            inicio = max(0, pos - i)
            comp   = random.randint(
                max(1, n_padrao - config.FOLGA_TAMANHO),
                n_padrao + config.FOLGA_TAMANHO
            )
            if inicio + comp <= n_texto:
                sementes.append([inicio, comp])
            pos = texto.find(grama, pos + 1)
    return sementes


def populacao_inicial(texto, padrao):
    """Populacao inicial com sementes de trigramas + individuos aleatorios."""
    n_texto  = len(texto)
    n_padrao = len(padrao)
    n_sementes = config.TAMANHO_POPULACAO // 5
    sementes   = semear_com_trigramas(texto, padrao, n_sementes)
    aleatorios = [criar_individuo(n_texto, n_padrao)
                  for _ in range(config.TAMANHO_POPULACAO - len(sementes))]
    return sementes + aleatorios


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
    Mutacao em 3 niveis de amplitude:
      - 60%: ajuste fino local (+/- 8)  — explora a vizinhança imediata
      - 25%: salto medio (+/- 50)       — sai de otimos locais proximos
      - 15%: posicao aleatoria          — mantem diversidade global
    Comprimento: +/- 1 ou 2 (trata insercoes/delecoes).
    No fim, garante que o individuo continua valido (dentro do texto).
    """
    novo = [individuo[0], individuo[1]]

    if random.random() < config.TAXA_MUTACAO:
        r = random.random()
        if r < 0.60:
            novo[0] += random.randint(-8, 8)               # ajuste fino
        elif r < 0.85:
            novo[0] += random.randint(-50, 50)             # salto medio
        else:
            novo[0] = random.randint(0, max(0, n_texto - 1))  # salto global

    if random.random() < config.TAXA_MUTACAO:
        novo[1] += random.choice([-2, -1, 1, 2])

    # Correcoes de validade
    novo[1] = max(1, min(novo[1], n_padrao + config.FOLGA_TAMANHO))
    if novo[0] < 0:
        novo[0] = 0
    if novo[0] + novo[1] > n_texto:
        novo[0] = max(0, n_texto - novo[1])
    return novo
