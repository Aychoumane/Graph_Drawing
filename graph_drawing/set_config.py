#Ichou Aymane 
#Fichier pour configurer le fichier config.txt 

name_config_file = "config.txt"

print("### Configuration du fichier config ###")

# Vérification du mode éditeur
edit_mode = input("Souhaitez-vous activer le mode éditeur: 1 = oui / 0 = non \n")
while edit_mode != '0' and edit_mode != '1':
    print("Erreur ! Entrez une valeur valide pour le mode éditeur : 1 = oui / 0 = non ")
    edit_mode = input("")

# Vérification de l'identifiant
while True:
    indicatif = input("Entrez l'ID (nombre entier positif) à partir duquel vos fichiers seront nommés: \n")
    try:
        indicatif = int(indicatif)
        if indicatif < 0:
            raise ValueError("L'identifiant ne peut pas être inférieur à 0")
        break  # Sortir de la boucle si l'entrée est valide
    except ValueError as e:
        print(f"La valeur donnée n'est pas bonne:\n{e}")

#Ecriture dans le fichier config 
with open(name_config_file, 'w') as fichier:
	fichier.write(f"identifiant de fichier = {indicatif}\n")
	fichier.write(f"edit mode = {edit_mode}")