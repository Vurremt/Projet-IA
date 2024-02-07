#pragma once

#include "Couche.h"
#include "../Structure_Data.h"

class Model {
private:
	CoucheInput* coucheInput;
	Couche** tabCouche;
	CoucheOutput* coucheOutput;
	int nbCouches;
public:
	Model(int nbEntrees, int nbCouches, int* tabNbNeurones, int nbSorties);
	void initialiserEntrees(double* tab);
	void calculer();
	double* resultat();
	void display_resultat(Structure_Data* data, ostream& stream);
	void display_resultat_simplify(Structure_Data* data, const string nomFichier);
	void retropropagation(double* target);
	void mettreAJourPoids(double tauxApprentissage);
	void fit(Structure_Data_Fit * data_fit, int nbRepet, double tauxApprentissage, bool display, ostream& stream);
	void affiche(ostream& stream);
};