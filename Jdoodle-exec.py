# -*- coding: utf-8 -*-
"""
=============================================================================
 VERSAO DE ARQUIVO UNICO (para rodar no JDoodle)
=============================================================================
 Esta e a uniao dos modulos config / texto / fitness / operadores /
 algoritmo_genetico / main em um unico arquivo, porque o JDoodle gratuito
 executa apenas UM arquivo .py.

 A versao organizada em modulos (mais facil de explicar) esta na pasta do
 projeto; esta aqui e funcionalmente identica.
=============================================================================
"""

import random
import re
import time

# ============================== PARAMETROS =================================
PADRAO = "A casa em que moro é própria"   # >>> TROQUE A CADA TESTE <<<
ARQUIVO_ENTRADA   = "dom_casmurro.txt"
ARQUIVO_ENTRADA_2 = "/uploads/dom_casmurro.txt"

TAMANHO_POPULACAO = 120
NUMERO_GERACOES   = 150
TAXA_MUTACAO      = 0.20
TAXA_CROSSOVER    = 0.90
TAMANHO_TORNEIO   = 3
TAMANHO_ELITISMO  = 4
FOLGA_TAMANHO     = 8
PACIENCIA         = 40
LIMIAR_PARADA     = 0.999
METODO_SELECAO    = "torneio"   # "torneio" ou "roleta"

TEXTO_FALLBACK = """
Uma noite destas, vindo da cidade para o Engenho Novo, encontrei num trem da
Central um rapaz aqui do bairro, que eu conheço de vista e de chapeu.
A casa em que moro e propria; fi-la construir de proposito, levado de um desejo
tao particular que me vexa imprimi-lo, mas va la. Um dia, ha bastantes anos,
lembrou-me reproduzir no Engenho Novo a casa em que me criei na antiga Rua de
Matacavalos, dando-lhe o mesmo aspecto e economia daquela outra, que desapareceu.
"""

# =============================== ENTRADA ===================================
def carregar_texto():
    caminhos = [ARQUIVO_ENTRADA, ARQUIVO_ENTRADA_2]
    for caminho in caminhos:
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                print("[OK] Arquivo carregado de '%s'." % caminho)
                return f.read()
        except FileNotFoundError:
            continue
        except UnicodeDecodeError:
            with open(caminho, "r", encoding="latin-1") as f:
                print("[OK] Arquivo carregado de '%s' (latin-1)." % caminho)
                return f.read()

    print("[AVISO] Arquivo nao encontrado em nenhum dos caminhos. "
          "Usando texto de exemplo embutido.\n")
    return TEXTO_FALLBACK


def normalizar(s):
    return re.sub(r"\s+", " ", s).strip()


# =============================== FITNESS ===================================
def distancia_edicao(a, b):
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    anterior = list(range(lb + 1))
    for i in range(1, la + 1):
        atual = [i] + [0] * lb
        ca = a[i - 1]
        for j in range(1, lb + 1):
            custo = 0 if ca == b[j - 1] else 1
            atual[j] = min(anterior[j] + 1, atual[j - 1] + 1,
                           anterior[j - 1] + custo)
        anterior = atual
    return anterior[lb]


def similaridade(a, b):
    if not a and not b:
        return 1.0
    m = max(len(a), len(b))
    return 1.0 - distancia_edicao(a, b) / m if m else 0.0


MEMO = {}


def fitness(individuo, texto, padrao):
    chave = (individuo[0], individuo[1])
    if chave in MEMO:
        return MEMO[chave]
    trecho = texto[individuo[0]: individuo[0] + individuo[1]]
    valor = similaridade(padrao, trecho)
    MEMO[chave] = valor
    return valor


# =========================== OPERADORES GENETICOS ==========================
def criar_individuo(n_texto, n_padrao):
    comp = random.randint(max(1, n_padrao - FOLGA_TAMANHO), n_padrao + FOLGA_TAMANHO)
    inicio = random.randint(0, max(0, n_texto - comp))
    return [inicio, comp]


def populacao_inicial(n_texto, n_padrao):
    return [criar_individuo(n_texto, n_padrao) for _ in range(TAMANHO_POPULACAO)]


