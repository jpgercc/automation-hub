import cv2
import numpy as np
import os
from pathlib import Path

def inverter_cores_imagem(caminho_entrada, caminho_saida=None):
    """
    Inverte as cores de uma imagem.
    
    Args:
        caminho_entrada (str): Caminho para a imagem de entrada
        caminho_saida (str, optional): Caminho para salvar a imagem invertida.
                                     Se None, adiciona '_invertido' ao nome original.
    
    Returns:
        str: Caminho da imagem salva com cores invertidas ou None se erro
    """
    try:
        # Carrega a imagem
        img = cv2.imread(caminho_entrada)
        if img is None:
            print(f"Erro: Não foi possível carregar a imagem '{caminho_entrada}'.")
            return None
        
        # Inverte as cores (255 - valor_pixel para cada canal)
        img_invertida = 255 - img
        
        # Define o caminho de saída se não foi fornecido
        if caminho_saida is None:
            caminho_entrada_path = Path(caminho_entrada)
            nome_sem_extensao = caminho_entrada_path.stem
            extensao = caminho_entrada_path.suffix
            caminho_saida = str(caminho_entrada_path.parent / f"{nome_sem_extensao}_invertido{extensao}")
        
        # Salva a imagem invertida
        cv2.imwrite(caminho_saida, img_invertida)
        print(f"Imagem com cores invertidas salva em: '{caminho_saida}'")
        
        return caminho_saida
        
    except Exception as e:
        print(f"Erro ao processar a imagem '{caminho_entrada}': {e}")
        return None

def inverter_cores_pasta(caminho_pasta, pasta_saida=None):
    """
    Inverte as cores de todas as imagens em uma pasta.
    
    Args:
        caminho_pasta (str): Caminho da pasta com as imagens
        pasta_saida (str, optional): Pasta onde salvar as imagens invertidas.
                                   Se None, cria uma pasta 'invertidas'
    
    Returns:
        list: Lista dos caminhos das imagens processadas
    """
    try:
        pasta_entrada = Path(caminho_pasta)
        if not pasta_entrada.exists():
            print(f"Erro: Pasta '{caminho_pasta}' não existe.")
            return []
        
        # Define pasta de saída
        if pasta_saida is None:
            pasta_saida = pasta_entrada / "invertidas"
        else:
            pasta_saida = Path(pasta_saida)
        
        # Cria a pasta de saída se não existir
        pasta_saida.mkdir(exist_ok=True)
        
        # Extensões de imagem suportadas
        extensoes_imagem = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
        
        imagens_processadas = []
        
        # Processa todas as imagens na pasta
        for arquivo in pasta_entrada.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in extensoes_imagem:
                caminho_saida_arquivo = pasta_saida / f"{arquivo.stem}_invertido{arquivo.suffix}"
                resultado = inverter_cores_imagem(str(arquivo), str(caminho_saida_arquivo))
                if resultado:
                    imagens_processadas.append(resultado)
        
        print(f"\nProcessamento concluído! {len(imagens_processadas)} imagens processadas.")
        print(f"Imagens salvas na pasta: '{pasta_saida}'")
        
        return imagens_processadas
        
    except Exception as e:
        print(f"Erro ao processar a pasta '{caminho_pasta}': {e}")
        return []

def mostrar_comparacao(caminho_original, caminho_invertido):
    """
    Mostra a comparação lado a lado entre a imagem original e invertida.
    
    Args:
        caminho_original (str): Caminho da imagem original
        caminho_invertido (str): Caminho da imagem invertida
    """
    try:
        img_original = cv2.imread(caminho_original)
        img_invertida = cv2.imread(caminho_invertido)
        
        if img_original is None or img_invertida is None:
            print("Erro ao carregar as imagens para comparação.")
            return
        
        # Redimensiona as imagens se necessário (para visualização)
        altura = min(img_original.shape[0], 600)
        fator_escala = altura / img_original.shape[0]
        largura = int(img_original.shape[1] * fator_escala)
        
        img_original_resize = cv2.resize(img_original, (largura, altura))
        img_invertida_resize = cv2.resize(img_invertida, (largura, altura))
        
        # Combina as imagens lado a lado
        comparacao = np.hstack((img_original_resize, img_invertida_resize))
        
        # Mostra a comparação
        cv2.imshow('Comparacao: Original (esquerda) vs Invertida (direita)', comparacao)
        print("Pressione qualquer tecla para fechar a janela de comparacao...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Erro ao mostrar comparação: {e}")

def main():
    """
    Função principal do script com menu interativo.
    """
    print("=== CONVERSOR DE CORES - INVERSÃO ===")
    print("1. Inverter cores de uma imagem específica")
    print("2. Inverter cores de todas as imagens em uma pasta")
    print("3. Processar pasta 'qr_code_processado'")
    print("4. Processar todas as imagens na pasta atual")
    
    try:
        opcao = input("\nEscolha uma opção (1-4): ").strip()
        
        if opcao == "1":
            caminho_imagem = input("Digite o caminho da imagem: ").strip()
            if not caminho_imagem:
                print("Caminho não pode estar vazio!")
                return
            
            resultado = inverter_cores_imagem(caminho_imagem)
            if resultado:
                mostrar_comparacao(caminho_imagem, resultado)
        
        elif opcao == "2":
            caminho_pasta = input("Digite o caminho da pasta: ").strip()
            if not caminho_pasta:
                print("Caminho não pode estar vazio!")
                return
            
            inverter_cores_pasta(caminho_pasta)
        
        elif opcao == "3":
            pasta_qr = "qr_code_processado"
            if os.path.exists(pasta_qr):
                inverter_cores_pasta(pasta_qr)
            else:
                print(f"Pasta '{pasta_qr}' não encontrada!")
        
        elif opcao == "4":
            pasta_atual = "."
            inverter_cores_pasta(pasta_atual)
        
        else:
            print("Opção inválida!")
            
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
