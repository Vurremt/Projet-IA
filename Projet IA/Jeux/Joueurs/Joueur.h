#pragma once

#include <string>

using namespace std;

class Joueur {
protected:
	string nom;

public:
	Joueur(string nom) : nom(nom) {}
	string getNom() {
		return nom;
	}
	virtual int FaireAction() = 0;
};