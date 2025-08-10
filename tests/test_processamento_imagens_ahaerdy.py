import os
from processamento_imagens import aplicar_filtro_pb, redimensionar

def teste_funcional():
    arquivo_entrada = "green_forest.jpg"
    saida_pb = "green_forest_pb.jpg"
    saida_red = "green_forest_redim.jpg"

    # Verifica se arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print(f"Arquivo de entrada '{arquivo_entrada}' não encontrado. Coloque uma imagem para o teste.")
        return

    print("Executando aplicar_filtro_pb...")
    aplicar_filtro_pb(arquivo_entrada, saida_pb)
    if os.path.exists(saida_pb):
        print(f"Arquivo '{saida_pb}' criado com sucesso.")
    else:
        print(f"Falha ao criar '{saida_pb}'.")

    print("Executando redimensionar...")
    redimensionar(arquivo_entrada, saida_red, 200, 200)
    if os.path.exists(saida_red):
        print(f"Arquivo '{saida_red}' criado com sucesso.")
    else:
        print(f"Falha ao criar '{saida_red}'.")

if __name__ == "__main__":
    teste_funcional()

