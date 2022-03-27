from datetime import datetime
from re import *
from modules.athl import generate_athelete
from modules.dates import generate_dates, read_dates
from modules.mod import generate_DistMod, read_Mod
from modules.moradas import generate_DistMoradas, read_Morada
from modules.resultados import generate_Resultados, read_Resultados
from modules.idade import generate_IdadeGen, read_Idade
from modules.genero import generate_DistGen, read_Gen
from modules.fed import generate_fed, read_Fed
from modules.jogador import *

f = open("assets/emd.csv")
inde = open("index.html", "w")

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>[true|false]),(?P<resultado>[true|false])'


jogadores = {}

def reader():
    for l in f.readlines():
        m = match(reg, l)
        if m:
            data = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
            j = Jogador(m)
            jogadores[j.id] = j
            gd = m.groupdict()
            # gera o atleta, individual
            generate_athelete(gd)

            # Datas Extremas
            read_dates(j, data)

            # Género
            read_Gen(j, data, m.group("genero"))

            # Idade
            read_Idade(j, int(m.group("idade")), m.group("genero"))

            # Morada
            read_Morada(j, m.group("morada"))

            # Resultados
            read_Resultados(j, data, m.group("resultado"))

            # Federados
            read_Fed(j, data, m.group("federado"))

            # Modalidade
            read_Mod(j, data, m.group("modalidade"))

    generate_dates(jogadores)
    generate_DistGen(jogadores)
    generate_IdadeGen(jogadores)
    generate_Resultados(jogadores)
    generate_fed(jogadores)
    generate_DistMoradas(jogadores)
    generate_DistMod(jogadores)
    f.close()


reader()
