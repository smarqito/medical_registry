from modules.athl import *
from datetime import datetime
from modules.globals import create_folder_output, output
distPorGen = {}


def read_Gen(j: Jogador, data: datetime, gen: str):
    if not distPorGen.__contains__(data.year):
        distPorGen[data.year] = {"M": [], "F": []}

    distPorGen[data.year][gen].append(j.id)


def generate_DistGen(jogadores):
    global output
    file_name = 'genero'
    create_folder_output(file_name)
    cont = {}
    cont['rows'] = []
    for membro in sorted(distPorGen):
        # Ref Masculino
        generate_Index(distPorGen[membro]["M"], jogadores,
                       f"{output}/{file_name}/masc_{membro}.html")

        # Ref Femenino
        generate_Index(distPorGen[membro]["F"], jogadores,
                       f"{output}/{file_name}/fem_{membro}.html")

        new_ano = {'ano': membro}
        new_ano['refM'] = f'"{output}/{file_name}/masc_{membro}.html"'
        new_ano['refF'] = f'"{output}/{file_name}/fem_{membro}.html"'
        new_ano['TotalM'] = len(distPorGen[membro]["M"])
        new_ano['TotalF'] = len(distPorGen[membro]["F"])
        new_ano['Total'] = len(
            distPorGen[membro]["M"]) + len(distPorGen[membro]["F"])
        cont["rows"].append(new_ano)

    temps = templates.load_templates(f'template/{file_name}/',
                                     {
                                         'rowsGenTemp': 'row.html',
                                         'main': 'index.html'
                                     })

    res = templates.template(cont, "main", temps)
    w = open(f"{output}/{file_name}.html", "w")
    w.write(res)
    w.close
    return res
