#!/usr/bin/env python3
import templates
from modules.jogador import *
from modules.globals import create_folder_output, get_output

def generate_athelete(j : Jogador):
    output = get_output()
    file_name = 'athlete'
    create_folder_output(file_name)
    temps = templates.load_templates(f'template/{file_name}/',
                                     {
                                         'main': 'athlete.html'
                                     })
    
    res = templates.template(vars(j), "main", temps)
    nathl = open(f'{output}/{file_name}/{j.id}.html', 'w')
    nathl.write(res)
    nathl.close()


def generate_Index(lista, jogadores, filePath):
    cont = {}
    cont['rows'] = []

    for m in lista:
        new_ind = {'ID': m}
        new_ind["Primeiro"] = jogadores[m].nome
        new_ind["Ultimo"] = jogadores[m].ultimo
        cont['rows'].append(new_ind)

    cont['rows'] = sorted(cont['rows'], key=lambda j: (j['Primeiro'], j['Ultimo']))
    
    temps = templates.load_templates('template/common/',
                                     {
                                         'rowIndex': 'rowIndex.html',
                                         'main': 'index.html'
                                     })
    res = templates.template(cont, "main", temps)
    w = open(filePath, "w")
    w.write(res)
    w.close()



