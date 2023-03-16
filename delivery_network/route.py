from graph import graph_from_file

def route_from_file(filename):
    """ La fonction prend un fichier routes.nombre.in en entrée et crée 
    un fichier routes.nombre.out dans le sous-dossier output dans lequel
    le numéro sur chaque ligne correspond à la puissance minimale pour 
    couvrir le trajet
    """
    with open(filename, "r") as file:
        liste = list(file)
        for k in range(len(liste)):
            liste[k] = liste[k].split()
    
    with open(filename.replace("in", "out"), 'w') as file2:
        premiere_ligne = f"le fichier {filename} est composé de {int(liste[0][0])} trajets\n"
        file2.write(premiere_ligne)
        for k in range((len(liste))):
            if len(liste[k]) == 3:
                src, dest, utilite = liste[k]
                file2.write(str(graph_from_file(filename.replace("routes", "network")).min_power(int(src), int(dest))[1]) + "\n")