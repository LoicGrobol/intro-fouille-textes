#! /usr/bin/env python3

import argparse
import ast
import pathlib
import re
import sys

from collections import Counter


def _process(class_dirs, mots_vides, boolean=False, lexicon=None, characters=False):
    contents = {
        d.name: [bag_of_words(f, mots_vides, characters) for f in files]
        for d, files in class_dirs
    }
    if lexicon is None:
        lexicon = sorted(
            set(
                w
                for bows in contents.values()
                for b in bows
                for w in b.keys()
                if w and w not in mots_vides
            )
        )
    class_names = sorted(contents.keys())
    return (
        lexicon,
        class_names,
        ([*vec(b, lexicon, boolean), c] for c in class_names for b in contents[c]),
    )


def nettoyage(texte):
    texte = re.sub(r"[&%!?\|\"{\(\[|_\)\]},\.;/:§»«”“‘…–—−\\]", "", texte)
    texte = re.sub(r"\d", "", texte)
    texte = texte.replace("’", "'")
    texte = texte.replace("'", "' ")
    return texte


def bag_of_words(nom_fichier, mots_vides, characters=False):
    with open(nom_fichier) as fichier:
        text = fichier.read()
    text = nettoyage(text)
    if characters:
        return Counter(w for w in text if w and not w.isspace() and w not in mots_vides)
    return Counter(
        l
        for w in filter(None, re.split(r"\s+", text))
        for l in (w.lower(),)
        if l not in mots_vides
    )


def vec(bow, lexicon, boolean):
    vecteur = [bow.get(m, 0) for m in lexicon]
    if boolean:
        vecteur = [1 if v else 0 for v in vecteur]
    return vecteur


def process(
    corpus_path,
    out_path=None,
    boolean=False,
    fichier_mots_vides=None,
    lexicon=None,
    characters=False,
):
    dossier = pathlib.Path(corpus_path)
    if out_path is None:
        out_path = dossier / "fichier-resultat.arff"
    if fichier_mots_vides is None:
        mots_vides = []
    else:
        with open(fichier_mots_vides) as in_stream:
            mots_vides = set(l.strip() for l in in_stream)
    if lexicon is not None:
        with open(lexicon) as in_stream:
            if lexicon.endswith(".arff"):
                lexicon = sorted(
                    set(
                        word
                        for l in in_stream
                        if l.startswith("@attribute")
                        # unescape (quoted) string
                        for word in (
                            ast.literal_eval((re.search(r"'.*'", l).group(0))),
                        )
                        if word != "xClasse"
                    )
                )
            else:
                lexicon = sorted(set(l.strip() for l in in_stream))
    # Chaque sous-dossier (non-caché) du dossier principal est une étiquette de classe
    class_dirs = (
        (d, sorted(d.glob("*.txt")))
        for d in dossier.iterdir()
        if d.is_dir and not d.name.startswith(".") and not d.name.endswith("\r")
    )
    lexicon, class_names, rows = _process(
        class_dirs, mots_vides, boolean, lexicon, characters=characters
    )

    # Écriture des donnees au format .arff dans la variable `sortie`
    sortie = ["@relation corpus"]
    for mot in lexicon:
        sortie.append("@attribute '{m}' numeric".format(m=mot.replace("'", r"\'")))
    sortie.append(f"@attribute 'xClasse' {{{','.join(class_names)}}}")
    sortie.append("@data")
    for r in rows:
        sortie.append(",".join(map(str, r)))

    # ecriture du contenu de la variable dans le fichier de sortie
    with open(out_path, "w") as fichier_sortie:
        fichier_sortie.write("\n".join(sortie))
        fichier_sortie.write("\n")

    print(f"{out_path} produit !")


def main_entry_point(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        parser = argparse.ArgumentParser(
            description="Transforme un corpus sous la forme « un fichier par document » en fichier arff lisible par Weka"
        )
        parser.add_argument(
            "corpus_path",
            metavar="dossier_corpus",
            type=str,
            help="Le dossier contenant le corpus (un sous-dossier par classe)",
        )
        parser.add_argument(
            "out_path",
            metavar="fichier_sortie",
            nargs="?",
            type=str,
            default=None,
            help="Le chemin du fichier de sortie",
        )
        parser.add_argument(
            "--mots-vides",
            metavar="fichier_mots_vides",
            type=str,
            default=None,
            help="Un fichier contenant une liste de mots vides (un par ligne)",
        )
        parser.add_argument(
            "--lexicon",
            metavar="fichier_lexique",
            type=str,
            default=None,
            help="Un fichier contenant un lexique (un mot par ligne ou arff)",
        )
        parser.add_argument(
            "--boolean",
            action="store_true",
            help="Utiliser des représentations booléennes",
        )
        parser.add_argument(
            "--character",
            action="store_true",
            help="Segmenter par caractère (par exemple pour les langues logographiques)",
        )

        args = parser.parse_args(argv)
        return process(
            args.corpus_path,
            args.out_path,
            args.boolean,
            args.mots_vides,
            args.lexicon,
            characters=args.character,
        )

    # Legacy interactive mode
    print("Mode interactif (legacy). Utiliser `vectorisation.py -h` pour le mode CLI.`")
    corpus_path = input("Nom du dossier contenant le corpus : ")
    fichier_mots_vides = input(
        "Nom du fichier de mots vides (se terminant par .txt) : "
    )

    choix = None
    while choix not in ("1", "2"):
        choix = input(
            "Représentation booléenne (taper 1) ou en nombre d'occurrences (taper 2) ? "
        )
    process(
        corpus_path,
        boolean=choix == 1,
        fichier_mots_vides=fichier_mots_vides,
    )


if __name__ == "__main__":
    sys.exit(main_entry_point(sys.argv[1:]))
