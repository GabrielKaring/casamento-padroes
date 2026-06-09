"""
fitness.py
-----------------------------------------------------------------------------
FUNCAO FITNESS do AG (o "coracao" da avaliacao).

A qualidade de um individuo e a SIMILARIDADE entre o trecho que ele aponta
no texto e o padrao buscado:

        fitness = 1 - distancia_de_edicao / tamanho_maximo

A distancia de edicao (Levenshtein) conta o numero minimo de:
  - insercoes
  - delecoes
  - substituicoes
necessarias para transformar uma string na outra. Por isso o AG tolera
pequenas variacoes (acentos, letras trocadas, palavras a mais/menos).

O dicionario `memo` e passado como parametro (nao e global) para que cada
busca tenha seu proprio cache e nao haja vazamento entre padroes diferentes.
-----------------------------------------------------------------------------
"""


def distancia_edicao(a, b):
    """
    Distancia de Levenshtein entre 'a' e 'b'.
    Implementacao O(len(a) * len(b)) usando apenas duas linhas (rapida).
    """
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
            atual[j] = min(anterior[j] + 1,         # delecao
                           atual[j - 1] + 1,         # insercao
                           anterior[j - 1] + custo)  # substituicao/igual
        anterior = atual
    return anterior[lb]


def similaridade(a, b):
    """Similaridade normalizada em [0, 1] a partir da distancia de edicao."""
    if not a and not b:
        return 1.0
    m = max(len(a), len(b))
    if m == 0:
        return 0.0
    return 1.0 - distancia_edicao(a, b) / m


def fitness(individuo, texto, padrao, memo):
    """Avalia um individuo: similaridade entre o trecho apontado e o padrao.
    memo e isolado por padrao — sem vazamento de cache entre buscas."""
    chave = (individuo[0], individuo[1])
    if chave in memo:
        return memo[chave]
    trecho = texto[individuo[0]: individuo[0] + individuo[1]]
    valor = similaridade(padrao, trecho)
    memo[chave] = valor
    return valor