#include <iostream>
#include <fstream>

#include "Structure_Data.h"

Structure_Data::Structure_Data(double** tabEntrees, int nbData, int nbEntrees) :
	tabEntrees(tabEntrees),
	nbData(nbData),
	nbEntrees(nbEntrees) {}

Structure_Data_Fit::Structure_Data_Fit(double** tabEntrees, double** tabSorties, int nbData, int nbEntrees, int nbSorties) :
	Structure_Data(tabEntrees, nbData, nbEntrees),
	tabSorties(tabSorties),
	nbSorties(nbSorties) {}


Structure_Data* recup_Data(const string nomFichier) {

	ifstream file(nomFichier);
	if (file) {
		int nbEntrees = 0;
		int nbData = 0;

		file >> nbData;
		file >> nbEntrees;

		double** tabEntrees = new double* [nbData];
		for (int iData = 0; iData < nbData; iData++) {
			tabEntrees[iData] = new double[nbEntrees];

			for (int i = 0; i < nbEntrees; i++) file >> tabEntrees[iData][i];
		}

		return new Structure_Data(tabEntrees, nbData, nbEntrees);
	}
	else {
		throw new exception("Le fichier n'a pas pu s'ouvrir");
	}
}


Structure_Data_Fit* recup_Data_Fit(const string nomFichier) {

	ifstream file(nomFichier);
	if (file) {
		int nbEntrees = 0;
		int nbSorties = 0;
		int nbData = 0;

		file >> nbData;
		file >> nbEntrees;
		file >> nbSorties;

		double** tabEntrees = new double*[nbData];
		double** tabSorties = new double*[nbData];
		for (int iData = 0; iData < nbData; iData++) {
			tabEntrees[iData] = new double[nbEntrees];
			tabSorties[iData] = new double[nbSorties];

			for (int i = 0; i < nbEntrees; i++) file >> tabEntrees[iData][i];
			for (int i = 0; i < nbSorties; i++) file >> tabSorties[iData][i];
		}

		return new Structure_Data_Fit(tabEntrees, tabSorties, nbData, nbEntrees, nbSorties);
	}
	else {
		throw new exception("Le fichier n'a pas pu s'ouvrir");
	}
}
