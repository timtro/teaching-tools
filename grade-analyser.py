#!/usr/bin/env python3

import argparse
from math import ceil

import pandas as pd
import numpy as np
import pylab as plt
import matplotlib.mlab as mlab


def main(csvFile, colName, bins=None, rng=None):

    table = pd.read_csv(csvFile, header=0, index_col=0)

    if rng is None:
        make_histogram(table[colName], bins=bins)
    else:
        assert len(rng) == 2
        make_histogram(table[colName], bins=bins, min=rng[0], max=rng[1])

    plt.show()


def make_histogram(data, min=None, max=None, bins=None, colour='k', alpha=.65):
    data = data[np.isfinite(data)]
    if min is None:
        min = 0
    if max is None:
        max = ceil(data.max())

    if bins is None:
        mplBins = np.arange(min, max, 1)
    else:
        mplBins = np.linspace(min, max, bins + 2)

    plt.hist(
        data,
        bins=mplBins,
        normed=True,
        histtype='bar',
        color=colour,
        alpha=alpha)
    plt.axvline(data.mean(), color=colour, linestyle='dashed', linewidth=1)
    fit_normal(data, colour=colour)
    print_stats(data)


def print_stats(data):
    data = data[np.isfinite(data)]
    print('  Data Count: ' + str(data.size) + ',  Mean: ' + str(data.mean()) +
          ',  SD: ' + str(data.std()) + ', MIN: ' + str(
              data.min()) + ', MAX: ' + str(data.max()))


def fit_normal(data, colour='k', scalef=1):
    sigma = data.std()
    mu = data.mean()
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
    plt.plot(x, mlab.normpdf(x, mu, sigma) * scalef, color=colour)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Plot a histogram from a column of a csv file.')
    parser.add_argument('csvFilename', metavar='PATH', help='Path to CSV file')
    parser.add_argument(
        'colName', metavar='COLUMN', help='Name of column to plot in CSV file')
    parser.add_argument(
        '-b', '--bins', type=int, help='Number of bins in histogram')
    parser.add_argument(
        '-r',
        '--range',
        type=int,
        nargs=2,
        metavar='RNG',
        help='Minimum and maximum for bins.')
    args = parser.parse_args()

    main(args.csvFilename, args.colName, args.bins, args.range)
