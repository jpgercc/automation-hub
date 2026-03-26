import pywhatkit as kit
from datetime import datetime

# Numero de telefone no formato internacional 
telefone = "+xxxxxxxxxxxxxx"  # Substitua pelo número desejado
mensagem = "Olá, esta é uma mensagem programada!"

# Substitua pelo horario desejado
hora_envio = 10  
minuto_envio = 20 

# Obtem o horario atual
now = datetime.now()
hora_atual = now.hour
minuto_atual = now.minute

# Verificar se o horario é válido (minimo 1 minuto a frente do horario atual)
if hora_envio < hora_atual or (hora_envio == hora_atual and minuto_envio <= minuto_atual):
    print("Erro: O horário especificado deve ser no futuro!")
else:
    # Enviar a mensagem no horario programado
    kit.sendwhatmsg(telefone, mensagem, hora_envio, minuto_envio)
    print(f"Mensagem programada para {hora_envio:02d}:{minuto_envio:02d} com sucesso!")
