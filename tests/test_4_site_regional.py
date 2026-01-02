# SPDX-FileCopyrightText: 2025-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Test the expreccs functionality in a site and regional deck"""

import os
import pathlib

testpth: pathlib.Path = pathlib.Path(__file__).parent


def test_site_regional():
    """See regional/ and site/"""
    if not os.path.exists(f"{testpth}/output"):
        os.system(f"mkdir {testpth}/output")
    os.chdir(f"{testpth}/output")
    os.system(f"cp -R {testpth}/site .")
    os.system(f"cp -R {testpth}/regional .")
    flow = "flow --relaxed-max-pv-fraction=0 "
    for name in ["site", "regional"]:
        os.chdir(f"{testpth}/output/{name}")
        os.system(f"{flow} {name.upper()}.DATA")
    base = "expreccs -i 'regional/REGIONAL site/SITE' -o expreccs"
    for name, flag, nlines in zip(
        ["", "_dpincrease", "_perfipnum"], ["", " -e 0", " -z 1"], [65, 65, 35]
    ):
        os.chdir(f"{testpth}/output")
        os.system(f"{base}{name}{flag}")
        os.chdir(f"{testpth}/output/expreccs{name}")
        os.system(f"{flow} EXPRECCS{name.upper()}.DATA")
        assert os.path.exists(
            f"{testpth}/output/expreccs{name}/EXPRECCS{name.upper()}.UNRST"
        )
        with open(
            f"{testpth}/output/expreccs{name}/bc/BCPROP6.INC", "r", encoding="utf8"
        ) as file:
            assert len(file.readlines()) == nlines
