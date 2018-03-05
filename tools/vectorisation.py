# -*- coding: utf8 -*-

import math,os,glob,re,codecs

def nettoyage(texte):
        texte = re.sub(u"[&%!?\|\"{\(\[|_\)\]},\.;/:§»«”“‘…–—−]", "", texte) #toutes les poctuations à partir du regxp
        chiffre=re.compile(ur"[0123456789]",re.I)                               #tous les chiffres
        texte = chiffre.sub("", texte)
        #transformation de la mise en forme des apostrophes
        texte = texte.replace(u"’", u"'")
        texte = texte.replace(u"'", u"\\' ")
        return texte

def lecture(nom_fichier):
# fonction qui lit un fichier dont on donne le nom en parametre, et
# qui transforme son contenu en une liste
        fichier = codecs.open(nom_fichier, "r", "utf-8-sig")
#	fichier = open(nom_fichier,"r")
	text = fichier.read()
#	reg=re.compile(u"\'")
#	chaine_segmente=reg.sub(u"\' ",texte)
	text=nettoyage(text)
        liste = (re.compile(u"[\s+-]")).split(text)
#	liste=text.split()
	fichier.close
	return liste

def vocabulaire(liste_fichiers,mots_vides):
# fonction a qui on fournit une liste de fichiers et une liste de mots
# vides qui construit l'espace de representation defini par ces
# fichiers, c-a-d la liste sans doublons de tous les mots non vides
# contenus dans au moins l'un d'eux
	vocab = []
	for nom in liste_fichiers:
		liste = lecture(nom)
		for mot in liste:
			if mot[-1:] in [',','.']:
				mot = mot[0:-1]
			if (mot.lower() not in vocab) and (mot.lower() not in mots_vides) :
				vocab.append(mot.lower())
	if "" in vocab:
		vocab.remove("")
	return sorted(vocab)

def construire_vecteur(voc_ref,mots_fichier,representation):
# fonction a qui on fournit une liste de mots (espace de
# representation) et le contenu d'un fichier (sous la forme d'une
# autre liste) et qui fournit le vecteur qui represente le fichier
# dans l'espace, en comptant les occurrences des mots
	mots_traites = []
	for mot in mots_fichier :
		if mot[-1:] in [',','.']:
			mot = mot[0:-1]
		mots_traites.append(mot.lower())
	vecteur = {}
	for mot in voc_ref :
		if (representation == 1):
			if mots_traites.count(mot) > 0 :
				vecteur[mot] = 1
			else :
				vecteur[mot] = 0
		else :
			vecteur[mot] = mots_traites.count(mot)
	return vecteur

# def norme(vecteur):
# calcul de la norme d'un vercteur
#	valeur = 0
#	for mot in vecteur :
#		valeur = valeur+vecteur[mot]**2
#	return math.sqrt(valeur)

# programme principal
# demande de saisie du nom du dossier principal et du fichier de mots vides
dossier = raw_input("Nom du dossier contenant le corpus : ")
fichier_mots_vides = raw_input("Nom du fichier de mots vides (se terminant par .txt) : ")
liste_mots_vides = lecture(fichier_mots_vides)
choix=0
while (choix <> 1 and choix <> 2):
	choix=input("représentation booléenne (taper 1) ou en nombre d\'occurrences (taper 2) ? ")
# chaque sous-dossier du dossier principal est une etiquette de classe
etiquettes = os.listdir(dossier)
if '.DS_Store' in etiquettes :
	etiquettes.remove('.DS_Store')
# print etiquettes
# construction de la liste de tous les noms de fichiers
os.chdir(dossier)
les_fichiers=[]
for nom in etiquettes :
	os.chdir(nom)
	liste = glob.glob("*.txt")
	for fichier in liste :
		nom_fichier = nom + "/" + fichier
		les_fichiers.append(nom_fichier)
	os.chdir("../")
# construction de l'espace de representation
v = vocabulaire(les_fichiers,liste_mots_vides)
# print v
# ecriture des donnees au format .arff dans la variable sortie
sortie = '@relation corpus\n'
for mot in v :
	sortie += "@attribute '" + mot + "' numeric\n"
sortie += "@attribute 'classe' {"
for i in range(0,len(etiquettes)) :
	sortie += etiquettes[i]
	if i != len(etiquettes)-1 :
		sortie += ","
sortie += "}\n"
sortie += "@data\n"
for nom in etiquettes :
	os.chdir(nom)
	liste = glob.glob("*.txt")
	for fichier in liste :
		liste_mots = lecture(fichier)
		vecteur = construire_vecteur(v,liste_mots,choix)
		for mot in v :
			sortie += str(vecteur[mot]) + ','
		sortie += nom + "\n"
	os.chdir("../")
# print sortie
os.chdir("../")
# ecriture du contenu de la variable dans le fichier de sortie
fichier_sortie = codecs.open("fichier-resultat.arff", "w", "utf-8")
# fichier_sortie = open("corpus.arff","w")
fichier_sortie.write(sortie)
fichier_sortie.close
print "fichier-resultat.arff produit !"
