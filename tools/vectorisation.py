#! /usr/bin/env python3

import argparse
import pathlib
import re
import sys

from collections import Counter


def nettoyage(texte):
    texte = re.sub(r"[&%!?\|\"{\(\[|_\)\]},\.;/:§»«”“‘…–—−]", '', texte)
    texte = re.sub(r'\d', '', texte)
    texte = texte.replace("’", "'")
    texte = texte.replace("'", "' ")
    return texte


def lecture(nom_fichier):
    with open(nom_fichier, "r") as fichier:
        text = fichier.read()
    text = nettoyage(text)
    return [w.lower() for w in re.split(r"[\s\.]+", text) if w]


def vocabulaire(liste_fichiers, mots_vides):
    vocab = set(mot
                for fichier in liste_fichiers
                for mot in lecture(fichier)
                if mot not in mots_vides)
    return sorted(vocab)


def construire_vecteur(voc_ref, mots_fichier, boolean):
    this_voc = Counter(mots_fichier)
    vecteur = [this_voc.get(m, 0) for m in voc_ref]
    if boolean:
        vecteur = [1 if v else 0 for v in vecteur]
    return vecteur


def process(corpus_path, out_path=None, boolean=False, fichier_mots_vides=None):
    dossier = pathlib.Path(corpus_path)
    if out_path is None:
        out_path = dossier.parent/'fichier-resultat.arff'
    if fichier_mots_vides is None:
        liste_mots_vides = []
    else:
        liste_mots_vides = lecture(fichier_mots_vides)
    # chaque sous-dossier du dossier principal est une etiquette de classe
    etiquettes = [d.name for d in dossier.iterdir() if d.is_dir]
    v = vocabulaire(pathlib.Path(dossier).glob('*/*.txt'), liste_mots_vides)
    # ecriture des donnees au format .arff dans la variable sortie
    sortie = ['@relation corpus']
    sortie.append('\n'.join("@attribute '{m}' numeric".format(m=mot.replace("'", r"\'"))
                            for mot in v))
    sortie.append(f"@attribute 'classe' {{{','.join(etiquettes)}}}")
    sortie.append("@data")
    for nom in etiquettes:
        liste = (dossier/nom).glob("*.txt")
        for fichier in liste:
            liste_mots = lecture(fichier)
            vecteur = construire_vecteur(v, liste_mots, boolean)
            vecteur.append(nom)
            sortie.append(','.join(map(str, vecteur)))

    # ecriture du contenu de la variable dans le fichier de sortie
    with open(out_path, 'w') as fichier_sortie:
        fichier_sortie.write('\n'.join(sortie))

    print('fichier-resultat.arff produit !')


def main_entry_point(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('corpus_path', metavar='dossier_corpus', type=str,
                            help='Le dossier contenant corpus (un sous-dossier par étiquette)')
        parser.add_argument('out_path', metavar='fichier_sortie',
                            nargs='?', type=str, default=None,
                            help='Le dossier contenant corpus (un sous-dossier par étiquette)')
        parser.add_argument('--mots-vides', metavar='fichier_mots_vides', type=str, default=None,
                            help='Un fichier contenant une liste de mots vides (un par ligne)')
        parser.add_argument('--boolean', action='store_true',
                            help='Utiliser des représentations booléennes')

        args = parser.parse_args(argv)
        return process(args.corpus_path, args.out_path, args.boolean, args.mots_vides)

    # Legacy interactive mode
    print('Mode interactif (legacy). Utiliser `vectorisation.py -h` pour le mode CLI.`')
    corpus_path = input("Nom du dossier contenant le corpus : ")
    fichier_mots_vides = input("Nom du fichier de mots vides (se terminant par .txt) : ")

    choix = None
    while choix not in ('1', '2'):
        choix = input("Représentation booléenne (taper 1) ou en nombre d'occurrences (taper 2) ? ")
    process(corpus_path, boolean=choix == 1, fichier_mots_vides=fichier_mots_vides)


if __name__ == '__main__':
    sys.exit(main_entry_point(sys.argv[1:]))
