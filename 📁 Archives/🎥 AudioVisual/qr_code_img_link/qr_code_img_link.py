import numpy as np # cv2 
import cv2 # Manipula de imagens
from pyzbar.pyzbar import decode # Para decodificação de QR Codes
import sys # Manipula de argumentos de linha de comando como o caminho do arquivo
import os # Manipula de arquivos e diretórios
import glob # Manipula de caminhos de arquivo e criação de pastas
# pip install pyzbar opencv-python numpy

def ler_qr_code(caminho_da_imagem):
    """
    Tenta ler um QR Code de uma imagem usando múltiplas técnicas de processamento.
    """
    try:
        img = cv2.imread(caminho_da_imagem)
        if img is None:
            print(f"Erro: Não foi possível carregar a imagem em '{caminho_da_imagem}'.")
            return None

        # Converte para tons de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        processed_images = []

        # 1. Binarização adaptativa (Gaussian)
        thresh_adapt_gauss = cv2.adaptiveThreshold(gray, 255, 
                                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                   cv2.THRESH_BINARY, 11, 2)
        processed_images.append(("Adaptive Gaussian", thresh_adapt_gauss))

        # 2. Binarização adaptativa (Mean)
        thresh_adapt_mean = cv2.adaptiveThreshold(gray, 255, 
                                                  cv2.ADAPTIVE_THRESH_MEAN_C, 
                                                  cv2.THRESH_BINARY, 11, 2)
        processed_images.append(("Adaptive Mean", thresh_adapt_mean))

        # 3. Binarização Otsu
        _, thresh_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed_images.append(("Otsu Binarization", thresh_otsu))

        # 4. Binarização Otsu com inversão
        _, thresh_otsu_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        processed_images.append(("Otsu Binarization Inverted", thresh_otsu_inv))

        # 5. Desfoque (blur) + Binarização Adaptativa
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh_blurred = cv2.adaptiveThreshold(blurred, 255, 
                                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                cv2.THRESH_BINARY, 11, 2)
        processed_images.append(("Blurred + Adaptive", thresh_blurred))

        # Tenta decodificar cada versão da imagem
        for name, current_img in processed_images:
            print(f"Tentando decodificar com: {name}...")
            decoded_objects = decode(current_img)
            
            if decoded_objects:
                for obj in decoded_objects:
                    link = obj.data.decode('utf-8')
                    print(f"SUCESSO! Link do QR Code encontrado com {name}: {link}")
                    return link
        
        print("Nenhum QR Code encontrado após todas as tentativas de pré-processamento.")
        return None
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

