from recherche import *
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from data_to_modify import folder



CHEMIN_CACM = folder+"cacm/"

resultglob = []

def rechercher():
    r = champ_saisie.get()
    for item in tableau.get_children():
        tableau.delete(item)
    result = dic_produit_scalaire(traiement_requetes(r))
    resultat_triees = sorted(result.items(), key=lambda t: t[1], reverse=True) #tri du dictionnaire, retourne une liste de tuples
    lbl_resultat_norme.config(text=f"Nombre de résultats: {len(resultat_triees)}", fg="blue")
    for document in resultat_triees:
        titre = ""
        chemin_complet = CHEMIN_CACM + document[0]
        with open(chemin_complet, 'r', encoding='utf-8', errors='replace') as f:
            contenu = f.read()
            i = 0
            while contenu[i] != '\n':
                titre+=contenu[i]
                i+=1
        tableau.insert('', 'end', values=(document[0], titre, document[1]))
    global resultglob 
    resultglob = resultat_triees

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

def precision():
    n = 20
    if(len(resultglob) < n):
        if(len(resultglob) == 0):
            print("liste resultats vide")
            return
        n = len(resultglob)
    y = []
    for i in resultglob[:20]:
        y.append(i[1])
    x = np.linspace(0, n, n)
    fig, ax = plt.subplots()
    ax.set_ylim(0, 1) 
    ax.plot(x, y, linewidth=2.0)
    plt.show()



if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("RaySearch - Moteur de Recherche")
    fenetre.geometry("1400x1400")

    photo = tk.PhotoImage(file=folder+"logo.png")
    lbl = tk.Label(fenetre,image=photo)
    lbl.pack()

    frame_haut = tk.Frame(fenetre)
    frame_haut.pack(pady=10) 

    champ_saisie = tk.Entry(frame_haut, width=50, font=('Arial 20 italic'))
    champ_saisie.pack(side=tk.LEFT, padx=5)

    bouton = tk.Button(frame_haut, text="Rechercher", command=rechercher, height = 2, width = 20)
    bouton.pack(side=tk.LEFT)

    colonnes = ("Document", "Titre", "Pertinance")
    tableau = ttk.Treeview(fenetre, columns=colonnes, show='headings')

    tableau.heading("Document", text="Document")
    tableau.heading("Titre", text="Titre")
    tableau.heading("Pertinance", text="Pertinance")

    tableau.column("Document", width=20)
    tableau.column("Titre", width=400)
    tableau.column("Pertinance", width=20)
    tableau.bind("<Double-1>", afficher_contenu_fichier)

    tableau.pack(expand=True, fill='both', padx=10, pady=10)

    frame_bas = tk.Frame(fenetre)
    frame_bas.pack(pady=10) 
    lbl_resultat_norme = tk.Label(frame_bas, text="Nombre de résultats: N/A", font='Arial 12 ')
    lbl_resultat_norme.pack(side=tk.LEFT)
    boutonp = tk.Button(frame_bas, text="Précision", command=precision)
    boutonp.pack(side=tk.RIGHT)



    fenetre.mainloop()
