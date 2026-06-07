"""
main.py
-----------------------------------------------------------------------------
PONTO DE ENTRADA do programa. Junta tudo:

  1. carrega e normaliza o texto (texto.py)
  2. roda o algoritmo genetico (algoritmo_genetico.py)
  3. imprime o melhor individuo e a porcentagem de similaridade

Execucao local:   python main.py
-----------------------------------------------------------------------------
"""

import time

import config
import fitness
from texto import carregar_texto, normalizar
from algoritmo_genetico import algoritmo_genetico


def main():
    # zera a memoizacao (importante se o programa rodar varios padroes)
    fitness.MEMO.clear()

    texto = normalizar(carregar_texto())
    padrao = normalizar(config.PADRAO)

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
    print("Metodo de selecao ......: %s" % config.METODO_SELECAO)
    print("Populacao / Geracoes ...: %d / %d (parou na geracao %d)"
          % (config.TAMANHO_POPULACAO, config.NUMERO_GERACOES, geracoes))
    print("Taxa de mutacao ........: %.2f" % config.TAXA_MUTACAO)
    print("-" * 70)
    print("Melhor individuo encontrado = %s" % trecho)
    print("Posicao inicial = %d | Comprimento = %d" % (melhor[0], melhor[1]))
    print("Porcentagem de similaridade = %.2f%%" % (fit * 100.0))
    print("Tempo de execucao = %.2f s" % duracao)
    print("=" * 70)


if __name__ == "__main__":
    main()