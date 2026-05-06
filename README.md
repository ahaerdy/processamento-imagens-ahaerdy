# processamento-imagens

> **Pacote Python para processamento de imagens** — implementando filtros e transformações com [Pillow](https://python-pillow.org/), publicado no [Test PyPI](https://test.pypi.org/) e no [PyPI](https://pypi.org/). Projeto desenvolvido como parte do bootcamp da [DIO](https://www.dio.me/).

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Repositório](#estrutura-do-repositório)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Instalação](#instalação)
5. [Código-Fonte Detalhado](#código-fonte-detalhado)
   - [\_\_init\_\_.py](#__init__py)
   - [filtros.py](#filtrospy)
   - [transformacoes.py](#transformacoespy)
6. [Uso](#uso)
7. [Testes](#testes)
   - [test_basico.py](#test_basicopy)
   - [test_processamento_imagens_ahaerdy.py](#test_processamento_imagens_ahaerdypy)
8. [Resultados Visuais](#resultados-visuais)
9. [Publicação no PyPI](#publicação-no-pypi)
10. [Referências](#referências)

---

## Visão Geral

O **processamento-imagens** é um pacote Python minimalista e didático que demonstra como encapsular funcionalidades de processamento de imagens em um módulo reutilizável e distribuível. O projeto cobre o ciclo completo de desenvolvimento de um pacote Python:

- **Desenvolvimento** do código com boas práticas de orientação a funções e documentação (`docstrings`).
- **Empacotamento** com `setuptools` e geração de distribuições (`sdist` e `wheel`).
- **Publicação** no Test PyPI (ambiente de homologação) e, após validação, no PyPI oficial.
- **Testes** com scripts de validação funcional e de importação.

As funcionalidades implementadas são:

| Função | Descrição |
|---|---|
| `aplicar_filtro_pb` | Converte uma imagem colorida para escala de cinza (preto e branco) |
| `redimensionar` | Redimensiona uma imagem para largura e altura especificadas |

---

## Estrutura do Repositório

```
processamento-imagens-ahaerdy/
│
├── processamento_imagens/          # Pacote principal
│   ├── __init__.py                 # Ponto de entrada do pacote; exporta as funções públicas
│   ├── filtros.py                  # Módulo de filtros (ex.: preto e branco)
│   └── transformacoes.py           # Módulo de transformações (ex.: redimensionamento)
│
├── tests/                          # Diretório de testes e assets
│   ├── green_forest.jpg            # Imagem de entrada usada nos testes
│   ├── green_forest_pb.jpg         # Saída esperada: imagem em preto e branco
│   ├── green_forest_redim.jpg      # Saída esperada: imagem redimensionada (200×200 px)
│   ├── test_basico.py              # Teste de importação das funções do pacote
│   └── test_processamento_imagens_ahaerdy.py  # Teste funcional completo
│
├── setup.py / pyproject.toml       # Configuração do pacote para distribuição
├── README.md                       # Documentação do projeto (este arquivo)
└── LICENSE                         # Licença do projeto
```

> **Convenção de nomes:** o diretório do pacote utiliza `_` (underline) — `processamento_imagens` — pois Python não permite `-` em nomes de módulos. O repositório Git usa `-` (hífen) por convenção de URLs.

---

## Tecnologias Utilizadas

| Tecnologia | Versão mínima | Finalidade |
|---|---|---|
| Python | 3.8+ | Linguagem principal |
| [Pillow](https://python-pillow.org/) | Qualquer recente | Manipulação de imagens (open, convert, resize, save) |
| [setuptools](https://setuptools.pypa.io/) | — | Empacotamento e geração de distribuições |
| [pip](https://pip.pypa.io/) | — | Instalação de dependências e do próprio pacote |
| [twine](https://twine.readthedocs.io/) | — | Upload seguro das distribuições para o PyPI |

---

## Instalação

### Opção 1 — Via PyPI (produção)

```bash
pip install processamento-imagens
```

### Opção 2 — Via Test PyPI (homologação)

```bash
pip install --index-url https://test.pypi.org/simple/ processamento-imagens
```

### Opção 3 — A partir do código-fonte

```bash
# Clone o repositório
git clone https://github.com/ahaerdy/processamento-imagens-ahaerdy.git
cd processamento-imagens-ahaerdy

# Instale as dependências e o pacote em modo editável
pip install -e .
```

> **Requisito:** Python 3.8 ou superior. A dependência `Pillow` é instalada automaticamente.

---

## Código-Fonte Detalhado

### `__init__.py`

O arquivo `__init__.py` é o que transforma o diretório `processamento_imagens/` em um **pacote Python**. Ele define a API pública do módulo, tornando as funções diretamente acessíveis a partir do namespace raiz do pacote — sem que o usuário precise conhecer a estrutura interna de arquivos.

```python
"""
Pacote de processamento de imagens - exemplo para Test PyPI
"""
from .filtros import aplicar_filtro_pb
from .transformacoes import redimensionar
```

**Como funciona:**

- `from .filtros import aplicar_filtro_pb` → importação relativa: busca `filtros.py` dentro do próprio pacote (o ponto `.` representa o pacote atual).
- `from .transformacoes import redimensionar` → idem para o módulo de transformações.

**Benefício para o usuário:** em vez de escrever `from processamento_imagens.filtros import aplicar_filtro_pb`, basta:

```python
from processamento_imagens import aplicar_filtro_pb, redimensionar
```

---

### `filtros.py`

Responsável pela aplicação de filtros de imagem. Atualmente implementa a conversão para **escala de cinza** (preto e branco).

```python
from PIL import Image

def aplicar_filtro_pb(caminho_entrada, caminho_saida):
    """
    Converte a imagem para preto e branco.

    Parâmetros
    ----------
    caminho_entrada : str
        Caminho para o arquivo de imagem de entrada (ex.: "foto.jpg").
    caminho_saida : str
        Caminho onde a imagem convertida será salva (ex.: "foto_pb.jpg").

    Exemplo
    -------
    >>> aplicar_filtro_pb("green_forest.jpg", "green_forest_pb.jpg")
    """
    imagem = Image.open(caminho_entrada).convert("L")
    imagem.save(caminho_saida)
```

**Análise linha a linha:**

| Linha | Descrição |
|---|---|
| `from PIL import Image` | Importa a classe `Image` da biblioteca Pillow, ponto central de toda operação sobre imagens. |
| `Image.open(caminho_entrada)` | Abre o arquivo de imagem e carrega seus dados em memória. Suporta JPG, PNG, BMP, TIFF e outros formatos. |
| `.convert("L")` | Converte o modo de cor para **Luminance** (`"L"`), que é a escala de cinza de 8 bits (0 = preto, 255 = branco). Pillow aplica a fórmula padrão de luminância: `L = 0.299·R + 0.587·G + 0.114·B`. |
| `imagem.save(caminho_saida)` | Grava a imagem processada em disco. O formato é inferido automaticamente pela extensão do arquivo. |

> 🔬 **Detalhe técnico:** o modo `"L"` (Luminance) é diferente de `"1"` (bitmap binário, somente preto ou branco puro). `"L"` preserva os **256 tons de cinza**, produzindo resultados visualmente ricos.

---

### `transformacoes.py`

Responsável por transformações geométricas na imagem. Atualmente implementa o **redimensionamento**.

```python
from PIL import Image

def redimensionar(caminho_entrada, caminho_saida, largura, altura):
    """
    Redimensiona a imagem para a largura e altura especificadas.

    Parâmetros
    ----------
    caminho_entrada : str
        Caminho para o arquivo de imagem de entrada.
    caminho_saida : str
        Caminho onde a imagem redimensionada será salva.
    largura : int
        Largura desejada em pixels.
    altura : int
        Altura desejada em pixels.

    Exemplo
    -------
    >>> redimensionar("green_forest.jpg", "green_forest_redim.jpg", 200, 200)
    """
    imagem = Image.open(caminho_entrada)
    imagem = imagem.resize((largura, altura))
    imagem.save(caminho_saida)
```

**Análise linha a linha:**

| Linha | Descrição |
|---|---|
| `Image.open(caminho_entrada)` | Abre a imagem de entrada. |
| `imagem.resize((largura, altura))` | Redimensiona para as dimensões especificadas (em pixels). O argumento é uma **tupla** `(width, height)`. Por padrão, Pillow usa o filtro `BICUBIC` para interpolação, garantindo boa qualidade visual. |
| `imagem.save(caminho_saida)` | Salva a imagem resultante. |

> ⚠️ **Atenção:** `resize()` **não** preserva a proporção (aspect ratio) automaticamente. Se as proporções originais forem diferentes das desejadas, a imagem ficará distorcida. Para preservar proporções, use `Image.thumbnail()` ou calcule as dimensões proporcionalmente antes de chamar `resize()`.

---

## Uso

### Exemplo completo em Python

```python
from processamento_imagens import aplicar_filtro_pb, redimensionar

# --- Filtro Preto e Branco ---
aplicar_filtro_pb("green_forest.jpg", "green_forest_pb.jpg")
print("Imagem convertida para preto e branco com sucesso!")

# --- Redimensionamento ---
redimensionar("green_forest.jpg", "green_forest_redim.jpg", 200, 200)
print("Imagem redimensionada para 200×200 px com sucesso!")
```

### Execução via linha de comando (chamada direta do script de teste)

```bash
cd tests/
python test_processamento_imagens_ahaerdy.py
```

**Saída esperada no terminal:**

```
Executando aplicar_filtro_pb...
Arquivo 'green_forest_pb.jpg' criado com sucesso.
Executando redimensionar...
Arquivo 'green_forest_redim.jpg' criado com sucesso.
```

---

## Testes

O projeto conta com dois scripts de teste localizados na pasta `tests/`.

### `test_basico.py`

Teste de **sanidade de importação**: verifica se as funções do pacote são importadas corretamente e se são chamáveis (objetos do tipo função). Ideal para integração contínua (CI) com `pytest`.

```python
def test_imports():
    from processamento_imagens import aplicar_filtro_pb, redimensionar
    assert callable(aplicar_filtro_pb)
    assert callable(redimensionar)
```

**Como executar:**

```bash
# Na raiz do projeto
pytest tests/test_basico.py -v
```

**Saída esperada:**

```
tests/test_basico.py::test_imports PASSED     [100%]
1 passed in 0.XXs
```

---

### `test_processamento_imagens_ahaerdy.py`

Teste **funcional de ponta a ponta**: executa as funções com arquivos reais de imagem e verifica se os arquivos de saída foram gerados no disco.

```python
import os
from processamento_imagens import aplicar_filtro_pb, redimensionar

def teste_funcional():
    arquivo_entrada = "green_forest.jpg"
    saida_pb        = "green_forest_pb.jpg"
    saida_red       = "green_forest_redim.jpg"

    # Verifica se o arquivo de entrada existe antes de prosseguir
    if not os.path.exists(arquivo_entrada):
        print(f"Arquivo de entrada '{arquivo_entrada}' não encontrado.")
        return

    # --- Teste do filtro preto e branco ---
    print("Executando aplicar_filtro_pb...")
    aplicar_filtro_pb(arquivo_entrada, saida_pb)
    if os.path.exists(saida_pb):
        print(f"Arquivo '{saida_pb}' criado com sucesso.")
    else:
        print(f"Falha ao criar '{saida_pb}'.")

    # --- Teste do redimensionamento ---
    print("Executando redimensionar...")
    redimensionar(arquivo_entrada, saida_red, 200, 200)
    if os.path.exists(saida_red):
        print(f"Arquivo '{saida_red}' criado com sucesso.")
    else:
        print(f"Falha ao criar '{saida_red}'.")

if __name__ == "__main__":
    teste_funcional()
```

**Fluxo do teste:**

```
green_forest.jpg  ──►  aplicar_filtro_pb()  ──►  green_forest_pb.jpg
green_forest.jpg  ──►  redimensionar()      ──►  green_forest_redim.jpg
```

**Como executar:**

```bash
cd tests/
python test_processamento_imagens_ahaerdy.py
```

---

## Resultados Visuais

A seguir, a demonstração visual das transformações aplicadas sobre a imagem de entrada `green_forest.jpg`.

### Imagem Original — `green_forest.jpg`

![green_forest.jpg](tests/green_forest.jpg)

*Imagem original colorida de uma floresta. Dimensões originais: 640×426 px (aprox.). Formato: JPEG.*

---

### Após `aplicar_filtro_pb()` — `green_forest_pb.jpg`

![green_forest_pb.jpg](tests/green_forest_pb.jpg)

*Resultado da conversão para escala de cinza (modo `"L"` do Pillow). Observe que todos os canais RGB foram combinados em um único canal de luminância, preservando os 256 tons de cinza.*

---

### Após `redimensionar(200, 200)` — `green_forest_redim.jpg`

![green_forest_redim.jpg](tests/green_forest_redim.jpg)

*Resultado do redimensionamento para 200×200 pixels. A proporção original foi alterada para caber nas dimensões especificadas.*

---

### Comparativo resumido

| Arquivo | Operação | Modo de Cor | Dimensões |
|---|---|---|---|
| `green_forest.jpg` | — (original) | RGB | ~640×426 px |
| `green_forest_pb.jpg` | `aplicar_filtro_pb()` | L (escala de cinza) | ~640×426 px (mantida) |
| `green_forest_redim.jpg` | `redimensionar(200, 200)` | RGB | 200×200 px |

---

## Publicação no PyPI

O pacote segue o fluxo padrão de distribuição recomendado pela Python Packaging Authority ([PyPA](https://packaging.python.org/)).

### 1. Estrutura de empacotamento

O `setup.py` (ou `pyproject.toml`) define os metadados do pacote:

```python
# setup.py (exemplo)
from setuptools import setup, find_packages

setup(
    name="processamento-imagens",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["Pillow"],
    author="ahaerdy",
    description="Pacote Python para filtros e transformações de imagens",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ahaerdy/processamento-imagens-ahaerdy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
```

### 2. Geração das distribuições

```bash
# Instala as ferramentas necessárias
pip install build twine

# Gera os arquivos de distribuição (sdist + wheel) na pasta dist/
python -m build
```

Isso cria:
```
dist/
├── processamento_imagens-0.1.0.tar.gz   # Source distribution (sdist)
└── processamento_imagens-0.1.0-py3-none-any.whl  # Built distribution (wheel)
```

### 3. Publicação no Test PyPI (homologação)

```bash
# Faz upload para o ambiente de testes
twine upload --repository testpypi dist/*
```

### 4. Validação da instalação a partir do Test PyPI

```bash
pip install --index-url https://test.pypi.org/simple/ processamento-imagens
```

### 5. Publicação no PyPI oficial

Após validação completa no ambiente de homologação:

```bash
twine upload dist/*
```

> Acesse [https://pypi.org/project/processamento-imagens/](https://pypi.org/project/processamento-imagens/) para confirmar a publicação.

---

## Referências

- [Documentação oficial do Pillow](https://pillow.readthedocs.io/)
- [Python Packaging User Guide — PyPA](https://packaging.python.org/en/latest/)
- [Test PyPI](https://test.pypi.org/)
- [PyPI](https://pypi.org/)
- [Repositório de Estudos — Bootcamp Suzano Python Developer](https://github.com/ahaerdy/DIO-learning/tree/main/Suzano%20-%20Python%20Developer)
- [Repositório de Estudos — Bootcamp NTT DATA: Engenharia de Dados com Python](https://github.com/ahaerdy/DIO-learning/tree/main/NTT%20DATA-Engenharia%20de%20Dados%20com%20Python)
