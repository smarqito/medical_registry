import re
from datetime import datetime
from athl import *
from templates import *

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<gen>[MF]),(?P<morada>\w+),(?P<mod>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<fed>\w+),(?P<result>\w+)'


def generate_dates(dict, dataMax, dataMin, templat):
    
    # Ref para os atletas com exames na data mínima
    generate_Index(dict["Min"], "www/datas_extremas/dataMin.html")

    # Ref para os atletas com exames na data máxima
    generate_Index(dict["Max"], "www/datas_extremas/dataMax.html")

    cont = {}
    cont['MinRef'] = '"dataMin.html"'
    cont['dataMin'] = dataMin
    cont['MaxRef'] = '"dataMax.html"'
    cont['dataMax'] = dataMax

    temps = templates.load_templates('template/datas_extremas/', {
        'main': 'index.html'
    })

    w = open("www/datas_extremas/datas_extrema.html", "w")
    res = template(cont, "main", temps)
    w.write(res)
    w.close()

# Função que calcula as datas extremas - Mínima e Máxima dos exames elaborados aos atletas
def dist_date():
    f = open("assets/emd.csv")

    dataMin = datetime.max.date()
    dataMax = datetime.min.date()

    distPorDate = {}

    inde = open("index.html", "w")
    inde.write('<ul>\n')
    inde.write(
        f'<li><a href="ww/datas_extremas/datas_extrema.html">Datas Extremas</a></li>\n')
    templ = open("template/datas_extremas/index.html")
    templat = templ.read()
    for l in f:
        m = re.match(reg, l)
        if m:
            data = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
            j = Jogador(m)
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

    generate_dates(distPorDate, dataMax, dataMin, templat)

    inde.write('</ul>')
    inde.close()
    templ.close()
    f.close()


dist_date()
