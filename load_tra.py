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
                columns = [float(col.strip()) for col in columns]
                data.append(columns)
            lnum += 1
    out = {'name':tra_name, 'data':np.array(data).T[cols,:])
    return out


def load_tras(tra_names, colsep=';', cols=[], skip_lines=2):
    """
    Loads given .tra files into a list of load_single_tra's outputs.
    """
    out = list()
    for tra_name in tra_names:
        out.append(load_single_tra(tra_name, colsep=colsep, cols=cols, skip_lines=skip_lines))
    return out


def split_cycles(data, t_row=3, d_row=1, up_treshold=.1, down_treshold=-.1, start_up=True):
    """
    Splits measured data into loading/unloading cycles.
    Returns list of data-like arrays.
    """
    # diff data - left differences are used.
    ddata = np.diff(data[d_row]) / np.diff(data[t_row])

    ups = ddata < down_treshold
    dns = ddata > up_treshold
    current_up = start_up
    start_pt = 0
    out = []
    for i in range(len(ddata)):
        if (current_up and dns[i]) or (not(current_up) and ups[i]):
            stop_pt = i+1
            out.append(np.array([d[start_pt:stop_pt] for d in data]))
            current_up = not(current_up)
            start_pt = stop_pt
    return out

def smooth_data(data, cols=[0,], n=1, w=None):
    """
    Smoothes given columns in data and reshapes the other to the same dimension.
    """
    if w is None:
        w = np.ones(2 * n + 1)
    print 'w:', w
    out = []
    for ii, cc in enumerate(data):
        if ii in cols:
            out.append(np.array([
                sum(w * cc[jj - n : jj + n + 1]) / sum(w) for jj in range(n, len(cc) - n)]))
        else:
            out.append(np.array(cc[n:-n]))
    return out

if __name__ == '__main__':
    tra_files = sys.argv[1:]
    data = load_tras(tra_files, cols=[0,1,2,3], skip_lines=2)
    for dat in data:
        print dat.name, ' -> ', dat.name[dat.name.rfind('/') + 1:dat.name.rfind('.')]
        dat['name'] = dat['name'][dat['name'].rfind('/') + 1:dat['name'].rfind('.')]))

    cols = ('0', '.3', '.5')
    mark_styles = ('o', '^', 'v', 's', '>', '<')
    fs = 20

    # plot force vs. time
    plt.figure()
    leg = []
    for i, dat in enumerate(data):
        plt.plot(dat.data[3,:] / 3600.,dat.data[0,:] - dat.data[0,0],
                 marker = mark_styles[i % len(mark_styles)], markevery=(i * len(dat.data[3,:]) / 20, len(dat.data[3,:]) / 6), markersize=8, #markerfacecolor = '.9',
                 label = dat.name)
    plt.xlabel('time [h]', fontsize=fs)
    plt.ylabel('force [N]', fontsize=fs)
    plt.legend(loc=0, fontsize=fs)
    plt.setp(plt.gca().get_xticklabels() + plt.gca().get_yticklabels(), fontsize=fs)
    plt.grid()
    plt.tight_layout()

    plt.show()
