# #Ichou Aymane 
# #Programme qui s'occupe de la génération du graphe

# import random 
# import sys

# if len(sys.argv) != 2:
#     print("Usage: python3 gen_graph.py <nombre_de_noeuds>")
#     sys.exit(1)

# nb_noeud = int(sys.argv[1])	


# name_file = "generated_graph.txt"
# flag_write = True 


# with open(name_file, 'w') as fichier:
	
# 	while(nb_noeud>100 or nb_noeud< 0):
# 		nb_noeud = int(input("Erreur, entrez un nombre correct [0,100] : "))

# 	proba = 1/nb_noeud 
# 	for i in range(0, nb_noeud):
# 		for j in range (0, nb_noeud): 
# 			random_float = random.uniform(0.0, 1.0)
# 			if(random_float < proba and i != j):
# 				print(f"lien crée : {i} à {j}")
# 				if(flag_write == True):
# 					fichier.write(f"{i}->{j}")
					
# 					flag_write = False
# 				else: 
# 					fichier.write(f" {j}")
# 		if(flag_write == False):
# 			fichier.write(f"\n")
# 		flag_write = True

#     #fichier.write("Contenu à écrire dans le fichier\n")
#     # Vous pouvez écrire d'autres lignes ici
# 	print(nb_noeud)
# 	fichier.write(f"Nombre de noeud: {nb_noeud}\n")


	#Ichou Aymane 
#Programme qui s'occupe de la génération du graphe

import random 
import sys

if len(sys.argv) != 2:
    print("Usage: python3 gen_graph.py <nombre_de_noeuds>")
    sys.exit(1)

nb_noeud = int(sys.argv[1])	


name_file = "generated_graph.txt"
flag_write = True 
compt_arete = 0 

with open(name_file, 'w') as fichier:
	
	while(nb_noeud>100 or nb_noeud< 0):
		nb_noeud = int(input("Erreur, entrez un nombre correct [0,100] : "))

	proba = 1/nb_noeud 
	for i in range(0, nb_noeud):
		for j in range (0, nb_noeud): 
			random_float = random.uniform(0.0, 1.0)
			if(random_float < proba and i != j):
				compt_arete += 1 
				print(f"lien crée : {i} à {j}")
				fichier.write(f"{i}->{j}\n")
				print(f"lien crée : {j} à {i}")
				fichier.write(f"{j}->{i}\n")
	
    #fichier.write("Contenu à écrire dans le fichier\n")
    # Vous pouvez écrire d'autres lignes ici
	print("Le nombre est de noeuds est :", nb_noeud,".")
	print(compt_arete, "arêtes ont été crées.")
	fichier.write(f"Nombre de noeud: {nb_noeud}\n")