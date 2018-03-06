ALL := vectorisation
.PHONY: vectorisation all
.DEFAULT_GOAL := all

all: $(ALL)

targets:
	mkdir targets

vectorisation: targets
	python3 ../tools/vectorisation.py --mots-vides ../data/mots_vides.txt ../data/expl1 targets/expl1.arff
	cmp targets/expl1.arff fixtures/expl1.arff
