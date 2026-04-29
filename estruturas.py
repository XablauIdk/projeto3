class FilaBacklog:

    def __init__(self):
        
        self._fila = [] 
        
    def enqueue(self, jogo):
        
        self._fila.append(jogo)

    def dequeue(self):
        if self.is_empty():
            return None
        return self._fila.pop(0)  # Remove do indice 0 (comeco da lista)

    def is_empty(self):
        # Verifica se a fila esta vazia
        # Retorna: True se vazia, False se tem jogos
        return len(self._fila) == 0

    def mostrar(self):
        # Retorna uma copia da fila para visualizacao
        # Nao remove os elementos, apenas mostra
        # Retorna: lista copia da fila
        return list(self._fila)  # retorna copia da lista para nao alterar a fila

    def tamanho(self):
        # Retorna a quantidade de jogos na fila
        # Retorna: numero inteiro de jogos
        return len(self._fila)


# -------- CLASSE PILHA RECENTES --------
class PilhaRecentes:
    # Implementa uma pilha LIFO para armazenar jogos recentes
    # Ultimo a entrar, primeiro a sair - mostra jogos mais recentes primeiro

    LIMITE = 20  # Limite maximo de jogos armazenados na pilha

    def __init__(self):
        # Inicializa a pilha vazia como uma lista Python
        self._pilha = []  # lista usada como pilha (LIFO)

    def push(self, jogo):
        # Adiciona um jogo no topo da pilha (jogo mais recente)
        # Se atingir o limite (20 jogos), remove o mais antigo
        # Parametro: jogo - objeto Jogo a ser adicionado

        # Verifica se passou do limite de 20 jogos
        if len(self._pilha) >= self.LIMITE:
            self._pilha.pop(0)  # Remove o primeiro (mais antigo do fundo)
        self._pilha.append(jogo)  # Adiciona no final (topo da pilha)

    def pop(self):
        # Remove e retorna o ultimo jogo da pilha (o mais recente)
        # Retorna: objeto Jogo ou None se pilha vazia
        if self.is_empty():
            return None
        return self._pilha.pop()  # Remove do final (topo da pilha)

    def topo(self):
        # Retorna o jogo do topo da pilha SEM remover
        # Util para visualizar qual foi o ultimo jogo
        # Retorna: objeto Jogo ou None se pilha vazia
        if self.is_empty():
            return None
        return self._pilha[-1]  # retorna o ultimo jogo sem remover

    def is_empty(self):
        # Verifica se a pilha esta vazia
        # Retorna: True se vazia, False se tem jogos
        return len(self._pilha) == 0

    def mostrar(self):
        # Retorna a pilha do mais recente para o mais antigo (invertida)
        # Util para exibir em ordem correta de recencia
        # Retorna: lista invertida da pilha
        return list(reversed(self._pilha))  # retorna do mais recente para o mais antigo

    def tamanho(self):
        # Retorna a quantidade de jogos na pilha
        # Retorna: numero inteiro de jogos
        return len(self._pilha)
