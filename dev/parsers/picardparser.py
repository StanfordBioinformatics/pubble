#!/usr/bin/env python

from argparse import ArgumentParser

def genericparser(filename):
    resultsdata = {
        'rows': []
    }

    with open(filename) as f:
        for line in f:
            if line.startswith('## METRICS'):
                # Skip line
                # Save next line as header
                line = f.next()
                resultsdata['header'] = line.rstrip().split()
                
                # Get rows
                line = f.next().rstrip()
                while line:
                    resultsdata['rows'].append(line.rstrip().split())
                    try:
                        line = f.next().rstrip()
                    except StopIteration:
                        break

    return resultsdata

def alignmentsummarymetrics(filename):
    results = {'picard_alignmentsummarymetrics': genericparser(filename)}
    imagefiles = None
    return (results, imagefiles)

# ## net.sf.picard.metrics.StringHeader
# # net.sf.picard.analysis.CollectAlignmentSummaryMetrics METRIC_ACCUMULATION_LEVEL=[ALL_READS] INPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/SAMPLE.bam OUTPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/picard/CollectAlignmentSummaryMetrics.out REFERENCE_SEQUENCE=/srv/gs1/projects/scg/Resources/GATK/hg19/ucsc.hg19.fasta    MAX_INSERT_SIZE=100000 ADAPTER_SEQUENCE=[AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT, AGATCGGAAGAGCTCGTATGCCGTCTTCTGCTTG, AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT, AGATCGGAAGAGCGGTTCAGCAGGAATGCCGAGACCGATCTCGTATGCCGTCTTCTGCTTG, AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT, AGATCGGAAGAGCACACGTCTGAACTCCAGTCACNNNNNNNNATCTCGTATGCCGTCTTCTGCTTG] IS_BISULFITE_SEQUENCED=false ASSUME_SORTED=true STOP_AFTER=0 VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false
# ## net.sf.picard.metrics.StringHeader
# # Started on: Mon Mar 31 19:55:44 PDT 2014

# ## METRICS CLASSnet.sf.picard.analysis.AlignmentSummaryMetrics
# CATEGORYTOTAL_READSPF_READSPCT_PF_READSPF_NOISE_READSPF_READS_ALIGNEDPCT_PF_READS_ALIGNEDPF_ALIGNED_BASESPF_HQ_ALIGNED_READSPF_HQ_ALIGNED_BASESPF_HQ_ALIGNED_Q20_BASESPF_HQ_MEDIAN_MISMATCHESPF_MISMATCH_RATEPF_HQ_ERROR_RATEPF_INDEL_RATEMEAN_READ_LENGTHREADS_ALIGNED_IN_PAIRSPCT_READS_ALIGNED_IN_PAIRSBAD_CYCLESSTRAND_BALANCEPCT_CHIMERASPCT_ADAPTERSAMPLELIBRARYREAD_GROUP
# FIRST_OF_PAIR665309278665309278106597893050.99170365067453745461371922458920160964338684668300.0077610.0061240.0002121006558670040.99405500.503810.0281510.000278
# SECOND_OF_PAIR665309517665309517106597845160.99169665052804161461411853459251375164354479961400.0077060.0058560.0002111006558490720.99403500.5038120.0288470.000277
# PAIR133061879513306187951013195738210.991699130120257906922783775918171536128693164629700.0077330.005990.00021110013117160760.99404500.5038110.0284990.000277

def gcbiasmetrics(filename):
    results = {'picard_gcbiasmetrics': genericparser(filename)}
    imagefiles = None
    return (results, imagefiles)


# ## net.sf.picard.metrics.StringHeader
# # net.sf.picard.analysis.CollectGcBiasMetrics REFERENCE_SEQUENCE=/srv/gs1/projects/scg/Resources/GATK/hg19/ucsc.hg19.fasta INPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/SAMPLE.bam OUTPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/picard/CollectGcBiasMetrics.out CHART_OUTPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/picard/CollectGcBiasMetrics.pdf SUMMARY_OUTPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/picard/CollectGcBiasMetrics.summary    WINDOW_SIZE=100 MINIMUM_GENOME_FRACTION=1.0E-5 ASSUME_SORTED=false IS_BISULFITE_SEQUENCED=false VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false
# ## net.sf.picard.metrics.StringHeader
# # Started on: Tue Apr 01 12:41:28 PDT 2014

# ## METRICS CLASS        net.sf.picard.analysis.GcBiasDetailMetrics
# GC      WINDOWS READ_STARTS     MEAN_BASE_QUALITY       NORMALIZED_COVERAGE     ERROR_BAR_WIDTH
# 0       133376  81534   13      1.338986        0.004689
# 1       95527   61665   15      1.413929        0.005694
# 2       110295  65359   16      1.29797 0.005077
# 3       140901  92174   16      1.432878        0.00472
# 4       151462  102430  16      1.481284        0.004628
# 5       154134  104491  17      1.484894        0.004594
# 6       175760  126686  17      1.578787        0.004436
# 7       189498  129825  18      1.500613        0.004165


