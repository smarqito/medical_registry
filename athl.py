#!/usr/bin/env python3
from re import *
import sys
from datetime import datetime

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'

f = open("assets/emd.csv")

class Jogador:
    def __init__(self, m):
        self.id = m.group("id")
        self.nome = m.group("nome")
        self.ultimo = m.group("ultimo")

jogadores = {}
distPorGen = {}
distPorIdade = {"MaisOuIgual35" : {"M" : [], "F" : []}, "Menos35" : {"M" : [], "F" : []}}~
resultados = {}
distPorMorada = {}

def reader():
    inde = open("index.html", "w")
    inde.write('<ul>')
    for l in f.readlines():
        data = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
        templ = open("template/athlete.html")
        templat = templ.read()
        m = match(reg, l)
        if m:
            j = Jogador(m)
            jogadores[j.id] = j
            gd = m.groupdict()
            inde.write(f'<li><a href="athlete/{gd["id"]}.html">{gd["primeiro"]}, {gd["ultimo"]}</a></li>')
            for k in gd.keys():
                templat = sub(rf'{{{{{k}}}}}', gd[k], templat)
            nathl = open(f'athlete/{gd["id"]}.html', 'w')
            nathl.write(templat)

            #Género
            if not distPorGen.__contains__(data.year):
                distPorGen[data.year] = {"M": [], "F":[]}

            distPorGen[data.year][j.gen].append(j.id)

            #Idade
            if int(j.idade) >= 35:
                distPorIdade["MaisOuIgual35"][j.gen].append(j.id)
            else:
                distPorIdade["Menos35"][j.gen].append(j.id)

            #Morada
            morada = j.morada
            if not distPorMorada.__contains__(morada):
                distPorMorada[morada] = []
            distPorMorada[morada].append(j.id)

            #Resultados
            if not resultados.__contains__(data.year):
                resultados[data.year] = {"aptos": [], "naoAptos":[]}

            fed = j.result == "true"
            if fed:
                resultados[data.year]["aptos"].append(j.id)
            else:
                resultados[data.year]["naoAptos"].append(j.id)

        templ.close()
        

    inde.write('</ul>')
    inde.close()

    generate_DistGen(distPorGen)
    generate_IdadeGen(distPorIdade)
    generate_Resultados(resultados)
    generate_DistMoradas(distPorMorada)

reader()

def generate_DistGen(lista_anos):
    w = open("gen.html", "w")
    row = open('template/rowsGenTemp.html', "r")
    body = ''
    for membro in sorted(lista_anos):
        #Ref Masculino
        masc = open("Genero/masc_{}.html".format(membro), "w")
        masc.write('<ul>')
        for m in lista_anos[membro]["M"]:
            masc.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
        masc.write('</ul>')
        masc.close()

        #Ref Femenino
        fem = open("Genero/fem_{}.html".format(membro), "w")
        fem.write('<ul>')
        for m in lista_anos[membro]["F"]:
            fem.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
        fem.write('</ul>')
        fem.close()

        content = row.read()
        content = sub(r'{{ano}}', '{}'.format(membro), content)
        content = sub(r'{{refM}}', '"Genero/masc_{}.html"'.format(membro), content)
        content = sub(r'{{refF}}', '"Genero/fem_{}.html"'.format(membro), content)
        content = sub(r'{{TotalM}}', '{}'.format(len(lista_anos[membro]["M"])), content)
        content = sub(r'{{TotalF}}', '{}'.format(len(lista_anos[membro]["F"])), content)
        content = sub(r'{{Total}}', '{}'.format(len(lista_anos[membro]["M"]) + len(lista_anos[membro]["F"])), content)
        body += content
        row.seek(0)
        
    row.close()
    genT = open('template/genTemplate.html', "r")
    temp = genT.read()
    temp = sub(r'{{rows}}', '{}'.format(body), temp)
    w.write(temp)
    w.close

