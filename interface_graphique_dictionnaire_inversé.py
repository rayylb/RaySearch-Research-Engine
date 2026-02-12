from indexer_gendico import *

import tkinter as tk
from tkinter import ttk
import json


INDEXINVERSEE = "/home/ray/Documents/TP_semester_8/Acces_et_Recherche_informations/TP1/Index_Inversee.json"
DICONORMES = "/home/ray/Documents/TP_semester_8/Acces_et_Recherche_informations/TP1/dictionnaire_normes.json"
CHEMIN_CACM = "/home/ray/Documents/TP_semester_8/Acces_et_Recherche_informations/TP1/cacm/"

with open(INDEXINVERSEE, 'r') as fp:
    II = json.load(fp)
    fp.close()
with open(DICONORMES, 'r') as fp:
    DN = json.load(fp)
    fp.close()

def rechercher():
    mot = mot2racine(champ_saisie.get())
    for item in tableau.get_children():
        tableau.delete(item)
    l = II[mot]
    for document in l:
        tableau.insert('', 'end', values=(document, l[document]))

def rechercher_norme():
    document = champ_saisie2.get()
    norme = DN[document]
    lbl_resultat_norme.config(text=f"Norme : {norme}", fg="blue")

def afficher_contenu_fichier(event):
    selection = tableau.selection()
    if not selection:
        return
    
    item = selection[0]
    nom_doc = tableau.item(item, "values")[0]
    
    if nom_doc == "Aucun résultat":
        return

    chemin_complet = CHEMIN_CACM + nom_doc
    
    top = tk.Toplevel(fenetre)
    top.title(f"Contenu de {nom_doc}")
    top.geometry("600x400")
    
    zone_texte = tk.Text(top, wrap='word')
    zone_texte.pack(expand=True, fill='both')
    
    scrollbar = tk.Scrollbar(zone_texte, command=zone_texte.yview)
    zone_texte.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    with open(chemin_complet, 'r', encoding='utf-8', errors='replace') as f:
        contenu = f.read()
        zone_texte.insert('1.0', contenu)

fenetre = tk.Tk()
fenetre.title("RaySearch - Index Inversé")
fenetre.geometry("1000x1200")

frame_thaut = tk.Frame(fenetre)
frame_thaut.pack(pady=5) 
frame_haut = tk.Frame(fenetre)
frame_haut.pack(pady=10) 


lbl=tk.Label(frame_thaut, text="Rechercher dans l'index inversé", font='Arial 20 bold')
lbl.pack(padx=15, pady=15)

champ_saisie = tk.Entry(frame_haut, width=30)
champ_saisie.pack(side=tk.LEFT, padx=5)

bouton = tk.Button(frame_haut, text="Rechercher", command=rechercher)
bouton.pack(side=tk.LEFT)


colonnes = ("Document", "Valeur")
tableau = ttk.Treeview(fenetre, columns=colonnes, show='headings')

tableau.heading("Document", text="Document")
tableau.heading("Valeur", text="Valeur")

tableau.column("Document", width=50)
tableau.column("Valeur", width=300)
tableau.bind("<Double-1>", afficher_contenu_fichier)

tableau.pack(expand=True, fill='both', padx=10, pady=10)

frame_bas = tk.Frame(fenetre)
frame_bas.pack(pady=10) 
frame_tbas = tk.Frame(fenetre)
frame_tbas.pack(pady=10) 

lbl2=tk.Label(frame_bas, text="Rechercher norme d'un document", font='Arial 20 bold')
lbl2.pack(padx=15, pady=15)

champ_saisie2 = tk.Entry(frame_tbas, width=30)
champ_saisie2.pack(side=tk.LEFT, padx=5)

bouton = tk.Button(frame_tbas, text="Rechercher", command=rechercher_norme)
bouton.pack(side=tk.LEFT)
lbl_resultat_norme = tk.Label(frame_tbas, text="", font='Arial 12 bold')
lbl_resultat_norme.pack(side=tk.LEFT, padx=20)





fenetre.mainloop()