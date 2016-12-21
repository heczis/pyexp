"""
Provides functions for operating on experimental data.
"""
import numpy as np

def diff(row, dnum=2):
    """
    Auxliary function for implementing finite differences.
    """
    return row[dnum:] - row[:-dnum]

def get_strain_rate(data, td_row=(0, 1), dnum=1):
    # diff data - left differences are used.
    ddata = diff(data[td_row[1]], dnum) / diff(data[td_row[0]], dnum)
    return ddata

def split_cycles(data, td_row=(0, 1), tresholds=(.1, -.1), start_up=True, dnum=1):
    """
    Splits measured data into loading/unloading cycles according to
    strain rate.

    data : np.array, each rows correspond to measured quantities
    td_row : which row of data contains measured time and displacement

    tresholds : strain rates at which loading/unloading is
      is considered as started. Has two components, first is the up-loading
      rate, second is the down-loading rate.

    start_up : boolean
      If True, the first loading cycle should start in tension.

    dnum : int
      Finite-differences step (in array indices)

    Returns list of data-like arrays.
    """
    # diff data - left differences are used.
    ddata = diff(data[td_row[1]], dnum) / diff(data[td_row[0]], dnum)

    ups = ddata > tresholds[0]
    dns = ddata < tresholds[1]
    current_up = start_up
    start_pt = 0
    out = []
    for i in range(len(ddata)):
        if (current_up and dns[i]) or (not(current_up) and ups[i]) \
           or (i == len(ddata)-1):
            stop_pt = i+1
            out.append(np.array([d[start_pt:stop_pt] for d in data]))
            current_up = not current_up
            start_pt = stop_pt
    return out

def trans_data_linear(x, y, a=2., b=.5, c=.75):
    """
    Transformation of data, linear in both coordinates.
    Can take the function's slope (at origin) into account.
    X = a * x
    Y = (c - (c-b)/a * x) * y
    """
    return (
        a * x,
        (c - (c-b)/a * x) * y)

def trans_data_power(x, y, ky=.5, m=2.):
    """
    Transformation if data, linear in y, power-law in x.
    """
    return (
        (x+1)**m-1,
        ky*y)
