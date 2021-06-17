# FIGURES = images/DataExtraction.png images/task1.png images/haser.png images/orbit.png images/structure.png images/task2.png

ALL: orbit haser report clean

orbit: src/orbit.py
	python src/orbit.py

haser: src/calc-haser.py src/plot-haser.py
	python src/calc-haser.py
	python src/plot-haser.py

report: report.tex
	pdflatex report.tex
	bibtex report.aux
	pdflatex report.tex

.PHONY: clean clean_report

clean: clean_report
	rm haser_ds

clean_report:
	rm report.aux
	rm report.log
	rm report.out
	rm report.bbl