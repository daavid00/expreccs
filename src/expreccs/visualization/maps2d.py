# SPDX-FileCopyrightText: 2023-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0
# pylint: disable=E1102,R0913,R0914,R0917

"""Generate two-dimensional maps for expreccs simulation results.

The module reshapes active-cell arrays onto top-surface grids and writes final
state, geological, and reference-to-site difference maps with consistent axes,
color scales, labels, and progress reporting.
"""

import sys
from contextlib import nullcontext

import matplotlib.pyplot as plt
import numpy as np
from alive_progress import alive_bar
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

from expreccs.utils.terminal import expreccs_info


def reshape_to_2d(array_1d, nx, ny):
    """Reshape a flat cell array onto a two-dimensional grid.

    Parameters
    ----------
    array_1d : Any
        Flat cell-data array.
    nx : Any
        Number of cells in the x direction.
    ny : Any
        Number of cells in the y direction.

    Returns
    -------
    np.ndarray
        Array reshaped to ``(ny, nx)`` with reversed rows.
    """
    expected = nx * ny

    if array_1d.size > expected:
        array_1d = array_1d[:expected]

    return array_1d.reshape(ny, nx)[::-1, :]


def plot_map(
    x,
    y,
    data,
    title,
    filename,
    cmap,
    units=None,
    xticks=True,
    yticks=True,
    show_colorbar=True,
    difference=False,
):
    """Write one two-dimensional field map.

    Parameters
    ----------
    x : Any
        X coordinates.
    y : Any
        Y coordinates.
    data : Any
        Values to plot.
    title : Any
        Figure title.
    filename : Any
        Output filename.
    cmap : Any
        Matplotlib colormap.
    units : Any, optional
        Colorbar label.
    xticks : Any, optional
        Whether to show x-axis ticks.
    yticks : Any, optional
        Whether to show y-axis ticks.
    show_colorbar : Any, optional
        Whether to draw a colorbar.
    difference : Any, optional
        Whether to use symmetric difference limits.
    """

    fig, axis = plt.subplots()

    imag = axis.pcolormesh(
        x,
        y,
        data,
        shading="flat",
        cmap=cmap,
    )

    axis.axis("scaled")

    if xticks:
        axis.set_xticks(np.linspace(np.min(x), np.max(x), 6))
    else:
        axis.set_xticks([])

    if yticks:
        axis.set_yticks(np.linspace(np.min(y), np.max(y), 6))
    else:
        axis.set_yticks([])

    axis.set_xlabel("Easting [km]")
    axis.set_ylabel("Northing [km]")
    axis.set_title(title)

    if show_colorbar:
        maxp = np.max(data)
        minp = np.min(data)

        if difference and minp < 0 < maxp:
            bnd = max(abs(maxp), abs(minp))
            maxp = bnd
            minp = -bnd

        cax = make_axes_locatable(axis).append_axes("right", size="5%", pad=0.05)

        ticks = np.linspace(minp, maxp, 5)

        fig.colorbar(
            imag,
            cax=cax,
            orientation="vertical",
            ticks=ticks,
            label=units,
            format=lambda x, _: f"{x:.2f}",
        )

        imag.set_clim(minp, maxp)

    fig.savefig(filename, bbox_inches="tight")
    plt.close()


def model_group(res):
    """Resolve a model name to its geometry group.

    Parameters
    ----------
    res : Any
        Reservoir case name.

    Returns
    -------
    str
        Normalized geometry-group name.
    """
    if "regional" in res:
        return "regional"
    if "site" in res:
        return "site"
    return res


def final_time_maps(dic):
    """Plot final-time fields for all selected reservoirs.

    Parameters
    ----------
    dic : Any
        Shared mutable expreccs configuration and runtime data.
    """
    expreccs_info("final time 2d maps:")

    show_progress = sys.stdout.isatty()
    if show_progress:
        bar_ctx = alive_bar(dic["tot"], bar="fish")
    else:
        bar_ctx = nullcontext()
    with bar_ctx as bar_animation:
        for nfol, fol in enumerate(dic["folders"]):
            for res in dic[fol]["decks"]:
                if show_progress:
                    bar_animation()
                name = model_group(res)

                nx = len(dic[fol][name]["xmx"]) - 1
                ny = len(dic[fol][name]["ymy"]) - 1

                x = dic[fol][name]["xcor"] / 1000.0
                y = dic[fol][name]["ycor"] / 1000.0

                for j, quantity in enumerate(dic["quantity"]):

                    data = reshape_to_2d(
                        dic[fol][res][f"{quantity}_array"][-1],
                        nx,
                        ny,
                    )

                    title = dic[f"l{res}"] + f" ({dic['lfolders'][nfol]})"

                    filename = f"{dic['where']}/{dic['id']}{res}_{dic['names'][j]}.png"

                    plot_map(
                        x,
                        y,
                        data,
                        title,
                        filename,
                        cmap=dic["cmaps"][j],
                        units=dic["units"][j],
                    )


