from datetime import datetime
from modules.athl import *
from modules.globals import create_folder_output, get_output

distPorMod = {}
modalidades = []

def read_Mod(j : Jogador):
    data = j.date
    mod = j.modalidade
    if not distPorMod.__contains__(data.year):
        distPorMod[data.year] = {}
    if not distPorMod[data.year].__contains__(mod):
        distPorMod[data.year][mod] = []
    distPorMod[data.year][mod].append(j.id)
    if not modalidades.__contains__(mod):
        modalidades.append(mod)

        
def generate_DistMod(jogadores):
    '''
    _modalidades: { ano: { modalidade: [ids_jog] } }
    '''
    output = get_output()
    file_name = 'modalidade'
    create_folder_output(file_name)
    cont = {}  # conteudo html
    cont['anos_header'] = []
    for ano in sorted(distPorMod):
        cont['anos_header'].append(ano)

    cont['rows'] = []

    for mod in sorted(modalidades):
        temp = {'mod': mod}
        temp['colls'] = []
        for ano in sorted(distPorMod):
            new_ano = {'ano': ano}
            if not distPorMod[ano].__contains__(mod):
                l = 0
            else:
                l = len(distPorMod[ano][mod])

            if (l != 0):
                generate_Index(
                    distPorMod[ano][mod], jogadores, f"{output}/{file_name}/{mod}_{ano}.html")

            new_ano['total'] = l
            new_ano['ref'] = f'{file_name}/{mod}_{ano}.html'
            temp['colls'].append(new_ano)
        cont['rows'].append(temp)
    '''
    Estrutura dos dados para templating
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
    temps = templates.load_templates(f'template/{file_name}/',
                                     {
                                         'ano_colunas': 'ano_colunas.html',
                                         'row': 'row.html',
                                         'column_row': 'column_row.html',
                                         'main': 'index.html'
                                     })

    w = open(f"{output}/{file_name}.html", "w")
    res = templates.template(cont, "main", temps)
    w.write(res)
    w.close()
    return res
