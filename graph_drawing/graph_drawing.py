#Ichou Aymane 
#Programme qui s'occupe de la lecture du graphe

#Ligne de commande python3 gen_graph.py && python3 read_graph.py

# -----------------Imports--------------------- 
import matplotlib.pyplot as plt
import copy
import random
import math 
import sys
from dataclasses import dataclass
#from collections import defaultdict
from matplotlib.animation import FuncAnimation
import csv

# --------------- Classes----------------------- 
@dataclass
class Vec2:
    x : float 
    y : float 

@dataclass
class Point:
    x : float 
    y : float 


if len(sys.argv) != 3:
    print("Usage: python3 read_graph.py <nombre_d'itérations> <cooling_factor>")
    sys.exit(1)

#Renvoie l'id present + edit_mode dans le fichier config 
def get_config(name_config_file):
	with open(name_config_file, 'r') as fichier:
		lignes = fichier.readlines()
		ligne = lignes[0].split()
		num_fichier = int(ligne[4])
		ligne = lignes[1].split()
		edit_mode = int(ligne[3])

	with open(name_config_file, 'w') as fichier:
		fichier.write(f"identifiant de fichier = {num_fichier + 1}\n")
		fichier.write(f"edit mode = {edit_mode}")

	return (str(num_fichier),int(edit_mode))

# Classe pour rendre les points déplaçables
class DraggablePoints:
    def __init__(self, ax, node_positions, edges):
        self.ax = ax
        self.node_positions = node_positions
        self.edges = edges
        self.selected_node = None

        self.points = ax.plot(
            [pos[0] for pos in node_positions.values()],
            [pos[1] for pos in node_positions.values()],
            'o', markersize=12, markerfacecolor='skyblue', markeredgecolor='red'
        )[0]
        
        self.texts = [ax.text(pos[0], pos[1], node, ha='center', va='center', fontsize=7)
                      for node, pos in node_positions.items()]
        
        self.lines = [ax.plot([node_positions[start][0], node_positions[end][0]],
                              [node_positions[start][1], node_positions[end][1]], 'k-', linewidth=0.85)[0]
                      for start, end in edges]

        self.press = self.points.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.release = self.points.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.motion = self.points.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        #self.export = self.points.figure.canvas.mpl_connect('button_press_event', self.on_export)

    def on_press(self, event):
        if event.inaxes != self.ax: return
        if event.button != 1: return  # Left mouse button
        contains, attr = self.points.contains(event)
        if not contains: return
        x, y = event.xdata, event.ydata
        self.selected_node = min(self.node_positions.keys(),
                                 key=lambda node: (self.node_positions[node][0] - x) ** 2 + (self.node_positions[node][1] - y) ** 2)

    def on_motion(self, event):
        if self.selected_node is None: return
        if event.inaxes != self.ax: return
        if event.button != 1: return  # Left mouse button
        self.node_positions[self.selected_node] = (event.xdata, event.ydata)
        self.update_plot()

    def on_release(self, event):
        self.selected_node = None

    def update_plot(self):
        all_x = [pos[0] for pos in self.node_positions.values()]
        all_y = [pos[1] for pos in self.node_positions.values()]
        self.ax.set_xlim(min(all_x) - 20, max(all_x) + 20)
        self.ax.set_ylim(min(all_y) - 20, max(all_y) + 20)
        self.points.set_data(
            [pos[0] for pos in self.node_positions.values()],
            [pos[1] for pos in self.node_positions.values()]
        )
        for text, (node, pos) in zip(self.texts, self.node_positions.items()):
            text.set_position(pos)
        for line, (start, end) in zip(self.lines, self.edges):
            line.set_data([self.node_positions[start][0], self.node_positions[end][0]],
                          [self.node_positions[start][1], self.node_positions[end][1]])
        #self.ax.figure.canvas.draw()
        self.ax.figure.canvas.draw()


# -------------Variables globales---------------
name_file = "generated_graph.txt"
name_config_file = "config.txt"
liste_gauche = []
liste_droite = []
_nb_iterations = int(sys.argv[1])
_cooling_factor = float(sys.argv[2])
animation_paused = False
animation_finish = False 
_frame_actuelle = None 
_is_modified = False 
edit_mode = get_config(name_config_file)[1]


