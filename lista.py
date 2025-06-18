class Lista:
    # Classe interna que representa um nó da lista 
    class No:
        def __init__(self, valor, proximo=None):
            self.valor = valor  # Valor armazenado no nó
            self.proximo = proximo  # Referência para o próximo nó
        
    def __init__(self):
        self.inicio = None   # Referência para o primeiro nó da lista
        self.fim = None      # Referência para o último nó da lista
        self.tamanho = 0     # Quantidade de elementos na lista

    def __iter__(self):
        # Permite iterar sobre os valores da lista usando um loop for
        atual = self.inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __len__(self):
        # Retorna o tamanho da lista (quantidade de nós)
        count = 0
        atual = self.inicio
        while atual:
            count += 1
            atual = atual.proximo
        return count
    
    def inserir(self, valor, linha, chave):
        # Insere um novo nó no final da lista com uma tupla (valor, linha, chave)
        novo_no = self.No((valor, linha, chave))
        if self.inicio is None:
            # Se a lista está vazia, o novo nó é o início e o fim
            self.inicio = novo_no
            self.fim = novo_no
        else:
            # Caso contrário, adiciona ao final e atualiza o ponteiro fim
            self.fim.proximo = novo_no
            self.fim = novo_no
        self.tamanho += 1  # Atualiza o tamanho da lista
        