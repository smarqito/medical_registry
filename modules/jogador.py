class Jogador:
    def __init__(self, m):
        self.id = m.group("id")
        self.nome = m.group("primeiro")
        self.ultimo = m.group("ultimo")