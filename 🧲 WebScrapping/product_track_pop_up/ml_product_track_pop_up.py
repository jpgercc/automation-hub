import smtplib
import schedule
import time
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import logging

# Configurar logging para registrar informações e erros
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def enviar_notificacao(mensagem):
    """Mostra uma notificação usando o tkinter."""
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    messagebox.showinfo("Notificação", mensagem)
    root.destroy()

def obter_preco(produto_url):
    """Obtém o preço do produto a partir da página web."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(produto_url, headers=headers, timeout=10)
        response.raise_for_status()  # Verifica erros HTTP

        soup = BeautifulSoup(response.text, 'html.parser')
        # Ajuste para o Mercado Livre
        preco_texto = soup.find('span', {'class': 'andes-money-amount__fraction'}).text
        preco = float(preco_texto.replace('R$', '').replace('.', '').replace(',', '.'))
        return preco

    except Exception as e:
        logging.error(f"Erro ao obter o preço: {e}")
        return None

def monitorar_preco(produto_url, preco_alvo, produto):
    """Verifica se o preço atual é menor ou igual ao preço alvo."""
    preco_atual = obter_preco(produto_url)

    if preco_atual is None:
        logging.warning("Não foi possível obter o preço.")
        return  # Sai da função se o preço não foi obtido

    if preco_atual <= preco_alvo:
        mensagem = (f"O produto '{produto}' caiu de preço!\n"
                    f"Preço atual: R${preco_atual:.2f}\n"
                    f"Preço alvo: R${preco_alvo:.2f}")
        enviar_notificacao(mensagem)
        logging.info("Notificação enviada.")
    else:
        logging.info(f"Preço atual: R${preco_atual:.2f}. Ainda acima do preço alvo.")

def configurar_monitoramento(produto_url, preco_alvo, produto, intervalo=0.1666667):
    """Configura a tarefa de monitoramento usando schedule."""
    schedule.every(intervalo).minutes.do(monitorar_preco, produto_url, preco_alvo, produto)
    logging.info(f"Monitorando o produto '{produto}' a cada {intervalo} minutos...")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # INFO DO PRODUTO
    produto_url = 'https://www.mercadolivre.com.br/terre-dhermes-parfum-75ml-para-masculino/p/MLB19056226#wid%3DMLB3393944509%26sid%3Dsearch%26searchVariation%3DMLB19056226%26position%3D5%26search_layout%3Dgrid%26type%3Dproduct%26tracking_id%3D17f39e5b-3d5b-44d2-aed6-8e51ee004b5b'
    preco_alvo = 1000.0
    produto = 'Terre d Hermes 200ml'

    # Monitoramento configurado para rodar a cada x minutos
    configurar_monitoramento(produto_url, preco_alvo, produto, intervalo=0.1666667)
