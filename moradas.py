from athl import *

def read_Morada(j :Jogador, morada : str) -> dict:
    distPorMorada = {}
    if not distPorMorada.__contains__(morada):
        distPorMorada[morada] = []
    distPorMorada[morada].append(j.id)
    return distPorMorada

def generate_DistMoradas(lista_moradas, jogadores, inde):
    #w = open("moradas.html", "w")

    cont = {}
    cont['rows'] = []
    for morada in sorted(lista_moradas):
        # Ref moradores
        generate_Index(lista_moradas[morada], jogadores,
                       "www/locais/local_{}.html".format(morada))

        new_morada = {'Morada': morada}
        new_morada['MoradoresRef'] = 'local_{}.html"'.format(morada)
        new_morada['Moradores'] = len(lista_moradas[morada])
        cont["rows"].append(new_morada)

    temps = templates.load_templates('template/moradas/',
                                     {
                                         'rowMoradaTemp': 'row.html',
                                         'main': 'index.html'
                                     })

    res = templates.template(cont, "main", temps)
    inde.write(res)
    #w.close