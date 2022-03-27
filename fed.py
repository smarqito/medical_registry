import re
from datetime import datetime
from athl import*
from templates import load_templates, template

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

def generate_fed(jogadores, inde):
    cont = {}
    cont['federados'] = []

    for ano in distPorFed:
        # Ref Federados
        generate_Index(distPorFed[ano]["Fed"], jogadores, f"www/federado/fed_{ano}.html")

        # Ref Nao Federados
        generate_Index(distPorFed[ano]["NFed"], jogadores, f"www/federado/naoFed_{ano}.html")

        t = len(distPorFed[ano]["Fed"]) + len(distPorFed[ano]["NFed"])
        new_ano = {'ano': ano}

        new_ano['ano'] = ano
        new_ano['FedRef'] = f'fed_{ano}.html'
        new_ano['Federado'] = len(distPorFed[ano]["Fed"])
        new_ano['NFedRef'] = f'naoFed_{ano}.html'
        new_ano['NaoFederado'] = len(distPorFed[ano]["NFed"])

        cont['federados'].append(new_ano)

    temps = load_templates('template/federado/', {
        'federadoPorAno': 'row.html',
        'main': 'index.html'
    })

    res = template(cont, "main", temps)
    inde.write(res)