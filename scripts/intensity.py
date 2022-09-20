import pathlib
import WrightTools as wt
import attune
import numpy as np

folder = pathlib.Path(r"C:\Users\John\path\to\folder")


# data.wt5 (yaqc) or primary.wt5 (bluesky)
data_filename = "primary.wt5"

# only matters if using ingaas.
# Should be wavelengths (yaqc) or array_wavelengths (bluesky)
array_axis = "array_wavelengths"


datapath = folder / data_filename
opa = "w1"
channel = "daq_sample"
arrangement = "non-sh-sh-idl"
tune = "mixer_2"
apply = False


d = wt.open(datapath)
d.transform(
    f"{opa}_points", f"{opa}_{tune}_points"
)
# The `_points` arrays represent the squeezed versions of the arrays
# Some methods require this.


instr = attune.load(opa)

if channel == "ingaas" or channel == "array_ingaas":
    d.transform(f"{opa}_points", f"{opa}_{tune}_points", array_axis)
    # second argument might be "w1_Delay_2", "w1_Delay_2_centers"
    # data.print_tree()
    d.level(channel, -1, 5)  # leveling along array signal before moment

    d.moment(
        axis=array_axis,
        channel=channel,
        moment=0,
        resultant=wt.kit.joint_shape(d[opa], d[f"{opa}_{tune}_points"]),
    )
    channel = -1
    d.transform(
        f"{opa}_points", f"{opa}_{tune}_points"
    )


instr2 = attune.intensity(
    data=d,
    channel=channel,
    arrangement=arrangement,
    tune=tune,
    instrument=instr,
    gtol=0.01,
    autosave=apply,
    save_directory=datapath.parent,
)


# This section sets the instrument as the active instrument for the OPA
if apply:
    import yaqc

    c = yaqc.Client(39300 + int(opa[1]))
    c.set_instrument(instr2.as_dict())
