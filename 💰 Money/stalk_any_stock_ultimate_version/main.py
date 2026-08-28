import requests
import json
import datetime
import time
import os
import winsound
from urllib.parse import quote

class PriceAlertTracker:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.load_config()
        
    def load_config(self):
        # Carrega toda a configuracao do JSON
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.crypto_mapping = config.get("crypto_mapping", {})
            self.assets = config.get("assets", [])
            self.settings = config.get("settings", {})
            
            print(f"# Configuracao carregada: {len(self.assets)} ativos")
            print(f"# Mapeamento: {len(self.crypto_mapping)} criptomoedas")
            
        except FileNotFoundError:
            print(f"# ERRO: Arquivo {self.config_file} nao encontrado!")
            raise
        except json.JSONDecodeError as e:
            print(f"# ERRO no JSON: {e}")
            raise
    
    def get_crypto_price(self, symbol: str) -> tuple:
        # Obtem preco de criptomoeda - RETORNA (preco, moeda)
        try:
            coin_id = self.crypto_mapping.get(symbol.upper())
            if not coin_id:
                print(f"# {symbol} nao encontrado no mapeamento")
                return 0, "USD"
            
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd,brl"
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"# Erro HTTP {response.status_code} na API")
                return 0, "USD"
                
            data = response.json()
            
            # Verifica qual moeda esta disponivel (prioriza BRL se disponivel)
            if coin_id in data:
                price_data = data[coin_id]
                if "brl" in price_data:
                    price = price_data["brl"]
                    currency = "BRL"
                    print(f"   # Preco obtido: R${price:.2f}")
                    return price, currency
                elif "usd" in price_data:
                    price = price_data["usd"]
                    currency = "USD"
                    print(f"   # Preco obtido: ${price:.2f}")
                    return price, currency
            
            print(f"# Dados invalidos da API para {symbol}")
            return 0, "USD"
                
        except requests.exceptions.Timeout:
            print(f"# Timeout ao buscar {symbol}")
            return 0, "USD"
        except requests.exceptions.ConnectionError:
            print(f"# Erro de conexao ao buscar {symbol}")
            return 0, "USD"
        except Exception as e:
            print(f"# Erro inesperado com {symbol}: {e}")
            return 0, "USD"
    
    def get_stock_price(self, symbol: str) -> tuple:
        # Obtem preco de acao - RETORNA (preco, moeda)
        try:
            # Para acoes da B3, adicionamos .SA ao simbolo
            clean_symbol = symbol.strip().upper()
            if not clean_symbol.endswith('.SA'):
                clean_symbol += '.SA'
            
            # Yahoo Finance API
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{clean_symbol}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"# Erro HTTP {response.status_code} para {clean_symbol}")
                return 0, "BRL"  # Assume BRL para acoes da B3
            
            data = response.json()
            
            # Verifica se a estrutura de dados esta correta
            if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
                result = data["chart"]["result"][0]
                if "meta" in result and "regularMarketPrice" in result["meta"]:
                    price = result["meta"]["regularMarketPrice"]
                    currency = result["meta"].get("currency", "BRL")
                    
                    # Para acoes da B3, forcar BRL
                    if '.SA' in clean_symbol:
                        currency = "BRL"
                    
                    # Formata a exibicao baseado na moeda
                    if currency == "BRL":
                        print(f"   # Preco obtido: R${price:.2f}")
                    else:
                        print(f"   # Preco obtido: ${price:.2f} ({currency})")
                    
                    return price, currency
            
            print(f"# Estrutura de dados invalida para {clean_symbol}")
            return 0, "BRL"
            
        except requests.exceptions.Timeout:
            print(f"# Timeout ao buscar acao {symbol}")
            return 0, "BRL"
        except requests.exceptions.ConnectionError:
            print(f"# Erro de conexao ao buscar {symbol}")
            return 0, "BRL"
        except Exception as e:
            print(f"# Erro ao buscar acao {symbol}: {e}")
            return 0, "BRL"
    
    def play_alert_sound(self):
        # Toca alerta sonoro
        try:
            winsound.Beep(1000, 1000)
            time.sleep(0.3)
            winsound.Beep(1200, 800)
        except:
            print("# Alerta sonoro!")
    
    def check_alerts(self):
        # Verifica todos os ativos em busca de alertas
        print(f"\n# Verificando precos - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        alerts_triggered = []
        successful_checks = 0
        
        for asset in self.assets:
            print(f"\n# Verificando {asset['symbol']} ({asset['name']})...")
            
            current_price, currency = self.get_current_price(asset)
            
            if current_price > 0:
                successful_checks += 1
                self.print_asset_status(asset, current_price, currency)
                
                if current_price >= asset["alert_price"]:
                    alert_data = self.trigger_alert(asset, current_price, currency)
                    alerts_triggered.append(alert_data)
            else:
                print(f"   # Nao foi possivel obter preco para {asset['symbol']}")
        
        print(f"\n# Resumo: {successful_checks}/{len(self.assets)} ativos verificados")
        
        if alerts_triggered:
            self.save_alerts_to_log(alerts_triggered)
        
        return alerts_triggered
    
    def get_current_price(self, asset: dict) -> tuple:
        # Obtem preco atual baseado no tipo do ativo - RETORNA (preco, moeda)
        if asset["type"] == "crypto":
            return self.get_crypto_price(asset["symbol"])
        else:
            return self.get_stock_price(asset["symbol"])
    
    def print_asset_status(self, asset: dict, current_price: float, currency: str):
        # Mostra status do ativo com a moeda correta
        status = "# ALERTA ATINGIDO!" if current_price >= asset["alert_price"] else "# Aguardando..."
        print(f"   {status}")
        
        # Formata o preco baseado na moeda
        if currency == "BRL":
            print(f"   Preco atual: R${current_price:.2f}")
            print(f"   Alerta: R${asset['alert_price']:.2f}")
        else:
            print(f"   Preco atual: ${current_price:.2f} ({currency})")
            print(f"   Alerta: ${asset['alert_price']:.2f}")
        
        if current_price < asset["alert_price"]:
            difference = asset["alert_price"] - current_price
            percent_to_go = (difference / current_price) * 100
            
            if currency == "BRL":
                print(f"   Faltam R${difference:.2f} ({percent_to_go:.1f}%)")
            else:
                print(f"   Faltam ${difference:.2f} ({percent_to_go:.1f}%)")
        else:
            profit = current_price - asset["alert_price"]
            if currency == "BRL":
                print(f"   # Acima do alvo por R${profit:.2f}")
            else:
                print(f"   # Acima do alvo por ${profit:.2f}")
    
    def trigger_alert(self, asset: dict, current_price: float, currency: str) -> dict:
        # Dispara alerta para um ativo
        if currency == "BRL":
            alert_msg = f"# ALERTA! {asset['symbol']} atingiu R${current_price:.2f}"
        else:
            alert_msg = f"# ALERTA! {asset['symbol']} atingiu ${current_price:.2f} ({currency})"
        
        print(f"   # {alert_msg}")
        
        if self.settings.get("play_sound_alert", True):
            self.play_alert_sound()
        
        return {
            "symbol": asset["symbol"],
            "name": asset["name"],
            "type": asset["type"],
            "current_price": current_price,
            "currency": currency,
            "alert_price": asset["alert_price"],
            "timestamp": datetime.datetime.now().isoformat(),
            "buy_date": asset.get("buy_date", ""),
            "buy_price": asset.get("buy_price", 0)
        }
    
    def save_alerts_to_log(self, alerts: list):
        # Salva alertas no arquivo de log
        log_file = "alert_log.json"
        
        try:
            # Carrega alertas existentes
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    existing_alerts = json.load(f)
            else:
                existing_alerts = []
            
            # Adiciona apenas alertas novos do dia
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            new_alerts = 0
            
            for alert in alerts:
                alert_date = alert["timestamp"][:10]
                
                # Verifica se ja existe alerta igual hoje
                existing_today = any(
                    a["symbol"] == alert["symbol"] and a["timestamp"][:10] == alert_date
                    for a in existing_alerts
                )
                
                if not existing_today:
                    existing_alerts.append(alert)
                    new_alerts += 1
            
            # Salva arquivo atualizado
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(existing_alerts, f, indent=2, ensure_ascii=False)
            
            print(f"# {new_alerts} novo(s) alerta(s) salvos no log")
            
        except Exception as e:
            print(f"# Erro ao salvar log: {e}")
    
    def run_continuous_monitoring(self):
        # Executa monitoramento continuo
        print("\n# Iniciando monitoramento continuo...")
        print("# Pressione Ctrl+C para parar")
        
        try:
            while True:
                self.check_alerts()
                
                interval = self.settings.get("check_interval_minutes", 60)
                next_check = datetime.datetime.now() + datetime.timedelta(minutes=interval)
                print(f"\n# Proxima verificacao: {next_check.strftime('%H:%M')}")
                print("-" * 50)
                time.sleep(interval * 60)
                
        except KeyboardInterrupt:
            print("\n# Monitoramento parado pelo usuario")

def main():
    print("# SISTEMA DE ALERTAS DE PRECOS")
    print("=" * 40)
    
    tracker = PriceAlertTracker()
    
    # Verificacao unica
    alerts = tracker.check_alerts()
    
    if alerts:
        print(f"\n# {len(alerts)} ALERTA(S) DISPARADOS!")
    else:
        print(f"\n# Nenhum alerta disparado")
    
    # Monitoramento continuo
    response = input("\n# Iniciar monitoramento continuo? (s/n): ").strip().lower()
    if response in ['s', 'sim', 'y', 'yes']:
        tracker.run_continuous_monitoring()
    else:
        print("# Execucao unica concluida")

if __name__ == "__main__":
    main()