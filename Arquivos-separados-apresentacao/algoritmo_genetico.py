"""
algoritmo_genetico.py
-----------------------------------------------------------------------------
Laco principal do ALGORITMO GENETICO. Junta os operadores e evolui a
populacao ao longo das geracoes ate encontrar um bom trecho.

Fluxo de cada geracao:
  1. avalia o fitness de todos os individuos
  2. guarda o melhor encontrado (elitismo + melhor global)
  3. verifica parada antecipada (atingiu o limiar OU ficou sem melhorar)
  4. reinjecao de aleatorios a cada 20 geracoes sem melhora (diversidade)
  5. gera a nova populacao: SELECAO -> CROSSOVER -> MUTACAO

Apos o laco, aplica BUSCA LOCAL (hill climbing) sobre o melhor individuo
para refinar a posicao/comprimento na vizinhança imediata.
-----------------------------------------------------------------------------
"""

import config
from fitness import fitness
from operadores import populacao_inicial, criar_individuo, selecionar, crossover, mutacao


# =========================== BUSCA LOCAL (HILL CLIMBING) ===================

def busca_local(individuo, texto, padrao, memo, janela=30):
    """Refina o individuo explorando a vizinhanca de posicao e comprimento."""
    melhor     = list(individuo)
    melhor_fit = fitness(melhor, texto, padrao, memo)
    n_texto    = len(texto)
    n_padrao   = len(padrao)

    melhorou = True
    while melhorou:
        melhorou = False
        for delta_inicio in range(-janela, janela + 1):
            for delta_comp in range(-config.FOLGA_TAMANHO, config.FOLGA_TAMANHO + 1):
                candidato = [melhor[0] + delta_inicio, melhor[1] + delta_comp]
                candidato[0] = max(0, min(candidato[0], n_texto - 1))
                candidato[1] = max(1, min(candidato[1], n_padrao + config.FOLGA_TAMANHO))
                if candidato[0] + candidato[1] > n_texto:
                    candidato[0] = max(0, n_texto - candidato[1])
                f = fitness(candidato, texto, padrao, memo)
                if f > melhor_fit:
                    melhor_fit = f
                    melhor     = candidato
                    melhorou   = True
    return melhor, melhor_fit


# ============================ ALGORITMO GENETICO ===========================

def algoritmo_genetico(texto, padrao, memo):
    n_texto  = len(texto)
    n_padrao = len(padrao)

    populacao        = populacao_inicial(texto, padrao)
    melhor_individuo = None
    melhor_fit       = -1.0
    sem_melhora      = 0
    geracao_final    = 0

    for geracao in range(config.NUMERO_GERACOES):
        geracao_final = geracao + 1

        # 1) avalia toda a populacao
        fits = [fitness(ind, texto, padrao, memo) for ind in populacao]

        # ordena indices do melhor para o pior (usado no elitismo)
        ordenados = sorted(range(len(populacao)),
                           key=lambda i: fits[i], reverse=True)

        # 2) atualiza o melhor global
        if fits[ordenados[0]] > melhor_fit:
            melhor_fit       = fits[ordenados[0]]
            melhor_individuo = list(populacao[ordenados[0]])
            sem_melhora      = 0
        else:
            sem_melhora += 1

        # 3) parada antecipada
        if melhor_fit >= config.LIMIAR_PARADA or sem_melhora >= config.PACIENCIA:
            break

        # 4) reinjecao de aleatorios a cada 20 geracoes sem melhora
        if sem_melhora > 0 and sem_melhora % 20 == 0:
            n_reinjecao = config.TAMANHO_POPULACAO // 10
            for i in range(n_reinjecao):
                populacao[ordenados[-(i + 1)]] = criar_individuo(n_texto, n_padrao)

        # ELITISMO: copia os melhores diretamente para a proxima geracao
        nova_populacao = [list(populacao[ordenados[i]])
                          for i in range(min(config.TAMANHO_ELITISMO,
                                             len(populacao)))]

        # 5) preenche o restante com filhos
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

    # Refinamento final com busca local
    melhor_individuo, melhor_fit = busca_local(melhor_individuo, texto, padrao, memo)
    return melhor_individuo, melhor_fit, geracao_final
