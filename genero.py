from athl import *
from datetime import datetime

distPorGen = {}

def read_Gen(j : Jogador, data : datetime, gen : str):
    if not distPorGen.__contains__(data.year):
        distPorGen[data.year] = {"M": [], "F": []}

    distPorGen[data.year][gen].append(j.id)

def generate_DistGen(jogadores, inde):
    cont = {}
    cont['rows'] = []
    for membro in sorted(distPorGen):
        # Ref Masculino
        generate_Index(distPorGen[membro]["M"], jogadores,
                       "www/genero/masc_{}.html".format(membro))

        # Ref Femenino
        generate_Index(distPorGen[membro]["F"], jogadores,
                       "www/genero/fem_{}.html".format(membro))

        new_ano = {'ano': membro}
        new_ano['refM'] = '"masc_{}.html"'.format(membro)
        new_ano['refF'] = '"fem_{}.html"'.format(membro)
        new_ano['TotalM'] = len(distPorGen[membro]["M"])
        new_ano['TotalF'] = len(distPorGen[membro]["F"])
        new_ano['Total'] = len(
            distPorGen[membro]["M"]) + len(distPorGen[membro]["F"])
        cont["rows"].append(new_ano)

    temps = templates.load_templates('template/genero/',
                                     {
                                         'rowsGenTemp': 'row.html',
                                         'main': 'index.html'
                                     })

    #w = open("gen.html", "w")
    res = templates.template(cont, "main", temps)
    inde.write(res)
    #w.close