#!/bin/bash

eval `modulecmd sh load python/3.2 $*`
modulecmd sh load chqpoint/0.1
modulecmd sh load texlive

root=/srv/gs1/software/gbsc/pubble/dev
data=/srv/gsfs0/SCGS/cases/case0019/medgap-2.0/QC-0.1
map=$root/inputlayouts/case0019_demo.json

$root/makereport.py --analysisroot $data --chqpointmap $map --pdftemplate report.tex --pdfdestfile out.pdf
