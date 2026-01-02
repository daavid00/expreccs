# SPDX-FileCopyrightText: 2025-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Test the expreccs functionality in a site deck with nonregular boundaries"""

import os
import pathlib
import subprocess

testpth: pathlib.Path = pathlib.Path(__file__).parent


def test_site_regional():
    """See regional/ and site/"""
    message = "Please run first test_4_site_regional"
    assert os.path.exists(f"{testpth}/output/expreccs_perfipnum"), message
    flow = "flow"
    base = "expreccs -i 'regional/REGIONAL site/SITE' -n 1 -o expreccs"
    for i, (name, flag, nlines) in enumerate(
        zip(["_zones", "_frequency"], [" -z 1", " -f 2"], [29, 53])
    ):
        os.chdir(f"{testpth}/output")
        os.system(f"{base}{name}{flag}")
        os.chdir(f"{testpth}/output/expreccs{name}")
        subprocess.run([flow, f"EXPRECCS{name.upper()}.DATA"], check=True)
        assert os.path.exists(
            f"{testpth}/output/expreccs{name}/EXPRECCS{name.upper()}.UNRST"
        )
        with open(
            f"{testpth}/output/expreccs{name}/bc/BCPROP{6*(i+1)}.INC",
            "r",
            encoding="utf8",
        ) as file:
            assert len(file.readlines()) == nlines
