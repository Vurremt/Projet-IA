#pragma once

#include "Joueur.h"

class JoueurHumain : public Joueur {
public:
	JoueurHumain(string nom);
	~JoueurHumain();

	int FaireAction();
};
