"""
texto.py
-----------------------------------------------------------------------------
Responsavel pela ENTRADA DE DADOS:
  - carregar_texto(): le o arquivo dom_casmurro.txt
  - normalizar():     limpa espacos/quebras de linha para facilitar o casamento

Se o arquivo nao for encontrado, usa um trecho de exemplo embutido
(dominio publico) para que o programa rode mesmo sem o arquivo.
-----------------------------------------------------------------------------
"""

import re
import config


# Texto de exemplo usado SOMENTE se 'dom_casmurro.txt' nao for encontrado.
# Trecho de dominio publico de "Dom Casmurro" (Machado de Assis).
TEXTO_FALLBACK = """
Uma noite destas, vindo da cidade para o Engenho Novo, encontrei num trem da
Central um rapaz aqui do bairro, que eu conheço de vista e de chapeu.
Cumprimentou-me, sentou-se ao pe de mim, falou da Lua e dos ministros, e
acabou recitando-me versos. A viagem era curta, e os versos pode ser que nao
fossem inteiramente maus.

A casa em que moro e propria; fi-la construir de proposito, levado de um desejo
tao particular que me vexa imprimi-lo, mas va la. Um dia, ha bastantes anos,
lembrou-me reproduzir no Engenho Novo a casa em que me criei na antiga Rua de
Matacavalos, dando-lhe o mesmo aspecto e economia daquela outra, que desapareceu.
Construtor e pintor entenderam bem as indicacoes que lhes fiz: e o mesmo predio
assobradado, tres janelas de frente, varanda ao fundo, as mesmas alcovas e salas.

Na principal dessas salas, a pintura do teto e das paredes era mais ou menos a
mesma, umas grinaldas de flores miudas e grandes passaros que as tomavam nos
bicos, de espaco a espaco. Os meus fins eram outros. Como ali em menino, assim
agora quis representar o livro que nao escrevi.
"""


def carregar_texto():
    """Le o arquivo de entrada; se nao existir, usa o texto de exemplo."""
    try:
        with open(config.ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("[AVISO] '%s' nao encontrado. Usando texto de exemplo embutido.\n"
              % config.ARQUIVO_ENTRADA)
        return TEXTO_FALLBACK
    except UnicodeDecodeError:
        # Alguns arquivos vem em latin-1
        with open(config.ARQUIVO_ENTRADA, "r", encoding="latin-1") as f:
            return f.read()


def normalizar(s):
    """Substitui qualquer sequencia de espacos/quebras de linha por 1 espaco."""
    return re.sub(r"\s+", " ", s).strip()