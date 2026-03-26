import yt_dlp
import os

def baixar_musica(link):
    # Caminho para a pasta de Músicas do usuário
    pasta_musicas = os.path.join(os.path.expanduser("~"), "Music")
    os.makedirs(pasta_musicas, exist_ok=True)

    # Caminho onde você extraiu o ffmpeg
    caminho_ffmpeg = r'C:\ffmpeg\bin'  # <-- ajuste se estiver em outro local

    # Configurações do yt-dlp
    opcoes = {
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }
        ],
        'outtmpl': os.path.join(pasta_musicas, '%(title)s.%(ext)s'),
        'quiet': False,
        'noplaylist': False,  # <-- aqui muda para False para permitir playlists
        'ffmpeg_location': caminho_ffmpeg,  # <-- aqui adiciona o caminho do ffmpeg
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            print(f"Baixando música do link: {link}")
            ydl.download([link])
            print(f"Download concluído! Arquivo salvo em: {pasta_musicas}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    link = input("Digite o link do YouTube (apenas o vídeo desejado): ")
    baixar_musica(link)
