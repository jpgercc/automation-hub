"""
Assistente Pessoal de Início de Dia
Fornece saudação, clima, eventos astronômicos e abre páginas de trabalho.
"""
import asyncio
import logging
from datetime import datetime
from typing import Tuple

from climate import ClimateService
from communication import VoiceService, BrowserService


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


class DailyAssistant:
    """Assistente pessoal para iniciar o dia."""
    
    def __init__(self, 
                 user_name: str = "John",
                 city: str = "Porto Alegre",
                 voice_key: str = "en-in-male"):
        """
        Inicializa o assistente.
        
        Args:
            user_name: Nome do usuário
            city: Cidade para informações climáticas
            voice_key: Voz a ser utilizada
        """
        self.user_name = user_name
        self.climate = ClimateService(city)
        self.voice = VoiceService(voice_key)
        self.browser = BrowserService()
        
    def get_greeting(self) -> str:
        """
        Retorna saudação apropriada baseada na hora do dia.
        
        Returns:
            Saudação adequada
        """
        hour = datetime.now().hour
        
        if hour < 5:
            return "Welcome... early bird"
        elif hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"
    
    def should_skip_routine(self) -> Tuple[bool, str]:
        """
        Verifica se a rotina deve ser pulada (final de semana ou madrugada).
        
        Returns:
            Tupla (deve_pular, mensagem)
        """
        now = datetime.now()
        
        # Sábado
        if now.weekday() == 6:
            return True, "It's Saturday, take it easy today!"
        
        # Madrugada (antes das 5h)
        if now.hour < 5:
            return True, "It's quite late, maybe you should rest... Have a good night!"
        
        return False, ""
    
    async def build_daily_message(self) -> str:
        """
        Constrói a mensagem completa do dia com todas as informações.
        
        Returns:
            Mensagem formatada
        """
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%A, %B %d, %Y")
        
        # Obter informações climáticas e astronômicas em paralelo
        weather_task = self.climate.get_weather()
        astro_task = self.climate.get_astronomical_events()
        
        weather_data, astro_events = await asyncio.gather(weather_task, astro_task)
        
        # Montar mensagem
        greeting = self.get_greeting()
        
        message = (
            f"{greeting} {self.user_name}, I hope you're having a great day. "
            f"Today is {current_date}. The time is {current_time}. "
        )
        
        # Adicionar informações climáticas
        weather_message = self.climate.format_weather_message(weather_data, astro_events)
        message += weather_message + " "
        
        message += "I'll now open your work pages to kickstart your day."
        
        return message
    
    async def run(self):
        """Executa a rotina completa do assistente."""
        try:
            logger.info("Iniciando assistente diário...")
            
            # Verificar se deve pular a rotina
            should_skip, skip_message = self.should_skip_routine()
            if should_skip:
                logger.info(f"Rotina pulada: {skip_message}")
                await self.voice.speak(skip_message)
                return
            
            # Construir e falar mensagem principal
            daily_message = await self.build_daily_message()
            await self.voice.speak(daily_message)
            
            # Abrir páginas de trabalho
            await self.browser.open_work_pages()
            
            # Mensagem final
            await self.voice.speak("There you go, have a productive day!")
            
            logger.info("Rotina concluída com sucesso")
            
        except KeyboardInterrupt:
            logger.info("Rotina interrompida pelo usuário")
        except Exception as e:
            logger.error(f"Erro na execução da rotina: {e}", exc_info=True)
            await self.voice.speak("Sorry, I encountered an error. Please check the logs.")


async def main():
    """Função principal."""
    # Configurações personalizáveis
    assistant = DailyAssistant(
        user_name="John",
        city="Porto Alegre",
        voice_key="en-in-male"  # Altere para sua preferência
    )
    
    await assistant.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Programa encerrado pelo usuário")
