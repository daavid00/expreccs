# SPDX-FileCopyrightText: 2024-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Test the expreccs functionality for back-coupling"""

import os
import pathlib

testpth: pathlib.Path = pathlib.Path(__file__).parent


def test_back_coupling():
    """See configs/back-coupling.toml"""
    if not os.path.exists(f"{testpth}/output"):
        os.system(f"mkdir {testpth}/output")
    os.system(
        f"expreccs -i {testpth}/configs/back-coupling.toml -o {testpth}/output/back -p yes"
    )
    assert os.path.exists(
        f"{testpth}/output/back/postprocessing/back_difference_site_porvproj_watfluxi+.png"
    )
