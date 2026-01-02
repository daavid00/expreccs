# SPDX-FileCopyrightText: 2024-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Test the expreccs functionality to rotate grids and to handle generic decks"""

import os
import pathlib

testpth: pathlib.Path = pathlib.Path(__file__).parent


def test_generic_deck():
    """See configs/rotate.toml"""
    if not os.path.exists(f"{testpth}/output"):
        os.system(f"mkdir {testpth}/output")
    os.chdir(f"{testpth}/output")
    os.system(
        f"expreccs -i {testpth}/configs/rotate.toml -o rotate -m all -t 30 -p site"
    )
    assert os.path.exists(
        f"{testpth}/output/rotate/postprocessing/rotate_site_closed_pressure.png"
    )
    os.system(
        f"scp -r {testpth}/output/rotate/preprocessing/regional/. "
        f"{testpth}/output/rotate/simulations/regional"
    )
    os.system(
        f"scp -r {testpth}/output/rotate/preprocessing/site_closed/. "
        f"{testpth}/output/rotate/simulations/site_closed"
    )
    os.chdir(f"{testpth}/output/rotate/simulations")
    os.system("expreccs -o expreccs -i 'regional/REGIONAL site_closed/SITE_CLOSED'")
    assert os.path.exists(f"{testpth}/output/rotate/simulations/expreccs/BCCON.INC")
    os.chdir(f"{testpth}/output/rotate/simulations/expreccs")
    os.system("flow EXPRECCS.DATA --enable-tuning=true")
    assert os.path.exists(
        f"{testpth}/output/rotate/simulations/expreccs/EXPRECCS.UNRST"
    )
