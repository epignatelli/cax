import jax
import jax.numpy as np
import numpy as onp
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FuncFormatter
import IPython
from IPython.display import HTML
import math
from . import convert


def plot_state(state, **kwargs):
    array = tuple(state)
    fig, ax = plt.subplots(1, len(array), figsize=(kwargs.pop("figsize", None) or (25, 5)))
    vmin = kwargs.pop("vmin", 0)
    vmax = kwargs.pop("vmax", 1)
    cmap = kwargs.pop("cmap", "RdBu")

    for i in range(len(ax)):
        im = ax[i].imshow(array[i], vmin=vmin, vmax=vmax, cmap=cmap, **kwargs)
        plt.colorbar(im, ax=ax[i])
        ax[i].set_title(state._fields[i])
        ax[i].xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y / 100)))
        ax[i].set_xlabel("x [cm]")
        ax[i].yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y / 100)))
        ax[i].set_ylabel("y [cm]")
    return fig, ax


def animate_state(states, times=None, **kwargs):
    cached_backend = matplotlib.get_backend()
    matplotlib.use("nbAgg")
    fig, ax = plt.subplots(1, len(states[0]), figsize=(kwargs.pop("figsize", None) or (25, 5)))
    vmin = kwargs.pop("vmin", 0)
    vmax = kwargs.pop("vmax", 1)
    cmap = kwargs.pop("cmap", "RdBu")
    times = times or range(len(states))

    # setup figure
    state = states[0]
    graphics = []
    for i in range(len(ax)):
        im = ax[i].imshow(state[i], vmin=vmin, vmax=vmax, cmap=cmap, **kwargs)
        plt.colorbar(im, ax=ax[i])
        ax[i].set_title(state._fields[i])
        ax[i].xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y / 100)))
        ax[i].set_xlabel("x [cm]")
        ax[i].yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y / 100)))
        ax[i].set_ylabel("y [cm]")
        fig.title = "time: {}".format(times[0])
        graphics.append(im)

    def update(t):
        state = states[t]
        for i in range(len(ax)):
            im = graphics[i].set_data(state[i])
            fig.title = "time: {}".format(times[t])
        return graphics


    animation = FuncAnimation(fig, update, frames=range(len(states)), blit=True)
    matplotlib.use(cached_backend)
    return animation


def show_grid(states, times=[], figsize=None, rows=5, font_size=10, vmin=-85, vmax=15, cmap="magma"):
    cols = math.ceil(len(states) / rows)
    rows = max(2, min(rows, len(states)))
    fig, ax = plt.subplots(cols, rows, figsize=figsize)
    ax = ax.flatten()
    idx = 0

    plt.rc('font', size=font_size)          # controls default text sizes
    plt.rc('axes', titlesize=font_size)     # fontsize of the axes title
    plt.rc('axes', labelsize=font_size)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=font_size)    # fontsize of the tick labels
    plt.rc('legend', fontsize=font_size)    # legend fontsize
    plt.rc('figure', titlesize=font_size)  # fontsize of the figure title

    for idx in range(len(states)):
        im = ax[idx].imshow(states[idx], cmap=cmap, vmin=vmin, vmax=vmax,)
        ax[idx].xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y / 100)))
        ax[idx].set_xlabel("x [cm]")
        ax[idx].yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y / 100)))
        ax[idx].set_ylabel("y [cm]")
        cbar = fig.colorbar(im, ax=ax[idx])
        cbar.ax.set_title("mV")
        if idx + 1 < len(times):
            ax[idx].set_title("t: {:d}".format(times[idx]))
    fig.tight_layout()
    return fig, ax


def show3d(state, rcount=200, ccount=200, zlim=None, figsize=None):
    # setup figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(projection="3d")
    # make surface plot
    r = list(range(0, len(state)))
    x, y = np.meshgrid(r, r)
    plot = ax.plot_surface(x, y, state, rcount=rcount, ccount=ccount, cmap="magma")
    # add colorbar
    cbar = fig.colorbar(plot)
    cbar.ax.set_title("mV")
    if zlim is not None:
        ax.set_zlim3d(zlim[0], zlim[1])
    # format axes
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y / 100)))
    ax.set_xlabel("x [cm]")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y / 100)))
    ax.set_ylabel("y [cm]")
    ax.set_zlabel("Voltage [mV]")
    # crop image
    fig.tight_layout()
    return fig, ax


def plot_stimuli(*stimuli, **kwargs):
    fig, ax = plt.subplots(1, len(stimuli), figsize=(kwargs.pop("figsize", None) or (10, 3)))
    vmin = kwargs.pop("vmin", -1)
    vmax = kwargs.pop("vmax", 1)
    cmap = kwargs.pop("cmap", "RdBu")
    for i, stimulus in enumerate(stimuli):
        im = ax[i].imshow(stimulus.field, vmin=vmin, vmax=vmax, cmap=cmap, **kwargs)
        plt.colorbar(im, ax=ax[i])
        ax[i].set_title("Stimulus %d" % i)
    plt.show()
    return