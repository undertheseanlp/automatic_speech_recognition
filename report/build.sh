#!/usr/bin/env bash
name="technique_report"
pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=. $name.tex
bibtex $name.aux
pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=. $name.tex
pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=. $name.tex

rm -rf $name.blg
rm -rf $name.log
rm -rf $name.out
rm -rf *.aux
rm -rf $name.bbl
rm -rf $name.synctex.gz