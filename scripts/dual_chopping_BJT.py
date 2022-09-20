from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import numpy as np


def process(shots, names, kinds):
    """
    Parameters
    ----------
    shots : ndarray
        A ndarray (inputs, shots)
    names : list of str
        A list of input names
    kinds : list of {'channel', 'chopper'}
        Kind of each input

    Returns
    -------
    list
        [ndarray (channels), list of channel names]
    """
    channel_indicies = [i for i, x in enumerate(kinds) if x == "channel"]
    out = np.full(len(channel_indicies) + 1, np.nan)
    channel_indicies.pop(0)
    out_names = []
    # signal diff
    #            A B C D
    # chopper 1: - + + -
    # chopper 2: - - + +
    #   we want A-B+C-D
    c1 = shots[-2]
    c2 = shots[-1]
    a = np.mean(shots[0, (c1 == -1) * (c2 == -1)])
    b = np.mean(shots[0, (c1 == +1) * (c2 == -1)])
    c = np.mean(shots[0, (c1 == +1) * (c2 == +1)])
    d = np.mean(shots[0, (c1 == -1) * (c2 == +1)])
    out[0] = a - b + c - d
    out_names.append("signal_diff")
    # signal mean
    out[1] = np.mean(shots[0])
    out_names.append("signal_mean")
    # others
    for i in channel_indicies:
        out[i + 1] = np.mean(shots[i])
        out_names.append(names[i])
    # finish
    return [out, out_names]
