import asciichartpy
import requests
import pygame
from pathlib import Path
import sys


class CryptoTracker:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    # 🎯 CONFIGURAÇÃO PRINCIPAL - MUDE AQUI PARA TROCAR DE CRIPTO
    CRYPTO_ID = "bitcoin"           # ethereum, cardano, solana, binancecoin, ripple, etc. (exitente na coingecko)
    CRYPTO_SYMBOL = "BTC"           # ETH, ADA, SOL, BNB, XRP, etc. (exitente na coingecko)

    # Preço de referência e data (para comparação)
    REFERENCE_PRICE = 106913       # Preço de referência para comparação (preço da venda)
    REFERENCE_DATE = "junho"        # Data de referência
    
    # Configurações de alerta de áudio
    AUDIO_ALERT_RULES = [
        {"threshold": 100000, "condition": ">", "file": "high_alert.mp3", "loops": 2},
        {"threshold": 105000, "condition": "<", "file": "low_alert.mp3", "loops": 0},
        # Adicione mais regras conforme necessário
    ]

    def __init__(self, audio_dir=None):
        self.audio_dir = Path(audio_dir) if audio_dir else None
        self._setup_encoding()

    def _setup_encoding(self):
        try:
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8')
        except (AttributeError, Exception):
            pass

    def get_current_price(self):
        url = f"{self.BASE_URL}/simple/price?ids={self.CRYPTO_ID}&vs_currencies=usd"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            price = response.json()[self.CRYPTO_ID]['usd']
            return float(price)
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f"Erro ao obter preço atual de {self.CRYPTO_SYMBOL}: {e}")
            return None

    def get_historical_data(self, days=30):
        url = f"{self.BASE_URL}/coins/{self.CRYPTO_ID}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [price[1] for price in data['prices']]
        except (requests.RequestException, KeyError) as e:
            print(f"Erro ao obter dados históricos de {self.CRYPTO_SYMBOL}: {e}")
            return []

    def format_price(self, price):
        # Formata preço baseado no valor
        if price < 1:
            return f"${price:.6f}"
        elif price < 100:
            return f"${price:.2f}"
        else:
            return f"${price:,.2f}"

    def display_price_info(self, current_price):
        print("\n" * 18)  # Limpa a tela
        print(f"{self.CRYPTO_SYMBOL} em {self.REFERENCE_DATE}: {self.format_price(self.REFERENCE_PRICE)} USD (data da venda)\n")
        
        if current_price:
            print(f"Preço atual do {self.CRYPTO_SYMBOL}: {self.format_price(current_price)} USD")
            
            variation = ((current_price - self.REFERENCE_PRICE) / self.REFERENCE_PRICE) * 100
            status = "📈" if variation > 0 else "📉"
            print(f"Variação desde {self.REFERENCE_DATE}: {status} {variation:+.2f}%")
        else:
            print(f"Não foi possível obter o preço atual do {self.CRYPTO_SYMBOL}.")

    def display_chart(self, historical_data):
        if not historical_data:
            print("Não foi possível gerar o gráfico - dados indisponíveis.")
            return
        
        print(f"\nGráfico do {self.CRYPTO_SYMBOL} (últimos {len(historical_data)} dias):")
        try:
            chart = asciichartpy.plot(historical_data, {'height': 15})
            print(chart)
        except Exception as e:
            print(f"Erro ao gerar gráfico: {e}")

    def play_sound_alert(self, price):
        if not price or not self.audio_dir:
            return
        
        try:
            pygame.mixer.init()
            
            for rule in self.AUDIO_ALERT_RULES:
                threshold = rule["threshold"]
                condition = rule["condition"]
                audio_file_name = rule["file"]
                loops = rule["loops"]
                
                trigger = False
                if condition == ">" and price > threshold:
                    trigger = True
                elif condition == "<" and price < threshold:
                    trigger = True
                elif condition == "=" and abs(price - threshold) < 0.01:  # Para igualdade com tolerância
                    trigger = True

                if trigger:
                    audio_file = self.audio_dir / audio_file_name
                    if audio_file.exists():
                        pygame.mixer.music.load(str(audio_file))
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(loops)
                        
                        # Aguarda finalizar o som atual
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        return  # Toca o primeiro som que bate a condição e sai
                    else:
                        print(f"Arquivo de áudio não encontrado: {audio_file}")
                
        except pygame.error as e:
            print(f"Erro no áudio: {e}")
        finally:
            try:
                pygame.mixer.quit()
            except:
                pass
    
    def run(self):
        current_price = self.get_current_price()
        
        self.display_price_info(current_price)
        
        historical_data = self.get_historical_data(30)
        self.display_chart(historical_data)
        
        if current_price:
            self.play_sound_alert(current_price)


def main():
    # Configure o caminho para seus arquivos de áudio aqui (opcional)
    # audio_directory = r"C:\Users\x\Music"
    audio_directory = None
    
    tracker = CryptoTracker(audio_directory)
    tracker.run()


if __name__ == "__main__":
    main()
