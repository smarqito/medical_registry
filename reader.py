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
from modules.globals import create_folder, output

f = open("assets/emd.csv")
inde = open("index.html", "w")

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'


jogadores = {}

def reader():
    global output
    create_folder(output)
    for l in f.readlines():

        m = match(reg, l)
        if m:
            data = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
            j = Jogador(m)
            jogadores[j.id] = j
            gd = m.groupdict()
            # gera o atleta, individual
            index[''] = generate_athelete(gd)

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
    index = {
        'date' : 'Não gerado',
        'genero' : 'Não gerado',
        'idade' : 'Não gerado',
        'resultados' : 'Não gerado',
        'federados' : 'Não gerado',
        'moradas' : 'Não gerado',
        'modalidades' : 'Não gerado',
    }
    index['date'] = generate_dates(jogadores)
    index['genero'] = generate_DistGen(jogadores)
    index['idade'] = generate_IdadeGen(jogadores)
    index['resultados'] = generate_Resultados(jogadores)
    index['federados'] = generate_fed(jogadores)
    index['moradas'] = generate_DistMoradas(jogadores)
    index['modalidades'] = generate_DistMod(jogadores)
    f.close()


reader()
