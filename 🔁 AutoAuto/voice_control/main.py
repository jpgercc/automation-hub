from app import record_audio, transcribe_audio, check_trigger_phrase
import os
import subprocess

def main():
    temp_dir = 'temp'
    audio_file = os.path.join(temp_dir, "microfone_audio.wav")
    # Garante que a pasta temp existe
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    # Depuração: mostra o caminho do arquivo de áudio
    print(f"Arquivo de áudio será salvo em: {audio_file}")

    # Dicionário de frases acionadoras e scripts correspondentes
    # Adicione quantas frases/scripts quiser
    trigger_scripts = {
        "executar a tarefas": "C:\\Users\\user\\py_scripts\\apps\\tarefas\\start_server.bat",
        "executar tarefas": "C:\\Users\\user\\py_scripts\\apps\\tarefas\\start_server.bat",
        "iniciar tarefas": "C:\\Users\\user\\py_scripts\\apps\\tarefas\\start_server.bat",
        "iniciar a tarefas": "C:\\Users\\user\\py_scripts\\apps\\tarefas\\start_server.bat",
        "rodar tarefas": "C:\\Users\\user\\py_scripts\\apps\\tarefas\\start_server.bat",
        "tarefas": "C:\\Users\\user\\py_scripts\\apps\\tarefas\\start_server.bat",
        "por favor, execute a automação": "auomatizacao.py",
        # Exemplo de outra frase/script:
        # "abrir relatório": "relatorio.py",
    }
    trigger_phrases = list(trigger_scripts.keys())

    # Grava o áudio
    recorded_file = record_audio(filename=audio_file)

    # Transcreve o áudio
    transcribed_text = transcribe_audio(recorded_file)

    # Verifica se a frase específica está na transcrição
    is_triggered, detected_phrase = check_trigger_phrase(transcribed_text, trigger_phrases)

    
    if is_triggered and detected_phrase in trigger_scripts:
        script_para_executar = trigger_scripts[detected_phrase]
        print(f"Frase '{detected_phrase}' detectada! Executando script '{script_para_executar}'...")
        if os.path.exists(script_para_executar):
            try:
                if script_para_executar.endswith('.bat'):
                    # Abre o .bat em outro terminal
                    subprocess.Popen(f'start "" "{script_para_executar}"', shell=True)
                else:
                    subprocess.run(["python", script_para_executar], check=True)
                print(f"Script '{script_para_executar}' executado com sucesso.")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar o script '{script_para_executar}': {e}")
            except FileNotFoundError:
                print(f"Interpretador Python não encontrado. Verifique sua instalação.")
        else:
            print(f"Script '{script_para_executar}' não encontrado.")
    else:
        print(f"Nenhuma das frases acionadoras foi detectada na transcrição.")
if __name__ == "__main__":
    main()
