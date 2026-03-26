import yt_dlp
import os

def baixar_e_melhorar_musica(link):
    # Caminho completo para a pasta Música no diretório do usuário
    pasta_destino = os.path.expanduser('~/Música')
    
    # Configurações para baixar apenas o áudio do vídeo
    opcoes = {
        'format': 'bestaudio/best',  # Melhor qualidade de áudio disponível
        'postprocessors': [
            {  # Converte o áudio para MP3 após o download
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # Qualidade máxima do MP3
            }
        ],
        'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),  # Nome do arquivo de saída com caminho completo
        'quiet': False,  # Exibe o progresso no terminal
        'noplaylist': True,  # Garante que apenas o vídeo especificado será baixado
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            print(f"Baixando música do link: {link}")
            ydl.download([link])
            print("Download concluído!")
            # Melhorias de áudio após o download
            nome_arquivo = f"{link.split('=')[1]}.mp3"  # Nome do arquivo baixado
            aplicar_melhorias(nome_arquivo)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def aplicar_melhorias(arquivo):
    try:
        # Aplicando melhorias no áudio (igualando volume, compressão e equalização)
        print(f"Aplicando melhorias no arquivo: {arquivo}")
        
        # Comando para melhorar qualidade no FFmpeg:
        # - Reduz o volume para evitar clipping
        # - Equaliza para dar mais clareza aos instrumentos de sopro e violão
        # - Aplica compressão dinâmica para suavizar os picos e reduzir tremores
        comando = f'ffmpeg -i "{arquivo}" ' \
                  '-af "volume=-3dB, ' \
                  'equalizer=f=500:width_type=h:width=200:g=5, ' \
                  'compand=attacks=0:decays=1:points=-90/-90|-50/-20|-20/-5|0/-5" ' \
                  f'output_{arquivo}'

        os.system(comando)
        print(f"Melhorias aplicadas com sucesso! Arquivo salvo como output_{arquivo}")
    except Exception as e:
        print(f"Ocorreu um erro ao aplicar melhorias: {e}")

if __name__ == "__main__":
    link = input("Digite o link do YouTube (apenas o vídeo desejado): ")
    baixar_e_melhorar_musica(link)
