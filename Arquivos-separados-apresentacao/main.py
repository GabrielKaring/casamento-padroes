"""
main.py
-----------------------------------------------------------------------------
PONTO DE ENTRADA do programa. Junta tudo:

  1. carrega e normaliza o texto (texto.py)
  2. para cada padrao em config.PADROES, roda o AG ate MAX_TENTATIVAS vezes
  3. imprime o relatorio final com [OK]/[FAIL], posicao, similaridade e tempo

Execucao local:   python main.py
-----------------------------------------------------------------------------
"""

import time

import config
from texto import carregar_texto, normalizar
from algoritmo_genetico import algoritmo_genetico


# ==================== BUSCA COMPLETA PARA UM PADRAO =======================

def buscar_padrao(texto, padrao):
    melhor_global, fit_global, geracoes_global = None, -1.0, 0

    for tentativa in range(1, config.MAX_TENTATIVAS + 1):
        memo = {}
        print("  [Tentativa %d/%d]..." % (tentativa, config.MAX_TENTATIVAS), end=" ")
        melhor, fit, geracoes = algoritmo_genetico(texto, padrao, memo)

        if fit > fit_global:
            fit_global      = fit
            melhor_global   = melhor
            geracoes_global = geracoes

        status = "%.2f%%" % (fit * 100.0)
        if fit_global >= config.LIMIAR_PARADA:
            print(status, "-> 100% encontrado!")
            break
        elif fit_global >= config.SIMILARIDADE_MINIMA:
            print(status, "-> meta atingida!")
            break
        else:
            print(status)

    trecho = texto[melhor_global[0]: melhor_global[0] + melhor_global[1]].strip()
    return {
        "padrao"      : padrao,
        "trecho"      : trecho,
        "inicio"      : melhor_global[0],
        "comprimento" : melhor_global[1],
        "fit"         : fit_global,
        "geracoes"    : geracoes_global,
        "atingiu"     : fit_global >= config.SIMILARIDADE_MINIMA,
    }


# ================================= MAIN ====================================

def main():
    texto = normalizar(carregar_texto())
    if not texto:
        print("Texto vazio. Verifique o arquivo de entrada.")
        return

    padroes      = [normalizar(p) for p in config.PADROES]
    resultados   = []
    inicio_total = time.time()
    separador    = "=" * 70

    print(separador)
    print("CASAMENTO DE PADROES COM ALGORITMO GENETICO — MULTIPLOS PADROES")
    print("Metodo: %s | Populacao: %d | Geracoes max: %d | Tentativas max: %d"
          % (config.METODO_SELECAO, config.TAMANHO_POPULACAO,
             config.NUMERO_GERACOES, config.MAX_TENTATIVAS))
    print(separador)

    for idx, padrao in enumerate(padroes, 1):
        print("\n[%d/%d] Padrao: \"%s\"" % (idx, len(padroes), padrao))
        t0  = time.time()
        res = buscar_padrao(texto, padrao)
        res["tempo"] = time.time() - t0
        resultados.append(res)

    duracao_total = time.time() - inicio_total

    # ===================== RELATORIO FINAL =================================
    print("\n" + separador)
    print("RELATORIO FINAL")
    print(separador)

    atingidos = 0
    for idx, r in enumerate(resultados, 1):
        marcador = "[OK]  " if r["atingiu"] else "[FAIL]"
        if r["atingiu"]:
            atingidos += 1
        print("\n%s Padrao %d: \"%s\"" % (marcador, idx, r["padrao"]))
        print("        Trecho encontrado    : %s" % r["trecho"])
        print("        Posicao / Comprimento: %d / %d"
              % (r["inicio"], r["comprimento"]))
        print("        Similaridade         : %.2f%%  |  Geracoes: %d  |  Tempo: %.2fs"
              % (r["fit"] * 100.0, r["geracoes"], r["tempo"]))

    print("\n" + separador)
    print("RESUMO: %d/%d padroes atingiram >= %.0f%% de similaridade"
          % (atingidos, len(padroes), config.SIMILARIDADE_MINIMA * 100))
    print("Tempo total de execucao: %.2f s" % duracao_total)
    print(separador)


if __name__ == "__main__":
    main()
