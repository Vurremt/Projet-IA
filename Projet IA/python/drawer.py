import matplotlib.pyplot as plt

with open("../test_fit.txt", 'r') as file:
    ligne = file.readline()
    tab = ligne.strip("\n").split(' ');
    nbData = int(tab[0])
    nbEntrees = int(tab[1])
    nbSorties = int(tab[2])

    tabX = []
    tabY = []
    tabS = []
    for i in range(nbData):
        ligne = file.readline()
        tab = ligne.strip("\n").split(' ');
        
        tabX.append(float(tab[0]))
        tabY.append(float(tab[1]))
        tabS.append(float(tab[2]))

    plt.scatter(tabX, tabY,c=tabS)
    plt.show()
