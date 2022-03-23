#!/usr/bin/env python3
from re import *
import sys
from datetime import datetime

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'

f = open("assets/emd.csv")

class Jogador:
    def __init__(self, m):
        self.id = m.group("id")
        self.nome = m.group("primeiro")
        self.ultimo = m.group("ultimo")

jogadores = {}
distPorGen = {}
distPorIdade = {"MaisOuIgual35" : {"M" : [], "F" : []}, "Menos35" : {"M" : [], "F" : []}}
resultados = {}
distPorMorada = {}

def generate_Index(lista, filePath):
    file = open(filePath, "w")
    file.write('<ul>')
    for m in lista:
        file.write('<li><a href="athlete/{}.html">{}, {}</a></li>'.format(m, jogadores[m].nome, jogadores[m].ultimo))
    file.write('</ul>')
    file.close()


def generate_DistGen(lista_anos):
    w = open("gen.html", "w")
    row = open('template/rowsGenTemp.html', "r")
    body = ''
    for membro in sorted(lista_anos):
        #Ref Masculino
        generate_Index(lista_anos[membro]["M"], "Genero/masc_{}.html".format(membro))

        #Ref Femenino
        generate_Index(lista_anos[membro]["F"], "Genero/fem_{}.html".format(membro))

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
    generate_Index(lista_generos["MaisOuIgual35"]["M"], "Idade/mais35Masc.html")

    #Ref Masculino < 35
    generate_Index(lista_generos["Menos35"]["M"], "Idade/menos35Masc.html")

    #Ref Feminino >=35
    generate_Index(lista_generos["MaisOuIgual35"]["F"], "Idade/mais35Fem.html")

    #Ref Feminino < 35
    generate_Index(lista_generos["Menos35"]["F"], "Idade/menos35fem.html")

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
        generate_Index(lista_resultados[ano]["aptos"], "Resultados/aptos_{}.html".format(ano))

        #Ref Nao Aptos
        generate_Index(lista_resultados[ano]["naoAptos"], "Resultados/naoAptos_{}.html".format(ano))

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
        generate_Index(lista_moradas[morada], "Locais/local_{}.html".format(morada))


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


def reader():
    inde = open("index.html", "w")
    inde.write('<ul>')
    for l in f.readlines():
        templ = open("template/athlete.html")
        templat = templ.read()
        m = match(reg, l)
        if m:
            data = datetime.strptime(m.group("date"), '%Y-%m-%d').date()
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

            distPorGen[data.year][m.group("genero")].append(j.id)

            #Idade
            if int(m.group("idade")) >= 35:
                distPorIdade["MaisOuIgual35"][m.group("genero")].append(j.id)
            else:
                distPorIdade["Menos35"][m.group("genero")].append(j.id)

            #Morada
            morada = m.group("morada")
            if not distPorMorada.__contains__(morada):
                distPorMorada[morada] = []
            distPorMorada[morada].append(j.id)

            #Resultados
            if not resultados.__contains__(data.year):
                resultados[data.year] = {"aptos": [], "naoAptos":[]}

            fed = m.group("resultado") == "true"
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