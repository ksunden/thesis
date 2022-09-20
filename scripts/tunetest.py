import numpy as np
import pathlib

import attune
import WrightTools as wt
import matplotlib.pyplot as plt


folder = pathlib.Path(
    r"C:\Users\john\path\to\folder"
)
datapath = folder / "primary.wt5"

opa = "w1"
channel = "daq_signal_mean"
arrangement = "non-sh-sh-idl"
filtering = False
apply = False
sub_baseline = False
save_plot = apply

d = wt.open(datapath)


instr = attune.load(opa)

if channel == "array_ingaas":
    d.level(channel, -1, 5)  # leveling along array signal before moment

    if sub_baseline:
        baseline = wt.open(baseline_datapath)
        baseline.level("ingaas", -1, 5)
        d[channel][:] -= baseline[channel][:]

    if filtering == True:

        if arrangement == "non-non-non-sig":
            for i, w2_color in enumerate(d[f"{opa}_points"][:, 0]):
                if w2_color > 1490:
                    for j, array_pixel_color in enumerate(
                        d["wavelengths"][i, :]
                    ):
                        if array_pixel_color > np.min([1700, w2_color + 40]):
                            d.ingaas[i, j] = np.nan
                if w2_color > 1580:
                    for j, array_pixel_color in enumerate(
                        d["wavelengths"][i, :]
                    ):
                        if array_pixel_color < np.min([1700, w2_color - 20]):
                            d.ingaas[i, j] = np.nan

        if arrangement == "non-non-sh-idl":
            for i, w2_color in enumerate(d[f"{opa}_points"][:, 0]):
                if w2_color > 1120:
                    for j, array_pixel_color in enumerate(
                        d["wavelengths"][i, :]
                    ):
                        if (
                            1080
                            < array_pixel_color
                            < np.min([1105, w2_color - 10])
                        ):
                            d.ingaas[i, j] = np.nan
    d.transform(f"{opa}_points", f"array_wavelengths-{opa}")

else:
    d.transform(f"{opa}_points", f"wm-{opa}")

instr2 = attune.tune_test(
    data=d,
    channel=channel,
    arrangement=arrangement,
    instrument=instr,
    gtol=0.005,
    ltol=0.00,
    autosave=apply,
    save_directory=datapath.parent,
    s=3,  # "smoothness"
    k=1,  # number of nodes
)

if apply:
    import yaqc

    c = yaqc.Client(39300 + int(opa[1]))
    c.set_instrument(instr2.as_dict())
