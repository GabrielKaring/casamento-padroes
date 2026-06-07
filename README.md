# Casamento de Padrões usando Algoritmos Genéticos

Aplicação que usa um **Algoritmo Genético (AG)** para encontrar, dentro de um
texto grande (*Dom Casmurro*), o trecho **mais parecido** com um padrão
informado — tolerando substituições, inserções e deleções de caracteres.

---

## Estrutura do projeto

O código foi separado em módulos, cada um com **uma responsabilidade**. Isso
deixa claro onde cada conceito do AG está implementado:

| Arquivo                   | Responsabilidade                                                     |
|---------------------------|----------------------------------------------------------------------|
| `config.py`               | Todos os **parâmetros** do AG num só lugar                           |
| `texto.py`                | **Entrada de dados**: carrega e normaliza o texto                    |
| `fitness.py`              | **Função fitness**: distância de edição e similaridade              |
| `operadores.py`           | **Operadores genéticos**: geração inicial, seleção, crossover, mutação |
| `algoritmo_genetico.py`   | **Laço principal** de evolução das gerações                          |
| `main.py`                 | **Ponto de entrada**: junta tudo e imprime o resultado               |
| `jdoodle_arquivo_unico.py`| Mesma lógica em **um único arquivo** (para o teste no JDoodle)       |

---

## Onde cada exigência da rubrica está documentada

| Exigência                  | Onde encontrar                                              |
|----------------------------|------------------------------------------------------------|
| Tamanho da população       | `config.TAMANHO_POPULACAO`                                 |
| Número de gerações         | `config.NUMERO_GERACOES`                                   |
| Taxa de mutação            | `config.TAXA_MUTACAO`                                       |
| Fitness                    | `fitness.py` → `fitness()` (1 − distância_edição / tam_máx) |
| Geração inicial            | `operadores.py` → `populacao_inicial()`                    |
| Seleção (torneio / roleta) | `operadores.py` → `selecao_torneio()` / `selecao_roleta()` |
| Crossover (um ponto)       | `operadores.py` → `crossover()`                            |
| Mutação                    | `operadores.py` → `mutacao()`                              |

---

## Como o AG funciona (fluxo)

```
1. Lê e normaliza o texto                          (texto.py)
2. Cria população inicial aleatória                (operadores.py)
3. Para cada geração:                              (algoritmo_genetico.py)
     a) avalia o fitness de cada indivíduo         (fitness.py)
     b) guarda o melhor (elitismo)
     c) verifica parada antecipada
     d) gera nova população: SELEÇÃO → CROSSOVER → MUTAÇÃO
4. Imprime o melhor indivíduo e a % de similaridade (main.py)
```

### Representação do cromossomo

Cada indivíduo é uma lista `[inicio, comprimento]`:

- **inicio** → posição inicial do trecho no texto (sugestão do enunciado);
- **comprimento** → tamanho do trecho. Deixar o comprimento *variar* é o que
  permite tratar **inserções e deleções** — o melhor trecho nem sempre tem o
  mesmo tamanho do padrão.

### Função fitness

```
fitness = 1 − distância_de_edição(padrão, trecho) / tamanho_máximo
```

A **distância de edição (Levenshtein)** conta o número mínimo de inserções,
deleções e substituições para transformar uma string na outra. Por isso o AG
encontra trechos *parecidos* mesmo com ruído (acentos, letras trocadas, etc.).

---

## Como executar

### Localmente (versão em módulos)

Coloque o arquivo `dom_casmurro.txt` na mesma pasta e rode:

```bash
python main.py
```

Para trocar o padrão buscado, edite `PADRAO` em `config.py`.

### No JDoodle (versão de arquivo único)

O JDoodle gratuito roda **apenas um arquivo**. Use o
`jdoodle_arquivo_unico.py`, suba o `dom_casmurro.txt` junto e edite o `PADRAO`
no topo do arquivo a cada teste.

> Se o `dom_casmurro.txt` não for encontrado, o programa usa um pequeno trecho
> de exemplo embutido (apenas para não quebrar durante testes).

---

## Ajustes de qualidade × velocidade

Tudo em `config.py`:

- **Mais qualidade:** aumentar `TAMANHO_POPULACAO` e `NUMERO_GERACOES`;
  aumentar `FOLGA_TAMANHO` se o padrão tiver muitas inserções/deleções.
- **Mais velocidade (JDoodle):** reduzir `TAMANHO_POPULACAO` e
  `NUMERO_GERACOES`. A memoização e a parada antecipada já ajudam bastante.