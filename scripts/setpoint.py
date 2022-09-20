import pathlib
import WrightTools as wt
import attune
import numpy as np

folder = pathlib.Path(
    r"C:\Users\john\path\to\folder"
)

# data.wt5 (yaqc) or primary.wt5 (bluesky)
data_filename = "primary.wt5"

datapath = folder / data_filename
opa = "w2"

# ingaas (yaqc) or array_ingaas (bluesky)
channel = "array_ingaas"

arrangement = "non-non-non-sig"
tune = "crystal_2"
apply = True
simple_filter = True

# "wavelengths" in yaqc-cmds, array_wavelengths in bluesky
array_axis = "array_wavelengths"

d = wt.open(datapath)

instr = attune.load(opa)

if channel == "ingaas":
    d.transform(f"{opa}_points", f"{opa}_{tune}_points", "wavelengths")
    # second argument might be "w1_Delay_2", "w1_Delay_2_centers"
    # data.print_tree()
    d.level("ingaas", -1, 5)  # leveling along array signal before moment

    if simple_filter == True:
        if arrangement == "non-non-non-sig":
            for i, w2_color in enumerate(d[f"{opa}_points"][:, 0]):
                for k, array_pixel_color in enumerate(
                    d["wavelengths"][i, 0, :]
                ):
                    if (
                        array_pixel_color >= w2_color + 50
                        or array_pixel_color <= w2_color - 50
                    ):
                        for j, signal in enumerate(d.ingaas[i, :, k]):
                            d.ingaas[i, j, k] = np.nan
if channel == "array_ingaas":
    d.transform(f"{opa}_{tune}_points", f"{opa}_points", "array_wavelengths")
    # second argument might be "w1_Delay_2", "w1_Delay_2_centers"
    # data.print_tree()
    d.level("array_ingaas", -1, 5)  # leveling along array signal before moment

    if simple_filter == True:
        if arrangement == "non-non-non-sig":
            d[channel][
                abs(d[array_axis][:] - d[f"{opa}_points"][:]) > 50
            ] = np.nan


d.moment(
    axis=array_axis,
    channel=channel,
    moment=0,
    resultant=wt.kit.joint_shape(d[opa], d[f"{opa}_{tune}_points"]),
)
d.moment(
    axis=array_axis,
    channel=channel,
    moment=1,
    resultant=wt.kit.joint_shape(d[opa], d[f"{opa}_{tune}_points"]),
)
channel = -1
gtol = 0.005
d.channels[-1][d.channels[-2] < gtol * d.channels[-2].max()] = np.nan

d.transform(f"{opa}_points", f"{opa}_{tune}_points")
d.channels[-1].clip(min=d[f"{opa}"].min() - 1000, max=d[f"{opa}"].max() + 1000)
d.channels[-1].null = d[
    array_axis
].min()  # setting effective zero to be wa min

instr2 = attune.setpoint(
    data=d,
    channel=channel,
    arrangement=arrangement,
    tune=tune,
    instrument=instr,
    autosave=apply,
    save_directory=datapath.parent,
    s=1,
    k=3,
)

if apply:
    import yaqc

    c = yaqc.Client(39300 + int(opa[1]))
    c.set_instrument(instr2.as_dict())
