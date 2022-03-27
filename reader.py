from re import *
from modules.athl import generate_Index, generate_athelete
from modules.dates import generate_dates, read_dates
from modules.mod import generate_DistMod, read_Mod
from modules.moradas import generate_DistMoradas, read_Morada
from modules.resultados import generate_Resultados, read_Resultados
from modules.idade import generate_IdadeGen, read_Idade
from modules.genero import generate_DistGen, read_Gen
from modules.fed import generate_fed, read_Fed
from modules.jogador import *
from modules.globals import *
import sys


reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'

jogadores = {}

generate = {
    'd' : generate_dates,
    'g' : generate_DistGen,
    'i' : generate_IdadeGen,
    'r' : generate_Resultados,
    'f' : generate_fed,
    'l' : generate_DistMoradas,
    'm' : generate_DistMod
}

def reader():
    handle_args()
    output = get_output()
    create_folder(output)
    opts = get_opts()
    while l := sys.stdin.readline():
        m = match(reg, l)
        if m:
            data = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
            j = Jogador(m)
            jogadores[j.id] = j

            # gera o atleta, individual
            generate_athelete(j)

            # Datas Extremas
            read_dates(j)

            # Género
            read_Gen(j)

            # Idade
            read_Idade(j)

            # Morada
            read_Morada(j)

            # Resultados
            read_Resultados(j)

            # Federados
            read_Fed(j, data, m.group("federado"))

            # Modalidade
            read_Mod(j)
    
    #falta ordenar
    generate_Index(jogadores.keys(), jogadores, f'{output}/athletes.html')
    
    index = {
        'd' : 'Não gerado',
        'g' : 'Não gerado',
        'i' : 'Não gerado',
        'r' : 'Não gerado',
        'f' : 'Não gerado',
        'l' : 'Não gerado',
        'm' : 'Não gerado',
    }
    for opt in opts:
        if opts[opt]:
            index[opt] = generate[opt](jogadores)

reader()
