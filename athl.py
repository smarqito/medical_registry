#!/usr/bin/env python3
from re import *
import sys
from datetime import datetime
import templates
reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<genero>[MF]),(?P<morada>\w+),(?P<modalidade>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<federado>\w+),(?P<resultado>\w+)'

f = open("assets/emd.csv")

class Jogador:
    def __init__(self, m):
        self.id = m.group("id")
        self.nome = m.group("primeiro")
        self.ultimo = m.group("ultimo")


jogadores = {}
distPorGen = {}
distPorIdade = {"MaisOuIgual35": {"M": [], "F": []},
                "Menos35": {"M": [], "F": []}}
resultados = {}
distPorMorada = {}
distPorMod = {}
modalidades = []


def generate_Index(lista, filePath):
    file = open(filePath, "w")
    file.write('<ul>')
    for m in lista:
        file.write('<li><a href="../athlete/{}.html">{}, {}</a></li>'.format(m,
                   jogadores[m].nome, jogadores[m].ultimo))
    file.write('</ul>')
    file.close()


def generate_DistGen(lista_anos):
    w = open("gen.html", "w")
    cont = {}
    cont['rows'] = []
    for membro in sorted(lista_anos):
        cont[membro] = {}
        # Ref Masculino
        generate_Index(lista_anos[membro]["M"],
                       "www/genero/masc_{}.html".format(membro))

        # Ref Femenino
        generate_Index(lista_anos[membro]["F"],
                       "www/genero/fem_{}.html".format(membro))

        new_ano = {'ano': membro}
        new_ano['ano'] = membro
        new_ano['refM'] = '"masc_{}.html"'.format(membro)
        new_ano['refF'] = '"fem_{}.html"'.format(membro)
        new_ano['TotalM'] = len(lista_anos[membro]["M"])
        new_ano['TotalF'] = len(lista_anos[membro]["F"])
        new_ano['Total'] = len(
            lista_anos[membro]["M"]) + len(lista_anos[membro]["F"])
        cont["rows"].append(new_ano)

    # row.close()
    temps = templates.load_templates('template/genero/',
                                     {
                                         'rowsGenTemp': 'rowsGenTemp.html',
                                         'main': 'genTemplate.html'
                                     })

    res = templates.template(cont, "main", temps)
    w.write(res)
    w.close


def generate_IdadeGen(lista_generos):

    # Ref Masculino >=35
    generate_Index(lista_generos["MaisOuIgual35"]
                   ["M"], "www/idade/mais35Masc.html")

    # Ref Masculino < 35
    generate_Index(lista_generos["Menos35"]["M"], "www/idade/menos35Masc.html")

    # Ref Feminino >=35
    generate_Index(lista_generos["MaisOuIgual35"]
                   ["F"], "www/idade/mais35Fem.html")

    # Ref Feminino < 35
    generate_Index(lista_generos["Menos35"]["F"], "www/idade/menos35fem.html")

    # Substituções das tags do template
    cont = {}
    cont['Mais35refM'] = '"mais35Masc.html"'
    cont['Mais35TotalM'] = len(lista_generos["MaisOuIgual35"]["M"])
    cont['Mais35refF'] = '"mais35Fem.html"'
    cont['Mais35TotalF'] = len(lista_generos["MaisOuIgual35"]["F"])

    cont['Mais35Total'] = len(
        lista_generos["MaisOuIgual35"]["M"]) + len(lista_generos["MaisOuIgual35"]["F"])
    cont['Menos35refM'] = 'menos35Masc.html"'
    cont['Menos35TotalM'] = len(lista_generos["Menos35"]["M"])
    cont['Menos35refF'] = 'menos35Fem.html"'
    cont['Menos35TotalF'] = len(lista_generos["Menos35"]["F"])
    cont['Menos35Total'] = len(
        lista_generos["Menos35"]["M"]) + len(lista_generos["Menos35"]["F"])

    temps = templates.load_templates('template/idade/',
                                     {
                                         'main': 'idadeGenTemplate.html'
                                     })

    w = open("genIdade.html", "w")
    res = templates.template(cont, "main", temps)
    w.write(res)
    w.close


def generate_Resultados(lista_resultados):
    cont = {}
    cont['rows'] = []
    for ano in sorted(lista_resultados):
        # Ref Aptos
        generate_Index(lista_resultados[ano]["aptos"],
                       "www/resultados/aptos_{}.html".format(ano))

        # Ref Nao Aptos
        generate_Index(
            lista_resultados[ano]["naoAptos"], "www/resultados/naoAptos_{}.html".format(ano))

        t = len(lista_resultados[ano]["aptos"]) + \
            len(lista_resultados[ano]["naoAptos"])

        new_ano = {'ano': ano}
        new_ano['ano'] = ano
        new_ano['AptosRef'] = 'aptos_{}.html"'.format(ano)
        new_ano['NaoAptosRef'] = 'naoAptos_{}.html"'.format(ano)
        new_ano['Aptos'] = (len(lista_resultados[ano]["aptos"]) / t) * 100
        new_ano['NaoAptos'] = (
            len(lista_resultados[ano]["naoAptos"]) / t) * 100
        cont["rows"].append(new_ano)

    temps = templates.load_templates('template/resultados/',
                                     {
                                         'rowResultsTemp': 'rowResultsTemp.html',
                                         'main': 'resultadosTemplate.html'
                                     })


    w = open("resultados.html", "w")
    res = templates.template(cont, "main", temps)
    w.write(res)
    w.close

