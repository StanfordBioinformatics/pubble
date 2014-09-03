#!/bin/bash

module load python/2.7
module load chqpoint/0.1
module load texlive

root=/srv/gs1/software/gbsc/pubble/dev
data=/srv/gsfs0/projects/gbsc/Clinical_Service/cases/case0019/medgap-2.0/QC-0.1
map=$root/inputlayouts/case0019_demo.json

$root/makereport.py --analysisroot $data --chqpointmap $map --pdftemplate report.tex --pdfdestfile out.pdf
