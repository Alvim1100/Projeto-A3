from lista import *
from ordenation import *
from testes import *
from avl import AVLTree
from btree import BTree
from huffman import huffman_compress, huffman_decompress
import pickle
import os
from collections import defaultdict

lista = Lista()
avl_index_file = "avl_index.pkl"
btree_index_file = "btree_index.pkl"
lista_file = "lista.pkl"


# Índice invertido global
indice_invertido = defaultdict(list)

# Função auxiliar: salvar índice invertido
def salvar_indice_invertido():
    with open(inverted_index_file, "wb") as f:
        pickle.dump(dict(indice_invertido), f)

# Função auxiliar: carregar índice invertido
def carregar_indice_invertido():
    global indice_invertido
    if os.path.exists(inverted_index_file):
        with open(inverted_index_file, "rb") as f:
            indice_invertido = defaultdict(list, pickle.load(f))
            
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

# Carrega a AVLTree do disco se existir, senão cria uma nova
if os.path.exists(avl_index_file):
    avl = AVLTree()
    avl.load(avl_index_file)
else:
    avl = AVLTree()

# Carrega a BTree do disco se existir, senão cria uma nova
if os.path.exists(btree_index_file):
    btree = BTree.load(btree_index_file)
else:
    btree = BTree()

# Função para indexar palavras no índice invertido
def indexar_palavras(chave, conteudo):
    palavras = conteudo.lower().split()
    for palavra in palavras:
        if chave not in indice_invertido[palavra]:
            indice_invertido[palavra].append(chave)
    salvar_indice_invertido()

# Função para contar frequência de uma palavra
def contar_frequencia(palavra, texto):
    return texto.lower().split().count(palavra.lower())

# Função para ordenar resultados por frequência usando heap sort
def ordenar_por_frequencia(palavra, documentos):
    frequencias = []
    for nome_doc, linha, chave in lista:
        if chave in documentos:
            freq = contar_frequencia(palavra, linha)
            frequencias.append((freq, chave, nome_doc))
    return OrderAlgos.heap_sort(frequencias)[::-1]

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
    
    # Recebe o conteúdo do documento
    linha = input("Digite o conteúdo do documento: ")
    # Comprime o conteúdo com Huffman
    compressed = huffman_compress(linha)
    # Salva o conteúdo comprimido em binário
    with open(nome_doc, "wb") as arquivo:
        arquivo.write(compressed)
    # Gera uma chave única para o documento
    chave = f"doc{len(lista) + 1}"
    # Insere o documento na lista (guarda o texto original para listagem)
    lista.inserir(nome_doc, linha, chave)
    # Indexa o documento na AVL e na BTree
    avl.insert(chave)
    btree.insert(chave, nome_doc)
    # Salva as árvores em disco
    avl.save(avl_index_file)
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
    palavra = input("Digite a palavra-chave para buscar: ").lower()

    if palavra not in indice_invertido:
        print("Nenhum documento contém essa palavra.")
        return

    documentos = indice_invertido[palavra]
    resultados = ordenar_por_frequencia(palavra, documentos)

    print(f"\nResultados para a palavra '{palavra}':")
    for freq, chave, nome_doc in resultados:
        print(f"- Documento: {nome_doc} | Chave: {chave} | Ocorrências: {freq}")

        # Exibe conteúdo descomprimido
        try:
            with open(nome_doc, "rb") as f:
                conteudo = huffman_decompress(f.read())
                print("  Trecho:", conteudo[:100], "...")  # mostra só os primeiros 100 caracteres
        except Exception as e:
            print("  Erro ao ler o documento:", e)

    print()

    
def menu():
    # Loop principal do menu do sistema
    while True:
        criamenu()
        i = int(input("Escolha uma opção:"))
        if i == 1:
            cadastradoc()
            input("Pressione Enter para continuar...")
        if i == 2:
            listadoc()
            input("Pressione Enter para continuar...")
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