def selecao_torneio(pop, fits):
    melhor_i = None
    for _ in range(TAMANHO_TORNEIO):
        i = random.randrange(len(pop))
        if melhor_i is None or fits[i] > fits[melhor_i]:
            melhor_i = i
    return list(pop[melhor_i])


def selecao_roleta(pop, fits):
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
    if METODO_SELECAO == "roleta":
        return selecao_roleta(pop, fits)
    return selecao_torneio(pop, fits)


def crossover(p1, p2):
    if random.random() > TAXA_CROSSOVER:
        return list(p1), list(p2)
    return [p1[0], p2[1]], [p2[0], p1[1]]


def mutacao(individuo, n_texto, n_padrao):
    novo = [individuo[0], individuo[1]]
    if random.random() < TAXA_MUTACAO:
        if random.random() < 0.7:
            novo[0] += random.randint(-15, 15)
        else:
            novo[0] = random.randint(0, max(0, n_texto - 1))
    if random.random() < TAXA_MUTACAO:
        novo[1] += random.choice([-2, -1, 1, 2])
    novo[1] = max(1, min(novo[1], n_padrao + FOLGA_TAMANHO))
    if novo[0] < 0:
        novo[0] = 0
    if novo[0] + novo[1] > n_texto:
        novo[0] = max(0, n_texto - novo[1])
    return novo


# ============================ ALGORITMO GENETICO ===========================
def algoritmo_genetico(texto, padrao):
    n_texto, n_padrao = len(texto), len(padrao)
    populacao = populacao_inicial(n_texto, n_padrao)
    melhor_individuo, melhor_fit, sem_melhora, geracao_final = None, -1.0, 0, 0

    for geracao in range(NUMERO_GERACOES):
        geracao_final = geracao + 1
        fits = [fitness(ind, texto, padrao) for ind in populacao]
        ordenados = sorted(range(len(populacao)), key=lambda i: fits[i], reverse=True)

        if fits[ordenados[0]] > melhor_fit:
            melhor_fit = fits[ordenados[0]]
            melhor_individuo = list(populacao[ordenados[0]])
            sem_melhora = 0
        else:
            sem_melhora += 1

        if melhor_fit >= LIMIAR_PARADA or sem_melhora >= PACIENCIA:
            break

        nova = [list(populacao[ordenados[i]])
                for i in range(min(TAMANHO_ELITISMO, len(populacao)))]
        while len(nova) < TAMANHO_POPULACAO:
            f1, f2 = crossover(selecionar(populacao, fits), selecionar(populacao, fits))
            nova.append(mutacao(f1, n_texto, n_padrao))
            if len(nova) < TAMANHO_POPULACAO:
                nova.append(mutacao(f2, n_texto, n_padrao))
        populacao = nova

    return melhor_individuo, melhor_fit, geracao_final


# ================================= MAIN ====================================
def main():
    MEMO.clear()
    texto = normalizar(carregar_texto())
    padrao = normalizar(PADRAO)
    if len(texto) == 0:
        print("Texto vazio. Verifique o arquivo de entrada.")
        return

    inicio_tempo = time.time()
    melhor, fit, geracoes = algoritmo_genetico(texto, padrao)
    duracao = time.time() - inicio_tempo
    trecho = texto[melhor[0]: melhor[0] + melhor[1]].strip()

    print("=" * 70)
    print("CASAMENTO DE PADROES COM ALGORITMO GENETICO")
    print("=" * 70)
    print("Padrao buscado .........: %s" % padrao)
    print("Metodo de selecao ......: %s" % METODO_SELECAO)
    print("Populacao / Geracoes ...: %d / %d (parou na geracao %d)"
          % (TAMANHO_POPULACAO, NUMERO_GERACOES, geracoes))
    print("Taxa de mutacao ........: %.2f" % TAXA_MUTACAO)
    print("-" * 70)
    print("Melhor individuo encontrado = %s" % trecho)
    print("Posicao inicial = %d | Comprimento = %d" % (melhor[0], melhor[1]))
    print("Porcentagem de similaridade = %.2f%%" % (fit * 100.0))
    print("Tempo de execucao = %.2f s" % duracao)
    print("=" * 70)


if __name__ == "__main__":
    main()
