"""
algoritmo_genetico.py
-----------------------------------------------------------------------------
Laco principal do ALGORITMO GENETICO. Junta os operadores e evolui a
populacao ao longo das geracoes ate encontrar um bom trecho.

Fluxo de cada geracao:
  1. avalia o fitness de todos os individuos
  2. guarda o melhor encontrado (elitismo + melhor global)
  3. verifica parada antecipada (atingiu o limiar OU ficou sem melhorar)
  4. gera a nova populacao: SELECAO -> CROSSOVER -> MUTACAO
-----------------------------------------------------------------------------
"""

import config
from fitness import fitness
from operadores import populacao_inicial, selecionar, crossover, mutacao


def algoritmo_genetico(texto, padrao):
    n_texto = len(texto)
    n_padrao = len(padrao)

    populacao = populacao_inicial(n_texto, n_padrao)
    melhor_individuo = None
    melhor_fit = -1.0
    sem_melhora = 0
    geracao_final = 0

    for geracao in range(config.NUMERO_GERACOES):
        geracao_final = geracao + 1

        # 1) avalia toda a populacao
        fits = [fitness(ind, texto, padrao) for ind in populacao]

        # ordena indices do melhor para o pior (usado no elitismo)
        ordenados = sorted(range(len(populacao)),
                           key=lambda i: fits[i], reverse=True)

        # 2) atualiza o melhor global
        if fits[ordenados[0]] > melhor_fit:
            melhor_fit = fits[ordenados[0]]
            melhor_individuo = list(populacao[ordenados[0]])
            sem_melhora = 0
        else:
            sem_melhora += 1

        # 3) parada antecipada
        if melhor_fit >= config.LIMIAR_PARADA or sem_melhora >= config.PACIENCIA:
            break

        # ELITISMO: copia os melhores diretamente para a proxima geracao
        nova_populacao = [list(populacao[ordenados[i]])
                          for i in range(min(config.TAMANHO_ELITISMO,
                                             len(populacao)))]

        # 4) preenche o restante com filhos
        while len(nova_populacao) < config.TAMANHO_POPULACAO:
            pai1 = selecionar(populacao, fits)
            pai2 = selecionar(populacao, fits)
            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutacao(filho1, n_texto, n_padrao)
            filho2 = mutacao(filho2, n_texto, n_padrao)
            nova_populacao.append(filho1)
            if len(nova_populacao) < config.TAMANHO_POPULACAO:
                nova_populacao.append(filho2)

        populacao = nova_populacao

    return melhor_individuo, melhor_fit, geracao_final