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

# ============================== PADROES A BUSCAR ===========================
# Frases extraidas diretamente do Dom Casmurro — existem literalmente no texto,
# distribuidas do inicio ao fim do livro. Troque a vontade por outras frases
# reais do livro para novos testes.
PADROES = [
    "Se só me faltassem os outros, vá",       # ~10% do livro
    "Você o que quer é um capote",             # ~30% do livro
    "Não foi despedido, como pedia então",     # ~50% do livro
    "São retratos que valem por originais",    # ~70% do livro
    "a imaginação os faz infinitos",           # ~90% do livro
]

ARQUIVO_ENTRADA   = "dom_casmurro.txt"
ARQUIVO_ENTRADA_2 = "/uploads/dom_casmurro.txt"

# ============================== PARAMETROS GA ==============================
TAMANHO_POPULACAO = 200
NUMERO_GERACOES   = 400
TAXA_MUTACAO      = 0.30
TAXA_CROSSOVER    = 0.85
TAMANHO_TORNEIO   = 3
TAMANHO_ELITISMO  = 6
FOLGA_TAMANHO     = 5
PACIENCIA         = 80
LIMIAR_PARADA     = 0.999
METODO_SELECAO    = "torneio"   # "torneio" ou "roleta"

SIMILARIDADE_MINIMA = 0.85
MAX_TENTATIVAS      = 5

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


# memo isolado por padrao — sem vazamento de cache entre buscas
def fitness(individuo, texto, padrao, memo):
    chave = (individuo[0], individuo[1])
    if chave in memo:
        return memo[chave]
    trecho = texto[individuo[0]: individuo[0] + individuo[1]]
    valor  = similaridade(padrao, trecho)
    memo[chave] = valor
    return valor


# =========================== BUSCA LOCAL (HILL CLIMBING) ===================
def busca_local(individuo, texto, padrao, memo, janela=30):
    melhor     = list(individuo)
    melhor_fit = fitness(melhor, texto, padrao, memo)
    n_texto    = len(texto)
    n_padrao   = len(padrao)

    melhorou = True
    while melhorou:
        melhorou = False
        for delta_inicio in range(-janela, janela + 1):
            for delta_comp in range(-FOLGA_TAMANHO, FOLGA_TAMANHO + 1):
                candidato = [melhor[0] + delta_inicio, melhor[1] + delta_comp]
                candidato[0] = max(0, min(candidato[0], n_texto - 1))
                candidato[1] = max(1, min(candidato[1], n_padrao + FOLGA_TAMANHO))
                if candidato[0] + candidato[1] > n_texto:
                    candidato[0] = max(0, n_texto - candidato[1])
                f = fitness(candidato, texto, padrao, memo)
                if f > melhor_fit:
                    melhor_fit = f
                    melhor     = candidato
                    melhorou   = True
    return melhor, melhor_fit


