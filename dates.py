import re
from datetime import datetime

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<gen>[MF]),(?P<morada>\w+),(?P<mod>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<fed>\w+),(?P<result>\w+)'

def writeJogs(jMin, jMax, templat):
    dates = open("resultado/data_extrema.html", "w")
    for jogadorMin in jMin:
        hrefMin = f"../athlete/{jogadorMin[0]}.html"
        tagMin = rf'<div class="row"><div class="col"><a href="{hrefMin}">{jogadorMin[2]}, {jogadorMin[1]}</a></div></div> \1'
        templat = re.sub(r'(\{\{min\}\})', tagMin, templat)

    for jogadorMax in jMax:
        hrefMax = f"../athlete/{jogadorMax[0]}.html"
        tagMax = rf'<div class="row"><div class="col"><a href="{hrefMax}">{jogadorMax[2]}, {jogadorMax[1]}</a></div></div> \1'
        templat = re.sub(r'(\{\{max\}\})', tagMax, templat)

    templat = re.sub(r'{{min}}', "", templat)
    templat = re.sub(r'{{max}}', "", templat)
    dates.write(templat)
    dates.close()


def datesReader():
    f = open("assets/emd.csv")

    dataMin = datetime.max.date()
    dataMax = datetime.min.date()

    allJogadores = []
    maxJ = []
    minJ = []

    inde = open("index.html", "w")
    inde.write('<ul>\n')
    inde.write(f'<li><a href="resultado/data_extrema.html">Datas Extremas</a></li>\n')
    templ = open("template/data_extrema/dates.html")
    templat = templ.read()
    for l in f:
        m = re.match(reg, l)
        if m:
            data = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
            j = (m.group('id'),m.group('primeiro'),m.group('ultimo'), data)
            allJogadores.append(j)
            if data < dataMin:
                dataMin = data
                minJ = [j]
            elif data > dataMax:
               dataMax = data
               maxJ = [j]
            elif data == dataMin:
                minJ.append(j)
            elif data == dataMax:
                maxJ.append(j)

    templat = re.sub(r'dataMinima', dataMin.strftime('%Y-%m-%d'), templat)
    templat = re.sub(r'dataMaxima', dataMax.strftime('%Y-%m-%d'), templat)

    writeJogs(sorted(minJ), sorted(maxJ), templat)

    inde.write('</ul>')
    inde.close()
    templ.close()
    f.close()

datesReader()


