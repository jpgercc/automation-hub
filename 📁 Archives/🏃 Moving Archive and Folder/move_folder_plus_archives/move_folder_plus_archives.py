import shutil
import os

def mover_pasta():
    
    origem = input("Digite o caminho da pasta que deseja mover: ")
    
    # verifica pasta de origem
    if not os.path.exists(origem):
        print(f"A pasta '{origem}' não existe.")
        return
    
    destino = input("Digite o caminho da pasta de destino: ")
    
    # verifica pasta destino
    if not os.path.exists(destino):
        print(f"A pasta de destino '{destino}' não existe.")
        return
    
    nome_pasta = os.path.basename(origem)
    
    # cria o novo caminho de destino
    novo_destino = os.path.join(destino, nome_pasta)
    
    try:
        shutil.move(origem, novo_destino)
        print(f"A pasta '{nome_pasta}' foi movida para '{destino}' com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao mover a pasta: {e}")

if __name__ == "__main__":
    mover_pasta()
