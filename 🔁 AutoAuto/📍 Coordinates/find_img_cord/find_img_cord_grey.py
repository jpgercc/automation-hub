import cv2 # pip install opencv-python # OpenCV (Open Source Computer Vision Library) é uma biblioteca de visão computacional e aprendizado de máquina de código aberto.
import numpy as np # pip install numpy # Usamos numpy para converter a captura de tela para um formato que o OpenCV possa usar. E também para manipular as imagens.
import pyautogui as gui# pip install pyautogui

def captura_tela():
    # Captura a tela e salva arquivo no local de execução do script
    screenshot = gui.screenshot()
    # Converte a captura de tela para um formato que o OpenCV possa usar
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY) #IMREAD_GRAYSCALE
    return screenshot_gray

def busca_botao(imagem_botao, screenshot_gray, confianca=0.3):
    # Realiza a busca pela imagem do botão na captura de tela
    resultado = cv2.matchTemplate(screenshot_gray, imagem_botao, cv2.TM_CCOEFF_NORMED)
    # Encontra as coordenadas do melhor match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
    
    if max_val > confianca:
        return max_loc
    else:
        return None

# Função para clicar no botão
def clicar_botao(max_loc, imagem_botao, eixo_x_divisao=2, eixo_y_divisao=2):
    # Se o match for bom o suficiente (pode ajustar o valor de confiança(é a probabilidade de encontrar o botão na tela))
#quanto mais próximo de 1, mais confiante o algoritmo estará de que encontrou o botão
    if max_loc:
        botao_x = max_loc[0] + imagem_botao.shape[1] // eixo_x_divisao
        botao_y = max_loc[1] + imagem_botao.shape[0] // eixo_y_divisao
        gui.click(botao_x, botao_y)
        print(f'Botão encontrado nas coordenadas: {max_loc}')
    else:
        print("Botão não encontrado na tela.")

# Função principal para processar o botão
def processar_botao(imagem_botao, confianca=0.3, eixo_x_divisao=2, eixo_y_divisao=2):
    screenshot_gray = captura_tela()
    max_loc = busca_botao(imagem_botao, screenshot_gray, confianca)
    clicar_botao(max_loc, imagem_botao, eixo_x_divisao, eixo_y_divisao)
