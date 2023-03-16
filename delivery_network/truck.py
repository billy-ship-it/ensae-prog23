class Truck:
    def __init__(self, trucks):
        self.truck = dict([(n, []) for n in range(1, trucks + 1)])
        self.nb_trucks = trucks

    def __str__(self):
        if not self.truck:
            output = "le catalogue est vide"
        else:
            output = f"le catalogue est composé de {self.nb_trucks} camion(s).\n"
            for numero, caracteristique in self.truck.items():
                output += f"camion {numero} --> p = {caracteristique[0]}, c = {caracteristique[1]}\n"
        return output



def truck_from_file(filename):
    """ créer un dictionnaire avec pour clés les catégories de camions et en arguments la puissance et le 
    coût du camion

    La fonction prend en entrée des fichiers du type trucks.nombre.in
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        for k in range(len(lines)):
            lines[k] = lines[k].split()
            for j in range(len(lines[k])):
                lines[k][j] = int(lines[k][j])
        nombre_camions = lines[0][0]
        t = Truck(nombre_camions)
        for k in range(1, nombre_camions + 1):
            t.truck[k] = tuple(lines[k])
        return t