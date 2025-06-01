import pickle

class AVLNode:
    def __init__(self, key):
        self.key = key          # Palavra armazenada no nó
        self.left = None        # Filho esquerdo
        self.right = None       # Filho direito
        self.height = 1         # Altura do nó

class AVLTree:
    """
    Árvore AVL para armazenar palavras ordenadas.
    Complexidade das operações principais:
    - Inserção: O(log n)
    - Remoção: O(log n)
    - Busca: O(log n)
    """

    def __init__(self):
        self.root = None    # Raiz da árvore

    def insert(self, key):
        """Insere uma palavra na árvore AVL."""
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        """Método recursivo para inserir um nó e rebalancear a árvore."""
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self._insert(root.left, key)
        else:
            root.right = self._insert(root.right, key)

        # Atualiza altura do nó
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        # Calcula fator de balanceamento
        balance = self.get_balance(root)

        # Casos de rotação para manter o balanceamento AVL
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, key):
        """Remove uma palavra da árvore AVL."""
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        """Método recursivo para remover um nó e rebalancear a árvore."""
        if not root:
            return root

        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            # Nó com apenas um filho ou nenhum
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            # Nó com dois filhos: pega o menor da subárvore direita
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self._delete(root.right, temp.key)

        if not root:
            return root

        # Atualiza altura do nó
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        # Calcula fator de balanceamento
        balance = self.get_balance(root)

        # Casos de rotação para manter o balanceamento AVL
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, key):
        """Busca uma palavra na árvore AVL. Retorna o nó se encontrar, senão None."""
        return self._search(self.root, key)

    def _search(self, root, key):
        """Método recursivo para busca."""
        if not root or root.key == key:
            return root
        if key < root.key:
            return self._search(root.left, key)
        return self._search(root.right, key)

    def inorder(self):
        """Imprime as palavras em ordem alfabética."""
        self._inorder(self.root)

    def _inorder(self, root):
        """Travessia em ordem (recursiva)."""
        if root:
            self._inorder(root.left)
            print(root.key)
            self._inorder(root.right)

    def get_height(self, node):
        """Retorna a altura do nó."""
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """Calcula o fator de balanceamento do nó."""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        """Rotação simples à esquerda."""
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        # Atualiza alturas
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        """Rotação simples à direita."""
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        # Atualiza alturas
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_min_value_node(self, node):
        """Retorna o nó com o menor valor (mais à esquerda)."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Métodos de persistência usando pickle
    def save(self, filename):
        """Salva a árvore AVL em um arquivo."""
        with open(filename, 'wb') as f:
            pickle.dump(self.root, f)

    def load(self, filename):
        """Carrega a árvore AVL de um arquivo."""
        with open(filename, 'rb') as f:
            self.root = pickle.load(f)
