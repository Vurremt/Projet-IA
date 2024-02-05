#include <iostream>
#include "JoueurHumain.h"

JoueurHumain::JoueurHumain(string nom) : Joueur(nom) {}

JoueurHumain::~JoueurHumain() {}

int JoueurHumain::FaireAction() {
	int val;
	cin >> val;
	return val;
}