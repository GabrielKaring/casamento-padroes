"""
config.py
-----------------------------------------------------------------------------
Centraliza TODOS os parâmetros do Algoritmo Genético em um único lugar.

Vantagem para a apresentacao: para ajustar o comportamento do AG (qualidade
vs. velocidade) basta mexer aqui, sem tocar na logica do algoritmo.
-----------------------------------------------------------------------------
"""

# >>> TROQUE AQUI OS PADROES A CADA TESTE <<<
# Frases extraidas diretamente do Dom Casmurro — existem literalmente no texto,
# distribuidas do inicio ao fim do livro.
PADROES = [
    "Se só me faltassem os outros, vá",       # ~10% do livro
    "Você o que quer é um capote",             # ~30% do livro
    "Não foi despedido, como pedia então",     # ~50% do livro
    "São retratos que valem por originais",    # ~70% do livro
    "a imaginação os faz infinitos",           # ~90% do livro
]

# Arquivos de entrada (tentados nesta ordem)
ARQUIVO_ENTRADA   = "dom_casmurro.txt"
ARQUIVO_ENTRADA_2 = "/uploads/dom_casmurro.txt"

# ------------------------- Parametros do AG --------------------------------
TAMANHO_POPULACAO = 200     # quantidade de individuos por geracao
NUMERO_GERACOES   = 400     # numero maximo de geracoes
TAXA_MUTACAO      = 0.30    # probabilidade de mutar cada gene
TAXA_CROSSOVER    = 0.85    # probabilidade de aplicar crossover
TAMANHO_TORNEIO   = 3       # nº de competidores na selecao por torneio
TAMANHO_ELITISMO  = 6       # melhores individuos copiados direto p/ proxima geracao
FOLGA_TAMANHO     = 5       # quanto o comprimento pode variar (trata insercao/delecao)
PACIENCIA         = 80      # geracoes sem melhora -> parada antecipada
LIMIAR_PARADA     = 0.999   # se atingir esta similaridade, para

SIMILARIDADE_MINIMA = 0.85  # meta minima aceitavel por padrao
MAX_TENTATIVAS      = 5     # tentativas independentes por padrao

# Metodo de selecao: "torneio" ou "roleta"
METODO_SELECAO = "torneio"
