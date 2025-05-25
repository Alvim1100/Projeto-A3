class Lista:
    class No:
        def __init__(self, valor, proximo=None):
            self.valor = valor
            self.proximo = proximo
        
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def __iter__(self):
        atual = self.inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __len__(self):
        count = 0
        atual = self.inicio
        while atual:
            count += 1
            atual = atual.proximo
        return count
    
    def inserir(self, valor,linha, chave):
        novo_no = self.No((valor, linha, chave))
        if self.inicio is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no
        self.tamanho += 1

        