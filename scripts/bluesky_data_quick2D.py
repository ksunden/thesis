import WrightTools as wt
import matplotlib.pyplot as plt
import pathlib

fil_dir = pathlib.Path(r"C:\Users\Wright\path\to\data\folder")
data = wt.open(fil_dir / "primary.wt5")
data.convert("wn")

wt.artists.quick2D(
    data, xaxis=0, yaxis=1, channel="daq_ai0_diff_abcd", pixelated=False
)
plt.show()
data.print_tree()
