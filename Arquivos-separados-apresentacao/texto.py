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


# Texto de exemplo usado SOMENTE se nenhum arquivo for encontrado.
# Trecho de dominio publico de "Dom Casmurro" (Machado de Assis).
TEXTO_FALLBACK = """
Uma noite destas, vindo da cidade para o Engenho Novo, encontrei num trem da
Central um rapaz aqui do bairro, que eu conheço de vista e de chapeu.
A casa em que moro e propria; fi-la construir de proposito, levado de um desejo
tao particular que me vexa imprimi-lo, mas va la. Um dia, ha bastantes anos,
lembrou-me reproduzir no Engenho Novo a casa em que me criei na antiga Rua de
Matacavalos, dando-lhe o mesmo aspecto e economia daquela outra, que desapareceu.
"""


def carregar_texto():
    """Le o arquivo de entrada; tenta os dois caminhos configurados em config."""
    caminhos = [config.ARQUIVO_ENTRADA, config.ARQUIVO_ENTRADA_2]
    for caminho in caminhos:
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                print("[OK] Arquivo carregado de '%s'.\n" % caminho)
                return f.read()
        except FileNotFoundError:
            continue
        except UnicodeDecodeError:
            with open(caminho, "r", encoding="latin-1") as f:
                print("[OK] Arquivo carregado de '%s' (latin-1).\n" % caminho)
                return f.read()
    print("[AVISO] Arquivo nao encontrado. Usando texto de exemplo embutido.\n")
    return TEXTO_FALLBACK


def normalizar(s):
    """Substitui qualquer sequencia de espacos/quebras de linha por 1 espaco."""
    return re.sub(r"\s+", " ", s).strip()
