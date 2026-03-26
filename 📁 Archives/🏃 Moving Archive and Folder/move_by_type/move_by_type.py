import os
import shutil

source_folder = r'caminho_origem'
destination_folder = r'caminho_origem'

for filename in os.listdir(source_folder):
    
    if filename.endswith('.pdf'):
        
        source_file = os.path.join(source_folder, filename)
        
        destination_file = os.path.join(destination_folder, filename)
        # preservando os metadados
        shutil.copy2(source_file, destination_file)
        print(f'Arquivo {filename} copiado com sucesso!')

print('Todos os arquivos PDF foram copiados.')

#!!!THIS CODE WAS ONLY TESTED IN PDFs!!!

#SOBRE O COMANDO shutil.copy2

# POSIX Platforms (como Linux e macOS):
# Proprietário e Grupo: O dono e o grupo do arquivo não são preservados.
# ACLs (Access Control Lists): Regras de controle de acesso mais detalhadas também são perdidas.
# Mac OS:
# Resource Fork: A parte dos metadados que armazena dados adicionais (como ícones e outros atributos específicos do aplicativo) não é copiada.
# File Type e Creator Codes: Códigos específicos de tipo e criador do arquivo também não são preservados.
# Windows:
# Proprietários de Arquivos: A informação sobre o dono do arquivo não é preservada.
# ACLs: As listas de controle de acesso (ACLs), que definem permissões detalhadas, não são copiadas.
# Alternate Data Streams: Fluxos de dados alternativos associados aos arquivos também não são copiados.

