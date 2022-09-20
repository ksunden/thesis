import os
import time
import itertools
import collections

import numpy as np

import WrightTools as wt

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import PyDAQmx

conversions_per_second = 1e6  # a property of the DAQ card
shots_per_second = 1100.0  # from laser (ensure OVERestimate)


def round_robin(channels, index, shots=7, plot=True, cycle="rgbk", freq=False):
    """Collect and plot data from a NI DAQ card.

    Parameters
    ----------
    channels : dictionary
        Dictionary of {name, index}.
    index : integer
        Plot a black vertial line at this index for every shot.
    shots : integer (optional)
        Number of shots to acquire. Default is 7.
    plot : boolean (optional)
        Toggle plotting. Default is True.
    cycle : iterable (optional)
        Color cycle for shot highlighting in background. Default is rgbk.
    """
    # coerce inputs
    channels = collections.OrderedDict(channels)
    task_handle = PyDAQmx.TaskHandle()
    read = PyDAQmx.int32()
    num_channels = len(channels)
    virtual_samples = int(
        conversions_per_second / (shots_per_second * num_channels)
    )
    us_per_virtual_sample = (1.0 / conversions_per_second) * 1e6
    try:
        # task
        PyDAQmx.DAQmxCreateTask("", PyDAQmx.byref(task_handle))
        # create global channels
        total_virtual_channels = 0
        for _ in range(virtual_samples):
            for channel in channels.keys():
                channel_name = "channel_" + str(total_virtual_channels).zfill(
                    2
                )
                PyDAQmx.DAQmxCreateAIVoltageChan(
                    task_handle,  # task handle
                    "Dev1/ai%i" % channel,  # physical chanel
                    channel_name,  # name to assign to channel (must be unique)
                    PyDAQmx.DAQmx_Val_Diff,  # the input terminal configuration
                    -10,
                    10,  # minVal, maxVal
                    PyDAQmx.DAQmx_Val_Volts,  # units
                    None,
                )  # custom scale
                total_virtual_channels += 1
        # timing
        PyDAQmx.DAQmxCfgSampClkTiming(
            task_handle,  # task handle
            "/Dev1/PFI0",  # sorce terminal
            1000.0,  # sampling rate (samples per second per channel) (float 64)
            PyDAQmx.DAQmx_Val_Rising,  # acquire samples on the rising edges
            PyDAQmx.DAQmx_Val_FiniteSamps,  # acquire a finite number of samples
            shots,
        )  # number of samples per global channel (unsigned integer 64)
    except PyDAQmx.DAQError as err:
        print("DAQmx Error: %s" % err)
        PyDAQmx.DAQmxStopTask(task_handle)
        PyDAQmx.DAQmxClearTask(task_handle)
        return
    # get data
    samples = np.zeros(
        shots * virtual_samples * num_channels, dtype=np.float64
    )
    for _ in range(1):
        try:
            start_time = time.time()
            PyDAQmx.DAQmxStartTask(task_handle)
            PyDAQmx.DAQmxReadAnalogF64(
                task_handle,  # task handle
                shots,  # number of samples per global channel (uint64)
                10.0,  # timeout (seconds) for each read operation
                # fill mode (specifies if the samples are interleaved)
                PyDAQmx.DAQmx_Val_GroupByScanNumber, 
                samples,  # read array
                len(
                    samples
                ),  # size of the array, in samples, into which samples are read
                PyDAQmx.byref(read),  # reference of thread
                None,
            )  # reserved by NI, pass NULL (?)
            PyDAQmx.DAQmxStopTask(task_handle)
            # create 2D data array
            out = np.copy(samples)
            out.shape = (shots, virtual_samples, num_channels)
            print(
                "Acquired %d shots in %f seconds"
                % (read.value, time.time() - start_time)
            )
        except PyDAQmx.DAQError as err:
            print("DAQmx Error: %s" % err)
            PyDAQmx.DAQmxStopTask(task_handle)
            PyDAQmx.DAQmxClearTask(task_handle)
            return
    # plot
    def get_plot_arrays(channel):
        y = out[:, :, channel].flatten()
        x = np.zeros(len(y))
        for i in range(shots * virtual_samples):
            offset = us_per_virtual_sample * channel
            shot_count, sample_count = divmod(i, virtual_samples)
            x[i] = (
                offset
                + shot_count * 1000
                + sample_count * (us_per_virtual_sample * num_channels)
            )
        mag = max(-y.min(), y.max())
        y /= mag
        return x, y

    if plot:
        # data
        fig = plt.figure(figsize=(10, 4))
        ax = plt.gca()

        for i, item in enumerate(channels.items()):
            plt.plot(*get_plot_arrays(i), lw=4, alpha=0.5, label=item[1])
        # boxes
        cs = itertools.cycle(cycle)
        for i in range(shots):
            rect = patches.Rectangle(
                (i * 1000, -1.1),
                1000,
                2.2,
                zorder=0,
                facecolor=next(cs),
                edgecolor="none",
                alpha=0.1,
            )
            ax.add_patch(rect)
        # lines
        for i in range(shots):
            plt.axvline(i * 1000 + index, c="k")
        plt.legend(loc="upper left", bbox_to_anchor=(1.04, 1))
        ax.set_xlim(0, shots * 1000)
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlabel(r"$\mu$s", fontsize=18)
    if freq:
        fig, gs = wt.artists.create_figure(
            width=10, nrows=3, default_aspect=0.25
        )

        for i, item in enumerate(channels.items()):
            ax = plt.subplot(gs[i])
            x, y = get_plot_arrays(i)
            x *= 1e-6
            x2, y2 = wt.kit.fft(x, y)
            y2 = np.abs(y2)
            y2 /= y2.max()
            ax.loglog(x2, y2, alpha=0.5, label=item[1])
            ax.set_xlim(100, 10000)
            plt.legend(loc="upper left", bbox_to_anchor=(1.04, 1))
            ax.grid()
        wt.artists.set_fig_labels(xlabel="frequency(Hz)", ylabel="abs")

    # finish 
    if task_handle:
        PyDAQmx.DAQmxStopTask(task_handle)
        PyDAQmx.DAQmxClearTask(task_handle)
    return out


channels = collections.OrderedDict()
# channel numbers here are the physical channels
channels[0] = "signal"
channels[4] = 'chopper 1'
channels[5] = "chopper 2"  # 1=open, 0=blocked
channels[3] = 'Pyro 2'
channels[2] = 'Pyro 1'

round_robin(channels, index=590, shots=10, plot=True, freq=False)
plt.show()
