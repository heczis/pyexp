"""
Provides functions for operating on experimental data.
"""
import numpy as np

def split_cycles(data, t_row=0, d_row=1, up_treshold=.1, down_treshold=-.1, start_up=True):
    """
    Splits measured data into loading/unloading cycles according to
    strain rate.

    data : np.array, each rows correspond to measured quantities
    t_row : which row of data contains measured time
    d_row : which row of data contains measured displacement

    up-/down_treshold : strain rates at which loading/unloading is
      is considered as started

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
        if ((current_up and dns[i]) or (not(current_up) and ups[i])
            or i == len(ddata)-1):
            stop_pt = i+1
            out.append(np.array([d[start_pt:stop_pt] for d in data]))
            current_up = not(current_up)
            start_pt = stop_pt
    return out
