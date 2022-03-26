import re
from datetime import datetime
from athl import*
from templates import load_templates, template

reg = r'(?P<id>\w+),(?P<index>\d+),(?P<date>\d{4}-\d{2}-\d{2}),(?P<primeiro>\w+),(?P<ultimo>\w+),(?P<idade>\d+),(?P<gen>[MF]),(?P<morada>\w+),(?P<mod>\w+),(?P<clube>\w+),(?P<email>.*?),(?P<fed>\w+),(?P<result>\w+)'


def generate_fed(dict):
    cont = {}
    cont['federados'] = []

    for ano in dict:
        # Ref Federados
        generate_Index(dict[ano]["Fed"], f"www/federado/fed_{ano}.html")

        # Ref Nao Federados
        generate_Index(dict[ano]["NFed"], f"www/federado/naoFed_{ano}.html")

        t = len(dict[ano]["Fed"]) + len(dict[ano]["NFed"])
        new_ano = {'ano': ano}

        new_ano['ano'] = ano
        new_ano['FedRef'] = f'fed_{ano}.html'
        new_ano['Federado'] = len(dict[ano]["Fed"])
        new_ano['NFedRef'] = f'naoFed_{ano}.html'
        new_ano['NaoFederado'] = len(dict[ano]["NFed"])

        cont['federados'].append(new_ano)

    temps = load_templates('template/federado/', {
        'federadoPorAno': 'row.html',
        'main': 'index.html'
    })

    w = open('www/federado/estatuto_federado.html', "w")
    res = template(cont, "main", temps)
    w.write(res)
    w.close()

def dist_Fed():
    f = open("assets/emd.csv")

    distPorFed = {}

    inde = open("index.html", "w")
    inde.write('<ul>\n')
    inde.write(
        f'<li><a href="www/federado/estatuto_federado.html">Estatuto de Federado</a></li>\n')

    for l in f:
        m = re.match(reg, l)
        if m:
            data = datetime.strptime(m.group("date"), "%Y-%m-%d").date()
            j = Jogador(m)

            # Se não existir o ano no dicionário, adiciona a vazio
            if not distPorFed.__contains__(data.year):
                distPorFed[data.year] = {"Fed": [], "NFed": []}

            fed = m.group('fed') == "true"
            # Coloca no respetivo array, caso tenha estatuto de federado e caso não tenha
            if fed:
                distPorFed[data.year]["Fed"].append(j.id)
            else:
                distPorFed[data.year]["NFed"].append(j.id)

    # Função para escrever a distribuição por federado
    generate_fed(distPorFed)

    inde.write('</ul>')
    inde.close()
    f.close()


dist_Fed()
