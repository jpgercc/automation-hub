import os
from bs4 import BeautifulSoup # Requer: pip install beautifulsoup4 (R$ 0,00)
enviei versaoaerrada cu
# ================= CONFIGURAÇÃO (Fácil Acesso) =================
TRECHO_ANTIGO = 'assets/css/styles.css'
TRECHO_NOVO   = '/assets/css/styles.css'

# Se quiser apenas arquivos específicos (mesmo em subpastas), coloque o nome: ['index.html']
# Para processar ABSOLUTAMENTE TUDO da imagem, deixe a lista vazia: []
ARQUIVOS_ESPECIFICOS = [] 
# ==============================================================

def processar_arquivo(caminho_completo):
    try:
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        alterado = False
        for tag in soup.find_all(['link', 'script', 'img', 'a']):
            for attr in ['href', 'src']:
                valor = tag.get(attr)
                
                if valor and valor.startswith(TRECHO_ANTIGO):
                    # Verifica se já não foi alterado para evitar erro de repetição
                    if not valor.startswith(TRECHO_NOVO):
                        tag[attr] = valor.replace(TRECHO_ANTIGO, TRECHO_NOVO, 1)
                        alterado = True

        if alterado:
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print(f"[OK] Alterado: {caminho_completo}")
            
    except Exception as e:
        print(f"[ERRO] Falha em {caminho_completo}: {e}")

def iniciar():
    # os.walk percorre todas as pastas e subpastas da imagem (recursividade)
    pasta_raiz = '.' 
    
    print(f"Varrendo diretórios a partir de: {os.path.abspath(pasta_raiz)}")

    for raiz, diretorios, arquivos in os.walk(pasta_raiz):
        # Ignora a pasta de backup (bkp) para não mexer no que está salvo
        if 'bkp' in diretorios:
            diretorios.remove('bkp')

        for arquivo in arquivos:
            if arquivo.endswith('.html'):
                # Se a lista estiver vazia OU o arquivo estiver na lista de específicos
                if not ARQUIVOS_ESPECIFICOS or arquivo in ARQUIVOS_ESPECIFICOS:
                    caminho_total = os.path.join(raiz, arquivo)
                    processar_arquivo(caminho_total)

if __name__ == "__main__":

    iniciar()
