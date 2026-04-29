class FilaBacklog:

    def __init__(self):
        self._fila = []

    def enqueue(self, jogo):
        self._fila.append(jogo)

    def dequeue(self):
        if self.is_empty():
            return None
        return self._fila.pop(0)

    def is_empty(self):
        return len(self._fila) == 0

    def mostrar(self):
        return list(self._fila)

    def tamanho(self):
        return len(self._fila)


class PilhaRecentes:

    LIMITE = 20

    def __init__(self):
        self._pilha = []

    def push(self, jogo):
        if len(self._pilha) >= self.LIMITE:
            self._pilha.pop(0)
        self._pilha.append(jogo)

    def pop(self):
        if self.is_empty():
            return None
        return self._pilha.pop()

    def topo(self):
        if self.is_empty():
            return None
        return self._pilha[-1]

    def is_empty(self):
        return len(self._pilha) == 0

    def mostrar(self):
        return list(reversed(self._pilha))

    def tamanho(self):
        return len(self._pilha)