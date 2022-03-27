import re
from datetime import datetime
from athl import *
from templates import *

distPorDate = {}

dateMin: datetime
dateMax: datetime

def read_dates(j: Jogador, data: datetime):
    if data < dataMin:
        dataMin = data
        distPorDate["Min"] = [j.id]
    elif data > dataMax:
        dataMax = data
        distPorDate["Max"] = [j.id]
    elif data == dataMin:
        distPorDate["Min"].append(j.id)
    elif data == dataMax:
        distPorDate["Max"].append(j.id)

def generate_dates(jogadores, inde):
    
    # Ref para os atletas com exames na data mínima
    generate_Index(distPorDate["Min"], jogadores, "www/datas_extremas/dataMin.html")

    # Ref para os atletas com exames na data máxima
    generate_Index(distPorDate["Max"], jogadores, "www/datas_extremas/dataMax.html")

    cont = {}
    cont['MinRef'] = '"dataMin.html"'
    cont['dataMin'] = dataMin
    cont['MaxRef'] = '"dataMax.html"'
    cont['dataMax'] = dataMax

    temps = templates.load_templates('template/datas_extremas/', {
        'main': 'index.html'
    })

    res = template(cont, "main", temps)
    inde.write(res)    
