#include <iostream>
#include <fstream>

#include "Model.h"

Model::Model(int nbEntrees, int nbCouches, int* tabNbNeurones, int nbSorties) : nbCouches(nbCouches)
{
	coucheInput = new CoucheInput(nbEntrees);
	tabCouche = new Couche * [nbCouches];
	if (nbCouches > 0) tabCouche[0] = new Couche(coucheInput->getTabNeurones(), nbEntrees, tabNbNeurones[0]);
	for (int i = 1; i < nbCouches; i++) {
		tabCouche[i] = new Couche(tabCouche[i - 1]->getTabNeurones(), tabNbNeurones[i - 1], tabNbNeurones[i]);
	}
	if (nbCouches > 0) coucheOutput = new CoucheOutput(tabCouche[nbCouches - 1]->getTabNeurones(), tabNbNeurones[nbCouches - 1], nbSorties);
	else coucheOutput = new CoucheOutput(coucheInput->getTabNeurones(), nbEntrees, nbSorties);
}

void Model::initialiserEntrees(double* tab)
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

void Model::display_resultat(Structure_Data * data, ostream& stream)
{
	for (int i = 0; i < data->nbData; i++) {
		stream << "---------------\nEntrees : " << endl;
		for (int j = 0; j < data->nbEntrees; j++) {
			stream << "   Entree " << j + 1 << " : " << data->tabEntrees[i][j] << endl;
		}

		initialiserEntrees(data->tabEntrees[i]);
		calculer();

		double* res = resultat();

		stream << "Sorties : " << endl;
		for (int j = 0; j < coucheOutput->getNbNeurones(); j++) {
			stream << "   Sortie " << j + 1 << " : " << res[j] << endl;
		}
	}
}

void Model::display_resultat_simplify(Structure_Data* data, const string nomFichier)
{
	ofstream file(nomFichier);
	if (file) {
		file << data->nbData;
		file << " ";
		file << data->nbEntrees;
		file << " ";
		file << coucheOutput->getNbNeurones();
		file << endl;

		for (int i = 0; i < data->nbData; i++) {
			for (int j = 0; j < data->nbEntrees; j++) {
				file << data->tabEntrees[i][j] << " ";
			}

			initialiserEntrees(data->tabEntrees[i]);
			calculer();

			double* res = resultat();

			for (int j = 0; j < coucheOutput->getNbNeurones(); j++) {
				if (j == coucheOutput->getNbNeurones() - 1) file << res[j] << endl;
				else file << res[j] << " ";
			}
		}
	}
}

void Model::retropropagation(double* target)
{
	coucheOutput->retropropagation(target);
	double* gradients = (nbCouches >= 1) ? coucheOutput->getSommeGradientPoids(tabCouche[nbCouches - 1]->getNbNeurones()) : nullptr;
	/*
	cout << "Le gradient propage de output a i-1 : " << endl;
	for (int i = 0; i < tabCouche[nbCouches - 1]->getNbNeurones(); i++) {
		cout << "   gradient " << i << " : " << gradients[i] << endl;
	}
	*/

	for (int i = nbCouches - 1; i >= 0; i--) {
		tabCouche[i]->retropropagation(gradients);
		gradients = (i >= 1) ? tabCouche[i]->getSommeGradientPoids(tabCouche[i - 1]->getNbNeurones()) : nullptr;
	}
}

void Model::mettreAJourPoids(double tauxApprentissage)
{
	for (int i = 0; i < nbCouches; i++) {
		tabCouche[i]->mettreAJourPoids(tauxApprentissage);
	}
	coucheOutput->mettreAJourPoids(tauxApprentissage);
}

void Model::fit(Structure_Data_Fit * data_fit, int nbRepet, double tauxApprentissage)
{
	
	double mean_square_error;
	cout << "Entrainement a 00% : ";
	mean_square_error = 0.0;

	for (int iData = 0; iData < data_fit->nbData; iData++) {
		initialiserEntrees(data_fit->tabEntrees[iData]);
		calculer();

		double* Results = resultat();

			for (int jResult = 0; jResult < coucheOutput->getNbNeurones(); jResult++) {
				cout << "Neurone " << jResult << " : " << endl;
				mean_square_error += (Results[jResult] - data_fit->tabSorties[iData][jResult]) * (Results[jResult] - data_fit->tabSorties[iData][jResult]);
				cout << "   Resultat obtenu : " << Results[jResult] << endl;
				cout << "   Resultat attendu : " << data_fit->tabSorties[iData][jResult] << endl;
				cout << "   Difference : " << Results[jResult] - data_fit->tabSorties[iData][jResult] << " | Carre : " << (Results[jResult] - data_fit->tabSorties[iData][jResult]) * (Results[jResult] - data_fit->tabSorties[iData][jResult]) << endl;
				cout << "   Val reinjectee dans rectropropagation : " << data_fit->tabSorties[iData][jResult] << endl;
			}

			retropropagation(data_fit->tabSorties[iData]);
			cout << "   Nouveau gradient du neurone output : " << dynamic_cast<Neurone*>(coucheOutput->getTabNeurones()[0])->getGradient() << endl;
			mettreAJourPoids(tauxApprentissage);
	}

	for (int jResult = 0; jResult < coucheOutput->getNbNeurones(); jResult++) {
		cout << sqrt(mean_square_error / data_fit->nbData) << " ( Moyenne des mean square error des toutes les donnees )" << endl;
	}

	int repet_modulo = nbRepet / 10;

	for (int iRepet = 0; iRepet < nbRepet; iRepet++) {

		double mean_square_error;
		if (iRepet % repet_modulo == 0) {
			cout << "Entrainement a " << iRepet / repet_modulo * 10 << "% : ";
			mean_square_error = 0.0;
		}

		for (int iData = 0; iData < data_fit->nbData; iData++) {
			initialiserEntrees(data_fit->tabEntrees[iData]);
			calculer();

			double* Results = resultat();

			if (iRepet % repet_modulo == 0) {
				for (int jResult = 0; jResult < coucheOutput->getNbNeurones(); jResult++) {
					mean_square_error += (Results[jResult] - data_fit->tabSorties[iData][jResult]) * (Results[jResult] - data_fit->tabSorties[iData][jResult]);
					//cout << (Results[jResult] - data_fit->tabSorties[iData][jResult]) * (Results[jResult] - data_fit->tabSorties[iData][jResult]) << endl;
				}
			}

			retropropagation(data_fit->tabSorties[iData]);
			mettreAJourPoids(tauxApprentissage);
		}
		if (iRepet % repet_modulo == 0) {
			for (int jResult = 0; jResult < coucheOutput->getNbNeurones(); jResult++) {
				cout << sqrt(mean_square_error / data_fit->nbData) << " ( Moyenne des mean square error des toutes les donnees )" << endl;
			}
		}
	}
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