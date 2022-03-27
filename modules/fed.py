import re
from datetime import datetime
from modules.athl import*
from templates import load_templates, template
from modules.globals import create_folder_output, get_output

distPorFed = {}

def read_Fed(j : Jogador, data : datetime, federado : str):
    if not distPorFed.__contains__(data.year):
        distPorFed[data.year] = {"Fed": [], "NFed": []}
    fed = federado == "true"
    # Coloca no respetivo array, caso tenha estatuto de federado e caso não tenha
    if fed:
        distPorFed[data.year]["Fed"].append(j.id)
    else:
        distPorFed[data.year]["NFed"].append(j.id)

def generate_fed(jogadores):
    output = get_output()
    file_name = 'federado'
    create_folder_output(file_name)
    
    cont = {}
    cont['federados'] = []

    for ano in distPorFed:
        # Ref Federados
        generate_Index(distPorFed[ano]["Fed"], jogadores, f"{output}/{file_name}/fed_{ano}.html")

        # Ref Nao Federados
        generate_Index(distPorFed[ano]["NFed"], jogadores, f"{output}/{file_name}/naoFed_{ano}.html")

        t = len(distPorFed[ano]["Fed"]) + len(distPorFed[ano]["NFed"])
        new_ano = {'ano': ano}

        new_ano['ano'] = ano
        new_ano['FedRef'] = f'{output}/{file_name}/fed_{ano}.html'
        new_ano['Federado'] = len(distPorFed[ano]["Fed"])
        new_ano['NFedRef'] = f'{output}/{file_name}/naoFed_{ano}.html'
        new_ano['NaoFederado'] = len(distPorFed[ano]["NFed"])

        cont['federados'].append(new_ano)

    temps = load_templates(f'template/{file_name}/', {
        'federadoPorAno': 'row.html',
        'main': 'index.html'
    })

    res = template(cont, "main", temps)
    w = open(f"{output}/{file_name}.html", "w")
    w.write(res)
    w.close
    return res