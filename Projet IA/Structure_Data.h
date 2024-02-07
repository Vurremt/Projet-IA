#pragma once

#include <string>

using namespace std;

class Structure_Data {
public:
	double** tabEntrees;
	int nbData;
	int nbEntrees;

	Structure_Data(double** tabEntrees, int nbData, int nbEntrees);
};

class Structure_Data_Fit : public Structure_Data {
public:
	double** tabSorties;
	int nbSorties;

	Structure_Data_Fit(double** tabEntrees, double** tabSorties, int nbData, int nbEntrees, int nbSorties);
};


Structure_Data* recup_Data(string nomFichier);
Structure_Data_Fit* recup_Data_Fit(string nomFichier);