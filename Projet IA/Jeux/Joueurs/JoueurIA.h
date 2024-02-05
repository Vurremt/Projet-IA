#pragma once

#include "Joueur.h"

class JoueurIA : public Joueur {
public:
	JoueurIA(string nom);
	~JoueurIA();

	int FaireAction();
};
