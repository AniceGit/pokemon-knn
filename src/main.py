import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/pokemon.csv', header=0, sep=';')
list_pokemons = df.to_dict(orient='records')

def affichage_tableau(liste:list)->None:
    """
    Affiche un graphique ASCII représentant les Pokémon selon leur Attaque et Points de vie.

    Paramètres :
        liste (list) : Liste de dictionnaires contenant les clés 'Attaque' et 'Points de vie'.

    Retour :
        None
    """
    graph = []
    for _ in range(0,200) :
        graph.append([' '] * 120)

    for pokemon in list_pokemons :
        graph[pokemon['Attaque']][pokemon['Points de vie']] = 'x'

    for ligne in graph :
        print(''.join(ligne))

def affichage_seaborn(list_pokemons:list)->None:
    """
    Affiche un nuage de points des Pokémon avec Matplotlib, coloré selon leur type.

    Paramètres :
        list_pokemons (list) : Liste de dictionnaires contenant les clés 'Attaque', 'Points de vie' et 'Type'.

    Retour :
        None
    """
    # Dictionnaire de couleurs par type
    couleurs = {
        'Eau': 'blue',
        'Psy': 'black'
    }
    max_att = 200
    max_hp = 200
    heatmap_matrix = [[0] * max_att for _ in range(max_hp)]
    for pokemon in list_pokemons:
        attack = pokemon['Attaque']
        hp = pokemon['Points de vie']
    
        # Si les valeurs sont dans les limites de la matrice
        if attack < max_att and hp < max_hp:
            heatmap_matrix[attack][hp] += 1

    # Utiliser Seaborn pour afficher une carte de chaleur (heatmap)
    plt.figure(figsize=(12, 8))

    df_pokemons = pd.DataFrame(list_pokemons)
    df_pokemons['Couleur'] = df_pokemons['Type'].map(couleurs)

    for i, row in df_pokemons.iterrows():
        plt.scatter(row['Attaque'], row['Points de vie'], color=row['Couleur'], s=60)

    # Ajouter des labels pour les axes
    plt.title('Distribution des Pokémon selon Attaque et Points de Vie')
    plt.xlabel('Attaque')
    plt.ylabel('Points de vie')
    plt.grid(True)

    # Afficher le graphique
    plt.savefig("img/pokemons.png")


def knn(atk:int, pv:int, k:int=3)-> str:
    """
    Détermine le type prédominant parmi les k pokémons les plus proches en fonction 
    de la différence d'attaque et de points de vie avec un pokémon donné.

    Paramètres:
    atk (int): L'attaque du pokémon à analyser.
    pv (int): Les points de vie du pokémon à analyser.
    k (int, optionnel): Le nombre de voisins à considérer (par défaut, k=3).

    Retourne:
    str: Le type prédominant ('eau' ou 'psy') parmi les k voisins les plus proches.
    """
    list_diff = []
    list_k_types = []

    #on récupère la différence de chaque pokemon de notre pokemon
    for pokemon in list_pokemons:
        diff=0
        for info in pokemon:
            if info == 'Attaque' or info == 'Points de vie':
                diff = (atk - pokemon['Attaque']) + (pv - pokemon['Points de vie'])
                if diff<0:
                    diff = -diff
        list_diff.append((pokemon['Type'], diff))
    list_diff.sort(key=lambda x: x[1])
    
    #on conserve les K données
    for i in range(0,k):
        list_k_types.append(list_diff[i])
    print(f"Les {k} pokémons les plus proches : {list_k_types}")

    #on récupère les occurences de types
    dict_occurences_types = {'Eau':0, 'Psy':0}
    for p in list_k_types:
        if p[0] == 'Eau' :
            dict_occurences_types['Eau'] += 1
        elif p[0] == 'Psy' :
            dict_occurences_types['Psy'] += 1
    print(f"Les types les plus présents autour de notre pokémon : {dict_occurences_types}")
    #on trouve l'occurence la plus élévée
    if dict_occurences_types['Eau'] > dict_occurences_types['Psy'] :
        type_max = 'Eau'
    else :
        type_max = 'Psy'
    return type_max

print("Le type de ce pokémon est : ", knn(48,50,5))

print("="*100)
#affichage_tableau(list_pokemons)

affichage_seaborn(list_pokemons)