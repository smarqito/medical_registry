from datetime import datetime
from modules.athl import *
from templates import *
from modules.globals import create_folder_output, output

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

def generate_dates(jogadores):
    global output
    file_name = 'datas_extremas'
    create_folder_output(file_name)
    
    # Ref para os atletas com exames na data mínima
    generate_Index(distPorDate["Min"], jogadores, f"{output}/{file_name}/dataMin.html")

    # Ref para os atletas com exames na data máxima
    generate_Index(distPorDate["Max"], jogadores, f"{output}/{file_name}/dataMax.html")

    cont = {}
    cont['MinRef'] = f'"{output}/{file_name}/dataMin.html"'
    cont['dataMin'] = dateMin
    cont['MaxRef'] = f'"{output}/{file_name}/dataMax.html"'
    cont['dataMax'] = dateMax

    temps = templates.load_templates(f'template/{file_name}/', {
        'main': 'index.html'
    })

    res = template(cont, "main", temps)
    w = open(f"{output}/{file_name}.html", "w")
    w.write(res)
    w.close
    return res