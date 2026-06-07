"""
config.py
-----------------------------------------------------------------------------
Centraliza TODOS os parâmetros do Algoritmo Genético em um único lugar.

Vantagem para a apresentacao: para ajustar o comportamento do AG (qualidade
vs. velocidade) basta mexer aqui, sem tocar na logica do algoritmo.
-----------------------------------------------------------------------------
"""

# >>> TROQUE AQUI O PADRAO A CADA TESTE <<<
PADRAO = "A casa em que moro é própria"

# Arquivo de entrada fornecido pelo professor
ARQUIVO_ENTRADA = "dom_casmurro.txt"

# ------------------------- Parametros do AG --------------------------------
TAMANHO_POPULACAO = 120     # quantidade de individuos por geracao
NUMERO_GERACOES   = 150     # numero maximo de geracoes
TAXA_MUTACAO      = 0.20    # probabilidade de mutar cada gene
TAXA_CROSSOVER    = 0.90    # probabilidade de aplicar crossover
TAMANHO_TORNEIO   = 3       # nº de competidores na selecao por torneio
TAMANHO_ELITISMO  = 4       # melhores individuos copiados direto p/ proxima geracao
FOLGA_TAMANHO     = 8       # quanto o comprimento pode variar (trata insercao/delecao)
PACIENCIA         = 40      # geracoes sem melhora -> parada antecipada
LIMIAR_PARADA     = 0.999   # se atingir esta similaridade, para

# Metodo de selecao: "torneio" ou "roleta"
METODO_SELECAO = "torneio"