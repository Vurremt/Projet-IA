// Projet IA.cpp : Ce fichier contient la fonction 'main'. L'exécution du programme commence et se termine à cet endroit.
//

#include <iostream>

#include "Jeux/Joueurs/Joueur.h"
#include "Jeux/Joueurs/JoueurHumain.h"
#include "Jeux/Joueurs/JoueurIA.h"

#include "Jeux/Puissance4.h"


#include "IA/Model.h"  

int main()
{
    srand(time(NULL));

    /*
    JoueurHumain* joueur1 = new JoueurHumain("Evahn");
    JoueurIA * joueur2 = new JoueurIA("Ordi");

    Jeu* jeu = new Jeu(joueur1, joueur2, cout);

    jeu->boucle_de_jeu();
    */

    int tabNbNeurones[] = {0};
    Model* m = new Model(2, 0, nullptr, 1);

    m->affiche(cout);

    int tabEntree[] = { 2,3 };

    m->initialiserEntrees(tabEntree);

    m->calculer();
    
    cout << "Resultat : " << m->resultat()[0] << endl;

    m->affiche(cout);
}
