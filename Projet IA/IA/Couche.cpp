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
	for (int i = 0; i < nbNeurones; i++) tab[i] = tabNeurones[i]->renvoyerVal();
	return tab;
}

CoucheInput::CoucheInput(int nbNeurones) : nbNeurones(nbNeurones)
{
	tabNeurones = new NeuroneFormat * [nbNeurones];
	for (int i = 0; i < nbNeurones; i++) tabNeurones[i] = new NeuroneInput();
}

NeuroneFormat** CoucheInput::getTabNeurones()
{
	return tabNeurones;
}

void CoucheInput::initialiserCouche(int* tab)
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