#include <iostream>
#include "Puissance4.h"

Colonne::Colonne() : hauteur(0) {
	colonne = new int[6] {0, 0, 0, 0, 0, 0};
}

Colonne::~Colonne() {
	delete[] colonne;
}

int Colonne::operator[](int i) {
	return colonne[i];
}

int Colonne::getHauteur() {
	return hauteur;
}

int Colonne::ajouterElem(int val) {
	colonne[hauteur] = val;
	hauteur++;
	return hauteur - 1;
}


Jeu::Jeu(Joueur * j1, Joueur * j2, ostream& stream): tour(0), stream(stream), vainqueur(0) {
	grille = new Colonne[7];
	joueur1 = j1;
	joueur2 = j2;
}

Jeu:: ~Jeu() {
	delete[] grille;
}

int Jeu::recupererAction(Joueur * j) {
	return j->FaireAction();
}

bool Jeu::colonnePleine(int col) {
	if (col < 0 || col > 7) return true;
	int hauteur = grille[col].getHauteur();
	return hauteur > 5;
}

int Jeu::ajouterElem(int col, int val) {
	return grille[col].ajouterElem(val);
}

void Jeu::affichage() {
	stream << "--1-2-3-4-5-6-7--" << endl;
	for (int j = 5; j >= 0; j--) {
		stream << "| ";
		for (int i = 0; i < 7; i++) {
			stream << grille[i][j] << " ";
		}
		stream << "|" << endl;
	}
	stream << "-----------------" << endl << endl;
}

bool Jeu::grillePleine() {
	for (int i = 0; i < 7; i++) {
		if (!colonnePleine(i)) return false;
	}
	return true;
}

bool Jeu::jeuFini(int c, int l, int J) {
	// Horizontal check
	for (int i = 0; i < 4; i++) {
		if (c - i >= 0 && c - i + 3 < 7) {
			if (grille[c - i][l] == J && grille[c - i + 1][l] == J && grille[c - i + 2][l] == J && grille[c - i + 3][l] == J) {
				return true;
			}
		}
	}

	// Vertical check
	if (l >= 3) {
		if (grille[c][l] == J && grille[c][l - 1] == J && grille[c][l - 2] == J && grille[c][l - 3] == J) {
			return true;
		}
	}

	// Diagonal check (bottom left to top right)
	for (int i = 0; i < 4; i++) {
		if (c - i >= 0 && c - i + 3 < 7 && l - i >= 0 && l - i + 3 < 6) {
			if (grille[c - i][l - i] == J && grille[c - i + 1][l - i + 1] == J && grille[c - i + 2][l - i + 2] == J && grille[c - i + 3][l - i + 3] == J) {
				return true;
			}
		}
	}

	// Diagonal check (top left to bottom right)
	for (int i = 0; i < 4; i++) {
		if (c - i >= 0 && c - i + 3 < 7 && l + i - 3 >= 0 && l + i < 6) {
			if (grille[c - i][l + i] == J && grille[c - i + 1][l + i - 1] == J && grille[c - i + 2][l + i - 2] == J && grille[c - i + 3][l + i - 3] == J) {
				return true;
			}
		}
	}

	// If no win condition is met, return false
	return false;
}

void Jeu::JouerUnTour() {
	tour++;
	Joueur* joueur_actif = (tour % 2) ? joueur1 : joueur2;
	
	stream << "------ Tour " << tour << " ------" << endl;

	int i_colonne = 0;
	do {
		stream << "Joueur " << joueur_actif->getNom() << " : ";
		i_colonne = recupererAction(joueur_actif) - 1;
	} while (colonnePleine(i_colonne));

	int ligne_ajout = ajouterElem(i_colonne, ((tour + 1) % 2) + 1);

	affichage();

	if (jeuFini(i_colonne, ligne_ajout, ((tour + 1) % 2) + 1)) vainqueur = ((tour + 1) % 2) + 1;
	else if (grillePleine()) vainqueur = 3;
	
}

void Jeu::boucle_de_jeu() {

	affichage();

	while(vainqueur == 0){
		JouerUnTour();
	}

	if (vainqueur == 3) stream << "Egalite ! Fin du jeu !";
	else stream << "Le vainqueur est : " << ((vainqueur == 1) ? joueur1->getNom() : joueur2->getNom()) << " ! Bravo !" << endl;
}