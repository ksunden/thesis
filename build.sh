#!/bin/bash
pdflatex --interaction=nonstopmode dissertation.tex
bibtex dissertation.aux
pdflatex --interaction=nonstopmode dissertation.tex
pdflatex --interaction=nonstopmode dissertation.tex