if(edit_mode):
	print("Mode édition activé")
else:
	print("Mode édition désactivé")

while(_cooling_factor >= 1): 
	print("Le facteur de refroidissement doit être inférieur à 1 strictement.")
	_cooling_factor = float(input("Erreur : Entrez un cooling_factor inférieur à 1 !\n"))

#---------------Constantes----------------------
_c_rep = 2
_c_spring = 1
_l = 4 

#--------------Fonctions------------------------
#Création d'un csv dans la fenêtre principale
def create_csv(positions_history,frame,chemin) :
	data = [
	['noeud', 'x' , 'y']
	]
	for cle, valeur in positions_history[frame].items():
		temp = []
		temp.append(int(cle))
		temp.append(round(float(valeur[0]), 2))
		temp.append(round(float(valeur[1]), 2))
		data.append(temp)
	#print(data)

	# Écriture des données dans le fichier CSV
	with open(chemin, 'w', newline='') as fichier:
	    writer = csv.writer(fichier)
	    writer.writerows(data)
	print(f"Fichier CSV nommée \"{chemin}\" a été créé avec succès.")

#Création d'un csv dans la fenêtre éditeur 
def create_csv2(dico_positions,chemin) :
	data = [
	['noeud', 'x' , 'y']
	]
	for cle, valeur in dico_positions.items():
		temp = []
		temp.append(int(cle))
		temp.append(round(float(valeur[0]), 2))
		temp.append(round(float(valeur[1]), 2))
		data.append(temp)
	print(data)

	# Écriture des données dans le fichier CSV
	with open(chemin, 'w', newline='') as fichier:
	    writer = csv.writer(fichier)
	    writer.writerows(data)
	print(f"Fichier CSV nommée \"{chemin}\" a été créé avec succès.")


#Calcule un vector entre deux points
#Je veux le vecteur uv, je donne les co de u puis de v , pas besoin d'inverser 
def compute_vector(xu , yu , xv, yv):
	xuv = xv - xu 
	yuv = yv - yu
	vec = Vec2(x = xuv , y = yuv)
	return vec 
	
#Multiplication entre un coefficient et un vecteur, et renvoie un vecteur
def mul_vector(coefficent, vecteur : Vec2):
	vecteur.x = vecteur.x * coefficent 
	vecteur.y = vecteur.y * coefficent
	return vecteur 

#Renvoie un float
def norme_vector(vecteur : Vec2): 
	return math.sqrt(vecteur.x**2 + vecteur.y ** 2)

#Renvoie un float 
def norme_vector_wo_sqrt(vecteur : Vec2): 
	return vecteur.x**2 + vecteur.y ** 2

#Addition deux vecteurs, et renvoie un vecteur
def sum_2_vec (vecteur_a : Vec2 , vecteur_b : Vec2): 
	vecteur_res : Vec2 = Vec2(0 , 0)
	vecteur_res.x = vecteur_a.x + vecteur_b.x 
	vecteur_res.y = vecteur_a.y + vecteur_b.y
	return vecteur_res 

#Prends deux listes de tailles égales, et crée un dictionnaire d'adjacence
def get_all_adjacence(elem_gauche, elem_droit): 
	new_list = []
	dico_res = dict()

	#On veut que la donné doit (noeud, liste_adjacence)
	for elem in all_nodes : 
		temp = (elem, [])
		new_list.append(temp)

	#On vérifie l'unicité avant d'ajouter
	for elem in new_list : 
		for i in range(0, len(elem_gauche)):
			if(elem_gauche[i] == int(elem[0])): 
				elem[1].append(elem_droit[i][0])

	#Ajout des éléments dans le dico 
	for elem in new_list : 
		dico_res[elem[0]] = elem[1]

	print("Concaténation des adjacences : \n " , dico_res)
	# print("new_list vaut : " , new_list)
	return dico_res 
		
