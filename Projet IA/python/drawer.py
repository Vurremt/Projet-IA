import matplotlib.pyplot as plt

with open("../data/recup_data.txt", 'r') as file:
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
        if(float(tab[2]) < 0.5) : tabS.append(0)
        else : tabS.append(1)
        

    plt.scatter(tabX, tabY,c=tabS, marker=".")
    plt.show()
