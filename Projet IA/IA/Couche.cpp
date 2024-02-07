#include <iostream>
#include "Couche.h"

Couche::Couche() : tabNeurones(nullptr), nbNeurones(0) {}

Couche::Couche(NeuroneFormat** tab, int taille, int nbNeurones) : nbNeurones(nbNeurones)
{
	tabNeurones = new NeuroneFormat * [nbNeurones];
	for (int i = 0; i < nbNeurones; i++) {
		tabNeurones[i] = new Neurone(tab, taille);
	}
}

int Couche::getNbNeurones()
{
	return nbNeurones;
}

NeuroneFormat** Couche::getTabNeurones()
{
	return tabNeurones;
}

void Couche::calculerCouche()
{
	for (int i = 0; i < nbNeurones; i++) {
		NeuroneFormat* nf = tabNeurones[i];
		Neurone* n = dynamic_cast<Neurone*>(nf);
		if (n != nullptr) {
			n->calculerVal();
		}
	}
}

void Couche::affiche(ostream& stream) {
	for (int i = 0; i < nbNeurones; i++) {
		stream << "\tNeurone " << i + 1 << " :" << endl;
		tabNeurones[i]->affiche(stream);
		stream << endl;
	}
}

double* Couche::renvoyerSorties()
{
	double* tab = new double[nbNeurones];
	for (int i = 0; i < nbNeurones; i++)
	{
		NeuroneFormat* nf = tabNeurones[i];
		Neurone* n = dynamic_cast<Neurone*>(nf);
		if (n != nullptr) {
			tab[i] = n->renvoyerVal();
		}
	}
	return tab;
}

double* Couche::getSommeGradientPoids(int nbEntrees)
{
	double* tabSomme = new double[nbEntrees];
	for (int i = 0; i < nbEntrees; i++) {
		double sommeGradientPoids = 0.0;
		for (int j = 0; j < nbNeurones; j++) {
			double poids = dynamic_cast<Neurone*>(tabNeurones[j])->getPoids(i);
			double gradient = dynamic_cast<Neurone*>(tabNeurones[j])->getGradient();
			sommeGradientPoids += poids * gradient;
		}
		tabSomme[i] = sommeGradientPoids;
	}
	return tabSomme;
}

void Couche::retropropagation(double* gradient)
{
	for (int i = 0; i < nbNeurones; i++) {
		dynamic_cast<Neurone*>(tabNeurones[i])->calculerGradient(gradient[i]);
	}
}

void Couche::mettreAJourPoids(double tauxApprentissage)
{
	for (int i = 0; i < nbNeurones; i++) {
		dynamic_cast<Neurone*>(tabNeurones[i])->mettreAJourPoids(tauxApprentissage);
	}
}


CoucheOutput::CoucheOutput(): Couche(){}

CoucheOutput::CoucheOutput(NeuroneFormat** tab, int taille, int nbNeurones) : Couche(tab, taille, nbNeurones) {
	tabNeurones = new NeuroneFormat * [nbNeurones];
	for (int i = 0; i < nbNeurones; i++) {
		tabNeurones[i] = new NeuroneOutput(tab, taille);
	}
}

void CoucheOutput::retropropagation(double* target)
{
	for (int i = 0; i < nbNeurones; i++) {
		dynamic_cast<NeuroneOutput*>(tabNeurones[i])->calculerGradient(target[i]);
	}
}



CoucheInput::CoucheInput(int nbNeurones) : nbNeurones(nbNeurones)
{
	tabNeurones = new NeuroneFormat * [nbNeurones];
	for (int i = 0; i < nbNeurones; i++) tabNeurones[i] = new NeuroneInput();
}

int CoucheInput::getNbNeurones()
{
	return nbNeurones;
}

NeuroneFormat** CoucheInput::getTabNeurones()
{
	return tabNeurones;
}

void CoucheInput::initialiserCouche(double* tab)
{
	for (int i = 0; i < nbNeurones; i++) {
		NeuroneFormat* nf = tabNeurones[i];
		NeuroneInput* n = dynamic_cast<NeuroneInput*>(nf);
		if (n != nullptr) {
			n->initialiserInput(tab[i]);
		}
	}
}

void CoucheInput::affiche(ostream& stream) {
	for (int i = 0; i < nbNeurones; i++) {
		stream << "\tNeuroneInput " << i + 1 << " :" << endl;
		tabNeurones[i]->affiche(stream);
		stream << endl;
	}
}