def final_time_maps_difference(dic):
    """Plot final-time differences between reference and site models.

    Parameters
    ----------
    dic : Any
        Shared mutable expreccs configuration and runtime data.
    """
    expreccs_info("final time 2d maps difference:")
    show_progress = sys.stdout.isatty()
    if show_progress:
        bar_ctx = alive_bar(dic["tod"], bar="fish")
    else:
        bar_ctx = nullcontext()
    with bar_ctx as bar_animation:
        for fol in dic["folders"]:
            for res in dic[fol]["sites"]:
                if show_progress:
                    bar_animation()
                name = model_group(res)

                nx = len(dic[fol]["site"]["xmx"]) - 1
                ny = len(dic[fol]["site"]["ymy"]) - 1

                x = dic[fol][name]["xcor"] / 1000.0
                y = dic[fol][name]["ycor"] / 1000.0

                for j, quantity in enumerate(dic["quantity"]):

                    diff = (
                        dic[fol]["reference"][f"{quantity}_array"][-1][
                            dic[fol]["reference"]["fipn"] != 2
                        ]
                        - dic[fol][res][f"{quantity}_array"][-1]
                    )

                    if quantity in ["FLOWATI+", "FLOGASI+"]:
                        for k in range(ny):
                            diff[(k + 1) * nx - 1] = 0

                    if quantity in ["FLOWATJ+", "FLOGASJ+"]:
                        for k in range(nx):
                            diff[(ny - 1) * nx + k] = 0

                    data = reshape_to_2d(diff, nx, ny)

                    magnitude = np.abs(np.sum(data))

                    title = (
                        r"SITE $\sum$|REF-" + f"{dic[f'l{res}']}" + f"|={magnitude:.2E}"
                    )

                    filename = f"{dic['where']}/{dic['id']}difference_{res}_{dic['names'][j]}.png"

                    plot_map(
                        x,
                        y,
                        data,
                        title,
                        filename,
                        cmap="seismic",
                        units=dic["units"][j],
                        difference=True,
                    )


def geological_maps(dic):
    """Plot static geological properties for selected reservoirs.

    Parameters
    ----------
    dic : Any
        Shared mutable expreccs configuration and runtime data.
    """
    expreccs_info("static 2d maps:")
    show_progress = sys.stdout.isatty()
    if show_progress:
        bar_ctx = alive_bar(dic["tot"], bar="fish")
    else:
        bar_ctx = nullcontext()
    with bar_ctx as bar_animation:
        for fol in dic["folders"]:
            for res in dic[fol]["decks"]:
                if show_progress:
                    bar_animation()
                name = model_group(res)

                nx = len(dic[fol][name]["xmx"]) - 1
                ny = len(dic[fol][name]["ymy"]) - 1

                x = dic[fol][name]["xcor"] / 1000.0
                y = dic[fol][name]["ycor"] / 1000.0

                for quan in dic[fol][res]["static"]:

                    if quan == "fipn" and dic[fol][res]["sensorijk"][2] == 0:
                        dic[fol][res][quan][
                            dic[fol][res]["sensorijk"][0]
                            + dic[fol][res]["sensorijk"][1] * nx
                        ] = 3

                    data = reshape_to_2d(
                        dic[fol][res][quan],
                        nx,
                        ny,
                    )

                    if quan == "fipn":
                        cmap = colors.ListedColormap(["red", "gray", "blue"])
                        title = dic[f"l{res}"] + " (site in red, sensor in blue)"
                        show_cb = False
                    else:
                        cmap = "jet"
                        title = dic[f"l{res}"] + f" {quan}"
                        show_cb = True

                    filename = (
                        f"{dic['where']}/{dic['id']}{res}_"
                        + ("fipnum_sensor" if quan == "fipn" else quan)
                        + ".png"
                    )

                    plot_map(
                        x,
                        y,
                        data,
                        title,
                        filename,
                        cmap=cmap,
                        units=None,
                        xticks=False,
                        yticks=False,
                        show_colorbar=show_cb,
                    )
