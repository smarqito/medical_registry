# from datetime import datetime
from modules.athl import *
from templates import *
from modules.globals import create_folder_output, get_output

distPorDate = {}

dateMin = datetime.max.date()
dateMax =  datetime.min.date()

def read_dates(j: Jogador):
    global dateMin
    global dateMax
    data = j.date
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
    output = get_output()
    file_name = 'datas_extremas'
    create_folder_output(file_name)
    
    # Ref para os atletas com exames na data mínima
    generate_Index(distPorDate["Min"], jogadores, f"{output}/{file_name}/dataMin.html")

    # Ref para os atletas com exames na data máxima
    generate_Index(distPorDate["Max"], jogadores, f"{output}/{file_name}/dataMax.html")

    cont = {}
    cont['MinRef'] = f'"{file_name}/dataMin.html"'
    cont['dataMin'] = dateMin
    cont['MaxRef'] = f'"{file_name}/dataMax.html"'
    cont['dataMax'] = dateMax

    temps = templates.load_templates(f'template/{file_name}/', {
        'main': 'index.html'
    })

    res = template(cont, "main", temps)
    w = open(f"{output}/{file_name}.html", "w")
    w.write(res)
    w.close
    return res