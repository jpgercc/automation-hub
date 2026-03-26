# Sistema de Alertas de Preços (Criptos e Ações B3)

Este projeto monitora preços de ativos (criptomoedas e ações da B3) e dispara alertas quando o preço atual atinge ou supera um preço-alvo definido. Ele suporta:
- Criptomoedas via API do CoinGecko (com BRL e USD)
- Ações da B3 via Yahoo Finance (forçando BRL)
- Registro de alertas do dia em arquivo JSON
- Alerta sonoro no Windows
- Execução única ou monitoramento contínuo


## Requisitos

- Windows 10/11 (o alerta sonoro usa `winsound` do Windows)
- Python 3.9+ instalado e disponível no PATH
- Acesso à internet

Dependências Python (constam em `requirements.txt`):
- requests

Observação: `winsound` é parte da biblioteca padrão do Python no Windows, não requer instalação extra.


## Instalação

1) Abra um terminal (Prompt de Comando) na pasta do projeto:
- Caminho do projeto: `c:\Users\jpger\Desktop\Win_Init`

2) (Opcional, recomendado) Crie e ative um ambiente virtual:
- python -m venv .venv
- .venv\Scripts\activate

3) Instale as dependências:
- pip install -r requirements.txt


## Arquivos principais

- main.py: script principal com a lógica de monitoramento/alertas
- config.json: configuração de ativos, mapeamento de cripto e parâmetros gerais
- alert_log.json: log de alertas gerados (criado/atualizado automaticamente)
- initial_prices.json: pode ser usado por você para armazenar preços iniciais (não é obrigatório)
- requirements.txt: dependências Python


## Configuração (config.json)

O arquivo `config.json` contém três blocos importantes:
- crypto_mapping: mapeia o símbolo que você usa (ex.: "BTC") para o id do CoinGecko (ex.: "bitcoin")
- assets: lista de ativos a monitorar
- settings: ajustes gerais

Exemplo de estrutura esperada:
{
  "crypto_mapping": {
    "BTC": "bitcoin",
    "ETH": "ethereum"
  },
  "assets": [
    {
      "symbol": "BTC",
      "name": "Bitcoin",
      "type": "crypto",
      "alert_price": 350000,
      "buy_date": "2024-01-10",
      "buy_price": 250000
    },
    {
      "symbol": "PETR4",
      "name": "Petrobras PN",
      "type": "stock",
      "alert_price": 40.0
    }
  ],
  "settings": {
    "play_sound_alert": true,
    "check_interval_minutes": 60
  }
}

Notas:
- type aceita "crypto" ou "stock".
- Para ações da B3, informe o símbolo sem o sufixo .SA (o sistema adiciona automaticamente). Ex.: PETR4, VALE3, ITUB4.
- alert_price deve estar na moeda do ativo: BRL para ações B3; para cripto o sistema tenta BRL (se CoinGecko retornar) e cai para USD se BRL não estiver disponível.
- play_sound_alert controla o beep de alerta.
- check_interval_minutes define o intervalo entre verificações no modo contínuo.


## Como funciona

- Para cada ativo em assets:
  - type=crypto: busca preço no CoinGecko, priorizando BRL; se indisponível, usa USD.
  - type=stock: busca preço no Yahoo Finance para SYMBOL.SA e força moeda BRL.
- Exibe status no console (aguardando/alvo atingido), diferença para o alvo e percentual.
- Quando o preço atual >= alert_price, dispara alerta:
  - Mostra mensagem no console
  - Emite som (se ativado)
  - Registra no arquivo alert_log.json apenas 1 vez por dia por ativo (evita duplicidade diária)


## Uso

Execução única (verifica uma vez e pergunta se deseja continuar):
- python main.py

Quando perguntado "Iniciar monitoramento continuo? (s/n):", responda:
- s para continuar monitorando a cada N minutos (settings.check_interval_minutes)
- n para encerrar após a verificação única

Monitoramento contínuo:
- Ao escolher "s", o programa repete o ciclo de verificação e aguarda o próximo intervalo, exibindo o horário da próxima checagem. Para parar, use Ctrl+C.


## Logs e persistência

- alert_log.json: o programa salva os alertas do dia. Se um ativo disparar novamente no mesmo dia, não será duplicado no log.
- Mensagens de status e erros aparecem no console.


## Solução de problemas

- Erro de JSON/arquivo não encontrado:
  - Verifique se `config.json` existe e contém JSON válido (aspas duplas, vírgulas corretas, etc.). O caminho esperado é o mesmo da pasta do script.

- Preço retornando 0 para cripto:
  - Confira se o símbolo em assets (ex.: BTC) está mapeado corretamente em crypto_mapping para um id válido do CoinGecko (ex.: bitcoin).
  - Verifique conexão com a internet e possíveis bloqueios de firewall.

- Preço retornando 0 para ações:
  - Confirme o símbolo (ex.: PETR4, VALE3). O sufixo .SA é adicionado automaticamente.
  - Verifique conexão e tente novamente mais tarde; a API do Yahoo pode falhar ocasionalmente.

- Alerta sonoro não toca:
  - O beep usa winsound.Beep do Windows. Se estiver em VM/ambiente sem áudio, uma mensagem "Alerta sonoro!" será mostrada no console.

- Intervalo de checagem:
  - Ajuste `settings.check_interval_minutes` no config.json para o valor desejado (inteiro, em minutos). O padrão observado no código é 60 minutos.


## Segurança e limites das APIs

- CoinGecko e Yahoo Finance possuem limites e políticas de uso. Chamadas excessivas podem resultar em bloqueios temporários. Ajuste o intervalo de checagem conforme necessário.


## Desenvolvimento

- Código principal em `main.py` dentro da raiz do projeto.
- Para modificar a lógica de busca/formatos, veja os métodos:
  - get_crypto_price, get_stock_price
  - check_alerts, print_asset_status, trigger_alert, save_alerts_to_log, run_continuous_monitoring


## Licença

Uso pessoal/educacional. Adapte conforme sua necessidade.
