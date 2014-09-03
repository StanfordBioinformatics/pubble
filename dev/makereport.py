#!/usr/bin/env python

from argparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader
import os
import re
from shutil import copy, rmtree, move
import subprocess
import tempfile

from chqpoint import Analysis
from parsers import samtoolsparser, gatkparser, fastqcparser, picardparser, common

# This dict maps each output file name to its parser module
# The key is the output 'name' in the chqpoint json
# file used to import the analysis
#

parsers = {
    'flagstat': samtoolsparser.flagstat,
    'varianteval_CountVariants': gatkparser.varianteval_CountVariants,
    'varianteval_TiTvVariantEvaluator': gatkparser.varianteval_TiTvVariantEvaluator,
    'fastqc_data': fastqcparser.fastqc_data,
    'fastqc_duplication_levels': fastqcparser.duplication_levels,
    'fastqc_kmer_profiles': fastqcparser.kmer_profiles,
    'fastqc_per_base_gc_content': fastqcparser.per_base_gc_content,
    'fastqc_per_base_n_content': fastqcparser.per_base_n_content,
    'fastqc_per_base_quality': fastqcparser.per_base_quality,
    'fastqc_per_base_sequence_content': fastqcparser.per_base_sequence_content,
    'fastqc_per_sequence_gc_content': fastqcparser.per_sequence_gc_content,
    'fastqc_per_sequence_quality': fastqcparser.per_sequence_quality,
    'fastqc_sequence_length_distribution': fastqcparser.sequence_length_distribution,
    'picard_alignmentsummarymetrics': picardparser.alignmentsummarymetrics,
    'picard_gcbiasmetrics': picardparser.gcbiasmetrics,
    'picard_gcdropoutmetrics': picardparser.gcdropoutmetrics,
    'picard_insertsizemetrics': picardparser.insertsizemetrics,
    'picard_gcbiasmetricsimage': common.imagenoop,
    'picard_insertsizemetricsimage': common.imagenoop,
    'picard_meanqualitybycycleimage': common.imagenoop,
    'picard_qualityscoredistributionimage': common.imagenoop,
    'coverage_acmg_exons_image': common.imagenoop,
    'coverage_dcm_exons_image': common.imagenoop,
    'coverage_MYLK2_image': common.imagenoop,
}


class ReportMaker:

    TEMPLATEDIR = os.path.join(os.path.dirname(__file__), 'templates')

    def __init__(self, analysisroot, analysismap):

        self.results = {}
        self.imagefiles = {}
        self.imagefilescopy = {} #Published copy for html
        self.getanalysisdata(analysisroot, analysismap)

        for resultsfile in self.resultsfiles:
            resultsname = resultsfile['name']
            parser = parsers[resultsname]
            (results, imagefile) = parser(resultsfile['path'])
            if results:
                self.results.update(results)
            if imagefile:
                self.imagefiles[resultsname] = imagefile

    def getanalysisdata(self, analysisroot, analysismap):

        analysis = Analysis.new(
            path=analysisroot, 
            configfile=analysismap
        )

        self.resultsfiles = analysis.getoutputs()
        self.metadata = analysis.getmetadata()

    def renderpdf(self, templatefile, destfile, dbg):
        tempdir = tempfile.mkdtemp()
        if dbg:
            print "Intermediate files for generating PDF will be preserved in %s" % tempdir
            print self.results
            print self.imagefiles

        tempbasename = '_temp_'
        latexfile = os.path.join(tempdir, tempbasename+'.tex')
        with open(latexfile, 'w') as f:
            f.write(self.rendertext(templatefile, self.results, self.imagefiles))

        cmd = 'pdflatex -output-directory=%s %s' % (tempdir, latexfile)
        subprocess.call(cmd, shell=True)
        move(os.path.join(tempdir, tempbasename+'.pdf'), destfile)
        if not dbg:
            rmtree(tempdir)

    def renderhtml(self, templatefile, destfile):

        self.copyimagefiles(destfile)

        with open(destfile, 'w') as f:
            f.write(self.rendertext(templatefile, self.results, self.imagefilescopy))

    def rendertext(self, templatefile, results, imagefiles):

        templateLoader = FileSystemLoader(searchpath=[self.TEMPLATEDIR, "/"])
        templateEnv = Environment(loader=templateLoader)
        template = templateEnv.get_template(templatefile)

        templatedict = {}
        templatedict.update(results)
        templatedict.update({'imagefiles': imagefiles})
        templatedict.update(self.metadata)

        outputText = template.render(templatedict)
        return outputText

    def supportingfilesdir(self, destfile):

        prefix = re.sub('\.html$', '', destfile)
        return prefix + '_files'

    def copyimagefiles(self, destfile):

        destdir = self.supportingfilesdir(destfile)
        if not os.path.exists(destdir):
            os.mkdir(destdir)

        for (imagename, imagefile) in self.imagefiles.iteritems():
            self.imagefilescopy[imagename] = os.path.join(
                destdir, os.path.basename(imagefile))
            copy(imagefile, destdir)
        
if __name__=='__main__':

    parser = ArgumentParser()
    parser.add_argument('--analysisroot')
    parser.add_argument('--chqpointmap')
    parser.add_argument('--htmltemplate')
    parser.add_argument('--htmldestfile')
    parser.add_argument('--pdftemplate')
    parser.add_argument('--pdfdestfile')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    r = ReportMaker(
        args.analysisroot, 
        args.chqpointmap
    )

    if args.pdftemplate:
        if args.pdfdestfile:
            pdfdestfile = args.pdfdestfile
        else:
            pdfdestfile = 'out.pdf'
        r.renderpdf(args.pdftemplate, args.pdfdestfile, args.debug)

    if args.htmltemplate:
        if args.htmldestfile:
            htmldestfile = args.htmldestfile
        else:
            htmldestfile = 'out.html'
        r.renderhtml(args.htmltemplate, htmldestfile)
