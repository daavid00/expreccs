# SPDX-FileCopyrightText: 2025-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Test the expreccs functionality to rotate grids and to handle generic 2D decks"""

import os
import pathlib

testpth: pathlib.Path = pathlib.Path(__file__).parent


def test_generic_deck_2d():
    """See configs/rotate_2d.toml"""
    if not os.path.exists(f"{testpth}/output"):
        os.system(f"mkdir {testpth}/output")
    os.chdir(f"{testpth}/output")
    os.system(
        f"expreccs -i {testpth}/configs/rotate_2d.toml -o rotate_2d -m all -t 30 -p site"
    )
    assert os.path.exists(
        f"{testpth}/output/rotate_2d/postprocessing/rotate_2d_site_closed_pressure.png"
    )
    os.system(
        f"scp -r {testpth}/output/rotate_2d/preprocessing/regional/. "
        f"{testpth}/output/rotate_2d/simulations/regional"
    )
    os.system(
        f"scp -r {testpth}/output/rotate_2d/preprocessing/site_closed/. "
        f"{testpth}/output/rotate_2d/simulations/site_closed"
    )
    os.chdir(f"{testpth}/output/rotate_2d/simulations")
    os.system(
        "expreccs -o expreccs -i 'regional/REGIONAL site_closed/SITE_CLOSED' "
        "-f 3 -a 3.2"
    )
    assert os.path.exists(f"{testpth}/output/rotate_2d/simulations/expreccs/BCCON.INC")
    os.chdir(f"{testpth}/output/rotate_2d/simulations/expreccs")
    os.system("flow EXPRECCS.DATA --enable-tuning=true")
    assert os.path.exists(
        f"{testpth}/output/rotate_2d/simulations/expreccs/EXPRECCS.UNRST"
    )
