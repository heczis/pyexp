import numpy as np
import pylab as plt
import glob
import sys

def check_single_tra(tra_name, colsep=';'):
    """
    Checks if the given .tra file has the same number of columns
    in each row.
    """
    data = list()
    with open(tra_name) as f:
        for line in f:
            columns = line.split(colsep)
            data.append(len(columns))
    plt.figure()
    plt.plot(data)
    plt.title(tra_name)
    plt.show()
    return None

if __name__ == '__main__':
    tra_files = sys.argv[1:]
    for tra_name in tra_files:
        check_single_tra(tra_name, colsep=' ')

