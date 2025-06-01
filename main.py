from lista import *
from ordenation import *
from testes import *
from btree import BTree
import pickle

import os

lista = Lista()
btree_index_file = "btree_index.pkl"
lista_file = "lista.pkl"

def salvar_lista():
    # Salva a lista de documentos no arquivo lista.pkl
    with open(lista_file, "wb") as f:
        pickle.dump(lista, f)

def carregar_lista():
    # Carrega a lista de documentos do arquivo lista.pkl, se existir
    global lista
    if os.path.exists(lista_file):
        with open(lista_file, "rb") as f:
            lista = pickle.load(f)
    else:
        lista = Lista()

# Carrega a lista ao iniciar o programa
carregar_lista()

# Carrega a BTree do disco se existir, senão cria uma nova
if os.path.exists(btree_index_file):
    btree = BTree.load(btree_index_file)
else:
    btree = BTree()

def criamenu():
    # Exibe o menu principal do sistema
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
    # Função para cadastrar um novo documento
    nome_base = input("Digite o nome do documento: ")

    # Adiciona a extensão .txt automaticamente
    nome_doc = nome_base + ".txt"
    
    # Abre o arquivo para escrita e salva o conteúdo digitado
    with open(nome_doc, "w", encoding="utf-8") as arquivo:
            linha = input("Digite o conteúdo do documento: ")
            arquivo.write(linha + "\n")
    # Gera uma chave única para o documento
    chave = f"doc{len(lista) + 1}"
    # Insere o documento na lista
    lista.inserir(nome_doc, linha, chave)
    # Indexa o documento na BTree usando a chave
    btree.insert(chave, nome_doc)
    # Salva a BTree em disco
    btree.save(btree_index_file)
    # Salva a lista após cadastrar o documento
    salvar_lista()
    # Exibe mensagem de sucesso
    print(f"Documento '{nome_doc}' cadastrado com a chave '{chave}'.")
    print(f"Arquivo '{nome_doc}' criado com sucesso!")

def listadoc():
    # Lista todos os documentos cadastrados
    if len(lista) == 0:
        print("Nenhum documento cadastrado.")
    else:
        print("Documentos cadastrados:")
        for i, (nome_doc, linha, chave) in enumerate(lista):
            print(f"{i + 1}. Nome: {nome_doc}, Conteúdo: {linha}, Chave: {chave}")
        print(f"Total de documentos cadastrados: {len(lista)}")

def buscarchave():
    # Busca um documento pela chave usando a BTree
    chave = input("Digite a chave do documento para buscar: ")
    nome_doc = btree.search(chave)
    if nome_doc:
        print(f"Documento encontrado: {nome_doc}")
        # Abre e exibe o conteúdo do documento encontrado
        with open(nome_doc, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            print("Conteúdo:", conteudo)
    else:
        print("Documento não encontrado.")
    
def menu():
    # Loop principal do menu do sistema
    while True:
        criamenu()
        i = int(input("Escolha uma opção:"))
        if i == 1:
            cadastradoc()
            print(len(lista))
            input("Pressione Enter para continuar...")
        if i == 2:
            listadoc()
        if i == 3:
            buscarchave()
            input("Pressione Enter para continuar...")
        if i == 4:
            print("Estatísticas e ordenações:")

            j = int(input("Testar algoritimos de ordenação? (1 - Sim, 0 - Não): "))

            if j == 1:

                p = int(input("Teste aleatório? (1 - Sim, 0 - Não): "))

                if p == 1:
                    print("Gerando lista aleatória...")
                    test_algorithms(random_test=True)
                else:
                    print("Digite os números separados por vírgula:")
                    k = input("Adicione elementos aleatórios separados por virgula a serem ordenados:  ")
                    print("Lista original:", k)

                    k = list(map(int, k.split(',')))
                    test_algorithms(random_test=False, arr=k)

        if i == 0:
            print("Saindo do sistema...")
            break

menu()