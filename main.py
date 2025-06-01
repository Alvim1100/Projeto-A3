from lista import *
from ordenation import *

lista = Lista()
def criamenu():
    print(''' 
===== Sistema de Documentos Compressos com Índice Dinâmico =====
    
    1 - Cadastrar novo documento
    2 - Listar documentos cadastrados
    3 - Buscar por palavra-chave
    4 - Ver estatísticas e ordenações
    5 - Gerenciar compressão e índices
    0 - Sair
    
          
 ''')
    
def cadastradoc():
    nome_base = input("Digite o nome do documento: ")

    # Adiciona a extensão .txt automaticamente
    nome_doc = nome_base + ".txt"
    

    # Abre o arquivo para escrita
    with open(nome_doc, "w", encoding="utf-8") as arquivo:
            linha = input("Digite o conteúdo do documento: ")
            arquivo.write(linha + "\n")
    # Adiciona o documento à lista
    chave = f"doc{len(lista) + 1}"
    lista.inserir(nome_doc, linha, chave)
    # Exibe mensagem de sucesso
    print(f"Documento '{nome_doc}' cadastrado com a chave '{chave}'.")
    print(f"Arquivo '{nome_doc}' criado com sucesso!")

def listadoc():
    if len(lista) == 0:
        print("Nenhum documento cadastrado.")
    else:
        print("Documentos cadastrados:")
        for i, (nome_doc, linha, chave) in enumerate(lista):
            print(f"{i + 1}. Nome: {nome_doc}, Conteúdo: {linha}, Chave: {chave}")
        print(f"Total de documentos cadastrados: {len(lista)}")
    
def menu():
    while True:
        criamenu()
        i = int(input("Escolha uma opção:"))
        if i == 1:
            cadastradoc()
            print(len(lista))
            input("Pressione Enter para continuar...")
        if i == 2:
            listadoc()
            

menu()
