#! /usr/bin/env python3

import pathlib
import re
import sys

from collections import Counter


def nettoyage(texte):
    texte = re.sub(r"[&%!?\|\"{\(\[|_\)\]},\.;/:§»«”“‘…–—−]", '', texte)
    texte = re.sub(r'\d', '', texte)
    texte = texte.replace("’", "'")
    texte = texte.replace("'", r"\' ")
    return texte


def lecture(nom_fichier):
    with open(nom_fichier, "r") as fichier:
        text = fichier.read()
    text = nettoyage(text)
    return re.split(r"[\s\.]+", text)


def vocabulaire(liste_fichiers, mots_vides):
    vocab = set(mot.lower()
                for fichier in liste_fichiers
                for mot in lecture(fichier)
                if mot not in mots_vides)
    return sorted(vocab)


def construire_vecteur(voc_ref, mots_fichier, representation):
    this_voc = Counter(mots_fichier)
    vecteur = [this_voc.get(m, 0) for m in voc_ref]
    if representation == 1:
        vecteur = [1 if v else 0 for v in vecteur]
    return vecteur


def main_entry_point(argv=sys.argv):
    # programme principal
    # demande de saisie du nom du dossier principal et du fichier de mots vides
    dossier = pathlib.Path(input("Nom du dossier contenant le corpus : "))
    fichier_mots_vides = input("Nom du fichier de mots vides (se terminant par .txt) : ")
    liste_mots_vides = lecture(fichier_mots_vides)
    choix = None
    while (choix not in ('1', '2')):
        choix = input("représentation booléenne (taper 1) ou en nombre d\'occurrences (taper 2) ? ")
    # chaque sous-dossier du dossier principal est une etiquette de classe
    etiquettes = [d.name for d in dossier.iterdir() if d.is_dir]
    v = vocabulaire(pathlib.Path(dossier).glob('*/*.txt'), liste_mots_vides)
    # ecriture des donnees au format .arff dans la variable sortie
    sortie = ['@relation corpus']
    sortie.append('\n'.join(f"@attribute '{mot}' numeric" for mot in v))
    sortie.append(f"@attribute 'classe' {{{','.join(etiquettes)}}}")
    sortie.append("@data")
    for nom in etiquettes:
        liste = (dossier/nom).glob("*.txt")
        for fichier in liste:
            liste_mots = lecture(fichier)
            vecteur = construire_vecteur(v, liste_mots, choix)
            vecteur.append(nom)
            sortie.append(','.join(map(str, vecteur)))

    # ecriture du contenu de la variable dans le fichier de sortie
    with open(dossier.parent/'fichier-resultat.arff', 'w') as fichier_sortie:
        fichier_sortie.write('\n'.join(sortie))

    print('fichier-resultat.arff produit !')


if __name__ == '__main__':
    sys.exit(main_entry_point(sys.argv))
