# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 16:08:50 2021

@author: John
"""
import WrightTools as wt
import pathlib
import matplotlib.pyplot as plt
import numpy as np

folder = pathlib.Path(
    r"G:\My Drive\Perovskite\CMDS\2021-10-20\(PA)2(EA)Pb2I7\2D harmonic generation"
)
datapath = folder / "data.wt5"
d = wt.open(datapath)
# d.signal_ratio.signed = True

# d = d.split('wm_points', (12500, 17500))[1]
# d = d.split('d0_points', 0.5)[0]
# d.smooth(3)
# d.create_variable('w1_is_wm_points', d["w1=wm_points"], units = 'wn')

# d.transform('wm_points', 'w2_points')
# d.transform('nd1_points')
# d.level('signal_ratio',0, 5 )

# d_first = d.split(1, [18800, 13000])[1]
# d_first.moment(0, 'signal_ratio', 0)
# plt.plot(d_first.wm_points[:], d_first.signal_ratio_0_moment_0[:])
# d_first.smooth([2,0])
# d.create_variable('delay', -1*d.d0_points[:])

# d.transform('wm_points', 'delay')
# d.create_channel('new_channel', values = np.sqrt(d.signal_mean[:]))
# wt.artists.quick2D(d, channel = 'new_channel', autosave=False, save_directory=folder)
wt.artists.quick2D(d)
