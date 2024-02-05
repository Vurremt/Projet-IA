// Projet IA.cpp : Ce fichier contient la fonction 'main'. L'exécution du programme commence et se termine à cet endroit.
//

#include <iostream>

#include "Jeux/Joueurs/Joueur.h"
#include "Jeux/Joueurs/JoueurHumain.h"
#include "Jeux/Joueurs/JoueurIA.h"

#include "Jeux/Puissance4.h"

int main()
{
    srand(time(NULL));

    JoueurHumain* joueur1 = new JoueurHumain("Evahn");
    //JoueurHumain* joueur2 = new JoueurHumain("Paul");
    JoueurIA * joueur2 = new JoueurIA("Ordi");

    Jeu* jeu = new Jeu(joueur1, joueur2, cout);

    jeu->boucle_de_jeu();
}