#Fonction de répulsion, prends 2 points et renvoie un vecteur 
def f_rep(u : Point , v : Point) : 
	vecteur_vu: Vec2 = compute_vector(v.x , v.y , u.x , u.y)
	coefficent = _c_rep / norme_vector_wo_sqrt( vecteur_vu)
	vecteur_vu = mul_vector( coefficent , vecteur_vu)
	return vecteur_vu

#Fonction d'attractivité, prends 2 points et renvoie un vecteur
def f_spring(u : Point , v : Point) :
	vecteur_uv: Vec2 = compute_vector(u.x , u.y , v.x , v.y)
	vecteur_vu: Vec2 = compute_vector(v.x , v.y , u.x , u.y)

	distance_eucl = norme_vector(vecteur_vu)
	mid_part = distance_eucl / _l 
	mid_part = math.log(mid_part,10)
	left_part = _c_spring * mid_part 

	resultat : Vec2 = mul_vector(left_part , vecteur_uv)
	return resultat 


#On calcule la somme des forces attractives associé à un point, le point donné est un str
#La force attractive provient de tous les points qui ont une arete avec un point donné 
#et Renvoie un vecteur 
def sum_fspring_to_1_point(dico_positions , dico_vertices , noeud): 

	# print("Notre noeud actuel : ", noeud)

	# On get les noeuds liés à notre noeud  
	liste_connected_vertices = dico_vertices.get(noeud)

	# On récupere les positions dans le dictionnaire de notre point 
	noeud_position = dico_positions.get(noeud)
	# On crée notre point 
	point_noeud = Point(noeud_position[0], noeud_position[1])

	vecteur_resultat = Vec2(0, 0)

	for vertices in liste_connected_vertices : 
		temp_noeud = dico_positions.get(str(vertices))
		temp_point = Point(temp_noeud[0], temp_noeud[1])
		temp_res = f_spring(point_noeud , temp_point)
		vecteur_resultat = sum_2_vec(vecteur_resultat, temp_res)

	return vecteur_resultat



#On calcule la somme des forces répulsives associé à un point
#La force répulsive provient de tous les points qui n'ont pas d'arete avec un point donné 
#et Renvoie un vecteur 
def sum_frep_to_1_point(dico_positions , dico_vertices , liste_all_point , noeud): 

	# print("Notre noeud actuel : ", noeud)

	# On get les noeuds liés à notre noeud  
	liste_connected_vertices = dico_vertices.get(noeud)

	# Création d'une str liste, on exclue les points qui sont liés avec notre point 
	liste_disconnected_points = [element for element in liste_all_point if int(element) not in liste_connected_vertices]
	liste_disconnected_points.remove(noeud)

	# On récupere les positions dans le dictionnaire de notre point 
	noeud_position = dico_positions.get(noeud)

	# On crée notre point 
	point_noeud = Point(noeud_position[0], noeud_position[1])
	vecteur_resultat = Vec2(0, 0)

	#On calcule toutes les forces pour les points déconnectés 
	for vertices in liste_disconnected_points : 
		temp_noeud = dico_positions.get(vertices)
		temp_point = Point(temp_noeud[0], temp_noeud[1])
		temp_res = f_rep(point_noeud, temp_point)
		vecteur_resultat = sum_2_vec(vecteur_resultat, temp_res)

	return vecteur_resultat


#Fonction principal qui calcule l'ensemble des états, où un état est l'ensemble du graphe 
def directed_force(node_positions, dic_adjacences, all_nodes, iterations, cool_factor): 
	print("Longueur de all nodes : ", len(all_nodes))
	tour = 1 
	positions_history = []


	pourcentage = 0 
	dic_pos_copy = copy.deepcopy(node_positions)
	while( tour < iterations ): 
		try : 
			liste_force = []
			for node in all_nodes : 
				temp = sum_2_vec(sum_frep_to_1_point(dic_pos_copy , dic_adjacences , all_nodes, node),
				              sum_fspring_to_1_point(dic_pos_copy , dic_adjacences ,node)) 
				liste_force.append(temp)

			for i in range(0, len(all_nodes)): 
				temp = dic_pos_copy.get(all_nodes[i])
				node_temp = Vec2(temp[0], temp[1])
				node_temp = sum_2_vec( node_temp , mul_vector(cool_factor, liste_force[i]) ) # 0.01 ou 0.001
				dic_pos_copy[all_nodes[i]] = (node_temp.x, node_temp.y)

			positions_history.append(copy.deepcopy(dic_pos_copy))
			tour += 1 
			pourcentage = (tour / iterations) * 100
			if( pourcentage % 1 == 0):
				print(f"Calcul à : {pourcentage} %" )
		except Exception as e : 
			print(f"Erreur: La valeur donnée ({cool_factor}) pour le facteur de refroidissement est trop grande :")
			quit()
	return positions_history



