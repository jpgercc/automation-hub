import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import keyboard
import subprocess
import os
import re # Importa a biblioteca de expressões regulares para limpeza de texto

def record_audio(samplerate=16000, filename="audio.wav"):

    # Se filename for um caminho absoluto ou relativo, usa como está
    audio_path = filename
    # Garante que a pasta do arquivo existe
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    audio_buffer = []

    def callback(indata, frames, time, status):
        """
        Callback usado pela lib sounddevice para capturar áudio do microfone.
        `indata` contém os dados de áudio capturados.
        `frames` é o número de quadros capturados.
        `time` é o tempo de captura.
        `status` contém informações sobre erros ou avisos.
        """
        if status:
            print(status)
        audio_buffer.append(indata.copy())

    print("Pressione 'Enter' para COMEÇAR a gravar.")
    keyboard.wait('enter')

    print("\nGRAVANDO... Pressione 'Enter' para parar.")
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16', callback=callback):
        keyboard.wait('enter')


    print("Gravação PARADA. Processando...")
    recorded_audio = np.concatenate(audio_buffer, axis=0)
    wavfile.write(audio_path, samplerate, recorded_audio)
    print(f"Arquivo '{audio_path}' salvo.")
    return audio_path

def transcribe_audio(audio_path, model_name="base", language="pt"):
    """
    Transcreve o áudio de um arquivo usando o modelo Whisper.
    Lista de modelos disponíveis em: https://huggingface.co/openai/whisper-base
    Lista de idiomas suportados: pt, en, es, fr, de, it, nl, ru, zh, ja, ko, etc.
    """
    print(f"Carregando modelo Whisper ({model_name})...")
    model = whisper.load_model(model_name)

    print("Transcrevendo áudio...")
    result = model.transcribe(audio_path, language=language)

    print("\n--- Transcrição ---")
    print(result["text"])
    print("-------------------")
    return result["text"]

def clean_text(text):
    """
    Limpa o texto removendo pontuações e convertendo para minúsculas
    para uma comparação mais flexível.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Remove tudo que não é letra, número ou espaço
    return text

def check_trigger_phrase(transcribed_text, trigger_phrases):
    """
    Verifica se alguma das frases acionadoras (ou suas variações)
    está presente no texto transcrito.
    A comparação é feita de forma redundante (case-insensitive e sem pontuação).
    """
    cleaned_transcribed_text = clean_text(transcribed_text)
    
    for phrase in trigger_phrases:
        cleaned_phrase = clean_text(phrase)
        if cleaned_phrase in cleaned_transcribed_text:
            return True, phrase # Retorna True e a frase que foi detectada
    return False, None # Retorna False se nenhuma frase for detectada
