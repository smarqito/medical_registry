from datetime import datetime
from re import *
from athl import generate_athelete
from dates import generate_dates, read_dates
from mod import generate_DistMod, read_Mod
from moradas import generate_DistMoradas, read_Morada
from resultados import generate_Resultados, read_Resultados
from idade import generate_IdadeGen, read_Idade
from genero import generate_DistGen, read_Gen
from fed import generate_fed, read_Fed
from jogador import *


f = open("assets/emd.csv")
inde = open("index.html", "w")

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'


jogadores = {}

def reader():
    #inde = open("index.html", "w")
    #inde.write('<ul>')
    for l in f.readlines():
        templ = open("template/athlete.html")
        templat = templ.read()
        m = match(reg, l)
        if m:
            data = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
            j = Jogador(m)
            jogadores[j.id] = j
            gd = m.groupdict()
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

            #Federados
            read_Fed(j, data, m.group("federado"))

            # Modalidade
            read_Mod(j, data, m.group("modalidade"))

        templ.close()

    generate_dates(jogadores, inde)
    generate_DistGen(jogadores, inde)
    generate_IdadeGen(jogadores, inde)
    generate_Resultados(jogadores, inde)
    generate_fed(jogadores, inde)
    generate_DistMoradas(jogadores, inde)
    generate_DistMod(jogadores, inde)
    inde.close()
    f.close()


reader()