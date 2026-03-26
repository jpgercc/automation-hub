import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = 'smtp.YOUREMAILPROVIDER.com'
smtp_port = 587  # Porta TLS comum para gmail
email_user = 'YOUREMAILADDRESS@PROVIDER.com'
email_password = 'YOUREMAILAPPPASSWORD' #gmail config --> senhas de aplicativo
email_destino = 'RECIPIENTEMAILADDRESS@PROVIDER.com'

def enviar_email(preco):
    subject = 'Alerta: Preço do Bitcoin'
    body = f'O preço do Bitcoin caiu para {preco} BRL, abaixo de 300 mil BRL!'
    
    # Cria email
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_destino
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password) 
            server.send_message(msg) 
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')

def verificar_preco_btc():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl'
    response = requests.get(url)
    data = response.json()
    preco_btc = data['bitcoin']['brl']
    return preco_btc

if __name__ == '__main__':
    preco_btc = verificar_preco_btc()
    print(f'Preço atual do Bitcoin: {preco_btc} BRL')
    
    if preco_btc > 300000:
        enviar_email(preco_btc)
    else:
        print('O preço do Bitcoin está acima de 300 mil BRL, nenhum e-mail será enviado.')