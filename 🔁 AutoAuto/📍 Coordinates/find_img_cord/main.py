import time
import cv2
from botao_finder import processar_botao

# Carrega a imagem do botão em escala cinza para o OpenCV
imagem_botao = cv2.imread('botao1.jpeg', cv2.IMREAD_GRAYSCALE)
imagem_botao_2 = cv2.imread('botao2.jpeg', cv2.IMREAD_GRAYSCALE)

# Os parametros devem ser ajustados conforme a necessidade, por botao
# Confiança é a probabilidade de encontrar o botão na tela
#quanto mais próximo de 1, mais confiante o algoritmo estará de que encontrou o botão
# A divisão dois eixos por 2 é para clicar no meio do botão, mas pode ser alterada conforme a necessidade
processar_botao(imagem_botao, confianca=0.3, eixo_x_divisao=2, eixo_y_divisao=2)

time.sleep(1)

processar_botao(imagem_botao_2, confianca=0.1, eixo_x_divisao=1.2, eixo_y_divisao=2)