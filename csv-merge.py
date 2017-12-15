#!/usr/bin/env python3

import argparse
from functools import reduce, partial
import pandas as pd


def main(csvFiles, outfile, index=None):

    assert len(csvFiles) > 1

    merge = partial(pd.merge, left_index=True, right_index=True, how='outer')
    read = partial(pd.read_csv, index_col=index)

    combined = reduce(merge, map(read, csvFiles))
    combined.to_csv(outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Plot a histogram from a column of a csv file.')
    parser.add_argument('csvFiles', nargs='+', metavar='PATHS',
                        help='Path to CSV file')
    parser.add_argument('csvOutput', metavar='PATH',
                        help='Path to combined CSV file output')
    parser.add_argument('-i', '--index', default="Username",
                        help='Index column name. (Must be same in all files.)')
    args = parser.parse_args()

    main(args.csvFiles, args.csvOutput, args.index)
