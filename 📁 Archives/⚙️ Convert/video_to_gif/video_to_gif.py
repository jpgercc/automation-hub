import os
from pathlib import Path
from moviepy import VideoFileClip, AudioFileClip
import matplotlib.pyplot as plt
import numpy as np

def mp4_para_gif(caminho_entrada, caminho_saida=None, fps=10, duracao_max=None, redimensionar=None):
    """
    Converte um arquivo MP4 para GIF.
    
    Args:
        caminho_entrada (str): Caminho para o arquivo MP4
        caminho_saida (str, optional): Caminho para salvar o GIF. Se None, usa o mesmo nome com .gif
        fps (int): Frames por segundo do GIF (padrão: 10)
        duracao_max (float, optional): Duração máxima em segundos (None para vídeo completo)
        redimensionar (tuple, optional): (largura, altura) para redimensionar (None para manter original)
    
    Returns:
        str: Caminho do GIF criado ou None se erro
    """
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(caminho_entrada):
            print(f"Erro: Arquivo '{caminho_entrada}' não encontrado.")
            return None
        
        # Define o caminho de saída se não foi fornecido
        if caminho_saida is None:
            caminho_entrada_path = Path(caminho_entrada)
            caminho_saida = str(caminho_entrada_path.parent / f"{caminho_entrada_path.stem}.gif")
        
        print(f"Carregando vídeo: {caminho_entrada}")
        
        # Carrega o vídeo
        video = VideoFileClip(caminho_entrada)
        
        # Aplica duração máxima se especificada
        if duracao_max and video.duration > duracao_max:
            video = video.subclip(0, duracao_max)
            print(f"Vídeo cortado para {duracao_max} segundos")
        
        # Redimensiona se especificado
        if redimensionar:
            video = video.resize(redimensionar)
            print(f"Vídeo redimensionado para {redimensionar}")
        
        print(f"Convertendo para GIF com {fps} fps...")
        
        # Converte para GIF
        video.write_gif(caminho_saida, fps=fps)
        
        # Fecha o clip para liberar recursos
        video.close()
        
        print(f"GIF criado com sucesso: '{caminho_saida}'")
        return caminho_saida
        
    except Exception as e:
        print(f"Erro ao converter MP4 para GIF: {e}")
        return None

