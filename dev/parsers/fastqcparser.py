#!/usr/bin/env python

from argparse import ArgumentParser

def duplication_levels(imagefile):
    results = None
    return (results, imagefile)

def kmer_profiles(imagefile):
    results = None
    return (results, imagefile)

def per_base_gc_content(imagefile):
    results = None
    return (results, imagefile)

def per_base_n_content(imagefile):
    results = None
    return (results, imagefile)

def per_base_quality(imagefile):
    results = None
    return (results, imagefile)

def per_base_sequence_content(imagefile):
    results = None
    return (results, imagefile)

def per_sequence_gc_content(imagefile):
    results = None
    return (results, imagefile)

def per_sequence_quality(imagefile):
    results = None
    return (results, imagefile)

def sequence_length_distribution(imagefile):
    results = None
    return (results, imagefile)

def fastqc_data(filename):
    resultsdata = {}

    with open(filename) as f:
        for line in f:

            if line.startswith('##FastQC'):
                resultsdata['fastqcversion'] = line.split()[1]
                continue

            if line.startswith('>>Basic Statistics'):
                resultsdata['basicstatistics'] = {}
                resultsdata['basicstatistics']['passfail'] = line.rstrip().split('\t')[1]
                resultsdata['basicstatistics']['data'] = {}
                data = resultsdata['basicstatistics']['data']
                
                # Skip line with "Measure  Value" labels
                nextrow = f.next()
                if nextrow.startswith('#Measure'):
                    nextrow = f.next()
                
                while not nextrow.startswith('>>END_MODULE'):
                    parts = nextrow.rstrip().split('\t')
                    key = parts[0]
                    value = parts[1]
                    data[key] = value
                    nextrow = f.next()
                continue

            if line.startswith('>>Per base sequence quality'):
                resultsdata['perbasesequencequality'] = {}
                resultsdata['perbasesequencequality']['passfail'] = line.rstrip().split('\t')[1]
                resultsdata['perbasesequencequality']['rows'] = []
                rows = resultsdata['perbasesequencequality']['rows']

                # Get header row
                resultsdata['perbasesequencequality']['header'] = f.next().rstrip().split('\t')

                # Get other rows
                nextrow = f.next()
                while not nextrow.startswith('>>END_MODULE'):
                    rows.append(nextrow.rstrip().split('\t'))
                    nextrow = f.next()
                continue

    results = {'fastqc': resultsdata}
    imagefiles = None
    return (results, imagefiles)

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    (results, imagefiles) = fastqc_data(args.filename)
    if results:
        print results
    if imagefiles:
        print imagefiles


#  ##FastQC        0.10.1
#  >>Basic Statistics      pass
#  #Measure        Value   
#  Filename        SAMPLE.bam      
#  File type       Conventional base calls 
#  Encoding        Sanger / Illumina 1.9   
#  Total Sequences 1333837971      
#  Filtered Sequences      0       
#  Sequence length 100     
#  %GC     39      
#  >>END_MODULE
#  >>Per base sequence quality     pass
#  #Base   Mean    Median  Lower Quartile  Upper Quartile  10th Percentile 90th Percentile
#  1       27.849785087577178      29.0    28.0    29.0    24.0    30.0
#  2       28.833317702124408      30.0    28.0    31.0    27.0    32.0
#  3       27.461216828711798      28.0    27.0    29.0    25.0    30.0
#  ...
#  95-99   28.53855984086391       31.4    27.0    32.8    17.0    34.0
#  100     28.389982711775716      31.0    27.0    33.0    16.0    34.0
#  >>END_MODULE
#  >>Per sequence quality scores   pass
#  #Quality        Count
#  0       38076.0
#  1       38055.0
#  2       33970.0

# duplication_levels.png                                                                                                                                                                                   # kmer_profiles.png                                                                                                                                                                                        # per_base_gc_content.png                                                                                                                                                                                  # per_base_n_content.png                                                                                                                                                                                   # per_base_quality.png                                                                                                                                                                                     # per_base_sequence_content.png                                                                                                                                                                            # per_sequence_gc_content.png                                                                                                                                                                              # per_sequence_quality.png                                                                                                                                                                                 # sequence_length_distribution.png
