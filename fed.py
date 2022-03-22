import re
from datetime import datetime

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<gen>[MF]),(?P<morada>\w+),(?P<mod>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<fed>\w+),(?P<result>\w+)'

def write_feds(dict):
    w = open('federado/estatutoFederado.html', "w")
    row = open('template/federadoPorAno.html', "r")
    body = ''
    for ano in dict:
        #Ref Federados
        fed = open("federado/fed_{}.html".format(ano), "w")
        fed.write('<ul>')
        fedList = sorted(dict[ano]["Fed"], key=lambda tup: tup[1])
        for m in fedList:
            fed.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m[0], m[2], m[1]))
        fed.write('</ul>')
        fed.close()

        #Ref Nao Federados
        naoFed = open("federado/naoFed_{}.html".format(ano), "w")
        naoFed.write('<ul>')
        naoFedList = sorted(dict[ano]["NFed"], key=lambda tup: tup[1])
        for m in naoFedList: 
            naoFed.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m[0], m[2], m[1]))
        naoFed.write('</ul>')
        naoFed.close()

        t = len(dict[ano]["Fed"]) + len(dict[ano]["NFed"])

        content = row.read()
        content = re.sub(r'{{ano}}', '{}'.format(ano), content)
        content = re.sub(r'{{FedRef}}', '"fed_{}.html"'.format(ano), content)
        content = re.sub(r'{{NFedRef}}', '"naoFed_{}.html"'.format(ano), content)
        content = re.sub(r'{{Federado}}', '{}'.format(len(dict[ano]["Fed"])), content)
        content = re.sub(r'{{NaoFederado}}', '{}'.format(len(dict[ano]["NFed"])), content)
        body += content
        row.seek(0)
        
    row.close()
    r = open('template/federado.html', "r")
    temp = r.read()
    temp = re.sub(r'{{federados}}', '{}'.format(body), temp)
    w.write(temp)
    r.close()
    w.close()

def dist_Fed():
    f = open("assets/emd.csv")

    distPorFed = {}

    inde = open("index.html", "w")
    inde.write('<ul>\n')
    inde.write(f'<li><a href="federado/estatutoFederado.html">Estatuto de Federado</a></li>\n')

    for l in f:
        m = re.match(reg,l)
        if m:
            data = datetime.strptime(m.group("date"), "%Y-%m-%d").date()
            j = (m.group('id'),m.group('primeiro'),m.group('ultimo'))

            if not distPorFed.__contains__(data.year):
                distPorFed[data.year] = {"Fed": [], "NFed": []}

            fed = m.group('fed') == "true"
            if fed:
                distPorFed[data.year]["Fed"].append(j)
            else: 
                distPorFed[data.year]["NFed"].append(j)

    write_feds(distPorFed)

    inde.write('</ul>')
    inde.close()
    f.close()

dist_Fed()