def generate_IdadeGen(lista_generos):

    #Ref Masculino >=35
    masc = open("Idade/mais35Masc.html", "w")
    masc.write('<ul>')
    for m in lista_generos["MaisOuIgual35"]["M"]:
        masc.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
    masc.write('</ul>')
    masc.close()

    #Ref Masculino < 35
    masc = open("Idade/menos35Masc.html", "w")
    masc.write('<ul>')
    for m in lista_generos["Menos35"]["M"]:
        masc.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
    masc.write('</ul>')
    masc.close()

    #Ref Feminino >=35
    fem = open("Idade/mais35Fem.html", "w")
    fem.write('<ul>')
    for m in lista_generos["MaisOuIgual35"]["F"]:
        fem.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
    fem.write('</ul>')
    fem.close()

    #Ref Feminino < 35
    fem = open("Idade/menos35fem.html", "w")
    fem.write('<ul>')
    for m in lista_generos["Menos35"]["F"]:
        fem.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
    fem.write('</ul>')
    fem.close()

    #Substituções das tags do template
    row = open('template/idadeGenTemplate.html', "r")
    content = row.read()
    content = sub(r'{{Mais35refM}}', '"Idade/mais35Masc.html"', content)
    content = sub(r'{{Mais35TotalM}}', '{}'.format(len(lista_generos["MaisOuIgual35"]["M"])), content)
    content = sub(r'{{Mais35refF}}', '"Idade/mais35Fem.html"', content)
    content = sub(r'{{Mais35TotalF}}', '{}'.format(len(lista_generos["MaisOuIgual35"]["F"])), content)
    content = sub(r'{{Mais35Total}}', '{}'.format(len(lista_generos["MaisOuIgual35"]["M"]) + len(lista_generos["MaisOuIgual35"]["F"])), content)


    content = sub(r'{{Menos35refM}}', '"Idade/menos35Masc.html"', content)
    content = sub(r'{{Menos35TotalM}}', '{}'.format(len(lista_generos["Menos35"]["M"])), content)
    content = sub(r'{{Menos35refF}}', '"Idade/menos35Fem.html"', content)
    content = sub(r'{{Menos35TotalF}}', '{}'.format(len(lista_generos["Menos35"]["F"])), content)
    content = sub(r'{{Menos35Total}}', '{}'.format(len(lista_generos["Menos35"]["M"]) + len(lista_generos["Menos35"]["F"])), content)   
    row.close()

    w = open("genIdade.html", "w")
    w.write(content)
    w.close


def generate_Resultados(lista_resultados):
    w = open("resultados.html", "w")
    row = open('template/rowResultsTemp.html', "r")
    body = ''
    for ano in sorted(lista_resultados):
        #Ref Aptos
        aptos = open("Resultados/aptos_{}.html".format(ano), "w")
        aptos.write('<ul>')
        for m in lista_resultados[ano]["aptos"]:
            aptos.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
        aptos.write('</ul>')
        aptos.close()

        #Ref Nao Aptos
        naoAptos = open("Resultados/naoAptos_{}.html".format(ano), "w")
        naoAptos.write('<ul>')
        for m in lista_resultados[ano]["naoAptos"]:
            naoAptos.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
        naoAptos.write('</ul>')
        naoAptos.close()

        t = len(lista_resultados[ano]["aptos"]) + len(lista_resultados[ano]["naoAptos"])

        content = row.read()
        content = sub(r'{{ano}}', '{}'.format(ano), content)
        content = sub(r'{{AptosRef}}', '"Resultados/aptos_{}.html"'.format(ano), content)
        content = sub(r'{{NaoAptosRef}}', '"Resultados/naoAptos_{}.html"'.format(ano), content)
        content = sub(r'{{Aptos}}', '{:.0f}%'.format((len(lista_resultados[ano]["aptos"])/ t) * 100), content)
        content = sub(r'{{NaoAptos}}', '{:.0f}%'.format((len(lista_resultados[ano]["naoAptos"])/t) * 100), content)
        body += content
        row.seek(0)
        
    row.close()
    r = open('template/resultadosTemplate.html', "r")
    temp = r.read()
    temp = sub(r'{{rows}}', '{}'.format(body), temp)
    w.write(temp)
    w.close

def generate_DistMoradas(lista_moradas):
    w = open("moradas.html", "w")
    row = open('template/rowMoradaTemp.html', "r")
    body = ''
    for morada in sorted(lista_moradas):
        #Ref moradores
        moradores = open("Locais/local_{}.html".format(morada), "w")
        moradores.write('<ul>')
        for m in lista_moradas[morada]:
            moradores.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
        moradores.write('</ul>')
        moradores.close()


        content = row.read()
        content = sub(r'{{Morada}}', '{}'.format(morada), content)
        content = sub(r'{{MoradoresRef}}', '"Locais/local_{}.html"'.format(morada), content)
        content = sub(r'{{Moradores}}', '{}'.format(len(lista_moradas[morada])), content)
        body += content
        row.seek(0)
        
    row.close()
    r = open('template/moradasTemplate.html', "r")
    temp = r.read()
    temp = sub(r'{{rows}}', '{}'.format(body), temp)
    w.write(temp)
    w.close
