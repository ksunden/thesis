import matplotlib.pyplot as plt
from bluesky.simulators import plot_raster_path
from ophyd.sim import motor1, motor2, det
from bluesky.plans import grid_scan, spiral

fig, axs = plt.subplot_mosaic("A\nB")
fig.set_size_inches(3.5, 6)

plan1 = grid_scan([det], motor1, -0.5, 0.5, 10, motor2, -0.5, 0.5, 10)
plot_raster_path(plan1, 'motor2', 'motor1', probe_size=.02, ax=axs["A"])

plan2 = spiral([det], motor1, motor2, x_start=0.0, y_start=0.0, x_range=1.,
              y_range=1.0, dr=0.1, nth=10)
plot_raster_path(plan2, 'motor2', 'motor1', probe_size=.02, ax=axs["B"])

plt.savefig("plan_raster.png")
