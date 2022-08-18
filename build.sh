#!/bin/bash
pdflatex --interaction=nonstopmode -shell-escape dissertation.tex
bibtex dissertation.aux
pdflatex --interaction=nonstopmode -shell-escape dissertation.tex
pdflatex --interaction=nonstopmode -shell-escape dissertation.tex
