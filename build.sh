#!/bin/bash
pdflatex --interaction=nonstopmode -shell-escape dissertation.tex
biber dissertation
makeglossaries dissertation
pdflatex --interaction=nonstopmode -shell-escape dissertation.tex
pdflatex --interaction=nonstopmode -shell-escape dissertation.tex
