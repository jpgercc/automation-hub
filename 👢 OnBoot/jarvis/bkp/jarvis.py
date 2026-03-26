
import asyncio # Para programação assíncrona usado com edge_tts e aiohttp
import edge_tts # Para conversão de texto em fala
import aiohttp # Para requisições HTTP assíncronas
import os # Nativo, para manipulação de arquivos
import subprocess # Nativo, para executar comandos do sistema
import logging # Nativo, para logging
import webbrowser # Nativo, para abrir URLs no navegador padrão
from datetime import datetime # Nativo, para manipulação de datas e horas

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constantes
SALES_URL = 'https://myaccount.mercadolivre.com.br/sales/list#menu-user'
PRODUCTS_URL = 'https://docs.google.com/spreadsheets/d/1zX_Om3d14lmBNgtKrjJCE3ElGSzfOph8FzwEZ8LmcWc/edit?usp=sharing'
TEMP_MP3 = 'temp_audio.mp3'
CITY = 'Porto Alegre'
WEATHER_URL = f'https://wttr.in/{CITY}?format=%C+%t'

async def abre_vendas():
    try:
        logging.info("Abrindo o navegador...")
        webbrowser.open(SALES_URL)
        webbrowser.open(PRODUCTS_URL)
        logging.info("Navegador aberto e páginas acessadas.")
    except Exception as e:
        logging.error(f"Erro ao abrir o navegador: {e}")
# OPÇÕES DE VOZ:
# "en-US-GuyNeural" - Voz masculina, clara e natural.
# "en-US-JennyNeural" - Voz feminina, clara e natural.
# "en-GB-RyanNeural" - Voz masculina com sotaque britânico.
# "en-GB-SoniaNeural" - Voz feminina com sotaque britânico.
# "en-AU-NatashaNeural" - Voz feminina com sotaque australiano
# "en-AU-WilliamNeural" - Voz masculina com sotaque australiano

# "en-IN-NeerjaNeural" - Voz feminina com sotaque indiano
# "en-IN-PrabhatNeural" - Voz masculina com sotaque indiano

# "pt-BR-AntonioNeural" - Voz masculina em português do Brasil
# "pt-BR-FranciscaNeural" - Voz feminina em português do Brasil

# "es-ES-AlvaroNeural" - Voz masculina em espanhol da Espanha
# "es-ES-ElviraNeural" - Voz feminina em espanhol da Espanha
# "es-MX-DaliaNeural" - Voz feminina em espanhol do México
# "es-MX-JorgeNeural" - Voz masculina em espanhol do México
# "fr-FR-DeniseNeural" - Voz feminina em francês da França
# "fr-FR-HenriNeural" - Voz masculina em francês da França
# "de-DE-ConradNeural" - Voz masculina em alemão da Alemanha
# "de-DE-KatjaNeural" - Voz feminina em alemão da Alemanha
# "it-IT-ElsaNeural" - Voz feminina em italiano da Itália
# "it-IT-GiorgioNeural" - Voz masculina em italiano da Itália

# "ja-JP-NanamiNeural" - Voz feminina em japonês do Japão
# "ja-JP-KeitaNeural" - Voz masculina em japonês do Japão

# "zh-CN-XiaoxiaoNeural" - Voz feminina em chinês mandarim da China
# "zh-CN-YunxiNeural" - Voz masculina em chinês mandarim da China

# "ru-RU-DariyaNeural" - Voz feminina em russo da Rússia
# "ru-RU-EgorNeural" - Voz masculina em russo da Rússia


async def speak(text, voice="en-IN-PrabhatNeural"):
    try:
        logging.info("Gerando áudio...")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(TEMP_MP3)

        logging.info("Reproduzindo áudio...")
        # Reproduz diretamente o MP3 sem conversão
        await asyncio.to_thread(subprocess.run, ["ffplay", "-nodisp", "-autoexit", TEMP_MP3], check=True)
    except Exception as e:
        logging.error(f"Erro ao processar áudio: {e}")
    finally:
        for file in [TEMP_MP3]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    logging.info(f"Arquivo temporário {file} removido.")
                except OSError as e:
                    logging.error(f"Erro ao remover arquivo temporário {file}: {e}")

async def get_weather():
    try:
        logging.info("Obtendo informações do clima...")
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_URL) as response:
                if response.status == 200:
                    weather = await response.text()
                    logging.info("Informações do clima obtidas com sucesso.")
                    return weather
                else:
                    logging.warning("Não foi possível obter o clima no momento.")
                    return "Não foi possível obter o clima no momento."
    except aiohttp.ClientError as e:
        logging.error(f"Erro de conexão ao tentar obter o clima: {e}")
        return "Erro de conexão ao tentar obter o clima."

def get_greeting():
    now = datetime.now()
    hour = now.hour

    if hour < 5:
        return "Welcome... early bird.."
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

async def main():
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%d/%m/%Y")


        if now.weekday() == 5:
            await speak("It's Saturday, take it easy today!")
            return
        elif now.hour < 5:
            await speak("It's quite late, maybe you should rest... Have a good night!")
            return

        weather_info = await get_weather()
        greeting = get_greeting()

        text_to_speak = (
            f"{greeting} John, I hope you're having a great day... "
            f"Today is {current_date}. It is {current_time}. "
            f"The weather is {weather_info}... "
            f"I'll now open your sales pages on your browser to kickstart your day."
        )
        # Reproduz o áudio e aguarda sua conclusão antes de abrir vendas
        await speak(text_to_speak)

        # Garante que abre_vendas seja executado após o áudio
        await abre_vendas()

        # Fala texto final após abrir vendas
        await speak("There you go, have a productive day!")
    except Exception as e:
        logging.error(f"Erro na execução do programa: {e}")

if __name__ == "__main__":
    asyncio.run(main())