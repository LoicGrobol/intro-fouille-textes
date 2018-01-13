NAME = syllabus
LATEX = latexmk -lualatex -halt-on-error -file-line-error -interaction=nonstopmode
CLEAN = latexmk -C

.DEFAULT_GOAL := $(NAME).pdf

$(NAME).pdf:
	$(LATEX) $(NAME)

.PHONY: clean
clean:
	$(CLEAN)
