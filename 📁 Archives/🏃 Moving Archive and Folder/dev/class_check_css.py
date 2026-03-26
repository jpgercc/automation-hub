import os
import re

def extrair_classes_css(caminho_css):
    """
    Extrai classes válidas ignorando números decimais, unidades e pseudos.
    Regra: Classes CSS não podem começar com números (sem escape).
    """
    classes = set()
    if not os.path.exists(caminho_css):
        return classes

    # EXPLICAÇÃO DO REGEX:
    # \.                -> Procura o ponto inicial da classe
    # (?![0-9])         -> Lookahead negativo: GARANTE que o próximo caractere NÃO seja um número
    # ([a-zA-Z_-]       -> O primeiro caractere DEVE ser letra, underline ou hífen
    # [a-zA-Z0-9_-]*)   -> O restante pode conter números, letras, etc.
    padrao_valido = re.compile(r'\.(?![0-9])([a-zA-Z_-][a-zA-Z0-9_-]*)')

    with open(caminho_css, 'r', encoding='utf-8') as f:
        for linha in f:
            # Ignora linhas que parecem propriedades (ex: margin: 0.5rem)
            # Focamos em linhas que contenham chaves ou vírgulas (seletores)
            if '{' in linha or ',' in linha or linha.strip().startswith('.'):
                matches = padrao_valido.findall(linha)
                for m in matches:
                    classes.add(m)
    return classes

def classe_esta_no_html(classe, conteudos_html):
    """Verifica presença da classe estritamente dentro de atributos class/id."""
    # Busca a classe cercada por aspas e espaços, garantindo que seja um token inteiro
    padrao_html = re.compile(rf'class=[\'"][^"\']*?\b{classe}\b[^"\']*?[\'"]', re.IGNORECASE)
    
    for html in conteudos_html:
        if padrao_html.search(html):
            return True
    return False

def principal():
    CSS_FILE = 'styles.css'
    OUTPUT_FILE = 'classes_nao_usadas.txt'

    classes_extraidas = extrair_classes_css(CSS_FILE)
    
    if not classes_extraidas:
        print("Nenhuma classe válida encontrada ou arquivo CSS ausente.")
        return

    # Scan de HTMLs
    arquivos_html = [f for f in os.listdir('.') if f.endswith('.html')]
    conteudos_html = [open(f, 'r', encoding='utf-8').read() for f in arquivos_html]

    # Filtro de não usadas
    nao_usadas = sorted([
        c for c in classes_extraidas 
        if not classe_esta_no_html(c, conteudos_html)
    ])

    # Escrita do resultado
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(nao_usadas))

    print(f"Total de classes legítimas no CSS: {len(classes_extraidas)}")
    print(f"Classes inúteis encontradas: {len(nao_usadas)}")
    print(f"Lista limpa salva em: {OUTPUT_FILE}")

if __name__ == "__main__":
    principal()