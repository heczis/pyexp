import numpy as np
import pylab as plt
import glob
import sys


def load_single_tra(tra_name, colsep=';', cols=[], skip_lines=2):
    """
    Loads a single .tra file named tra_name, skipping skip_lines first lines, columns separated by colsep, rows by newline.
    Returns columns with indices given in cols (in given order) as a list; nonexistent indices raise error.
    """
    data = list()
    with open(tra_name) as f:
        lnum = 0
        for line in f:
            if lnum >= skip_lines:
                columns = line.split(colsep)
                columns = [
                    float(col.strip().replace(',','.'))
                    for col in columns]
                data.append(columns)
            lnum += 1
    print(tra_name, ' data.shape =', np.array(data).shape)
    out = {'name':tra_name, 'data':np.array(data).T[cols,:]}
    return out

def load_tras(tra_names, colsep=';', cols=[], skip_lines=2):
    """
    Loads given .tra files into a list of load_single_tra's outputs.
    """
    out = list()
    for tra_name in tra_names:
        out.append(load_single_tra(tra_name, colsep=colsep, cols=cols, skip_lines=skip_lines))
    return out

if __name__ == '__main__':
    tra_files = sys.argv[1:]
    data = load_tras(tra_files, colsep=' ', cols=[0,1,2], skip_lines=2)
    for dat in data:
        dat['name'] = dat['name'][dat['name'].rfind('/') + 1:dat['name'].rfind('.')]

    # plot force vs. displacement
    plt.figure()
    for i, dat in enumerate(data):
        plt.plot(dat['data'][1,:], dat['data'][0,:],
                 label = dat['name'])
    plt.xlabel('displacement [mm]')
    plt.ylabel('force [N]')
    plt.legend(loc=0)
    plt.ylim((0, 40))
    plt.grid()
    
    plt.show()
