from datetime import datetime
from re import *
from mod import generate_DistMod
from moradas import generate_DistMoradas, read_Morada
from resultados import generate_Resultados, read_Resultados
from idade import generate_IdadeGen, read_Idade
from genero import generate_DistGen, read_Gen
from jogador import *


f = open("assets/emd.csv")
inde = open("index.html", "w")

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'


jogadores = {}
distPorGen = {}
distPorIdade = {}
resultados = {}
distPorMorada = {}
distPorMod = {}
modalidades = []

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
            # gd = m.groupdict()
            # #inde.write(f'<li><a href="athlete/{gd["id"]}.html">{gd["primeiro"]}, {gd["ultimo"]}</a></li>')
            # for k in gd.keys():
            #     templat = sub(rf'{{{{{k}}}}}', gd[k], templat)
            # nathl = open(f'athlete/{gd["id"]}.html', 'w')
            # nathl.write(templat)

            # Género
            distPorGen = read_Gen(j, data, m.group("genero"))

            # Idade
            distPorIdade = read_Idade(j, int(m.group("idade")), m.group("genero"))

            # Morada
            distPorMorada = read_Morada(j, m.group("morada"))
            

            # Resultados
            resultados = read_Resultados(j, data, m.group("resultado"))

            # Modalidade
            if not distPorMod.__contains__(data.year):
                distPorMod[data.year] = {}
            if not distPorMod[data.year].__contains__(m.group("modalidade")):
                distPorMod[data.year][m.group("modalidade")] = []
            distPorMod[data.year][m.group("modalidade")].append(j.id)

            if not modalidades.__contains__(m.group("modalidade")):
                modalidades.append(m.group("modalidade"))

        templ.close()

    generate_DistGen(distPorGen, jogadores, inde)
    generate_IdadeGen(distPorIdade, jogadores, inde)
    generate_Resultados(resultados, jogadores, inde)
    generate_DistMoradas(distPorMorada, jogadores, inde)
    #generate_DistMod(distPorMod)
    inde.close()
    f.close()


reader()