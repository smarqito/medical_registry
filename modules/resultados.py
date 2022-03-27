from modules.athl import *
import math 
from datetime import datetime
from modules.globals import create_folder, output

resultados = {}

def read_Resultados(j : Jogador, data : datetime, resultado : str) -> dict:
    if not resultados.__contains__(data.year):
                resultados[data.year] = {"aptos": [], "naoAptos": []}
    res = resultado == "true"
    if res:
        resultados[data.year]["aptos"].append(j.id)
    else:
        resultados[data.year]["naoAptos"].append(j.id)

def generate_Resultados(jogadores):
    global output
    file_name = 'resultados'
    create_folder(file_name)
    cont = {}
    cont['rows'] = []
    for ano in sorted(resultados):
        # Ref Aptos
        generate_Index(resultados[ano]["aptos"], jogadores,
                       f"{output}/{file_name}/aptos_{ano}.html")

        # Ref Nao Aptos
        generate_Index(
            resultados[ano]["naoAptos"], jogadores, f"{output}/{file_name}/naoAptos_{ano}.html")

        t = len(resultados[ano]["aptos"]) + \
            len(resultados[ano]["naoAptos"])

        new_ano = {'ano': ano}
        new_ano['AptosRef'] = f'"{output}/{file_name}/aptos_{ano}.html"'
        new_ano['NaoAptosRef'] = f'"{output}/{file_name}/naoAptos_{ano}.html"'
        new_ano['Aptos'] = math.ceil((len(resultados[ano]["aptos"]) / t) * 100)
        new_ano['NaoAptos'] = math.ceil((
            len(resultados[ano]["naoAptos"]) / t) * 100)
        cont["rows"].append(new_ano)

    temps = templates.load_templates(f'template/{file_name}/',
                                     {
                                         'rowResultsTemp': 'row.html',
                                         'main': 'index.html'
                                     })


    res = templates.template(cont, "main", temps)
    w = open(f"{output}/{file_name}.html", "w")
    w.write(res)
    w.close
    return res