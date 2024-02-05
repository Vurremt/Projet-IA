#pragma once

#include "Joueurs/Joueur.h"
#include "Joueurs/JoueurHumain.h"

class Colonne {
private:
	int* colonne;
	int hauteur;

public:
	Colonne();
	~Colonne();
	int getHauteur();
	int ajouterElem(int val);
	int operator[](int i);
};

class Jeu {
private : 
	Colonne* grille;
	int tour;
	ostream& stream;
	Joueur * joueur1;
	Joueur * joueur2;
	int vainqueur;

public:
	Jeu(Joueur* j1, Joueur* j2, ostream& stream);
	~Jeu();
	int recupererAction(Joueur * j);
	bool colonnePleine(int col);
	int ajouterElem(int col, int val);
	void affichage();
	bool grillePleine();
	bool jeuFini(int c, int l, int J);
	void JouerUnTour();
	void boucle_de_jeu();
};
