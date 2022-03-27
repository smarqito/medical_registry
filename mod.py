from datetime import datetime
from typing import Tuple
from athl import *

distPorMod = {}
modalidades = []

def read_Mod(j : Jogador, data : datetime, mod : str):
    if not distPorMod.__contains__(data.year):
        distPorMod[data.year] = {}
    if not distPorMod[data.year].__contains__(mod):
        distPorMod[data.year][mod] = []
    distPorMod[data.year][mod].append(j.id)
    if not modalidades.__contains__(mod):
        modalidades.append(mod)

        
def generate_DistMod():
    '''
    _modalidades: { ano: { modalidade: [ids_jog] } }
    '''
    cont = {}  # conteudo html
    cont['anos_header'] = []
    for ano in sorted(distPorMod):
        cont['anos_header'].append(ano)

    cont['rows'] = []

    for mod in sorted(modalidades):
        temp = {'mod': mod}
        temp['colls'] = []
        for ano in sorted(distPorMod):
            new_ano = {'ano': ano}
            if not distPorMod[ano].__contains__(mod):
                l = 0
            else:
                l = len(distPorMod[ano][mod])

            if (l != 0):
                generate_Index(
                    distPorMod[ano][mod], "www/modalidade/{}_{}.html".format(mod, ano))

            new_ano['total'] = l
            new_ano['ref'] = f'modalidade/{mod}_{ano}.html'
            temp['colls'].append(new_ano)
        cont['rows'].append(temp)
    '''
    {
        anos_header : [inteiros]
        rows: [{
            mod : string
            colls: [{
                    ano : int
                    total : string
                    ref : string
                }]
            }]
    }
    '''
    temps = templates.load_templates('template/modalidade/',
                                     {
                                         'ano_colunas': 'ano_colunas.html',
                                         'row': 'row.html',
                                         'column_row': 'column_row.html',
                                         'main': 'index.html'
                                     })

    w = open("www/modalidades.html", "w")
    res = templates.template(cont, "main", temps)
    w.write(res)
    w.close()