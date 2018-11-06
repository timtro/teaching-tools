#!/usr/bin/env python3

import random
import argparse
from itertools import zip_longest
import pandas as pd

from TeXPlaceCardFile import TeXPlaceCardFile


def main_roster(eventTitle, rosterFilePath, manifestFilePath, texFilename):

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
        for fourBlock in by_n(
                roster[['First Name', 'Last Name', 'Seat Number']].iterrows(),
                4, dfEmpty):
            tex.print_placecard_sheet(fourBlock)


def main_blanks(eventTitle, nblank, texFilename):

    numbers = random.sample(range(1, nblank+1), nblank)
    # numbers = range(1, nblank+1)

    # An empty value to use as padding in case the population of the roster is
    # not evenly divisible by 4:
    dfEmpty = -99
    with TeXPlaceCardFile(texFilename, eventTitle) as tex:
        for fourBlock in by_n(numbers, 4, dfEmpty):
            tex.print_blank_placecard_sheet(fourBlock)

def by_n(iterable, n, fillvalue=None):
    chunks = [iter(iterable)] * n
    return zip_longest(*chunks, fillvalue=fillvalue)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate placecards with random seating from a CSV file. The file must have columns named "Username", "First Name" and "Last Name".'
    )
    parser.add_argument(
        '--nblank',
        dest='nblank',
        action='store',
        default=None,
        help='Number of blank placecards. If using this option, a roster and manifest path should not be provided.')
    parser.add_argument(
        '--title',
        dest='eventTitle',
        metavar='TITLE',
        help='Title displayed on the cards')
    parser.add_argument(
        '--roster',
        dest='rosterFilePath',
        metavar='PATH',
        default=None,
        help='Path to CSV file containing Student ID, first and last names')
    parser.add_argument(
        '--manifest',
        dest='manifestFilePath',
        action='store',
        default=None,
        help='Destination for manifest.')
    parser.add_argument(
        '--texfile',
        dest='texfile',
        action='store',
        default='placecards.tex',
        help='Destination for texfile. Run through pdflatex.')
    parser.add_argument(
        '--rdmseed',
        dest='rdmseed',
        action='store',
        default=None,
        help='Seed for random number generator. Can be any hashabe object.')

    args = parser.parse_args()

    assert(args.eventTitle is not None)

    if args.rdmseed is None:
        random.seed(1)
    else:
        random.seed(args.rdmseed)


    if args.nblank is not None:
        assert(args.rosterFilePath is None)
        assert(args.manifestFilePath is None)
        main_blanks(args.eventTitle, int(args.nblank), args.texfile)
    else:
        assert(args.nblank is None)
        assert(args.rosterFilePath is not None)
        assert(args.manifestFilePath is not None)
        main_roster(args.eventTitle, args.rosterFilePath, args.manifestFilePath,
             args.texfile)
