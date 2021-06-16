# FIGURES = images/DataExtraction.png images/task1.png images/haser.png images/orbit.png images/structure.png images/task2.png

ALL: orbit haser report

orbit:
	python src/orbit.py

haser:
	python src/calc-haser.py
	python src/plot-haser.py

report:
	pdflatex report.tex
	bibtex report.aux
	pdflatex report.tex

.PHONY: clean clean_report

clean: clean_report
	rm images/haser.png
	rm images/orbit.png

clean_report:
	rm report.aux
	rm report.log
	rm report.out
	rm report.bbl
	rm report.pdf