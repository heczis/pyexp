"""
Provides functions for reading .tra files (measured quantities in
columns, each row corresponds to one time instant).
"""
import numpy as np
import pylab as plt
import os
import argparse
import codecs

def load_single_tra(tra_name, colsep=';', cols=None, skip_lines=2):
    """
    Loads a single .tra file named tra_name, skipping skip_lines first
    lines, columns separated by colsep, rows by newline.
    Returns columns with indices given in cols (in given order) as a
    list; nonexistent indices raise error.
    """
    data = []
    if cols is not None:
        with codecs.open(tra_name, 'r', encoding='utf-8', errors='ignore') as f:
            for lnum, line in enumerate(f):
                if lnum >= skip_lines:
                    columns = line.strip().split(colsep)
                    columns = [
                        float(col.strip().replace(',', '.'))
                        for col in columns if len(col) > 0]
                    if len(columns) >= max(cols):
                        data.append(columns)
            print(tra_name, ' data.shape =', np.array(data).shape)
    out = {'name':tra_name, 'data':np.array(data).T[cols, :]}
    return out

def load_tras(tra_names, colsep=';', cols=None, skip_lines=2):
    """
    Loads given .tra files into a list of load_single_tra's outputs.
    """
    out = []
    if cols is not None:
        for tra_name in tra_names:
            out.append(load_single_tra(tra_name, colsep=colsep, cols=cols, skip_lines=skip_lines))
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Load given TRA files and plot the data.')
    parser.add_argument(
        'file', metavar='FILE', nargs='+', type=str,
        help='TRA file(s) to be read.')
    parser.add_argument(
        '--colsep', '-c', metavar='COLSEP', type=str, default=';',
        help='column separator')
    parser.add_argument(
        '--colnum', '-n', metavar='NUM', type=int, default='2',
        help='number of columns to read')
    parser.add_argument(
        '--skiplines', metavar='SKIP', type=int, default='2',
        help='how many lines to skip at the beginning of each TRA file')
    args = parser.parse_args()

    tra_files = args.file
    column_separator = args.colsep
    colnum = args.colnum
    skiplines = args.skiplines

    if tra_files:
        data = load_tras(tra_files, colsep=column_separator,
                         cols=range(colnum), skip_lines=skiplines)
        for dat in data:
            dat['name'] = dat['name'][dat['name'].rfind(os.sep) + 1:dat['name'].rfind('.')]

        # plot force vs. displacement
        plt.figure()
        for i, dat in enumerate(data):
            plt.plot(dat['data'][1, :], dat['data'][0, :],
                     label=dat['name'])
        plt.xlabel('displacement [mm]')
        plt.ylabel('force [N]')
        plt.legend(loc=0)
        plt.grid()

        plt.show()
