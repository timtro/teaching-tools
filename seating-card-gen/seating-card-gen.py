#!/usr/bin/env python3

import random
import argparse
from itertools import zip_longest
import pandas as pd

from TeXPlaceCardFile import TeXPlaceCardFile


def main(eventTitle, rosterFilePath, manifestFilePath, texFilename):

    roster = pd.read_csv(rosterFilePath, index_col='Username')
    roster['Seat Number'] = random.sample(
        range(1, len(roster) + 1), len(roster))
    roster = roster.sort_values(by='Seat Number')

    roster[['First Name', 'Last Name', 'Seat Number']].to_csv(manifestFilePath)

    # An empty value to use as padding in case the population of the roster is
    # not evenly divisible by 4:
    dfEmpty = ("XXXXXXXXX", pd.Series(
        {
            'First Name': 'XX',
            'Last Name': 'XX',
            'Seat Number': 'XX'
        },
        index=['First Name', 'Last Name', 'Seat Number'],
        name='XXXXXXXXX'))

    with TeXPlaceCardFile(texFilename, eventTitle) as tex:
        for fourBlock in grouper(
                roster[['First Name', 'Last Name', 'Seat Number']].iterrows(),
                4, dfEmpty):
            tex.print_placecard(fourBlock)


def grouper(iterable, n, fillvalue=None):
    chunks = [iter(iterable)] * n
    return zip_longest(*chunks, fillvalue=fillvalue)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate placecards with random seating from a CSV file. The file must have columns named "Username", "First Name" and "Last Name".'
    )
    parser.add_argument(
        '--title',
        dest='eventTitle',
        metavar='TITLE',
        help='Title displayed on the cards')
    parser.add_argument(
        'rosterFilePath',
        metavar='PATH',
        help='Path to CSV file containing Student ID, first and last names')
    parser.add_argument(
        '-m',
        '--manifest',
        dest='manifestFilePath',
        action='store',
        default=None,
        help='Destination for manifest.')
    parser.add_argument(
        '-t',
        '--texfile',
        dest='texfile',
        action='store',
        default='placecards.tex',
        help='Destination for texfile. Run through pdflatex.')
    parser.add_argument(
        '-r',
        '--rdmseed',
        dest='rdmseed',
        action='store',
        default=None,
        help='Seed for random number generator. Can be any hashabe object.')

    args = parser.parse_args()

    if args.rdmseed is None:
        random.seed(1)
    else:
        random.seed(args.rdmseed)

    main(args.eventTitle, args.rosterFilePath, args.manifestFilePath,
         args.texfile)
