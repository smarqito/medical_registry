from athl import *
from datetime import datetime

def read_Gen(j : Jogador, data : datetime, gen : str) -> dict:
    distPorGen = {}
    if not distPorGen.__contains__(data.year):
        distPorGen[data.year] = {"M": [], "F": []}

    distPorGen[data.year][gen].append(j.id)
    return distPorGen

def generate_DistGen(lista_anos, jogadores, inde):
    cont = {}
    cont['rows'] = []
    for membro in sorted(lista_anos):
        # Ref Masculino
        generate_Index(lista_anos[membro]["M"], jogadores,
                       "www/genero/masc_{}.html".format(membro))

        # Ref Femenino
        generate_Index(lista_anos[membro]["F"], jogadores,
                       "www/genero/fem_{}.html".format(membro))

        new_ano = {'ano': membro}
        new_ano['refM'] = '"masc_{}.html"'.format(membro)
        new_ano['refF'] = '"fem_{}.html"'.format(membro)
        new_ano['TotalM'] = len(lista_anos[membro]["M"])
        new_ano['TotalF'] = len(lista_anos[membro]["F"])
        new_ano['Total'] = len(
            lista_anos[membro]["M"]) + len(lista_anos[membro]["F"])
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