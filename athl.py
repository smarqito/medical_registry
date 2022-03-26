#!/usr/bin/env python3
import imp
import sys
import templates
from jogador import *

def generate_Index(lista, jogadores, filePath):
    cont = {}
    cont['rows'] = []
    for m in lista:
        new_ind = {'ID': m}
        new_ind["Primeiro"] = jogadores[m].nome
        new_ind["Ultimo"] = jogadores[m].ultimo
        cont['rows'].append(new_ind)
    temps = templates.load_templates('template/',
                                     {
                                         'rowIndex': 'rowIndex.html',
                                         'main': 'index.html'
                                     })
    res = templates.template(cont, "main", temps)
    w = open(filePath, "w")
    w.write(res)
    w.close()



