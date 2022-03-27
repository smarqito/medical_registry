from modules.athl import *
from modules.globals import create_folder_output, get_output


distPorIdade = {"MaisOuIgual35": {"M": [], "F": []},
                "Menos35": {"M": [], "F": []}}

def read_Idade(j : Jogador, idade : int, genero : str) -> dict:
    if idade >= 35:
        distPorIdade["MaisOuIgual35"][genero].append(j.id)
    else:
        distPorIdade["Menos35"][genero].append(j.id)
    return distPorIdade

def generate_IdadeGen(jogadores):
    output = get_output()
    file_name = 'idade'
    create_folder_output(file_name)

    # Ref Masculino >=35
    generate_Index(distPorIdade["MaisOuIgual35"]
                   ["M"], jogadores, f"{output}/{file_name}/mais35Masc.html")

    # Ref Masculino < 35
    generate_Index(distPorIdade["Menos35"]["M"], jogadores, f"{output}/{file_name}/menos35Masc.html")

    # Ref Feminino >=35
    generate_Index(distPorIdade["MaisOuIgual35"]
                   ["F"], jogadores, f"{output}/{file_name}/mais35Fem.html")

    # Ref Feminino < 35
    generate_Index(distPorIdade["Menos35"]["F"], jogadores, f"{output}/{file_name}/menos35fem.html")

    # Substituções das tags do template
    cont = {}
    cont['Mais35refM'] = f'"{output}/{file_name}/mais35Masc.html"'
    cont['Mais35TotalM'] = len(distPorIdade["MaisOuIgual35"]["M"])
    cont['Mais35refF'] = f'"{output}/{file_name}/mais35Fem.html"'
    cont['Mais35TotalF'] = len(distPorIdade["MaisOuIgual35"]["F"])

    cont['Mais35Total'] = len(
        distPorIdade["MaisOuIgual35"]["M"]) + len(distPorIdade["MaisOuIgual35"]["F"])
    cont['Menos35refM'] = f'{output}/{file_name}/menos35Masc.html"'
    cont['Menos35TotalM'] = len(distPorIdade["Menos35"]["M"])
    cont['Menos35refF'] = f'{output}/{file_name}/menos35Fem.html"'
    cont['Menos35TotalF'] = len(distPorIdade["Menos35"]["F"])
    cont['Menos35Total'] = len(
        distPorIdade["Menos35"]["M"]) + len(distPorIdade["Menos35"]["F"])

    temps = templates.load_templates(f'template/{file_name}/',
                                     {
                                         'main': 'index.html'
                                     })

    res = templates.template(cont, "main", temps)
    w = open(f"{output}/{file_name}.html", "w")
    w.write(res)
    w.close