def gcdropoutmetrics(filename):
    results = {'picard_gcdropoutmetrics': genericparser(filename)}
    imagefiles = None
    return (results, imagefiles)


def insertsizemetrics(filename):
    results = {'picard_insertsizemetrics': genericparser(filename)}
    imagefiles = None
    return (results, imagefiles)
    #Ignoring histogram data


# ## net.sf.picard.metrics.StringHeader
# # net.sf.picard.analysis.CollectInsertSizeMetrics HISTOGRAM_FILE=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/picard/CollectInsertSizeMetrics.pdf METRIC_ACCUMULATION_LEVEL=[ALL_READS] INPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/SAMPLE.bam OUTPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/picard/CollectInsertSizeMetrics.out REFERENCE_SEQUENCE=/srv/gs1/projects/scg/Resources/GATK/hg19/ucsc.hg19.fasta    DEVIATIONS=10.0 MINIMUM_PCT=0.05 ASSUME_SORTED=true STOP_AFTER=0 VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false
# ## net.sf.picard.metrics.StringHeader
# # Started on: Wed Apr 02 15:30:45 PDT 2014

# ## METRICS CLASS        net.sf.picard.analysis.InsertSizeMetrics
# MEDIAN_INSERT_SIZE      MEDIAN_ABSOLUTE_DEVIATION       MIN_INSERT_SIZE MAX_INSERT_SIZE MEAN_INSERT_SIZE        STANDARD_DEVIATION      READ_PAIRS      PAIR_ORIENTATION        WIDTH_OF_10_PERCENT     WIDTH_OF_20_PERCENT     WIDTH_OF_30_PERCENT     WIDTH_OF_40_PERCENT     WIDTH_OF_50_PERCENT     WIDTH_OF_60_PERCENT     WIDTH_OF_70_PERCENT     WIDTH_OF_80_PERCENT     WIDTH_OF_90_PERCENT     WIDTH_OF_99_PERCENT     SAMPLE  LIBRARY READ_GROUP
# 290     38      1       249230519       290.430444      61.742891       610808551       FR      15      29      43      59      77      95      119     151     205     2707                    

# ## HISTOGRAM    java.lang.Integer
# insert_size     All_Reads.fr_count
# 1       1320
# 2       1447
# 3       1570
# 4       1520
# 5       1603
# 6       1579
# 7       1644


# ## net.sf.picard.metrics.StringHeader
# # net.sf.picard.analysis.CollectInsertSizeMetrics HISTOGRAM_FILE=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/picard/CollectInsertSizeMetrics.pdf METRIC_ACCUMULATION_LEVEL=[ALL_READS] INPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/SAMPLE.bam OUTPUT=/srv/gsfs0/projects/gbsc/benchmark/giab/NA12878.clia/hugeseq-1.3/hc2/manual-QC/picard/CollectInsertSizeMetrics.out REFERENCE_SEQUENCE=/srv/gs1/projects/scg/Resources/GATK/hg19/ucsc.hg19.fasta    DEVIATIONS=10.0 MINIMUM_PCT=0.05 ASSUME_SORTED=true STOP_AFTER=0 VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false
# ## net.sf.picard.metrics.StringHeader
# # Started on: Wed Apr 02 15:30:45 PDT 2014

# ## METRICS CLASS        net.sf.picard.analysis.InsertSizeMetrics
# MEDIAN_INSERT_SIZE      MEDIAN_ABSOLUTE_DEVIATION       MIN_INSERT_SIZE MAX_INSERT_SIZE MEAN_INSERT_SIZE        STANDARD_DEVIATION      READ_PAIRS      PAIR_ORIENTATION        WIDTH_OF_10_PERCENT     WIDTH_OF_20_PERCENT     WIDTH_OF_30_PERCENT     WIDTH_OF_40_PERCENT     WIDTH_OF_50_PERCENT     WIDTH_OF_60_PERCENT     WIDTH_OF_70_PERCENT     WIDTH_OF_80_PERCENT     WIDTH_OF_90_PERCENT     WIDTH_OF_99_PERCENT     SAMPLE  LIBRARY READ_GROUP
# 290     38      1       249230519       290.430444      61.742891       610808551       FR      15      29      43      59      77      95      119     151     205     2707                    

# ## HISTOGRAM    java.lang.Integer
# insert_size     All_Reads.fr_count
# 1       1320
# 2       1447
# 3       1570
# 4       1520
# 5       1603
# 6       1579


if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('parser')
    parser.add_argument('filename')
    args = parser.parse_args()

    parsefxn = None
    if args.parser == 'alignmentsummarymetrics':
        parsefxn = alignmentsummarymetrics
    if args.parser == 'gcbiasmetrics':
        parsefxn = gcbiasmetrics

    if parsefxn:
        (results, imagefiles) = parsefxn(args.filename)
        print results


