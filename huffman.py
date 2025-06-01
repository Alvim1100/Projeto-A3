import heapq
import pickle
from collections import defaultdict

# Classe para representar um nó da árvore de Huffman
class Node:
    def __init__(self, char=None, freq=0):
        self.char = char      # Caractere armazenado (folha) ou None (nó interno)
        self.freq = freq      # Frequência do caractere ou soma das frequências dos filhos
        self.left = None      # Filho à esquerda
        self.right = None     # Filho à direita

    def __lt__(self, other):
        # Permite comparar nós pela frequência (necessário para a heap)
        return self.freq < other.freq

# Função para construir a árvore de Huffman a partir do texto
def build_huffman_tree(text):
    freq = defaultdict(int)
    # Conta a frequência de cada caractere no texto
    for char in text:
        freq[char] += 1
    # Cria uma heap de nós folha
    heap = [Node(char, f) for char, f in freq.items()]
    heapq.heapify(heap)
    # Combina os dois nós de menor frequência até restar apenas um nó (raiz)
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(freq=n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)
    return heap[0] if heap else None  # Retorna a raiz da árvore

# Função para gerar o dicionário de códigos binários para cada caractere
def build_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node:
        if node.char is not None:
            # Nó folha: associa o prefixo ao caractere
            codebook[node.char] = prefix
        # Percorre recursivamente a árvore para esquerda (0) e direita (1)
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

# Função para comprimir um texto usando Huffman
def huffman_compress(text):
    tree = build_huffman_tree(text)         # Constrói a árvore de Huffman
    codebook = build_codes(tree)            # Gera os códigos para cada caractere
    encoded = ''.join(codebook[c] for c in text)  # Codifica o texto em bits
    # Preenche com zeros à direita para completar o último byte, se necessário
    extra = 8 - len(encoded) % 8 if len(encoded) % 8 != 0 else 0
    encoded += "0" * extra
    b = bytearray()
    # Converte a string de bits em bytes
    for i in range(0, len(encoded), 8):
        b.append(int(encoded[i:i+8], 2))
    # Salva a árvore, os dados comprimidos e o número de bits extras em um objeto serializado
    return pickle.dumps((tree, b, extra))

# Função para descomprimir dados comprimidos com Huffman
def huffman_decompress(data):
    tree, b, extra = pickle.loads(data)  # Recupera a árvore, os dados e o extra
    bits = ""
    # Converte os bytes de volta para uma string de bits
    for byte in b:
        bits += f"{byte:08b}"
    if extra:
        bits = bits[:-extra]  # Remove os bits extras adicionados na compressão
    # Decodifica os bits usando a árvore de Huffman
    result = []
    node = tree
    for bit in bits:
        node = node.left if bit == "0" else node.right
        if node.char is not None:
            result.append(node.char)
            node = tree
    return ''.join(result)  # Retorna o texto original descomprimido