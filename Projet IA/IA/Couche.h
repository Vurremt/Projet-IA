#pragma once

#include "Neurone.h"

class Couche {
protected:
	NeuroneFormat** tabNeurones;
	int nbNeurones;
public:
	Couche();
	Couche(NeuroneFormat** tab, int taille, int nbNeurones);
	int getNbNeurones();
	NeuroneFormat** getTabNeurones();
	void calculerCouche();
	void affiche(ostream& stream);
	double* renvoyerSorties();
	double* getSommeGradientPoids(int nbEntrees);
	void retropropagation(double* gradient);
	void mettreAJourPoids(double tauxApprentissage);
};

class CoucheOutput: public Couche {
public:
	CoucheOutput();
	CoucheOutput(NeuroneFormat** tab, int taille, int nbNeurones);
	void retropropagation(double* target);
};

class CoucheInput {
private:
	NeuroneFormat** tabNeurones;
	int nbNeurones;
public:
	CoucheInput(int nbNeurones);
	int getNbNeurones();
	NeuroneFormat** getTabNeurones();
	void initialiserCouche(double* tab);
	void affiche(ostream& stream);
};