#include <iostream>
#include "Neurone.h"

double sigmoid(double val) {
	return 1 / (1 + exp(-val));
}


NeuroneFormat::NeuroneFormat(): valeur(0){}

double NeuroneFormat::renvoyerVal()
{
	return valeur;
}

NeuroneInput::NeuroneInput(): NeuroneFormat(){}

void NeuroneInput::initialiserInput(int val) {
	valeur = sigmoid(val);
}

void NeuroneInput::affiche(ostream& stream)
{
	stream << "\t\tVal : " << valeur << endl;
}



Neurone::Neurone(NeuroneFormat** tab, int taille) : NeuroneFormat(), valeurApresSigmoid(0), tabEntrees(tab), nbEntrees(taille), biais((double)rand() / (double)RAND_MAX)
{
	tabPoids = new double[taille];
	for (int i = 0; i < taille; i++) {
		tabPoids[i] = (double)rand() / (double)RAND_MAX;
	}
}

int Neurone::getTaille()
{
	return nbEntrees;
}

void Neurone::calculerVal()
{
	valeur = 0;
	for (int i = 0; i < nbEntrees; i++) {
		valeur += tabEntrees[i]->renvoyerVal() * tabPoids[i];
	}
	valeur += biais;
	valeurApresSigmoid = sigmoid(valeur);
}

double Neurone::renvoyerVal()
{
	return valeurApresSigmoid;
}

void Neurone::affiche(ostream& stream)
{
	stream << "\t\t";
	for (int i = 0; i < nbEntrees; i++) {
		stream << "W" << i+1 << ":" << tabPoids[i] << " | ";
	}
	stream << "Biais: " << biais << endl;
	stream << "\t\tVal : " << valeur << endl;
}
