import pathlib
import attune
import WrightTools as wt

data_dir = pathlib.Path(
    r"C:\Users\john\bluesky-cmds-data\folder"
)

# data.wt5 (yaqc) or primary.wt5 (bluesky)
data_filename = "primary.wt5"

# wavelengths (yaqc) or array_wavelengths (bluesky)
array_axis = "array_wavelengths"

# ingaas (yaqc) or array_ingaas (bluesky)
channel_name = "array_ingaas"

opa = "w2"
apply = True
old_instrument = attune.load(opa)

data = wt.open(data_dir / data_filename)

data.transform(f"{opa}_crystal_1", f"{opa}_delay_1", array_axis)
data.level(channel_name, -1, 5)

new_instrument = attune.holistic(
    data=data,
    channels=channel_name,
    arrangement="non-non-non-sig",
    tunes=["crystal_1", "delay_1"],
    instrument=old_instrument,
    save_directory=data_dir,
    autosave=apply,
    level=False,
    gtol=0.04,
)


if apply:
    import yaqc

    c = yaqc.Client(39300 + int(opa[1]))
    c.set_instrument(new_instrument.as_dict())
