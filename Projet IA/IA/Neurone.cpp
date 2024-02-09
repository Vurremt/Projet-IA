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

void NeuroneInput::initialiserInput(double val) {
	valeur = sigmoid(val);
}

void NeuroneInput::affiche(ostream& stream)
{
	stream << "\t\tVal : " << valeur << endl;
}



Neurone::Neurone(NeuroneFormat** tab, int taille) :
	NeuroneFormat(),
	valeurApresSigmoid(0),
	tabEntrees(tab), nbEntrees(taille),
	biais((double)rand() / (double)RAND_MAX),
	gradient(0)
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
	//cout << "      avant sigmoid : " << valeur << ", Valeur de retour : " << valeurApresSigmoid << endl;
	return valeurApresSigmoid;
}

double NeuroneOutput::renvoyerVal()
{
	//cout << "      avant sigmoid output : " << valeur << ", Valeur de retour Output: " << valeurApresSigmoid << endl;
	return valeurApresSigmoid;
}

void Neurone::affiche(ostream& stream)
{
	stream << "\t\t";
	for (int i = 0; i < nbEntrees; i++) {
		stream << "W" << i+1 << ":" << tabPoids[i] << " | ";
	}
	stream << "Biais: " << biais << endl;
	stream << "\t\tGradient: " << gradient << endl;
	stream << "\t\tVal : " << valeur << ", Val apres Sigmoid : " << valeurApresSigmoid << endl;
}



void Neurone::calculerGradient(double sommeGradientPoids) {
	double expo = exp(-valeur);
	gradient = sommeGradientPoids* (expo / ((1 + expo) * (1 + expo)));
}

void Neurone::mettreAJourPoids(double tauxApprentissage) {
	for (int i = 0; i < nbEntrees; i++) {
		tabPoids[i] += tauxApprentissage * gradient * tabEntrees[i]->renvoyerVal();
	}
	biais += tauxApprentissage * gradient;
	gradient = 0;
}

double Neurone::getPoids(int index) {
	return tabPoids[index];
}

double Neurone::getGradient() {
	return gradient;
}

NeuroneOutput::NeuroneOutput(NeuroneFormat** tab, int taille): Neurone(tab, taille){}

void NeuroneOutput::calculerGradient(double target)
{
	double expo = exp(-valeur);
	gradient = (renvoyerVal()-target) * (expo / ((1 + expo) * (1 + expo)));
}
