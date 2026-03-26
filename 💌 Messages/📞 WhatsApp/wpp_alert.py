import pyautogui
import time

pyautogui.press('win')
pyautogui.typewrite('chrome')
pyautogui.press('enter')

# Aguardar o Chrome abrir
time.sleep(2)

pyautogui.hotkey('ctrl', 't')
pyautogui.typewrite('https://web.whatsapp.com/')
pyautogui.press('enter')

time.sleep(5)


pyautogui.click(x=299, y=283)

# Aguardar o chat abrir
time.sleep(2)


pyautogui.typewrite('MENSAGEM ENVIADA AUTOMATICAMENTE PRO PRIMEIRO CONTATO QUER O CÓDIGO ?PODE SER DE SUMA IMPORTANCIA')
pyautogui.press('enter')