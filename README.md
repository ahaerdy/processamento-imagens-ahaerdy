# processamento-imagens

Projeto de um pacote Python para processamento de imagens, implementando funções para aplicar filtros (preto e branco) e transformações (redimensionamento), utilizando a biblioteca Pillow. O pacote foi desenvolvido com setuptools para publicação no Test PyPI e no PyPI, incluindo scripts de teste para validação funcional das funcionalidades implementadas.

## Instalação
```bash
pip install processamento-imagens
```

## Uso
```python
from processamento_imagens import aplicar_filtro_pb, redimensionar

# Converter para preto e branco
aplicar_filtro_pb("entrada.jpg", "saida_pb.jpg")

# Redimensionar
redimensionar("entrada.jpg", "saida_red.jpg", 200, 200)
```

## Requisitos
- Python >= 3.8
- Pillow
