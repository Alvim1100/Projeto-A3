import pickle

# Classe que representa um nó da B-Tree
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf      # Indica se o nó é folha (True) ou interno (False)
        self.keys = []        # Lista de pares (chave, valor) armazenados no nó
        self.children = []    # Lista de filhos (referências para outros nós)

# Classe principal da B-Tree
class BTree:
    def __init__(self, t=2):
        self.root = BTreeNode(leaf=True)  # Cria a raiz como folha inicialmente
        self.t = t                        # Grau mínimo da árvore

    def search(self, k, x=None):
        # Busca por uma chave k na árvore, começando pelo nó x (ou raiz)
        if x is None:
            x = self.root
        i = 0
        # Procura a posição onde a chave pode estar ou deve ser inserida
        while i < len(x.keys) and k > x.keys[i][0]:
            i += 1
        # Se encontrou a chave, retorna o valor associado
        if i < len(x.keys) and k == x.keys[i][0]:
            return x.keys[i][1]
        # Se for folha e não encontrou, retorna None
        elif x.leaf:
            return None
        else:
            # Continua a busca no filho apropriado
            return self.search(k, x.children[i])

    def insert(self, k, v):
        # Insere um par (chave, valor) na árvore
        root = self.root
        # Se a raiz está cheia, precisa ser dividida
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k, v)
        else:
            self._insert_non_full(root, k, v)

    def _insert_non_full(self, x, k, v):
        # Insere (k, v) em um nó que não está cheio
        i = len(x.keys) - 1
        if x.leaf:
            # Insere a chave na posição correta no nó folha
            x.keys.append((None, None))
            while i >= 0 and k < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = (k, v)
        else:
            # Encontra o filho correto para descer
            while i >= 0 and k < x.keys[i][0]:
                i -= 1
            i += 1
            # Se estiver cheio, divide o filho antes de inserir
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i][0]:
                    i += 1
            self._insert_non_full(x.children[i], k, v)

    def _split_child(self, x, i):
        # Divide o filho x.children[i] em dois nós e move a chave do meio para x
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:t - 1]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    def save(self, filename):
        # Salva a árvore em um arquivo usando pickle
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        # Carrega uma árvore salva de um arquivo
        with open(filename, 'rb') as f:
            return pickle.load(f)