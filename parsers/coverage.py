#!/usr/bin/env python3

from argparse import ArgumentParser

def imagenoop(filename):
    results = None
    image = filename
    return (results, image)

def coverage_summary(filename):
    resultsname = 'coverage_summary'
    results = {resultsname : {}}
    with open(filename) as f:
        lines = []
        for line in f:
            lines.append(line)
        results[resultsname]['lines'] = lines
        return (results, None)

def parsetable(filename):
    # TODO
    return None

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('parser')
    parser.add_argument('filename')
    args = parser.parse_args()

    (results, imagefiles) = parsetable(args.filename)
    print(results)


