from datetime import datetime
class Jogador:
    def __init__(self, m):
        self.id = m.group("id")
        self.nome = m.group("primeiro")
        self.primeiro = m.group("primeiro")
        self.ultimo = m.group("ultimo")
        self.genero = m.group('genero')
        self.idade = m.group('idade')
        self.morada = m.group('morada')
        self.resultado = m.group('resultado')
        self.federado = m.group('federado')
        self.modalidade = m.group('modalidade')
        self.date = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
        self.email = m.group('email')
        self.clube = m.group('clube')