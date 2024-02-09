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
	void initialiserInput(double val);
	void affiche(ostream& stream);
};


class Neurone : public NeuroneFormat {
protected:
	NeuroneFormat** tabEntrees;
	double* tabPoids;
	int nbEntrees;
	double biais;
	double valeurApresSigmoid;

	double gradient;

public:
	Neurone(NeuroneFormat** tab, int taille);
	int getTaille();
	void calculerVal();
	double renvoyerVal();
	void affiche(ostream& stream);


	void calculerGradient(double sommeGradientPoids); // Ajout d'une fonction pour calculer le gradient pour les couches cachées
	void mettreAJourPoids(double tauxApprentissage); // Ajout d'une fonction pour mettre à jour les poids
	double getPoids(int index); // Ajout d'une fonction pour obtenir le poids à un index donné
	double getGradient(); // Ajout d'une fonction pour obtenir le gradient
};


class NeuroneOutput : public Neurone {
public:
	NeuroneOutput(NeuroneFormat** tab, int taille);
	void calculerGradient(double target);
	double renvoyerVal();
};
