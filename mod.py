from athl import *

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