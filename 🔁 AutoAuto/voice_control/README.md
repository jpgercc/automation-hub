# Transcreve Voice Trigger

Transcreve Voice Trigger é uma aplicação Python que permite acionar scripts automaticamente por comandos de voz. O programa grava o áudio do microfone, transcreve o que foi dito e executa scripts específicos quando frases pré-definidas são detectadas na transcrição.

## Funcionalidades
- Grava áudio do microfone e salva em arquivo `.wav`.
- Transcreve o áudio para texto.
- Detecta frases acionadoras na transcrição.
- Executa scripts ou arquivos batch automaticamente ao reconhecer frases específicas.

## Como usar
1. **Pré-requisitos:**
   - Python 3.11 ou superior.
   - Instale as dependências necessárias (veja abaixo).

2. **Configuração:**
   - Adicione ou edite as frases acionadoras e scripts correspondentes no dicionário `trigger_scripts` no arquivo `main.py`.

3. **Execução:**
   - Execute o programa principal:
     ```powershell
     python main.py
     ```
   - Siga as instruções no terminal e fale uma das frases acionadoras para executar o script desejado.

## Dependências
- Certifique-se de instalar as bibliotecas necessárias, por exemplo:
  ```powershell
  pip install sounddevice scipy SpeechRecognition
  ```
- O utilitário **ffmpeg** deve estar instalado e disponível no PATH do sistema operacional. Baixe em: https://ffmpeg.org/download.html
  - Para Windows: extraia o executável e adicione a pasta ao PATH do sistema.

## Estrutura do Projeto
```
app.py           # Funções principais de gravação e transcrição
main.py          # Script principal da aplicação
temp/            # Pasta para arquivos temporários de áudio
```

## Personalização
- Adicione novas frases e scripts no dicionário `trigger_scripts` em `main.py`.
- Para acionar scripts Python, use o caminho do arquivo `.py`.
- Para acionar scripts batch, use o caminho do arquivo `.bat`.

## Observações
- O reconhecimento de voz pode variar conforme o microfone e o ambiente.
- Scripts acionados devem existir no caminho especificado.
- O ffmpeg é obrigatório para funcionamento correto da gravação e transcrição de áudio.

---
