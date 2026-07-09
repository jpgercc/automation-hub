import os
import platform
from pathlib import Path
from typing import Dict, Any, Final
import yt_dlp

CONFIG_FORMATOS: Final[Dict[str, Dict[str, Any]]] = {
    "1": {
        "tipo": "audio",
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    },
    "2": {
        "tipo": "video",
        "format": "bestvideo+bestaudio/best",
    },
}


class DiretorioDestinoErro(Exception):
    pass


class GerenciadorDiretorio:
    def __init__(self, sistema_operacional: str, pasta_home: Path) -> None:
        self._sistema = sistema_operacional.lower()
        self._home = pasta_home

    def obter_caminho_absoluto(self, tipo_midia: str) -> Path:
        if "windows" in self._sistema:
            pastas = {"audio": self._home / "Music", "video": self._home / "Videos"}
        else:
            pastas = {"audio": self._home / "Músicas", "video": self._home / "Vídeos"}

        pasta_final = pastas.get(tipo_midia, self._home)
        
        try:
            pasta_final.mkdir(parents=True, exist_ok=True)
            if not os.access(pasta_final, os.W_OK):
                raise PermissionError()
        except (OSError, PermissionError) as erro:
            raise DiretorioDestinoErro(f"Sem permissao de escrita no diretorio: {pasta_final}") from erro

        return pasta_final


class GerenciadorDownload:
    def __init__(self, gerenciador_diretorio: GerenciadorDiretorio) -> None:
        self._gerenciador_diretorio = gerenciador_diretorio

    def processar(self, url: str, escolha: str) -> None:
        tipo_midia = CONFIG_FORMATOS[escolha]["tipo"]
        pasta_salvamento = self._gerenciador_diretorio.obter_caminho_absoluto(tipo_midia)

        ydl_opts = CONFIG_FORMATOS[escolha].copy()
        ydl_opts.pop("tipo", None)
        ydl_opts["outtmpl"] = str(pasta_salvamento / "%(title)s.%(ext)s")

        print("\n--------------------------------------------------")
        print(f"Tipo: {tipo_midia.upper()}")
        print(f"Destino: {pasta_salvamento}")
        print("--------------------------------------------------\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


class InterfaceUsuario:
    @staticmethod
    def validar_url(url: str) -> None:
        if not url:
            raise ValueError("A URL nao pode ser vazia.")
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL invalida. A URL deve iniciar com http:// ou https://")

    @staticmethod
    def obter_escolha() -> str:
        while True:
            escolha = input("Digite [1] para MP3 ou [2] para Vídeo: ").strip()
            if escolha in CONFIG_FORMATOS:
                return escolha
            print("Opcao invalida. Tente novamente.\n")

    @classmethod
    def executar(cls) -> None:
        try:
            print("===============================================\n")
            print("   === Gerenciador de Download de Midias ===\n")
            print("===============================================\n")
            print("MODO DE USO:\n")
            print("PLAYLIST (baixa tudo):\nhttps://youtu.be/siUEYNORlhM?list=RDsiUEYNORlhM\n")
            print("VÍDEO (baixa apenas ele):\nhttps://youtu.be/siUEYNORlhM\n")
            print("===============================================\n")

            url = input("Cole aqui sua URL: ").strip()
            cls.validar_url(url)  # <--- Validação imediata aqui

            escolha = cls.obter_escolha()
            
            fabricante_diretorio = GerenciadorDiretorio(platform.system(), Path.home())
            downloader = GerenciadorDownload(fabricante_diretorio)
            
            downloader.processar(url, escolha)
            print("\nProcesso concluido.")

        except KeyboardInterrupt:
            print("\n\nPrograma encerrado pelo usuario (Ctrl+C). Ate logo!")
        except yt_dlp.utils.DownloadError as erro:
            print(f"\nErro de Download (yt-dlp): {erro}")
        except (ValueError, DiretorioDestinoErro) as erro:
            print(f"\nErro de Validacao: {erro}")
        except Exception as erro:
            print(f"\nErro inesperado no sistema: {erro}")


if __name__ == "__main__":
    InterfaceUsuario.executar()