#!/usr/bin/env python3 
#----------------------------------------------------------------
# Created by: Grupo 53
# Created date: 2022-03-27
# Version = '1.0'
#----------------------------------------------------------------
''' emdtohtml.py: ./emdtohtml.py <flags> <input> '''
#----------------------------------------------------------------
from re import *
import sys

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
import templates
import sys


reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'

jogadores = {}

generate = {
    'd': generate_dates,
    'g': generate_DistGen,
    'i': generate_IdadeGen,
    'r': generate_Resultados,
    'f': generate_fed,
    'l': generate_DistMoradas,
    'm': generate_DistMod
}
read = {
    # Datas Extremas
    'd': read_dates,
    # Género
    'g': read_Gen,
    # Idade
    'i': read_Idade,
    # Resultados
    'r': read_Resultados,
    # Federados
    'f': read_Fed,
    # Morada
    'l': read_Morada,
    # Modalidade
    'm': read_Mod
}


def reader():
    handle_args()
    output = get_output()
    create_folder(output)
    opts = get_opts()
    while l := sys.stdin.readline():
        m = match(reg, l)
        if m:
            j = Jogador(m)
            jogadores[j.id] = j

            # gera o atleta, individual
            generate_athelete(j)

            for opt in opts:
                if opts[opt]:
                    read[opt](j)
    # falta ordenar
    generate_Index(jogadores.keys(), jogadores, f'{output}/athletes.html')

    index = {
        'd': '',
        'g': '',
        'i': '',
        'r': '',
        'f': '',
        'l': '',
        'm': '',
    }
    for opt in opts:
        if opts[opt]:
            index[opt] = generate[opt](jogadores)

    temps = templates.load_templates('template/', {'main': 'index.html'})
    t = templates.template(index, 'main', temps)
    i = open(f'{output}/index.html', 'w')
    i.write(t)
    i.close()


reader()
