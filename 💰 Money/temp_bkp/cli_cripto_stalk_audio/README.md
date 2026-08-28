# Crypto Price Tracker 📈

Script Python simples para monitorar o preço de qualquer criptomoeda em tempo real com gráfico ASCII e alertas sonoros.

## Funcionalidades

- 💰 Preço atual de qualquer cripto em USD
- 📊 Gráfico ASCII dos últimos 30 dias
- 📈 Cálculo de variação percentual desde preço de referência
- 🔊 Alertas sonoros configuráveis (opcional)
- 🎯 Fácil configuração - apenas 4 variáveis para trocar de moeda

## Instalação

```bash
pip install requests asciichartpy pygame
```

## Configuração Rápida

Para trocar de criptomoeda, edite apenas estas 4 linhas no código:

```python
CRYPTO_ID = "bitcoin"           # ethereum, cardano, solana, etc.
CRYPTO_SYMBOL = "BTC"           # ETH, ADA, SOL, etc.
REFERENCE_PRICE = 106971        # Preço de referência
REFERENCE_DATE = "junho"        # Data de referência
```

### Exemplos de Configuração:

**Ethereum:**
```python
CRYPTO_ID = "ethereum"
CRYPTO_SYMBOL = "ETH"
REFERENCE_PRICE = 3500
REFERENCE_DATE = "junho"
```

**Solana:**
```python
CRYPTO_ID = "solana"
CRYPTO_SYMBOL = "SOL"
REFERENCE_PRICE = 150
REFERENCE_DATE = "junho"
```

**Cardano:**
```python
CRYPTO_ID = "cardano"
CRYPTO_SYMBOL = "ADA"
REFERENCE_PRICE = 0.45
REFERENCE_DATE = "junho"
```

## Uso

```bash
python crypto_tracker.py
```

## Configuração de Áudio (Opcional)

Para habilitar alertas sonoros, configure o caminho dos áudios:

```python
# Na função main(), edite:
audio_directory = r"C:\caminho\para\seus\audios"
```

### Sistema de Alertas Configurável:

```python
AUDIO_ALERT_RULES = [
    {"threshold": 100000, "condition": ">", "file": "high_alert.mp3", "loops": 2},
    {"threshold": 105000, "condition": "<", "file": "low_alert.mp3", "loops": 0},
    # Adicione mais regras conforme necessário
]
```

**Condições suportadas:**
- `">"` - Maior que o threshold
- `"<"` - Menor que o threshold  
- `"="` - Igual ao threshold (com tolerância)

## Exemplo de Saída

```
BTC em junho: $106,971.00 USD

Preço atual do BTC: $98,450.00 USD
Variação desde junho: 📉 -7.96%

Gráfico do BTC (últimos 30 dias):
    98,450.00 ┤        ╭─╮
    95,230.00 ┤    ╭───╯ ╰╮
    92,010.00 ┤  ╭─╯      ╰─╮
    88,790.00 ┼──╯          ╰───
```

## Criptomoedas Suportadas

Qualquer criptomoeda da [CoinGecko API](https://www.coingecko.com/en/api). Exemplos de IDs populares:

- `bitcoin` - Bitcoin
- `ethereum` - Ethereum
- `cardano` - Cardano
- `solana` - Solana
- `binancecoin` - BNB
- `ripple` - XRP
- `polkadot` - Polkadot
- `chainlink` - Chainlink
- `litecoin` - Litecoin
- `dogecoin` - Dogecoin

## API Utilizada

[CoinGecko API](https://www.coingecko.com/en/api) - Gratuita, sem necessidade de chave

## Requisitos

- Python 3.6+
- Conexão com internet
- Terminal com suporte UTF-8 (recomendado)

## Recursos Extras

- ✅ Formatação automática de preços (adapta para moedas baratas)
- ✅ Tratamento de erros robusto
- ✅ Limpeza automática da tela
- ✅ Suporte a qualquer moeda da CoinGecko
- ✅ Sistema de alertas flexível