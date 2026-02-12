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

#constantes
DOSSIERDOCUMENTS = "/home/ray/Documents/TP_semester_8/Acces_et_Recherche_informations/TP1/cacm/" # repertoire qui contien la collectionA MODIFIER
FICHMOTSOUTILS = "/home/ray/Documents/TP_semester_8/Acces_et_Recherche_informations/TP1/fetch.txt" # fichier des mots outils A MODIFIER
FICHVOC = "/home/ray/Documents/TP_semester_8/Acces_et_Recherche_informations/TP1/Voc.json" # fichier json de sauvegarde du vocabulaire A MODIFIER
INDEXINVERSEE = "/home/ray/Documents/TP_semester_8/Acces_et_Recherche_informations/TP1/Index_Inversee.json"
DICONORMES = "/home/ray/Documents/TP_semester_8/Acces_et_Recherche_informations/TP1/dictionnaire_normes.json"
NBDOCS = len(os.listdir(DOSSIERDOCUMENTS)) # nombre de docs total
dictionnaire_de_vecteurs = {}
dictionnaire_normes = {}
index_inversee = {}


if __name__ == "__main__":
    chargeMotsOutils(FICHMOTSOUTILS) # on charge les mots outils dans le dico
    listefichiers = os.listdir(DOSSIERDOCUMENTS) # liste des fichiers dans le dossier
    with open(FICHVOC, 'r') as fp:
        V = json.load(fp)
        fp.close()
    #construction des vecteurs
    for filename in listefichiers: 
        print ("Traitement du fichier ",filename)
        doccontent = loaddocFile(filename)
        liste = stringtokenize(doccontent)
        listeclean = filtreMotsOutils(liste)
        dico = {}
        norme = 0

        for mot in listeclean:
            racine_mot = mot2racine(mot)
            if racine_mot in dico:
                dico[racine_mot] += 1
            else:
                dico[racine_mot] = 1
        for mot in dico:
            dico[mot] = dico[mot] * V[mot]
        dictionnaire_de_vecteurs[filename] = dico

    #Construction de l'index inversé            
        for mot in dico:
            norme += (dico[mot])**2
            if mot in index_inversee:
                index_inversee[mot][filename] = dico[mot]
            else:
                index_inversee[mot] = {filename: dico[mot]}
    
    #calcul de la norme
        dictionnaire_normes[filename] = math.sqrt(norme)
    #sauvegarde de l'index inversé completé
    with open(INDEXINVERSEE, 'w') as fp:
        json.dump(index_inversee, fp)
    fp.close()
    #sauvebarde du dictionnaire des normes
    with open(DICONORMES, 'w') as fp:
        json.dump(dictionnaire_normes, fp)
    fp.close()

