from athl import *

distPorMorada = {}

def read_Morada(j :Jogador, morada : str) -> dict:
    if not distPorMorada.__contains__(morada):
        distPorMorada[morada] = []
    distPorMorada[morada].append(j.id)
    return distPorMorada

def generate_DistMoradas(jogadores, inde):

    cont = {}
    cont['rows'] = []
    for morada in sorted(distPorMorada):
        # Ref moradores
        generate_Index(distPorMorada[morada], jogadores,
                       "www/locais/local_{}.html".format(morada))

        new_morada = {'Morada': morada}
        new_morada['MoradoresRef'] = '"www/locais/local_{}.html"'.format(morada)
        new_morada['Moradores'] = len(distPorMorada[morada])
        cont["rows"].append(new_morada)

    temps = templates.load_templates('template/moradas/',
                                     {
                                         'rowMoradaTemp': 'row.html',
                                         'main': 'index.html'
                                     })

    res = templates.template(cont, "main", temps)
    #w = open("moradas.html", "w")
    inde.write(res)
    #w.close