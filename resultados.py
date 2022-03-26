from athl import *
import math 
from datetime import datetime

def read_Resultados(j : Jogador, data : datetime, resultado : str) -> dict:
    resultados = {}
    if not resultados.__contains__(data.year):
                resultados[data.year] = {"aptos": [], "naoAptos": []}
    res = resultado == "true"
    if res:
        resultados[data.year]["aptos"].append(j.id)
    else:
        resultados[data.year]["naoAptos"].append(j.id)

def generate_Resultados(lista_resultados, jogadores, inde):
    cont = {}
    cont['rows'] = []
    for ano in sorted(lista_resultados):
        # Ref Aptos
        generate_Index(lista_resultados[ano]["aptos"], jogadores,
                       "www/resultados/aptos_{}.html".format(ano))

        # Ref Nao Aptos
        generate_Index(
            lista_resultados[ano]["naoAptos"], jogadores, "www/resultados/naoAptos_{}.html".format(ano))

        t = len(lista_resultados[ano]["aptos"]) + \
            len(lista_resultados[ano]["naoAptos"])

        new_ano = {'ano': ano}
        new_ano['AptosRef'] = 'aptos_{}.html"'.format(ano)
        new_ano['NaoAptosRef'] = 'naoAptos_{}.html"'.format(ano)
        new_ano['Aptos'] = math.ceil((len(lista_resultados[ano]["aptos"]) / t) * 100)
        new_ano['NaoAptos'] = math.ceil((
            len(lista_resultados[ano]["naoAptos"]) / t) * 100)
        cont["rows"].append(new_ano)

    temps = templates.load_templates('template/resultados/',
                                     {
                                         'rowResultsTemp': 'row.html',
                                         'main': 'index.html'
                                     })


    #w = open("resultados.html", "w")
    res = templates.template(cont, "main", temps)
    inde.write(res)
    #w.close