#------Fonctions d'évènements et animations-------------------

# Fonction pour mettre en pause ou reprendre l'animation
def read_or_pause(event):
    global animation_paused
    global animation_finish
    if event.key == ' ' and animation_finish == False:	
        if animation_paused:
            ani.event_source.start()
            animation_paused = False
            print("Animation relancé.")
        else:
            ani.event_source.stop()
            animation_paused = True
            print("Animation mise en pause.")
    if event.key == ' ' and animation_finish == True:
    	print("Vous avez mis fin à l'animation.")

#Fonction event qui met fin à l'animation et l'arrête complètement sans pouvoir recommencer
def finish_animation(event): 
	global animation_finish
	global animation_paused
	if event.key == 't' and animation_paused == True and animation_finish == False :
		ani.event_source.stop()
		on_animation_end()
		print("Animation coupé et terminée")
		fig.canvas.mpl_disconnect(read_or_pause)
		
#Fonction event qui permet l'export en fichier csv de la frame sur laquel l'animation a été arrêté 
def export(event):
	global animation_finish 
	global _frame_actuelle 
	global positions_history 
	global _is_modified 
	if event.key == 'e' and animation_finish == True:
		print("Exportation du graphe en fichier csv.")
		if(_is_modified == False): 
			create_csv(positions_history, _frame_actuelle, "./csv/graph_" + get_config(name_config_file)[0] + ".csv")
		else:
			pass
			#Recuperer l'état du graphe selon les modif du user 
	if event.key == 'e' and animation_finish == False:
		print("Il faut terminer l'animation si vous souhaitez exporter !")

#Fonction d'export pour la deuxieme fenetre 
def export2(event):
		if event.key == 'e':
			print("Exportation du graphe modifié en fichier csv.")
			if(_is_modified == False): 
				create_csv2(draggable.node_positions, "./csv/modified_graph_" + get_config(name_config_file)[0] + ".csv")



#Callback appelé à chaque rafraîchissement de page 
def update(frame):
	ax.clear()
	global _frame_actuelle
	current_positions = positions_history[frame]
	for edge in edges:
		start_node, end_node = edge
		start_pos, end_pos = current_positions[start_node], current_positions[end_node]
		ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], 'k-')
	for node, pos in current_positions.items():
		ax.plot(pos[0], pos[1], 'o', markersize=12, markerfacecolor='skyblue', markeredgecolor='red')
		ax.text(pos[0], pos[1], node, ha='center', va='center', fontsize=7)


	ax.axis('equal')
	ax.axis('off')
	_frame_actuelle = frame 

	if frame == len(positions_history) - 1:
		on_animation_end()
	else : 
		pourcentage_animation = frame / len(positions_history) * 100
		print("Animation à : %.3f " % pourcentage_animation , "%" )

#Fonction appelé à la fin de l'animation 
def on_animation_end() : 
	print("Animation terminée !")
	global animation_finish 
	animation_finish = True

#Fonction event qui met fin à l'animation et l'arrête complètement sans pouvoir recommencer
def modify(event): 
	global animation_finish
	global animation_paused
	global draggable
	global _frame_actuelle
	global edit_mode
	if event.key == 'm' and  (animation_paused == True or animation_finish) and edit_mode != 0:
		print("Transposition dans la fenêtre éditeur.")
		draggable.node_positions = positions_history[_frame_actuelle]
		draggable.update_plot()
	if event.key == 'm' and  animation_paused == True and edit_mode == 0:
		print("Erreur: Veuillez activer le mode édit dans le fichier config.")