def salvar_imgs_testes(caminho_da_imagem):
    """
    Salva imagens de teste do processamento para inspeção manual.
    """
    try:
        img = cv2.imread(caminho_da_imagem)
        if img is None:
            print(f"Erro: Não foi possível carregar a imagem em '{caminho_da_imagem}'.")
            return None

        # Cria uma pasta para salvar as imagens de teste
        output_folder = "qr_code_processado"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Salva a imagem original pra referência
        cv2.imwrite(os.path.join(output_folder, "00_original.png"), img)
        print(f"Salvando imagem original em '{output_folder}/00_original.png'")

        # Converte para tons de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(output_folder, "01_gray.png"), gray)
        print(f"Salvando imagem cinza em '{output_folder}/01_gray.png'")

        # 1. Binarização adaptativa (Gaussian)
        thresh_adapt_gauss = cv2.adaptiveThreshold(gray, 255, 
                                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                   cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite(os.path.join(output_folder, "02_adaptive_gaussian.png"), thresh_adapt_gauss)
        print(f"Salvando '02_adaptive_gaussian.png'")

        # 2. Binarização adaptativa (Mean)
        thresh_adapt_mean = cv2.adaptiveThreshold(gray, 255, 
                                                  cv2.ADAPTIVE_THRESH_MEAN_C, 
                                                  cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite(os.path.join(output_folder, "03_adaptive_mean.png"), thresh_adapt_mean)
        print(f"Salvando '03_adaptive_mean.png'")

        # 3. Binarização Otsu
        _, thresh_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite(os.path.join(output_folder, "04_otsu.png"), thresh_otsu)
        print(f"Salvando '04_otsu.png'")

        # 4. Binarização Otsu com inversão
        _, thresh_otsu_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        cv2.imwrite(os.path.join(output_folder, "05_otsu_inverted.png"), thresh_otsu_inv)
        print(f"Salvando '05_otsu_inverted.png'")

        # 5. Desfoque (blur) + Binarização Adaptativa
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imwrite(os.path.join(output_folder, "06_blurred_gray.png"), blurred)
        print(f"Salvando '06_blurred_gray.png'")
        
        thresh_blurred = cv2.adaptiveThreshold(blurred, 255, 
                                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite(os.path.join(output_folder, "07_blurred_adaptive.png"), thresh_blurred)
        print(f"Salvando '07_blurred_adaptive.png'")

        print(f"Todas as imagens de teste foram salvas na pasta '{output_folder}' para inspeção manual.")
        return output_folder
            
    except Exception as e:
        print(f"Ocorreu um erro ao salvar testes: {e}")
        return None

def ler_qr_code_com_testes(caminho_da_imagem):
    """
    Função que combina leitura de QR code com salvamento de testes.
    """
    # Primeiro tenta ler o QR code
    link = ler_qr_code(caminho_da_imagem)
    
    # Se não encontrou o QR code, salva as imagens de teste para inspeção manual
    if link is None:
        print("\nSalvando imagens de teste para inspeção manual...")
        salvar_imgs_testes(caminho_da_imagem)
    return link
    
# Processa todos os arquivos de imagem em uma pasta.
def processar_pasta_completa(pasta):
    
    extensoes = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.tif']
    arquivos_imagem = []
    
    for extensao in extensoes:
        arquivos_imagem.extend(glob.glob(os.path.join(pasta, extensao)))
        arquivos_imagem.extend(glob.glob(os.path.join(pasta, extensao.upper())))
    
    if not arquivos_imagem:
        print(f"Nenhum arquivo de imagem encontrado na pasta '{pasta}'")
        return
    
    print(f"Encontrados {len(arquivos_imagem)} arquivo(s) de imagem na pasta '{pasta}':")
    for arquivo in arquivos_imagem:
        print(f"  - {os.path.basename(arquivo)}")
    
    links_encontrados = []
    
    for arquivo in arquivos_imagem:
        print(f"\n{'='*60}")
        print(f"Processando: {os.path.basename(arquivo)}")
        print(f"{'='*60}")
        
        link = ler_qr_code_com_testes(arquivo)
        if link:
            links_encontrados.append((os.path.basename(arquivo), link))
    
    # Resumo final
    print(f"\n{'='*60}")
    print("RESUMO FINAL")
    print(f"{'='*60}")
    
    if links_encontrados:
        print(f"QR Codes encontrados em {len(links_encontrados)} arquivo(s):")
        for arquivo, link in links_encontrados:
            print(f"  {arquivo}: {link}")
    else:
        print("Nenhum QR Code foi encontrado em nenhum arquivo da pasta.")


# Obtém a entrada do usuário para escolher entre arquivo único ou pasta.
def obter_entrada_usuario():

    print("=== LEITOR DE QR CODE ===")
    print("Escolha uma opção:")
    print("1. Processar um arquivo específico")
    print("2. Processar todos os arquivos de imagem de uma pasta")
    
    while True:
        escolha = input("\nDigite sua escolha (1 ou 2): ").strip()
        
        if escolha == "1":
            arquivo = input("Digite o nome do arquivo (ou caminho completo): ").strip()
            if not arquivo:
                print("Nome do arquivo não pode estar vazio!")
                continue
            
            if not os.path.exists(arquivo):
                print(f"Arquivo '{arquivo}' não encontrado!")
                continuar = input("Deseja tentar novamente? (s/n): ").strip().lower()
                if continuar not in ['s', 'sim', 'y', 'yes']:
                    return None, None
                continue
            
            return "arquivo", arquivo
            
        elif escolha == "2":
            pasta = input("Digite o caminho da pasta (ou Enter para pasta atual): ").strip()
            if not pasta:
                pasta = "."
            
            if not os.path.exists(pasta):
                print(f"Pasta '{pasta}' não encontrada!")
                continuar = input("Deseja tentar novamente? (s/n): ").strip().lower()
                if continuar not in ['s', 'sim', 'y', 'yes']:
                    return None, None
                continue
            
            if not os.path.isdir(pasta):
                print(f"'{pasta}' não é uma pasta válida!")
                continuar = input("Deseja tentar novamente? (s/n): ").strip().lower()
                if continuar not in ['s', 'sim', 'y', 'yes']:
                    return None, None
                continue
            
            return "pasta", pasta
            
        else:
            print("Opção inválida! Digite 1 ou 2.")

if __name__ == "__main__":
    # Verifica se foi passado argumento via linha de comando
    if len(sys.argv) > 1:
        caminho_da_imagem_qr = sys.argv[1]
        
        if os.path.isfile(caminho_da_imagem_qr):
            print(f"Processando arquivo via linha de comando: {caminho_da_imagem_qr}")
            link_encontrado = ler_qr_code_com_testes(caminho_da_imagem_qr)
            
            if link_encontrado:
                print(f"\nLink final decodificado: {link_encontrado}")
            else:
                print("\nNão foi possível obter o link do QR Code.")
        
        elif os.path.isdir(caminho_da_imagem_qr):
            print(f"Processando pasta via linha de comando: {caminho_da_imagem_qr}")
            processar_pasta_completa(caminho_da_imagem_qr)
        
        else:
            print(f"Erro: '{caminho_da_imagem_qr}' não é um arquivo ou pasta válida.")
    
    else:
        tipo, caminho = obter_entrada_usuario()
        
        if tipo is None:
            print("Operação cancelada pelo usuário.")
            sys.exit(0)
        
        if tipo == "arquivo":
            print(f"\nProcessando arquivo: {caminho}")
            link_encontrado = ler_qr_code_com_testes(caminho)
            
            if link_encontrado:
                print(f"\nLink final decodificado: {link_encontrado}")
            else:
                print("\nNão foi possível obter o link do QR Code.")
        
        elif tipo == "pasta":
            print(f"\nProcessando pasta: {caminho}")
            processar_pasta_completa(caminho)