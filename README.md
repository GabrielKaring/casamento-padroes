# Casamento de Padrões usando Algoritmos Genéticos

Aplicação que usa um **Algoritmo Genético Memético (AG)** para encontrar, dentro de um
texto grande (*Dom Casmurro*), o trecho **mais parecido** com cada padrão
informado — tolerando substituições, inserções e deleções de caracteres.

---

## Estrutura do projeto

O código foi separado em módulos, cada um com **uma responsabilidade**. Isso
deixa claro onde cada conceito do AG está implementado:

| Arquivo                    | Responsabilidade                                                         |
|----------------------------|--------------------------------------------------------------------------|
| `config.py`                | Todos os **parâmetros** do AG num só lugar                               |
| `texto.py`                 | **Entrada de dados**: carrega e normaliza o texto                        |
| `fitness.py`               | **Função fitness**: distância de edição e similaridade                   |
| `operadores.py`            | **Operadores genéticos**: geração inicial (com trigramas), seleção, crossover, mutação |
| `algoritmo_genetico.py`    | **Laço principal** de evolução das gerações                              |
| `busca_local.py`           | **Hill climbing** pós-evolução para refinar o melhor indivíduo           |
| `main.py`                  | **Ponto de entrada**: itera sobre os padrões e imprime o relatório final |
| `jdoodle_arquivo_unico.py` | Mesma lógica em **um único arquivo** (para o teste no JDoodle)           |

---

## Onde cada exigência da rubrica está documentada

| Exigência                  | Onde encontrar                                                            |
|----------------------------|---------------------------------------------------------------------------|
| Tamanho da população       | `config.TAMANHO_POPULACAO` (200)                                          |
| Número de gerações         | `config.NUMERO_GERACOES` (400)                                            |
| Taxa de mutação            | `config.TAXA_MUTACAO` (0.30)                                              |
| Fitness                    | `fitness.py` → `fitness()` (1 − distância_edição / tam_máx)              |
| Geração inicial            | `operadores.py` → `populacao_inicial()` (aleatória + sementes trigramas) |
| Seleção (torneio / roleta) | `operadores.py` → `selecao_torneio()` / `selecao_roleta()`               |
| Crossover (um ponto)       | `operadores.py` → `crossover()`                                           |
| Mutação                    | `operadores.py` → `mutacao()` (3 níveis de amplitude)                    |

---

## Como o AG funciona (fluxo)

```
1. Lê e normaliza o texto                                    (texto.py)
2. Para cada padrão em PADROES (até MAX_TENTATIVAS vezes):
     2a. Cria população inicial: sementes por trigramas
         + indivíduos aleatórios                             (operadores.py)
     2b. Para cada geração:                                  (algoritmo_genetico.py)
           i.  avalia o fitness de cada indivíduo            (fitness.py)
           ii. guarda o melhor (elitismo — top 6)
           iii.verifica parada antecipada
           iv. a cada 20 gerações sem melhora: reinjeta
               10% de indivíduos aleatórios (diversidade)
           v.  gera nova população: SELEÇÃO → CROSSOVER → MUTAÇÃO
     2c. Refina o melhor indivíduo com hill climbing         (busca_local.py)
     2d. Guarda o melhor resultado entre as tentativas
3. Imprime o relatório final com todos os padrões           (main.py)
```

### Representação do cromossomo

Cada indivíduo é uma lista `[inicio, comprimento]`:

- **inicio** → posição inicial do trecho no texto;
- **comprimento** → tamanho do trecho. Deixar o comprimento *variar* é o que
  permite tratar **inserções e deleções** — o melhor trecho nem sempre tem o
  mesmo tamanho do padrão.

### Inicialização com sementes por trigramas

20% da população inicial é gerada de forma inteligente: substrings do padrão
(com ~|padrão|/4 caracteres) são buscadas literalmente no texto, e cada
ocorrência encontrada gera um indivíduo já próximo da solução. Os 80% restantes
são aleatórios. Isso acelera a convergência sem perder diversidade.

### Função fitness

```
fitness = 1 − distância_de_edição(padrão, trecho) / tamanho_máximo
```

A **distância de edição (Levenshtein)** conta o número mínimo de inserções,
deleções e substituições para transformar uma string na outra. Por isso o AG
encontra trechos *parecidos* mesmo com ruído (acentos, letras trocadas, etc.).

A memoização é **isolada por padrão**: cada rodada recebe um cache zerado,
evitando que resultados de um padrão contaminem a busca de outro.

### Mutação em 3 níveis

A mutação do gene `inicio` opera em três amplitudes:

| Probabilidade | Tipo                   | Delta         |
|---------------|------------------------|---------------|
| 60%           | Ajuste fino            | ±8 caracteres |
| 25%           | Exploração média       | ±50 caracteres|
| 15%           | Reinício global        | posição aleatória no texto |

### Busca local — Hill Climbing

Após o encerramento do AG, o melhor indivíduo é refinado por uma busca local
exaustiva: testa todas as combinações de deslocamento de posição (±30) e
comprimento (±folga), movendo-se para o vizinho de maior fitness enquanto
houver melhora. Isso transforma o AG puro em um **algoritmo memético**.

---

## Como executar

### Localmente (versão em módulos)

Coloque o arquivo `dom_casmurro.txt` na mesma pasta e rode:

```bash
python main.py
```

Para alterar os padrões buscados, edite a lista `PADROES` em `config.py`.

### No JDoodle (versão de arquivo único)

O JDoodle gratuito roda **apenas um arquivo**. Use o
`jdoodle_arquivo_unico.py`, suba o `dom_casmurro.txt` junto e edite a lista
`PADROES` no topo do arquivo antes de cada teste.

> Se o `dom_casmurro.txt` não for encontrado, o programa tenta o caminho
> `/uploads/dom_casmurro.txt` (JDoodle) e, em último caso, usa um pequeno
> trecho de exemplo embutido para não quebrar durante testes.

---

## Ajustes de qualidade × velocidade

Tudo em `config.py`:

| Parâmetro           | Valor atual | Efeito ao aumentar                              |
|---------------------|-------------|-------------------------------------------------|
| `TAMANHO_POPULACAO` | 200         | Mais diversidade, mais lento                    |
| `NUMERO_GERACOES`   | 400         | Mais tempo de evolução, mais lento              |
| `TAXA_MUTACAO`      | 0.30        | Mais exploração, risco de instabilidade         |
| `PACIENCIA`         | 80          | Mais tolerância à estagnação antes de parar     |
| `MAX_TENTATIVAS`    | 5           | Mais chances de escapar de ótimos locais        |
| `FOLGA_TAMANHO`     | 5           | Aceita trechos com mais inserções/deleções      |

- **Mais qualidade:** aumentar `TAMANHO_POPULACAO`, `NUMERO_GERACOES` e `MAX_TENTATIVAS`.
- **Mais velocidade (JDoodle):** reduzir `TAMANHO_POPULACAO` e `NUMERO_GERACOES`.
  A memoização, a parada antecipada e a reinjeção de diversidade já ajudam bastante.
