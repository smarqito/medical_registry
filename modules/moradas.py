from modules.athl import *
from modules.globals import create_folder_output, output
distPorMorada = {}


def read_Morada(j: Jogador, morada: str) -> dict:
    if not distPorMorada.__contains__(morada):
        distPorMorada[morada] = []
    distPorMorada[morada].append(j.id)
    return distPorMorada


def generate_DistMoradas(jogadores):
    global output
    file_name = 'moradas'
    create_folder_output(file_name)
    cont = {}
    cont['rows'] = []
    for morada in sorted(distPorMorada):
        # Ref moradores
        generate_Index(distPorMorada[morada], jogadores,
                       f"{output}/{file_name}/{morada}.html")

        new_morada = {'Morada': morada}
        new_morada['MoradoresRef'] = f'"moradas/{morada}.html"'
        new_morada['Moradores'] = len(distPorMorada[morada])
        cont["rows"].append(new_morada)

    temps = templates.load_templates(f'template/{file_name}/',
                                     {
                                         'rowMoradaTemp': 'row.html',
                                         'main': 'index.html'
                                     })

    res = templates.template(cont, "main", temps)
    w = open(f"{output}/{file_name}.html", "w")
    w.write(res)
    w.close
    return res
