import WrightTools as wt
import attune
import pathlib

data_dir = pathlib.Path(
    r"C:\Users\John\path\to\folder"
)
data = wt.open(data_dir / "primary.wt5")

opa = "w2"
delay = "d1"
channel = "daq_signal_mean"
arrangement = opa
tune = "non-sh-non-sig"
curve = f"autonomic_{delay}"
store = False
autosave = store

data.transform(f"{opa}_points", f"{delay}_points")
data.print_tree()
data.level(1, 1, -4)

instr = attune.intensity(
    data=data,
    channel=channel,
    arrangement=arrangement,
    level=False,
    tune=tune,
    ltol=0.01,
    gtol=0.01,
    # s=1,
    # k=1,
    autosave=autosave,
    save_directory=data_dir,
)

# This should be fixed in the workup method itself
instr.arrangements[opa][tune]._dep_units = data[f"{delay}_points"].units

instr = attune.update_merge(attune.load(arrangment), instr)

if store: 
    # Requires restart of the associated daemon to take effect
    attune.store(instr)
