import re
from datetime import datetime
from athl import *
from templates import *

distPorDate = {}

dateMin = datetime.max.date()
dateMax =  datetime.min.date()

def read_dates(j: Jogador, data: datetime):
    global dateMin
    global dateMax
    if data < dateMin:
        dateMin = data
        distPorDate["Min"] = [j.id]
    elif data > dateMax:
        dateMax = data
        distPorDate["Max"] = [j.id]
    elif data == dateMin:
        distPorDate["Min"].append(j.id)
    elif data == dateMax:
        distPorDate["Max"].append(j.id)

def generate_dates(jogadores, inde):
    
    # Ref para os atletas com exames na data mínima
    generate_Index(distPorDate["Min"], jogadores, "www/datas_extremas/dataMin.html")

    # Ref para os atletas com exames na data máxima
    generate_Index(distPorDate["Max"], jogadores, "www/datas_extremas/dataMax.html")

    cont = {}
    cont['MinRef'] = '"www/datas_extremas/dataMin.html"'
    cont['dataMin'] = dateMin
    cont['MaxRef'] = '"www/datas_extremas/dataMax.html"'
    cont['dataMax'] = dateMax

    temps = templates.load_templates('template/datas_extremas/', {
        'main': 'index.html'
    })

    res = template(cont, "main", temps)
    inde.write(res)    