#-------------------MAIN---------------------

#Lecture du fichier contenant le graphe
with open(name_file, 'r') as fichier:
	#A chaque ligne du fichier
	lignes = fichier.readlines()
	if len(lignes) >= 2:
		for i in range(0, len(lignes) -1):
			# Divise la ligne en fonction de  "->"
			parties = lignes[i].split("->")
			# Récupérer les informations à gauche et à droite de la flèche
			gauche = parties[0]
			droite = parties[1].split()

			# print("gauche vaut " , gauche)
			gauche = int(gauche)
			droite = list(map(int, droite))

			liste_gauche.append(gauche)
			liste_droite.append(droite)

	nb_noeud = int(lignes[-1].split()[3])

print(f"Le nombre de noeud trouvé est {nb_noeud}")
for i in range(0,len(liste_gauche)):
	print(f" {liste_gauche[i]} -> {liste_droite[i]} ")

#A cet etape, liste_gauche contient tout les noeuds possible 
#Et liste_droite des listes des liaisons, et les deux sont complémentaire à un certain indice
#exemple liste_gauche[0] , est le noeud parent, liste_droite[0] sont ses enfants



# On converti nos données par qlq chose lisible par matplotlib
left_nodes = list(map(str,liste_gauche))
all_nodes = []

#On récupère de manière unique chaque noeud 
for elem in left_nodes : 
	if (elem not in all_nodes) : 
		all_nodes.append(elem)

edges = []

#Sécurité : Vérification qu'il n'existe pas de noeud à droite qui n'est pas à gauche
for liste in liste_droite:
	for element in liste:
		element = str(element)
		if(element not in left_nodes):
			all_nodes.append(element)
			# print("ajout element")

print("all nodes" , all_nodes)
# print(left_nodes)

#On crée les arêtes allant d'un liste_gauche[i] à liste_droite[i]
for i in range(0, len(left_nodes)): 
	#Ca sert a rien de tracer deux fois le meme edge, une fois suffit 
	if((str(liste_droite[i][0]), left_nodes[i]) not in edges) : 
		edges.append((left_nodes[i], str(liste_droite[i][0])))
		# print("nodes vaut : ", nodes[i])
		# print("liste droite vaut : ", liste_droite[j])

print("egdes vaut : " ,edges)

#Calcul des positions des noeuds de manières aléatoires
node_positions = dict()
for string in all_nodes:
	x = round(random.uniform(0.00001, nb_noeud), 1)
	y = round(random.uniform(0.00001, nb_noeud), 1)
	node_positions[string] = (x , y)

#print("node pos " , node_positions)


#Dictionnaire contenait un noeud en clé , et liste de noeuds lié à ce noeud en valeur 
dic_adjacences = get_all_adjacence(liste_gauche, liste_droite)

#Renvoie toutes les positions calculé par la fonction 
#Une position est l'ensemble des points à un tour donné 
positions_history = directed_force(node_positions, dic_adjacences, all_nodes, _nb_iterations, _cooling_factor)

# Initialisation du tracé
if(edit_mode):
	fig2, ax2 = plt.subplots()
	plt.title("Noeuds déplaçables")
	draggable = DraggablePoints(ax2, positions_history[0], edges)

	fig2.canvas.mpl_connect('key_press_event', export2)
	plt.axis('equal')
	plt.axis('off')


#init fig
fig, ax = plt.subplots()

#Fonction d'animation 
ani = FuncAnimation(fig, update, frames=len(positions_history), interval= 5, repeat=False)

# Association des fonctions de gestion d'événements à la figure
if(animation_finish == False):
	fig.canvas.mpl_connect('key_press_event', read_or_pause)
fig.canvas.mpl_connect('key_press_event', finish_animation)
fig.canvas.mpl_connect('key_press_event', export)
fig.canvas.mpl_connect('key_press_event', modify)




plt.show()