# ===================== POPULACAO COM SEMENTES INTELIGENTES =================
def semear_com_trigramas(texto, padrao, n_sementes):
    sementes  = []
    n_padrao  = len(padrao)
    n_texto   = len(texto)
    tam_grama = max(3, n_padrao // 4)

    for i in range(0, n_padrao - tam_grama + 1, max(1, tam_grama // 2)):
        grama = padrao[i: i + tam_grama]
        pos   = texto.find(grama)
        while pos != -1 and len(sementes) < n_sementes:
            inicio = max(0, pos - i)
            comp   = random.randint(
                max(1, n_padrao - FOLGA_TAMANHO),
                n_padrao + FOLGA_TAMANHO
            )
            if inicio + comp <= n_texto:
                sementes.append([inicio, comp])
            pos = texto.find(grama, pos + 1)
    return sementes


# =========================== OPERADORES GENETICOS ==========================
def criar_individuo(n_texto, n_padrao):
    comp   = random.randint(max(1, n_padrao - FOLGA_TAMANHO), n_padrao + FOLGA_TAMANHO)
    inicio = random.randint(0, max(0, n_texto - comp))
    return [inicio, comp]


def populacao_inicial(texto, padrao):
    n_texto, n_padrao = len(texto), len(padrao)
    n_sementes = TAMANHO_POPULACAO // 5
    sementes   = semear_com_trigramas(texto, padrao, n_sementes)
    aleatorios = [criar_individuo(n_texto, n_padrao)
                  for _ in range(TAMANHO_POPULACAO - len(sementes))]
    return sementes + aleatorios


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
    r, acumulado = random.uniform(0, total), 0.0
    for ind, f in zip(pop, fits):
        acumulado += f
        if acumulado >= r:
            return list(ind)
    return list(pop[-1])


def selecionar(pop, fits):
    return selecao_roleta(pop, fits) if METODO_SELECAO == "roleta" \
           else selecao_torneio(pop, fits)


def crossover(p1, p2):
    if random.random() > TAXA_CROSSOVER:
        return list(p1), list(p2)
    return [p1[0], p2[1]], [p2[0], p1[1]]


def mutacao(individuo, n_texto, n_padrao):
    novo = [individuo[0], individuo[1]]
    if random.random() < TAXA_MUTACAO:
        r = random.random()
        if r < 0.60:
            novo[0] += random.randint(-8, 8)
        elif r < 0.85:
            novo[0] += random.randint(-50, 50)
        else:
            novo[0] = random.randint(0, max(0, n_texto - 1))
    if random.random() < TAXA_MUTACAO:
        novo[1] += random.choice([-2, -1, 1, 2])
    novo[1] = max(1, min(novo[1], n_padrao + FOLGA_TAMANHO))
    novo[0] = max(0, novo[0])
    if novo[0] + novo[1] > n_texto:
        novo[0] = max(0, n_texto - novo[1])
    return novo


# ============================ ALGORITMO GENETICO ===========================
def algoritmo_genetico(texto, padrao, memo):
    n_texto, n_padrao = len(texto), len(padrao)
    populacao = populacao_inicial(texto, padrao)
    melhor_individuo, melhor_fit, sem_melhora, geracao_final = None, -1.0, 0, 0

    for geracao in range(NUMERO_GERACOES):
        geracao_final = geracao + 1
        fits      = [fitness(ind, texto, padrao, memo) for ind in populacao]
        ordenados = sorted(range(len(populacao)), key=lambda i: fits[i], reverse=True)

        if fits[ordenados[0]] > melhor_fit:
            melhor_fit       = fits[ordenados[0]]
            melhor_individuo = list(populacao[ordenados[0]])
            sem_melhora      = 0
        else:
            sem_melhora += 1

        if melhor_fit >= LIMIAR_PARADA or sem_melhora >= PACIENCIA:
            break

        if sem_melhora > 0 and sem_melhora % 20 == 0:
            n_reinjecao = TAMANHO_POPULACAO // 10
            for i in range(n_reinjecao):
                populacao[ordenados[-(i + 1)]] = criar_individuo(n_texto, n_padrao)

        nova = [list(populacao[ordenados[i]])
                for i in range(min(TAMANHO_ELITISMO, len(populacao)))]
        while len(nova) < TAMANHO_POPULACAO:
            f1, f2 = crossover(selecionar(populacao, fits), selecionar(populacao, fits))
            nova.append(mutacao(f1, n_texto, n_padrao))
            if len(nova) < TAMANHO_POPULACAO:
                nova.append(mutacao(f2, n_texto, n_padrao))
        populacao = nova

    melhor_individuo, melhor_fit = busca_local(melhor_individuo, texto, padrao, memo)
    return melhor_individuo, melhor_fit, geracao_final


# ==================== BUSCA COMPLETA PARA UM PADRAO =======================
def buscar_padrao(texto, padrao):
    melhor_global, fit_global, geracoes_global = None, -1.0, 0

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        memo = {}
        print("  [Tentativa %d/%d]..." % (tentativa, MAX_TENTATIVAS), end=" ")
        melhor, fit, geracoes = algoritmo_genetico(texto, padrao, memo)

        if fit > fit_global:
            fit_global      = fit
            melhor_global   = melhor
            geracoes_global = geracoes

        status = "%.2f%%" % (fit * 100.0)
        if fit_global >= LIMIAR_PARADA:
            print(status, "-> 100% encontrado!")
            break
        elif fit_global >= SIMILARIDADE_MINIMA:
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
        "atingiu"     : fit_global >= SIMILARIDADE_MINIMA,
    }


# ================================= MAIN ====================================
def main():
    texto = normalizar(carregar_texto())
    if not texto:
        print("Texto vazio. Verifique o arquivo de entrada.")
        return

    padroes      = [normalizar(p) for p in PADROES]
    resultados   = []
    inicio_total = time.time()
    separador    = "=" * 70

    print(separador)
    print("CASAMENTO DE PADROES COM ALGORITMO GENETICO — MULTIPLOS PADROES")
    print("Metodo: %s | Populacao: %d | Geracoes max: %d | Tentativas max: %d"
          % (METODO_SELECAO, TAMANHO_POPULACAO, NUMERO_GERACOES, MAX_TENTATIVAS))
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
          % (atingidos, len(padroes), SIMILARIDADE_MINIMA * 100))
    print("Tempo total de execucao: %.2f s" % duracao_total)
    print(separador)


if __name__ == "__main__":
    main()
