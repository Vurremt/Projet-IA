#pragma once

#include <iostream>
#include <cmath>

using namespace std;

double sigmoid(double val);

class NeuroneFormat {
protected:
	double valeur;
public:
	NeuroneFormat();
	double renvoyerVal();
	virtual void affiche(ostream& stream) = 0;
};

class NeuroneInput : public NeuroneFormat {
public:
	NeuroneInput();
	void initialiserInput(int val);
	void affiche(ostream& stream);
};


class Neurone : public NeuroneFormat {
private:
	NeuroneFormat** tabEntrees;
	double* tabPoids;
	int nbEntrees;
	double biais;
	double valeurApresSigmoid;

	double gradient_biais;
	double* gradients_poids;

public:
	Neurone(NeuroneFormat** tab, int taille);
	int getTaille();
	void calculerVal();
	double renvoyerVal();
	void affiche(ostream& stream);
};
