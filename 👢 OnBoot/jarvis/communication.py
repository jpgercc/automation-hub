"""
Módulo para comunicação via síntese de voz e abertura de páginas.
"""
import asyncio
import edge_tts
import subprocess
import webbrowser
import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class VoiceService:
    """Serviço para conversão de texto em fala."""
    
    # Vozes disponíveis por idioma/sotaque
    VOICES = {
        "en-us-male": "en-US-GuyNeural",
        "en-us-female": "en-US-JennyNeural",
        "en-gb-male": "en-GB-RyanNeural",
        "en-gb-female": "en-GB-SoniaNeural",
        "en-in-male": "en-IN-PrabhatNeural",
        "en-in-female": "en-IN-NeerjaNeural",
        "pt-br-male": "pt-BR-AntonioNeural",
        "pt-br-female": "pt-BR-FranciscaNeural",
    }
    
    def __init__(self, voice_key: str = "en-in-male", temp_dir: str = "/tmp"):
        """
        Inicializa o serviço de voz.
        
        Args:
            voice_key: Chave da voz desejada (veja VOICES)
            temp_dir: Diretório para arquivos temporários
        """
        self.voice = self.VOICES.get(voice_key, self.VOICES["en-in-male"])
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        self.temp_audio = self.temp_dir / "assistant_audio.mp3"
        
    async def speak(self, text: str, rate: str = "+0%") -> bool:
        """
        Converte texto em fala e reproduz o áudio.
        
        Args:
            text: Texto a ser falado
            rate: Taxa de velocidade da fala (ex: "+10%" mais rápido, "-10%" mais lento)
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            logger.info("Gerando áudio...")
            
            # Gerar áudio com edge-tts
            communicate = edge_tts.Communicate(text, self.voice, rate=rate)
            await communicate.save(str(self.temp_audio))
            
            logger.info("Reproduzindo áudio...")
            
            # Reproduzir usando ffplay com configurações otimizadas
            # -nodisp: não mostra janela de vídeo
            # -autoexit: fecha automaticamente ao terminar
            # -loglevel quiet: suprime logs do ffplay
            process = await asyncio.create_subprocess_exec(
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel", "quiet",
                str(self.temp_audio),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            
            await process.wait()
            
            logger.info("Áudio reproduzido com sucesso")
            return True
            
        except FileNotFoundError:
            logger.error("ffplay não encontrado. Instale ffmpeg: sudo apt install ffmpeg")
            return False
        except Exception as e:
            logger.error(f"Erro ao processar áudio: {e}")
            return False
        finally:
            self._cleanup_temp_files()
    
    def _cleanup_temp_files(self):
        """Remove arquivos temporários de áudio."""
        try:
            if self.temp_audio.exists():
                self.temp_audio.unlink()
                logger.debug(f"Arquivo temporário removido: {self.temp_audio}")
        except OSError as e:
            logger.warning(f"Não foi possível remover arquivo temporário: {e}")
    
    async def speak_multiple(self, texts: list[str], pause_seconds: float = 0.5) -> bool:
        """
        Fala múltiplas mensagens com pausa entre elas.
        
        Args:
            texts: Lista de textos para falar
            pause_seconds: Pausa entre as mensagens
            
        Returns:
            True se todas foram bem-sucedidas
        """
        success = True
        for text in texts:
            if not await self.speak(text):
                success = False
            if pause_seconds > 0:
                await asyncio.sleep(pause_seconds)
        return success


class BrowserService:
    """Serviço para abrir páginas no navegador."""
    
    def __init__(self, urls: Optional[dict] = None):
        """
        Inicializa o serviço de navegador.
        
        Args:
            urls: Dicionário com URLs a serem abertas
        """
        self.urls = urls or {
            "sales": "https://myaccount.mercadolivre.com.br/sales/list#menu-user",
            "products": "https://docs.google.com/spreadsheets/d/1zX_Om3d14lmBNgtKrjJCE3ElGSzfOph8FzwEZ8LmcWc/edit?usp=sharing"
        }
    
    async def open_work_pages(self) -> bool:
        """
        Abre as páginas de trabalho no navegador.
        
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            logger.info("Abrindo páginas de trabalho no navegador...")
            
            for name, url in self.urls.items():
                logger.debug(f"Abrindo {name}: {url}")
                # Executa em thread separada para não bloquear
                await asyncio.to_thread(webbrowser.open, url)
                # Pequena pausa entre aberturas para evitar sobrecarga
                await asyncio.sleep(0.3)
            
            logger.info(f"{len(self.urls)} página(s) aberta(s) com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao abrir navegador: {e}")
            return False
    
    def add_url(self, name: str, url: str):
        """Adiciona uma nova URL à lista."""
        self.urls[name] = url
    
    def remove_url(self, name: str):
        """Remove uma URL da lista."""
        self.urls.pop(name, None)
