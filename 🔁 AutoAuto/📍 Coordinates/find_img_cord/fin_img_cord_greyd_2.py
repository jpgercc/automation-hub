import cv2 # pip install opencv-python # OpenCV (Open Source Computer Vision Library) é uma biblioteca de visão computacional e aprendizado de máquina de código aberto.
import numpy as np # pip install numpy # Usamos numpy para converter a captura de tela para um formato que o OpenCV possa usar. E também para manipular as imagens.
import pyautogui as gui# pip install pyautogui
import time

time.sleep(1)

# Carrega a imagem do botão em escala cinza para o OpenCV
imagem_botao = cv2.imread('botao.jpeg', cv2.IMREAD_GRAYSCALE)

# Captura a tela e salva arquivo no local de execução do script
screenshot = gui.screenshot()

# Converte a captura de tela para um formato que o OpenCV possa usar
screenshot = np.array(screenshot)
screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

# Realiza a busca pela imagem do botão na captura de tela
resultado = cv2.matchTemplate(screenshot_gray, imagem_botao, cv2.TM_CCOEFF_NORMED)

# Encontra as coordenadas do melhor match
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

# Se o match for bom o suficiente (pode ajustar o valor de confiança(é a probabilidade de encontrar o botão na tela))
#quanto mais próximo de 1, mais confiante o algoritmo estará de que encontrou o botão
if max_val > 0.3:
    print(f'Botão encontrado nas coordenadas: {max_loc}')
    # Clica no centro do botão
    botao_x = max_loc[0] + imagem_botao.shape[1] // 2
    botao_y = max_loc[1] + imagem_botao.shape[0] // 2
    gui.click(botao_x, botao_y)
else:
    print("Botão não encontrado na tela.")


