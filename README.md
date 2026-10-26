# APRESENTAÇÃO SOBRE TIMSORT

Projeto referente à apresentação do algoritmo de ordenação TimSort requisitado pelo professor Luis Henrique Sacchi, no curso de Bacharelado em Ciência da Computação pelo Instituto Federal de Educação, Ciência e Tecnologia (IFSP) — Campus Salto.
**Integrantes:**

- Eduardo Martins Corrêa
- Fábio Haruo de Freitas Nishioka
- Seren Iketani
- Yasmin Sampieri Tonello Cury

### 1 Requisitos

Para compilar o projeto, você precisará de:

1. um compilador, de preferência o [Gnu C Compiler (`gcc`)](https://gcc.gnu.org/);
2. o [`make`](https://www.gnu.org/software/make/);
3. o [`uv`](https://docs.astral.sh/uv/).

> [!WARNING]
> Se você está no Linux, tanto o `gcc` quanto o `make` já vêm instalados de fábrica. Caso você use Windows, terá de baixar as ferramentas manualmente. Procure sobre MSYS2 e adicione o `gcc.exe` ao `PATH` do sistema. A seguir, baixe o `choco` para baixar o `make`.

### 2 Setup do ambiente

1. Clone o repositório:

```bash
git clone https://github.com/Haruo09/TimSortPresentation && cd TimSortPresentation
```

ou utilize o GitHub CLI:

```bash
gh repo clone Haruo09/TimSortPresentation && cd TimSortPresentation
```

A seguir, compile com o `make`:

```bash
make clean && make
```

A biblioteca estará compilada em um arquivo `.so` (ou `.dll`, no Windows) dentro da pasta `./build/lib/` e o processo de compilação gerará um arquivo executável de teste em `./build/bin/`.

Após isso, inicie o ambiente o `uv`:

```bash
uv sync
source .venv/bin/activate
```

### 3 Como usar a CLI (`sort-analyzer`)

O projeto inclui uma interface de linha de comando (CLI) desenvolvida com Typer e Rich, permitindo executar benchmarks e gerar gráficos interativos e estáticos via Matplotlib.

#### 3.1 Análise de Algoritmo Único (`analyze`)

Executa testes empíricos de complexidade em três distribuições de dados (aleatória, quase ordenada e inversamente ordenada) e calcula o ajuste de curva (_curve fitting_).

```bash
uv run sort-analyzer analyze timsort -m 1000 -M 50000 -s 10 -o plots/timsort_analysis.png
```

#### 3.2 Comparação Direta (`compare`)

Realiza um teste _head-to-head_ entre dois algoritmos nas mesmas distribuições de entrada, destacando a diferença percentual de desempenho.

```bash
uv run sort-analyzer compare timsort quicksort -m 1000 -M 50000 -s 10 -o plots/comparison.png
```

---

### Tabela de Parâmetros e Opções

| Opção        | Atalho |  Padrão  | Descrição                                                              |
| :----------- | :----: | :------: | :--------------------------------------------------------------------- |
| `--min-size` |  `-m`  |  `1000`  | Tamanho inicial do vetor de teste.                                     |
| `--max-size` |  `-M`  | `100000` | Tamanho máximo do vetor no benchmark.                                  |
| `--steps`    |  `-s`  |   `10`   | Número de passos logarítmicos entre os tamanhos mínimo e máximo.       |
| `--output`   |  `-o`  |  `None`  | Caminho do arquivo `.png` onde o gráfico gerado será salvo (opcional). |

### 4 Como executar os testes unitários

> [!WARNING]
> Devido às atualizações da interface CLI, esta sessão não está mais funcional. Será corrigido futuramente.

Caso não tenha instalado o `uv` ainda, volte na seção anterior e o faça.
Tendo todas as dependências carregadas e o ambiente virtual ativo, execute:

```bash
pytest ./tests -v
```
