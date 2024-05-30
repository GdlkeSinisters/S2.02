import math
import random
import timeit

import numpy.random as rand


def matriceNumpy(n, a, b):
    M = rand.randint(0, 2, size=(n, n))
    M = M.astype(float)
    for i in range(n):
        for j in range(n):
            if M[i][j] == 0:
                M[i][j] = float('inf')
            else:
                M[i][j] = rand.randint(a, b)
    return M


def matricePNumpy(n, p, a, b):
    M = rand.binomial(1, p, (n, n))
    M = M.astype(float)
    for i in range(n):
        for j in range(n):
            if M[i][j] == 0:
                M[i][j] = float('inf')
            else:
                M[i][j] = rand.randint(a, b)
    return M



def matrice(n, a, b):
    return matricePRandom(n, 0.5, a, b)


def matricePRandom(n, p, a, b):
    G = [[0 for i in range(n)] for i in range(n)]
    # programmation d'un graphe aléatoire pondéré où p des arêtes sont des arêtes de poids 0 et 1 - p des arêtes de
    # poids dans l'intervalle [a,b[
    for i in range(n):
        for j in range(n):
            if random.random() < 1 - p:
                G[i][j] = float('inf')
            else:
                G[i][j] = random.randint(a, b)
    return G


def countPoids0(G):
    n = len(G)
    count = 0
    for i in range(n):
        for j in range(n):
            if G[i][j] != float('inf'):
                count += 1
    return count / n ** 2

def moyennePoidsGraphesNumpy(taille,p):
    a = 2
    b = 10
    moyenne = 0
    for i in range(100):
        G = matriceNumpy(taille, a, b)
        moyenne += countPoids0(G)
    return moyenne / 100

def moyennePoidsGraphesRandom(taille,p):
    a = 2
    b = 10
    moyenne = 0
    for i in range(100):
        G = matrice(taille, a, b)
        moyenne += countPoids0(G)
    return moyenne / 100


def moyennePoidsGraphesProportion(taille, p):
    a = 2
    b = 10
    moyenne = 0
    for i in range(100):
        G = matricePNumpy(taille, p, a, b)
        moyenne += countPoids0(G)
    return moyenne / 100


def affichageMatrice(mat):
    for i in range(len(mat)):
        print(mat[i])


# parcours d'un graphe selon dijkstra
def dijkstra(G, s):
    n = len(G)
    d = [float('inf') for i in range(n)]
    d[s] = 0
    S = []
    u = 0
    while len(S) < n:
        mini = float('inf')
        for i in range(n):
            if i not in S and d[i] < mini:
                mini = d[i]
                u = i
        S.append(u)
        for v in range(n):
            if G[u][v] != float('inf') and d[v] > d[u] + G[u][v]:
                d[v] = d[u] + G[u][v]
    return d


"""
Creer une fonction Python Bellman-Ford(M,d) qui prend en entree la matrice d’un
graphe ponderé a poids de signe quelconque, un sommet d de ce graphe donné par son indice
dans la liste des sommets, et qui, en executant l’algorithme de Bellman-Ford, retourne pour
chacun des autres sommets s :
- soit la longueur et l’itineraire du plus court chemin de d à s ;
- soit la mention ”sommet non joignable depuis d par un chemin dans le graphe G”.
- soit la mention ”sommet joignable depuis d par un chemin dans le graphe G, mais pas
de plus court chemin (presence d’un cycle negatif)”.
On codera à partir du pseudocode presenté dans le cours.
On pourra retourner le resultat sous forme de la liste des sommets du chemin obtenu, mais
aussi en l’affichant graphiquement à l’aide de l’outil d'affichage.
"""


