"""
Módulo para obtenção de informações climáticas e astronômicas.
"""
import aiohttp
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ClimateService:
    """Serviço para obter informações meteorológicas e astronômicas."""
    
    def __init__(self, city: str = "Porto Alegre"):
        self.city = city
        self.base_weather_url = f"https://wttr.in/{city}"
        
    async def get_weather(self) -> Dict[str, str]:
        """
        Obtém informações meteorológicas detalhadas.
        
        Returns:
            Dict contendo temperatura, condição e visibilidade do céu
        """
        try:
            logger.info(f"Obtendo clima para {self.city}...")
            
            async with aiohttp.ClientSession() as session:
                # Temperatura e condição
                weather_url = f"{self.base_weather_url}?format=%C+%t"
                async with session.get(weather_url) as response:
                    if response.status == 200:
                        weather_text = await response.text()
                        weather_text = weather_text.strip()
                    else:
                        weather_text = "information unavailable"
                
                # Visibilidade do céu (cloud cover percentage)
                cloud_url = f"{self.base_weather_url}?format=%c"
                async with session.get(cloud_url) as response:
                    if response.status == 200:
                        cloud_cover = await response.text()
                        cloud_cover = cloud_cover.strip()
                        # Calcular visibilidade aproximada (inverso da cobertura de nuvens)
                        sky_visibility = self._calculate_sky_visibility(cloud_cover)
                    else:
                        sky_visibility = "unknown"
                
                logger.info("Informações climáticas obtidas com sucesso")
                
                return {
                    "condition": weather_text,
                    "sky_visibility": sky_visibility,
                    "raw_cloud": cloud_cover
                }
                
        except aiohttp.ClientError as e:
            logger.error(f"Erro de conexão ao obter clima: {e}")
            return {
                "condition": "unavailable due to connection error",
                "sky_visibility": "unknown",
                "raw_cloud": ""
            }
        except Exception as e:
            logger.error(f"Erro inesperado ao obter clima: {e}")
            return {
                "condition": "unavailable",
                "sky_visibility": "unknown",
                "raw_cloud": ""
            }
    
    def _calculate_sky_visibility(self, cloud_icon: str) -> str:
        """
        Calcula a visibilidade do céu baseado no ícone de nuvens.
        
        Args:
            cloud_icon: Ícone unicode retornado pelo wttr.in
            
        Returns:
            Descrição da visibilidade em percentual aproximado
        """
        # Mapeamento de ícones para visibilidade aproximada
        visibility_map = {
            "☀️": "excellent, around 90-100% clear",
            "🌤️": "good, around 70-80% clear",
            "⛅": "moderate, around 50-60% clear",
            "🌥️": "fair, around 30-40% clear",
            "☁️": "poor, around 10-20% clear",
            "🌧️": "very poor, mostly clouded",
            "⛈️": "very poor, storm conditions",
            "🌨️": "very poor, snow conditions"
        }
        
        return visibility_map.get(cloud_icon.strip(), "moderate visibility")
    
    async def get_astronomical_events(self) -> Optional[str]:
        """
        Verifica se há eventos astronômicos notáveis hoje.
        
        Returns:
            Descrição do evento ou None se não houver
        """
        try:
            logger.info("Verificando eventos astronômicos...")
            
            async with aiohttp.ClientSession() as session:
                # Obter fase da lua e horários astronômicos
                moon_url = f"{self.base_weather_url}?format=%m"
                sunrise_url = f"{self.base_weather_url}?format=%S"
                sunset_url = f"{self.base_weather_url}?format=%s"
                
                moon_phase = ""
                sunrise = ""
                sunset = ""
                
                async with session.get(moon_url) as response:
                    if response.status == 200:
                        moon_phase = (await response.text()).strip()
                
                async with session.get(sunrise_url) as response:
                    if response.status == 200:
                        sunrise = (await response.text()).strip()
                
                async with session.get(sunset_url) as response:
                    if response.status == 200:
                        sunset = (await response.text()).strip()
                
                # Montar mensagem sobre eventos notáveis
                events = []
                
                if moon_phase:
                    events.append(f"Moon phase: {moon_phase}")
                
                if sunrise and sunset:
                    events.append(f"Sunrise at {sunrise}, sunset at {sunset}")
                
                # Verificar se é lua cheia ou nova (eventos mais notáveis)
                if "🌕" in moon_phase or "Full" in moon_phase:
                    events.append("Tonight features a full moon!")
                elif "🌑" in moon_phase or "New" in moon_phase:
                    events.append("It's a new moon tonight, perfect for stargazing!")
                
                if events:
                    logger.info(f"Eventos astronômicos encontrados: {len(events)}")
                    return " | ".join(events)
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Erro ao obter eventos astronômicos: {e}")
            return None
    
    def format_weather_message(self, weather_data: Dict[str, str], 
                              astro_events: Optional[str] = None) -> str:
        """
        Formata a mensagem sobre o clima para narração.
        
        Args:
            weather_data: Dados meteorológicos
            astro_events: Eventos astronômicos (opcional)
            
        Returns:
            Mensagem formatada para fala
        """
        message = f"The weather is {weather_data['condition']}. "
        message += f"Sky visibility is {weather_data['sky_visibility']}."
        
        if astro_events:
            message += f" By the way, {astro_events}"
        
        return message
