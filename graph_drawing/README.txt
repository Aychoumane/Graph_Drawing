ICHOU Aymane 

######## Projet tuteuré : Dessin de graphe avec l'algorithme de force dirigé. ########

Ce projet est constitué de plusieurs fichiers : 
- Le répertoire csv, qui va venir stocker les fichiers lorsque l'utilisateur va faire un export. 

- Le script "set_config.py" , qui va venir modifier le contenu du fichier "config.txt" .
	Ce script va simplifier la configuration du programme directed_force.
	La config est constitué de deux éléments : edit_mode et identifiant de fichier.
		-edit_mode : 0 pour désactiver, et 1 pour l'activer. 
		-identifiant de fichier : c'est la partie variable du nom de fichier lors de l'export pour
								  garder plusieurs résultats, et ne pas écraser les fichiers existants. 


- Le script "gen_graph.py", il va venir générer un graphe, et écrire dans le fichier "generated_graph.txt" . 
	La ligne de commande pour le lancer : 
		python3 gen_graph <nb_noeud>

	<nb_noeud> représente le nombre de noeud souhaité dans le graphe. Les arêtes seront crées à partir du hasard. 
	De manière simplifié, nous prenons la valeur 1/nb_noeud, nous tirons un nombre aléatoire, et si le nombre 
	tiré est inférieur à cet probabilité, l'arête va être crée. Ce test est effectué depuis tous les noeuds, vers
	tous les noeuds. 


- Et enfin le fichier principal, "directed_foce.py", c'est le programme qui va lire le fichier "generated_graph.txt", 
  calculer l'ensemble des forces répulsives et attractives entre chacun des points, ouvrir une interface à
  l'utilisateur et faire jouer l'animation. 
  	La ligne de commande pour le lancer : 
		python3 graph_drawing <nb_iterations> <cooling_factor>
		nb_iteration : Nombre de fois où les forces vont être calculé entre chacun des points
		cooling_factor : Autrement appelé facteur de refroidissement, c'est un coefficient qui va venir 
						 amenuiser les déplacements liés à l'application des forces. Il doit être inférieur à 1 strictement. Selon le nombre de noeud donné, certaines valeurs peuvent être trop grande, l'erreur sera affiché dans le terminal, et vous aurez besoin de changer de valeur.

	Durant l'animation, des entrées claviers sont disponible : 
		- Touche de la barre d'espace : Mettre en pause/Lire l'animation.
		- La touche t : Si l'animation est en pause, appuyer dessus termine/ met fin à l'animation.
		- la touche e : Si l'animation est terminé, cela permet l'export des points ainsi que leurs positions dans un 
		                fichier .csv
		- la touche m : Si le mode editeur est activé, cela permet la transposition de la fenêtre principal, à la
						fenêtre éditeur. Seulement si l'animation principale est en pause. 
 
 	Subtilité : Veillez à bien cliquer sur la fenêtre sur laquelle vous souhaitez appliquer une touche. 

 	Le mode éditeur : qu'est ce que c'est ? 
 		Tout d'abord, pour l'activer il faut mettre la valeur à 1 lors de la configuration avec "set.config.py".
 		Ce mode va permettre l'ouverture d'une deuxième fenêtre en arrière plan. 
 		Dans cette fenêtre, l'utilisateur va pouvoir peaufiner le résultat à ses goûts en ayant la possibilité de déplacer les noeuds avec son curseur. Il faudra maitenir le clic gauche sur un noeud, puis le déplacer et relâcher le clic à l'endroit souhaité. 
 		Dans ce mode, l'export est illimité et n'est pas figé à un seul résultat comme dans le mode classique. 
 		Le fichier exporté apparaitra avec un nom de fichier différent en ayant "modified", avant le nom. 


 	Bon amusement ! 

 	TIPS : Si le graphe possède peu de noeuds, le nombre d'itérations va être petit, et le facteur de refroidissement grand, et plus le graphe possède des noeuds, plus il faudra augmenter le nombre d'itérations et diminier le cooling factor. Mais cela n'est pas toujours vrai :) 