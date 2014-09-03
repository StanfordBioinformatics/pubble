#!/usr/bin/env python

from argparse import ArgumentParser

def imagenoop(filename):
    results = None
    image = filename
    return (results, image)

def parsetable(filename):
    # TODO
    return None

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('parser')
    parser.add_argument('filename')
    args = parser.parse_args()

    (results, imagefiles) = parsetable(args.filename)
    print results


