#!/usr/bin/env python
import re
from argparse import ArgumentParser

def flagstat(filename):

    with open(filename) as f:
        text = f.read()
    
    pattern = r'(?P<total_pf>[0-9]+) \+ (?P<total_fail>[0-9]+) in total.*\n'\
              +'(?P<duplicates_pf>[0-9]+) \+ (?P<duplicates_fail>[0-9]+) duplicates.*\n'\
              +'(?P<mapped_pf>[0-9]+) \+ (?P<mapped_fail>[0-9]+) mapped.*\n'\
              +'(?P<paired_pf>[0-9]+) \+ (?P<paired_fail>[0-9]+) paired.*\n'\
              +'(?P<read1_pf>[0-9]+) \+ (?P<read1_fail>[0-9]+) read1.*\n'\
              +'(?P<read2_pf>[0-9]+) \+ (?P<read2_fail>[0-9]+) read2.*\n'\
              +'(?P<properly_paired_pf>[0-9]+) \+ (?P<properly_paired_fail>[0-9]+) properly.*\n'\
              +'(?P<self_and_mate_pf>[0-9]+) \+ (?P<self_and_mate_fail>[0-9]+) with itself.*\n'\
              +'(?P<singletons_pf>[0-9]+) \+ (?P<singletons_fail>[0-9]+) singletons.*\n'\
              +'(?P<different_chr_pf>[0-9]+) \+ (?P<different_chr_fail>[0-9]+) with mate .*\n'\
              +'(?P<different_chr_gt5_pf>[0-9]+) \+ (?P<different_chr_gt5_fail>[0-9]+) with mate.*\n'

    m = re.match(pattern, text)

    if not m:
        raise Exception('regex did not match')

    results = {'flagstat': m.groupdict()}
    imagefile = None

    return (results, imagefile)

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    (results, imagefile) = flagstat(args.filename)

    if imagefile:
        print imagefile

    if results:
        print results

# 4198456 + 0 in total (QC-passed reads + QC-failed reads) 
# 0 + 0 duplicates 
# 4022089 + 0 mapped (95.80%:-nan%) 
# 4198456 + 0 paired in sequencing
# 2099228 + 0 read1 
# 2099228 + 0 read2 
# 3796446 + 0 properly paired (90.42%:-nan%)
# 4013692 + 0 with itself and mate mapped
# 8397 + 0 singletons (0.20%:-nan%)
# 167574 + 0 with mate mapped to a different chr
# 72008 + 0 with mate mapped to a different chr (mapQ>=5)
