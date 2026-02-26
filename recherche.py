from indexer_gendico import *

#lib
import os
from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
import string
import codecs
import operator
from operator import itemgetter
import math
import json
from data_to_modify import folder


#constantes
DOSSIERDOCUMENTS = folder+"cacm/" # repertoire qui contien la collectionA MODIFIER
FICHMOTSOUTILS = folder+"fetch.txt" # fichier des mots outils A MODIFIER
FICHVOC = folder+"Voc.json" # fichier json de sauvegarde du vocabulaire A MODIFIER
INDEXINVERSEE = folder+"Index_Inversee.json"
DICONORMES = folder+"dictionnaire_normes.json"

def chargeDictionnaire(fstopname):
    """
    charge un fichier d'antidictionnaire, qui contient un terme par ligne
    """
    dico = {}
    fstop = open(fstopname,'r') # ouverture du fichier
    dico = json.load(fstop)
    fstop.close()
    return dico

index_inversee = chargeDictionnaire(INDEXINVERSEE) #chargemet du dictionnaire inversé (clé mot, valeur doc)
voc = chargeDictionnaire(FICHVOC) #chargement du vocabulaire
diconorme = chargeDictionnaire(DICONORMES) #chargmeent des normes
chargeMotsOutils(FICHMOTSOUTILS) #chargement des mots outils

def traiement_requetes(q):
    print ("Traitement de la requête ",q)
    qt = stringtokenize(q)
    qtclean = filtreMotsOutils(qt)
    vecteur = {}
    for mot in qtclean:
        racine_mot = mot2racine(mot)
        if racine_mot in vecteur:
            vecteur[racine_mot] += 1
        else:
            vecteur[racine_mot] = 1
    norme = 0
    for mot in vecteur:
        print(mot)
        if mot in voc:
            vecteur[mot] = vecteur[mot] * voc[mot]
            norme += (vecteur[mot]**2)
    norme = math.sqrt(norme)

    return [vecteur, norme]

def dic_produit_scalaire(resultat):
    vecteur = resultat[0]
    norme = resultat[1]
    dico = {}
    for mot in vecteur:
        if mot in index_inversee:
            dico_mot = index_inversee[mot]
            for document in dico_mot:
                if document in dico:
                    dico[document] += vecteur[mot] * dico_mot[document]
                else:
                    dico[document] = vecteur[mot] * dico_mot[document]
    for document in dico:
        dico[document] = dico[document] / (norme*diconorme[document])
    return dico

def traiter_resultat_recherche(resultat):
    resultat_triees = sorted(resultat.items(), key=lambda t: t[1], reverse=True)
    # Affichage des n premiers 
    for doc, score in resultat_triees[:10]:
        print(f"Document: {doc} | Score: {score}")

if __name__ == "__main__":
    requete = ""
    while True:
        requete = input("Saisissez une requête: ")
        resultat_traitement_requete = traiement_requetes(requete)
        traiter_resultat_recherche(dic_produit_scalaire(resultat_traitement_requete))