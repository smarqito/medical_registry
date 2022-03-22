import re
from datetime import datetime

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<gen>[MF]),(?P<morada>\w+),(?P<mod>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<fed>\w+),(?P<result>\w+)'

def writeJogs(jMin, jMax, templat):
    w = open("athlete/dates.html", "w")
    for jogadorMin in jMin:
        hrefMin = "{}.html".format(jogadorMin[0])
        tagMin = r'<div class="row"><div class="col"><a href="{}">{}, {}</a></div></div> \1'.format(hrefMin, jogadorMin[2], jogadorMin[1])
        templat = re.sub(r'(\{\{min\}\})', tagMin, templat)

    for jogadorMax in jMax:
        hrefMax = "{}.html".format(jogadorMax[0])
        tagMax = r'<div class="row"><div class="col"><a href="{}">{}, {}</a></div></div> \1'.format(hrefMax, jogadorMax[2], jogadorMax[1])
        templat = re.sub(r'(\{\{max\}\})', tagMax, templat)

    templat = re.sub(r'{{min}}', "", templat)
    templat = re.sub(r'{{max}}', "", templat)
    w.write(templat)

f = open("assets/emd.csv")

def datesReader():
    dataMin = datetime.max.date()
    dataMax = datetime.min.date()

    allJogadores = []
    maxJ = []
    minJ = []

    inde = open("index.html", "w")
    inde.write('<ul>\n')
    inde.write(f'<li><a href="athlete/dates.html">Datas Extremas</a></li>\n')
    templ = open("template/dates.html")
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

datesReader()


