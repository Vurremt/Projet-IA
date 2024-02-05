#include <iostream>
#include "JoueurIA.h"

JoueurIA::JoueurIA(string nom) : Joueur(nom) {}

JoueurIA::~JoueurIA() {}

int JoueurIA::FaireAction() {
	int val = rand() % 7;
	cout << val << endl;
	return val;
}