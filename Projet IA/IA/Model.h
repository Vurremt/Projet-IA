#pragma once

#include "Couche.h"

class Model {
private:
	CoucheInput* coucheInput;
	Couche** tabCouche;
	Couche* coucheOutput;
	int nbCouches;
public:
	Model(int nbEntrees, int nbCouches, int* tabNbNeurones, int nbSorties);
	void initialiserEntrees(int* tab);
	void calculer();
	double* resultat();
	void affiche(ostream& stream);
};