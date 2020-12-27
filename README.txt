###############################################
#        Projet IA JEUX DE GO 2020            #
#                                             #
#          Duplantier Louis, Gr2              #
#          Flegon Valentin, Gr5               #
###############################################

##################################################################################################################

    Bonjour voici notre projet d'Intelligence Artificielle,
portant sur le jeu de Go. Dans ce projet il a fallu implémenter un 
joueur de Go capable de rivaliser avec les autres IA de la promotion M1 informatique.
Nous espérons que notre IA puisse arriver à bien se classer lors du tournoi.

Nous avons alors principalement du coder une heuristique ainsi qu'un
algorithme capable de trouver le meilleur coup à jouer afin de remporter 
la partie. Nous avons essayé Iterative Deepening ou d'autre algorithme comme Monte-Carlo,
qui même s'il aurait pu nous permettre de mieux jouer cela était plus complexe à mettre en place,
sans forcément apporter un gros changement sur la façon de jouer.

# Heuristique
        Nous avons choisi de coder une heuristique plutôt simple mais relativement efficace,
    nous nous sommes inspiré du livre "Deep Learning and the Game of Go" de Max Pumperla et Kevin Ferguson.
    Cette heuristique calcule la différence entre le nombre de pierre noire et blanche sur le plateau de jeu,
    Ce qui nous donne le nombre de pierre capturé. Ainsi ça retourne la différence ou -1*différence,
    selon qui l'appel.
    Nous avions également d'autres idées d'heuristique plus complexe voir dans myPlayer.py


# AlphaBeta
        Pour notre algorithme nous sommes partie sur AlphaBeta qui relativement
    simple et fonctionne bien. Nous avons commencé par faire minimax, il moins efficace que 
    AlphaBeta mais les deux algorithmes utilisent une base commune.
    On procède de la façon suivante, on donne pour valeur moins l'infini à alpha et plus l'infini à beta.
    Ensuite on boucle sur tous les mouvements légaux et on applique ce mouvement à notre plateau, 
    ce qui va nous donner un nouveau plateau de jeu.
    On appelle récursivement sur AlphaBeta_rec avec le nouveau plateau et une profondeur en moins.
    Ensuite en sortant de cet appel récursif on retire le coup joué et on cherche le meilleur coup
    à jouer en fonction de l'heuristique retourné par AlphaBeta_rec. 
    On peut couper si alpha est supérieur ou égal à beta, ce qui va faire gagner énormement de temps et de coup, 
    chose que minimax ne fait pas.

# AlphaBeta_rec
        Cette fonction est très similaire à AlphaBeta, mais elle vérifie si la profondeur
    n'est pas égale à zéro ou si la partie n'est pas fini, dans ce cas on retourne un  appel la fonction
    heuristique sur  le plateau tel qu'il est à ce moment-là. 
    Ce qui va nous faire remonter dans nos appels récursifs.


# Add 
        De plus il est possible d'améliorer notre heuristique en utilisant du deeplearning,
    afin de nous retourner une prédiction du plateau la plus juste possible.



Merci d'avoir pris le temps d'évaluer notre projet et espérant qu'il soit à la hauteur de vos espérances.
De joyeuse fête et une bonne année 2021.
Cordialement Louis et Valentin.

##################################################################################################################

================================
EXEMPLES DE LIGNES DE COMMANDES:
================================

python3 localGame.py
--> Va lancer un match myPlayer.py contre myPlayer.py

python3 namedGame.py myPlayer randomPlayer
--> Va lancer un match entre votre joueur (NOIRS) et le randomPlayer
 (BLANC)

 python3 namedGame gnugoPlayer myPlayer
 --> gnugo (level 0) contre votre joueur (très dur à battre)


