import graph as g
import affichageG as ag
import timeit

def main():
    matrice = g.matricePRandom(50, 0.05, 2, 10)
    g.affichageMatrice(matrice)
    # print(f"Bellman-Ford : \n{g.BellmanFord(matrice, 0)}")
    print("Bellman-Ford en parcours :")
    #print(g.parcoursLargeur(matrice, 0))
    g.printParcours(g.BellmanFordParcours(matrice, 0))
    #print(g.moyennePoidsGraphesNumpy(500, 0.6))
    #ag.affichage(matrice)
    ag.afficheCourbe()




if __name__ == '__main__':
    main()