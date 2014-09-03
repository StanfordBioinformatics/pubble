#!/usr/bin/env python
import re
from argparse import ArgumentParser

def generic_parser(filename, tablename):
    results = None

    with open(filename) as f:
        for line in f:
            if line.startswith('#:GATKTable:%s' % tablename):

                # Capture the table name and description from the second line.
                m = re.match(r'^#:GATKTable:(.*):(.*)$', line)
                if not m:
                    continue
                assert tablename == m.groups()[0]
                tabledescription = m.groups()[1]

                # Capture the column header info
                nextrow = f.next().rstrip()
                tableheader = re.split('\s+', nextrow)
                tableheader.pop(0) #Drop the table name

                # Capture data from all rows that start with the current tablename
                rows = []
                nextrow = f.next().rstrip()
                while nextrow.startswith(tablename):
                    rowdata = re.split('\s+', nextrow)
                    rowdata.pop(0) # Drop the table name from the row
                    rows.append(rowdata) # Save data to list of rows
                    nextrow = f.next().rstrip()

                results = {
                    'description': tabledescription,
                    'header': tableheader,
                    'rows': rows
                    }
    return results

def varianteval_CountVariants(filename):
    tablename = 'CountVariants'
    resultsname = 'varianteval_CountVariants'

    fullresults = generic_parser(filename, tablename)

    columns = []
    # Get a subset of the results; only SNP and Indel rows, and select columns
    col_varianttype = fullresults['header'].index('VariantType')
    columns.append(col_varianttype)
    columns.append(fullresults['header'].index('nProcessedLoci'))
    columns.append(fullresults['header'].index('nVariantLoci'))
    columns.append(fullresults['header'].index('nSNPs'))
    columns.append(fullresults['header'].index('nMNPs'))
    columns.append(fullresults['header'].index('nInsertions'))
    columns.append(fullresults['header'].index('nDeletions'))
    columns.append(fullresults['header'].index('nComplex'))
    columns.append(fullresults['header'].index('nNoCalls'))
    columns.append(fullresults['header'].index('nHets'))
    columns.append(fullresults['header'].index('nHomVar'))
    columns.append(fullresults['header'].index('hetHomRatio'))

    rownums = []
    for i in range(0, len(fullresults['rows'])):
        if fullresults['rows'][i][col_varianttype] == 'SNP':
            rownums.append(i)
        if fullresults['rows'][i][col_varianttype] == 'INDEL':
            rownums.append(i)

    header = []
    rows = []
    for col in columns:
        header.append(fullresults['header'][col])
    for rownum in rownums:
        row = []
        for col in columns:
            row.append(fullresults['rows'][rownum][col])
        rows.append(row)
                        
    results = {resultsname: {}}
    results[resultsname]['header'] = header
    results[resultsname]['rows'] = rows

    imagefiles = None
    return (results, imagefiles)

def varianteval_TiTvVariantEvaluator(filename):
    tablename = 'TiTvVariantEvaluator'
    resultsname = 'varianteval_TiTvVariantEvaluator'

    results = {resultsname: generic_parser(filename, tablename)}

    # Now we want to pull out some key results that can be displayed without the whole table.
    # Find the row with SNP's.
    
    col_varianttype = results[resultsname]['header'].index('VariantType')
    col_nTi = results[resultsname]['header'].index('nTi')
    col_nTv = results[resultsname]['header'].index('nTv')
    col_TiTvRatio = results[resultsname]['header'].index('tiTvRatio')

    for row in results[resultsname]['rows']:
        if row[col_varianttype] == 'SNP':
            break
    results[resultsname]['variantType'] = row[col_varianttype]
    results[resultsname]['nTi'] = row[col_nTi]
    results[resultsname]['nTv'] = row[col_nTv]
    results[resultsname]['TiTvRatio'] = row[col_TiTvRatio]

    imagefiles = None
    return (results, imagefiles)

def varianteval(filename):

    resultstables = {}

    with open(filename) as f:
        for line in f:
            if line.startswith('#:GATKTable:'):
                # New table found
                # Ignore the first line with format information. 

                # Capture the table name and description from the second line.
                nextrow = f.next()
                m = re.match(r'^#:GATKTable:(.*):(.*)$', nextrow)
                if not m:
                    continue
                tablename = m.groups()[0]
                tabledescription = m.groups()[1]

                # Capture the column header info
                nextrow = f.next().rstrip()
                tableheader = re.split('\s+', nextrow)
                tableheader.pop(0) #Drop the table name

                # Capture data from all rows that start with the current tablename
                rows = []
                nextrow = f.next().rstrip()
                while nextrow.startswith(tablename):
                    rowdata = re.split('\s+', nextrow)
                    rowdata.pop(0) # Drop the table name from the row
                    rows.append(rowdata) # Save data to list of rows
                    nextrow = f.next().rstrip()

                resultstables[tablename] = {
                    'description': tabledescription,
                    'header': tableheader,
                    'rows': rows
                    }
    results = {'varianteval': resultstables}
    imagefiles = None
    return (results, imagefiles)

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    results = parse(args.filename)

    print results


#  #:GATKTable:20:3:%s:%s:%s:%s:%s:%d:%d:%d:%.2f:%s:%d:%.2f:%.1f:%d:%s:%d:%.1f:%d:%s:%d:;
#  #:GATKTable:VariantSummary:1000 Genomes Phase I summary of variants table
#  VariantSummary  CompRod  EvalRod  JexlExpression  Novelty  nSamples  nProcessedLoci  nSNPs    TiTvRatio  SNPNoveltyRate  nSNPsPerSample  TiTvRatioPerSample  SNPDPPerSample  nIndels  IndelNoveltyRate  nIndelsPerSample  IndelDPPerSample  nSVs  SVNoveltyRate  nSVsPerSample
#  VariantSummary  dbsnp    set1     none            all             1      3137161264  3435755       2.06            1.21         3435755                2.06       3435545.0   708708              7.62            708708          708597.0  2001          68.27           2001
