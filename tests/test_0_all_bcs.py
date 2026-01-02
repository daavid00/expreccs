# SPDX-FileCopyrightText: 2024-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Test the expreccs framework"""

import os
import pathlib
from expreccs.core.expreccs import main

testpth: pathlib.Path = pathlib.Path(__file__).parent


def test_all_bcs():
    """See configs/*.toml"""
    if not os.path.exists(f"{testpth}/output"):
        os.mkdir(f"{testpth}/output")
    if not os.path.exists(f"{testpth}/output/bcs"):
        os.mkdir(f"{testpth}/output/bcs")
    os.chdir(f"{testpth}/output/bcs")
    os.system(f"cp {testpth}/configs/input.toml .")
    main()
    os.chdir(f"{testpth}/output/bcs")
    for name in ["wells", "interp"]:
        os.system(f"expreccs -i {testpth}/configs/{name}.toml -m site")
    os.system(f"expreccs -i {testpth}/configs/flux.toml -m site -p all")
    for name in ["wells_pressure", "pres_pressure", "flux_pressure"]:
        assert os.path.exists(
            f"{testpth}/output/bcs/output/postprocessing/output_difference_site_{name}.png"
        )
    os.system("expreccs -c compare")
    assert os.path.exists(
        f"{testpth}/output/bcs/compare/compareoutput_distance_from_border.png"
    )