def mp3_para_gif_waveform(caminho_entrada, caminho_saida=None, duracao_max=None, cor='blue'):
    """
    Converte um arquivo MP3 para GIF mostrando a forma de onda do áudio.
    
    Args:
        caminho_entrada (str): Caminho para o arquivo MP3
        caminho_saida (str, optional): Caminho para salvar o GIF. Se None, usa o mesmo nome com .gif
        duracao_max (float, optional): Duração máxima em segundos (None para áudio completo)
        cor (str): Cor da forma de onda
    
    Returns:
        str: Caminho do GIF criado ou None se erro
    """
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(caminho_entrada):
            print(f"Erro: Arquivo '{caminho_entrada}' não encontrado.")
            return None
        
        # Define o caminho de saída se não foi fornecido
        if caminho_saida is None:
            caminho_entrada_path = Path(caminho_entrada)
            caminho_saida = str(caminho_entrada_path.parent / f"{caminho_entrada_path.stem}_waveform.gif")
        
        print(f"Carregando áudio: {caminho_entrada}")
        
        # Carrega o áudio
        audio = AudioFileClip(caminho_entrada)
        
        # Aplica duração máxima se especificada
        if duracao_max and audio.duration > duracao_max:
            audio = audio.subclip(0, duracao_max)
            print(f"Áudio cortado para {duracao_max} segundos")
        
        # Obtém os dados do áudio
        audio_array = audio.to_soundarray(fps=22050)
        
        # Se for estéreo, converte para mono
        if len(audio_array.shape) > 1:
            audio_array = audio_array.mean(axis=1)
        
        # Cria frames para o GIF
        print("Criando frames da forma de onda...")
        frames = []
        fps_gif = 10
        samples_per_frame = len(audio_array) // (audio.duration * fps_gif)
        
        for i in range(int(audio.duration * fps_gif)):
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Calcula a janela de áudio para este frame
            start_sample = i * samples_per_frame
            end_sample = min(start_sample + samples_per_frame * 50, len(audio_array))  # Mostra 50 frames à frente
            
            # Plota a forma de onda
            time_axis = np.linspace(0, (end_sample - start_sample) / 22050, end_sample - start_sample)
            ax.plot(time_axis, audio_array[start_sample:end_sample], color=cor, linewidth=0.5)
            
            # Adiciona uma linha vertical para mostrar a posição atual
            current_time = i / fps_gif
            if current_time <= time_axis[-1] if len(time_axis) > 0 else False:
                ax.axvline(x=current_time, color='red', linestyle='--', linewidth=2)
            
            ax.set_ylim(-1, 1)
            ax.set_xlabel('Tempo (s)')
            ax.set_ylabel('Amplitude')
            ax.set_title(f'Forma de Onda do Áudio - {current_time:.1f}s')
            ax.grid(True, alpha=0.3)
            
            # Salva o frame como imagem temporária
            frame_path = f"temp_frame_{i:04d}.png"
            plt.savefig(frame_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            frames.append(frame_path)
        
        # Cria o GIF a partir dos frames
        print("Criando GIF...")
        from PIL import Image
        
        images = []
        for frame_path in frames:
            img = Image.open(frame_path)
            images.append(img)
        
        # Salva como GIF
        images[0].save(
            caminho_saida,
            save_all=True,
            append_images=images[1:],
            duration=100,  # 100ms entre frames = 10 fps
            loop=0
        )
        
        # Remove arquivos temporários
        for frame_path in frames:
            os.remove(frame_path)
        
        # Fecha o clip para liberar recursos
        audio.close()
        
        print(f"GIF da forma de onda criado com sucesso: '{caminho_saida}'")
        return caminho_saida
        
    except Exception as e:
        print(f"Erro ao converter MP3 para GIF: {e}")
        return None

def converter_para_gif(caminho_entrada, caminho_saida=None, **kwargs):
    """
    Converte automaticamente MP4 ou MP3 para GIF baseado na extensão do arquivo.
    
    Args:
        caminho_entrada (str): Caminho para o arquivo MP4 ou MP3
        caminho_saida (str, optional): Caminho para salvar o GIF
        **kwargs: Argumentos adicionais específicos para cada tipo de conversão
    
    Returns:
        str: Caminho do GIF criado ou None se erro
    """
    try:
        caminho_path = Path(caminho_entrada)
        extensao = caminho_path.suffix.lower()
        
        if extensao == '.mp4':
            print("Detectado arquivo MP4 - convertendo vídeo para GIF...")
            return mp4_para_gif(caminho_entrada, caminho_saida, **kwargs)
        elif extensao == '.mp3':
            print("Detectado arquivo MP3 - criando GIF da forma de onda...")
            return mp3_para_gif_waveform(caminho_entrada, caminho_saida, **kwargs)
        else:
            print(f"Erro: Formato '{extensao}' não suportado. Use .mp4 ou .mp3")
            return None
            
    except Exception as e:
        print(f"Erro na conversão: {e}")
        return None

def converter_pasta_para_gif(caminho_pasta, pasta_saida=None):
    """
    Converte todos os arquivos MP4 e MP3 de uma pasta para GIF.
    
    Args:
        caminho_pasta (str): Caminho da pasta com os arquivos
        pasta_saida (str, optional): Pasta onde salvar os GIFs. Se None, cria uma pasta 'gifs'
    
    Returns:
        list: Lista dos caminhos dos GIFs criados
    """
    try:
        pasta_entrada = Path(caminho_pasta)
        if not pasta_entrada.exists():
            print(f"Erro: Pasta '{caminho_pasta}' não existe.")
            return []
        
        # Define pasta de saída
        if pasta_saida is None:
            pasta_saida = pasta_entrada / "gifs"
        else:
            pasta_saida = Path(pasta_saida)
        
        # Cria a pasta de saída se não existir
        pasta_saida.mkdir(exist_ok=True)
        
        # Extensões suportadas
        extensoes_suportadas = {'.mp4', '.mp3'}
        
        gifs_criados = []
        
        # Processa todos os arquivos na pasta
        for arquivo in pasta_entrada.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in extensoes_suportadas:
                print(f"\nProcessando: {arquivo.name}")
                caminho_saida_gif = pasta_saida / f"{arquivo.stem}.gif"
                resultado = converter_para_gif(str(arquivo), str(caminho_saida_gif))
                if resultado:
                    gifs_criados.append(resultado)
        
        print(f"\nProcessamento concluído! {len(gifs_criados)} GIFs criados.")
        print(f"GIFs salvos na pasta: '{pasta_saida}'")
        
        return gifs_criados
        
    except Exception as e:
        print(f"Erro ao processar a pasta '{caminho_pasta}': {e}")
        return []

def main():
    """Função principal para demonstrar o uso do script."""
    print("=== Conversor de MP4/MP3 para GIF ===\n")
    
    while True:
        print("Opções:")
        print("1. Converter um arquivo específico")
        print("2. Converter todos os arquivos de uma pasta")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            caminho_arquivo = input("Digite o caminho do arquivo MP4/MP3: ").strip()
            if os.path.exists(caminho_arquivo):
                # Opções avançadas para MP4
                if caminho_arquivo.lower().endswith('.mp4'):
                    try:
                        fps = int(input("FPS do GIF (padrão 10): ") or "10")
                        duracao = input("Duração máxima em segundos (Enter para completo): ").strip()
                        duracao = float(duracao) if duracao else None
                        
                        redim = input("Redimensionar? Digite 'largura,altura' ou Enter para manter original: ").strip()
                        redimensionar = None
                        if redim:
                            w, h = map(int, redim.split(','))
                            redimensionar = (w, h)
                        
                        converter_para_gif(caminho_arquivo, fps=fps, duracao_max=duracao, redimensionar=redimensionar)
                    except ValueError:
                        print("Valores inválidos, usando configurações padrão...")
                        converter_para_gif(caminho_arquivo)
                else:
                    # Opções para MP3
                    try:
                        duracao = input("Duração máxima em segundos (Enter para completo): ").strip()
                        duracao = float(duracao) if duracao else None
                        cor = input("Cor da forma de onda (padrão 'blue'): ").strip() or 'blue'
                        
                        converter_para_gif(caminho_arquivo, duracao_max=duracao, cor=cor)
                    except ValueError:
                        print("Valores inválidos, usando configurações padrão...")
                        converter_para_gif(caminho_arquivo)
            else:
                print("Arquivo não encontrado!")
        
        elif opcao == "2":
            caminho_pasta = input("Digite o caminho da pasta: ").strip()
            if os.path.exists(caminho_pasta):
                converter_pasta_para_gif(caminho_pasta)
            else:
                print("Pasta não encontrada!")
        
        elif opcao == "3":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