def BellmanFord(M, s):
    n = len(M)
    d = {i: [float('inf'), []] for i in range(n)}
    d[s][0] = 0
    for r in range(n - 1):
        for i in range(n):
            for j in range(n):
                if M[i][j] != float('inf') and d[j][0] > d[i][0] + M[i][j]:
                    d[j][0] = d[i][0] + M[i][j]
                    d[j][1].append(i)
    for i in range(n):
        d[i][1].append(i)
    d = listeSommetEnFlèche(d)
    # detection de cycle negatif
    for h in range(n):
        for i in range(n):
            for j in range(n):
                if d[j][0] == float('inf'):
                    d[j] = "sommet non joignable depuis d par un chemin dans le graphe G"
                elif d[i][0] == float('inf'):
                    d[i] = "sommet non joignable depuis d par un chemin dans le graphe G"
                elif M[i][j] != float('inf') and not isinstance(d[i], str) and not isinstance(d[j], str):
                    # print(f"{j} : {d[j][0]} / {d[i][0] + M[i][j]}")
                    if d[j][0] > d[i][0] + M[i][j] or d[j][0] < 0:
                        d[j] = "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
        # renvoie les chemins
    return d


def parcoursLargeur(mat, s):
    n = len(mat)
    file = [s]
    visites = []
    fleche = []
    visites.append(s)
    while file != []:
        sommet = file.pop(0)
        for i in range(n):
            if mat[sommet][i] != float('inf') and i not in visites:
                visites.append(i)
                fleche.append((sommet, i))
                file.append(i)
    return fleche


def BellmanFordParcours(M, s):
    n = len(M)
    # intialisation du tableau d
    d = {i: [float('inf'), []] for i in range(n)}
    # parcours en largeur de M depuis s
    parcours = parcoursLargeur(M, s)
    # initialisation de d
    d[s][0] = 0
    modif = True
    # boucle principale
    while modif:
        modif = False
        # on parcourt chaque flèche dans le parcours en largeur
        for f in parcours:
            i = f[0]
            j = f[1]
            if d[j][0] > d[i][0] + M[i][j]:
                modif = True
                d[j][0] = d[i][0] + M[i][j]
                for x in d[i][1]:
                    d[j][1].append(x)
                d[j][1].append(i)
    # on ajoute le sommet d'arrivée à chaque chemin
    for i in range(n):
        d[i][1].append(i)
    #detection de cycle negatif
    #d = listeSommetEnFlèche(d)#on passe les sommets en flèche
    for r in range(n - 1):
        for f in parcours:
            i = f[0]
            j = f[1]
            if d[j][0] == float('inf'):
                d[j] = "sommet non joignable depuis d par un chemin dans le graphe G"
            elif d[i][0] == float('inf'):
                d[i] = "sommet non joignable depuis d par un chemin dans le graphe G"
            elif M[i][j] != float('inf') and not isinstance(d[i], str) and not isinstance(d[j], str):
                # print(f"{j} : {d[j][0]} / {d[i][0] + M[i][j]}")
                if d[j][0] > d[i][0] + M[i][j] or d[j][0] < 0:
                    d[j] = "sommet joignable depuis d par un chemin dans le graphe G, mais pas de plus court chemin (presence d’un cycle negatif)"
    return d


#on convertit une liste de sommet en flèche
def listeSommetEnFlèche(d):
    n = len(d)
    # on parcourt chaque sommet
    for i in range(n):
        # on initialise la liste de flèche
        line = []
        #on parcourt chaque flèche
        for x in range(len(d[i][1])):
            #on va de sommet en sommet pour former une liste de flèche
            line.append((d[i][1][x-1], d[i][1][x]))
        #on remplace la liste de sommet par la liste de flèche
        d[i][1] = line
    return d

def printParcours(parcours):
    for i in range(len(parcours)):
        print(f"Sommet : {i}")
        print(f"Distance : {parcours[i][0]} , Chemin : {parcours[i][1]}")

def TempsBF(n):
    p = (1 / n)
    M = matricePNumpy(n, p, 1, 2 ** 31)
    start = timeit.default_timer()
    BellmanFordParcours(M, 1)
    stop = timeit.default_timer()
    return (stop - start) * 1000
