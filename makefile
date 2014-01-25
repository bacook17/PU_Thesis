default: Cook_Thesis.pdf

thesis: Cook_Thesis.pdf 

subtexs = thesis_setup.tex
figs = Figs_Thesis/FbvM.pdf Figs_Thesis/FgvM.pdf Figs_Thesis/FgvR.pdf
cleans = Cook_Thesis.pdf Figs_Thesis/*.pdf

# Figures

# ./$< is macro for the first dependency (here, the .py)
# $@ is macro for the name of the file being made (here, the .pdf)
Figs_Thesis/FbvM.pdf: PlotFbvM.py F_all.dat
	./$< $@

Figs_Thesis/FgvM.pdf: PlotFgvM.py F_all.dat
	./$< $@

Figs_Thesis/FgvR.pdf: PlotFgvR.py F_all.dat
	./$< $@

Cook_Thesis.pdf: thesis_body.tex $(subtexs) $(figs)
	./latexdriver -b thesis_body.tex Cook_Thesis.pdf

clean:
	rm -f *~ \#*\# *.pyc $(cleans) .latexwork/*
