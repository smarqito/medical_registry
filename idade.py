from athl import *

def read_Idade(j : Jogador, idade : int, genero : str) -> dict:
    distPorIdade = {"MaisOuIgual35": {"M": [], "F": []},
                "Menos35": {"M": [], "F": []}}
    if idade >= 35:
        distPorIdade["MaisOuIgual35"][genero].append(j.id)
    else:
        distPorIdade["Menos35"][genero].append(j.id)
    return distPorIdade

def generate_IdadeGen(lista_generos, jogadores, inde):

    # Ref Masculino >=35
    generate_Index(lista_generos["MaisOuIgual35"]
                   ["M"], jogadores, "www/idade/mais35Masc.html")

    # Ref Masculino < 35
    generate_Index(lista_generos["Menos35"]["M"], jogadores, "www/idade/menos35Masc.html")

    # Ref Feminino >=35
    generate_Index(lista_generos["MaisOuIgual35"]
                   ["F"], jogadores, "www/idade/mais35Fem.html")

    # Ref Feminino < 35
    generate_Index(lista_generos["Menos35"]["F"], jogadores, "www/idade/menos35fem.html")

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
                                         'main': 'index.html'
                                     })

    #w = open("genIdade.html", "w")
    res = templates.template(cont, "main", temps)
    inde.write(res)
    #w.close