def generate_DistMoradas(lista_moradas):
    w = open("moradas.html", "w")

    cont = {}
    cont['rows'] = []
    for morada in sorted(lista_moradas):
        # Ref moradores
        generate_Index(lista_moradas[morada],
                       "www/locais/local_{}.html".format(morada))

        new_morada = {'morada': morada}
        new_morada['Morada'] = morada
        new_morada['MoradoresRef'] = 'local_{}.html"'.format(morada)
        new_morada['Moradores'] = len(lista_moradas[morada])
        cont["rows"].append(new_morada)

    temps = templates.load_templates('template/morada/',
                                     {
                                         'rowMoradaTemp': 'rowMoradaTemp.html',
                                         'main': 'moradasTemplate.html'
                                     })

    r = open('template/moradasTemplate.html', "r")
    res = templates.template(cont, "main", temps)
    w.write(res)
    w.close


def generate_DistMod(_modalidades: dict):
    '''
    _modalidades: { ano: { modalidade: [ids_jog] } }
    '''
    cont = {}  # conteudo html
    cont['anos_header'] = []
    for ano in sorted(_modalidades):
        cont['anos_header'].append(ano)

    cont['rows'] = []

    for mod in sorted(modalidades):
        temp = {'mod': mod}
        temp['colls'] = []
        for ano in sorted(_modalidades):
            new_ano = {'ano': ano}
            if not _modalidades[ano].__contains__(mod):
                l = 0
            else:
                l = len(_modalidades[ano][mod])

            if (l != 0):
                generate_Index(
                    _modalidades[ano][mod], "www/modalidade/{}_{}.html".format(mod, ano))

            new_ano['total'] = l
            new_ano['ref'] = f'modalidade/{mod}_{ano}.html'
            temp['colls'].append(new_ano)
        cont['rows'].append(temp)
    '''
    {
        anos_header : [inteiros]
        rows: [{
            mod : string
            colls: [{
                    ano : int
                    total : string
                    ref : string
                }]
            }]
    }
    '''
    temps = templates.load_templates('template/modalidade/',
                                     {
                                         'ano_colunas': 'ano_colunas.html',
                                         'row': 'row.html',
                                         'column_row': 'column_row.html',
                                         'main': 'index.html'
                                     })

    w = open("www/modalidades.html", "w")
    res = templates.template(cont, "main", temps)
    w.write(res)
    w.close()


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
            # gd = m.groupdict()
            # #inde.write(f'<li><a href="athlete/{gd["id"]}.html">{gd["primeiro"]}, {gd["ultimo"]}</a></li>')
            # for k in gd.keys():
            #     templat = sub(rf'{{{{{k}}}}}', gd[k], templat)
            # nathl = open(f'athlete/{gd["id"]}.html', 'w')
            # nathl.write(templat)

            # Género
            if not distPorGen.__contains__(data.year):
                distPorGen[data.year] = {"M": [], "F": []}

            distPorGen[data.year][m.group("genero")].append(j.id)

            # Idade
            if int(m.group("idade")) >= 35:
                distPorIdade["MaisOuIgual35"][m.group("genero")].append(j.id)
            else:
                distPorIdade["Menos35"][m.group("genero")].append(j.id)

            # Morada
            morada = m.group("morada")
            if not distPorMorada.__contains__(morada):
                distPorMorada[morada] = []
            distPorMorada[morada].append(j.id)

            # Resultados
            if not resultados.__contains__(data.year):
                resultados[data.year] = {"aptos": [], "naoAptos": []}

            fed = m.group("resultado") == "true"
            if fed:
                resultados[data.year]["aptos"].append(j.id)
            else:
                resultados[data.year]["naoAptos"].append(j.id)

            # Modalidade
            if not distPorMod.__contains__(data.year):
                distPorMod[data.year] = {}
            if not distPorMod[data.year].__contains__(m.group("modalidade")):
                distPorMod[data.year][m.group("modalidade")] = []
            distPorMod[data.year][m.group("modalidade")].append(j.id)

            if not modalidades.__contains__(m.group("modalidade")):
                modalidades.append(m.group("modalidade"))

        templ.close()

    # generate_DistGen(distPorGen)
    # inde.write(f'<li><a href="gen.html">Distribuição por género</a></li>')
    # generate_IdadeGen(distPorIdade)
    # inde.write(f'<li><a href="genIdade.html">Distribuição por idade</a></li>')
    # generate_Resultados(resultados)
    # inde.write(f'<li><a href="resultados.html">Resultados</a></li>')
    # generate_DistMoradas(distPorMorada)
    # inde.write(f'<li><a href="moradas.html">Distribuição por Morada</a></li>')
    # generate_DistMod(distPorMod)
    # inde.write(
    #     f'<li><a href="modalidades.html">Distribuição por Modalidade</a></li>')

    # inde.write('</ul>')
    # inde.close()


reader()
