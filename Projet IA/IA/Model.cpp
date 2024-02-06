#include <iostream>
#include "Model.h"

Model::Model(int nbEntrees, int nbCouches, int* tabNbNeurones, int nbSorties) : nbCouches(nbCouches)
{
	coucheInput = new CoucheInput(nbEntrees);
	tabCouche = new Couche * [nbCouches];
	if (nbCouches > 0) tabCouche[0] = new Couche(coucheInput->getTabNeurones(), nbEntrees, tabNbNeurones[0]);
	for (int i = 1; i < nbCouches; i++) {
		tabCouche[i] = new Couche(tabCouche[i - 1]->getTabNeurones(), tabNbNeurones[i - 1], tabNbNeurones[i]);
	}
	if (nbCouches > 0) coucheOutput = new Couche(tabCouche[nbCouches - 1]->getTabNeurones(), tabNbNeurones[nbCouches - 1], nbSorties);
	else coucheOutput = new Couche(coucheInput->getTabNeurones(), nbEntrees, nbSorties);
}

void Model::initialiserEntrees(int* tab)
{
	coucheInput->initialiserCouche(tab);
}

void Model::calculer()
{
	for (int i = 0; i < nbCouches; i++) {
		tabCouche[i]->calculerCouche();
	}
	coucheOutput->calculerCouche();
}

double* Model::resultat()
{
	return coucheOutput->renvoyerSorties();
}

void Model::affiche(ostream& stream)
{
	stream << "Couche Input : " << endl;
	coucheInput->affiche(stream);
	for (int i = 0; i < nbCouches; i++) {
		stream << "Couche " << i + 1 << endl;
		tabCouche[i]->affiche(stream);
	}
	stream << "Couche Output : " << endl;
	coucheOutput->affiche(stream);
	stream << "-------------------------------" << endl;
}