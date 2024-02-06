#pragma once

#include "Neurone.h"

class Couche {
private:
	NeuroneFormat** tabNeurones;
	int nbNeurones;
public:
	Couche();
	Couche(NeuroneFormat** tab, int taille, int nbNeurones);
	NeuroneFormat** getTabNeurones();
	void calculerCouche();
	void affiche(ostream& stream);
	double* renvoyerSorties();
};

class CoucheInput {
private:
	NeuroneFormat** tabNeurones;
	int nbNeurones;
public:
	CoucheInput(int nbNeurones);
	NeuroneFormat** getTabNeurones();
	void initialiserCouche(int* tab);
	void affiche(ostream& stream);
};