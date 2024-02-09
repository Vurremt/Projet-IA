// Projet IA.cpp : Ce fichier contient la fonction 'main'. L'exécution du programme commence et se termine à cet endroit.
//

#include <iostream>

#include "Jeux/Joueurs/Joueur.h"
#include "Jeux/Joueurs/JoueurHumain.h"
#include "Jeux/Joueurs/JoueurIA.h"

#include "Jeux/Puissance4.h"


#include "IA/Model.h"  

#include "Structure_Data.h"


int main()
{
    srand(time(NULL));

    /*
    JoueurHumain* joueur1 = new JoueurHumain("Evahn");
    JoueurIA * joueur2 = new JoueurIA("Ordi");

    Jeu* jeu = new Jeu(joueur1, joueur2, cout);

    jeu->boucle_de_jeu();
    */


    int tabNbNeurones[1] = {15};
    Model* m = new Model(2, 1, tabNbNeurones, 1);

    cout << "\n-------- Reseau Init --------\n" << endl;
    m->affiche(cout);

    Structure_Data_Fit * data_fit = recup_Data_Fit("data/spiral_data_fit.txt");

    m->fit(data_fit, 10000, 0.8);

    cout << "\n-------- Reseau Entraine --------\n" << endl;
    m->affiche(cout);

    cout << "\n-------- Entrainement Termine --------\n" << endl;


    Structure_Data* data = recup_Data("data/test_data_simple.txt");

    m->display_resultat(data, cout);


    Structure_Data * big_data = recup_Data("data/test_big_data.txt");
    m->display_resultat_simplify(big_data, "data/recup_data.txt");
}
