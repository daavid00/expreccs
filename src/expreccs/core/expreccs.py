# SPDX-FileCopyrightText: 2023-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0
# pylint: disable=R0912,R0914,R0915

"""Command-line entry point and top-level workflow coordination for expreccs.

expreccs creates and runs reference, regional, and site-scale OPM Flow models
for hierarchical CO2 storage studies. It can also project boundary data between
existing regional and site decks, perform iterative back-coupling, and generate
comparison figures.

This module parses and validates command-line arguments, initializes the shared
runtime configuration, dispatches the selected modeling workflow, and reports
generated outputs. Grid mapping, deck writing, simulation execution, result
processing, and plotting are delegated to utility and visualization modules.
"""

import argparse
import math
import os
import re
import shutil

from expreccs.utils.backcoupling import (
    backcoupling,
    init_multipliers,
)
from expreccs.utils.inputvalues import process_input
from expreccs.utils.mapproperties import mapping_properties
from expreccs.utils.reg_sit_given_decks import create_deck
from expreccs.utils.runs import plotting, run_models
from expreccs.utils.terminal import (
    cli_correct_value,
    cli_error_value,
    expreccs_error,
    expreccs_info,
    expreccs_success,
    expreccs_tip,
)
from expreccs.utils.writefile import write_folders, write_properties
from expreccs.visualization.plotting import plot_results


def main(argv: list[str] | None = None) -> None:
    """Run the expreccs command-line workflow.

    Parameters
    ----------
    argv : list[str] | None, optional
        Arguments to parse instead of ``sys.argv[1:]``.
    """
    cwd = os.getcwd()
    cmdargs = parse_args(argv)
    check_cmdargs(cmdargs)
    file = cmdargs.input.split(" ")
    dic = {"fol": os.path.abspath(cmdargs.output)}
    dic["pat"] = os.path.dirname(__file__)[:-5]
    dic["mode"], dic["plot"] = cmdargs.mode, cmdargs.plot
    dic["rotate"] = float(cmdargs.transform)
    dic["explicit"] = int(cmdargs.explicit) == 1
    dic["zones"] = int(cmdargs.zones) == 1
    dic["freq"] = cmdargs.frequency.split(",")
    dic["subfolders"] = int(cmdargs.subfolders) == 1
    dic["nonregular"] = int(cmdargs.nonregular) == 1
    dic["acoeff"] = cmdargs.acoeff.split(",")
    dic["boundaries"] = [int(val) for val in cmdargs.boundaries[1:-1].split(",")]
    dic["compare"] = cmdargs.compare

    if dic["compare"]:
        expreccs_info("processing the comparison, please wait...")
        dic["iterations"] = 0
        plot_results(dic)
        expreccs_success("", f"{os.getcwd()}/compare", [""])
        return

    expreccs_info("executing expreccs, please wait...")

    if len(file) > 1:
        for i, name in enumerate(["reg", "sit"]):
            dic[name] = file[i].split("/")[-1]
            dic[f"f{name}"] = (
                os.path.abspath("/".join(file[i].split("/")[:-1]))
                if "/" in file[i]
                else os.path.abspath(".")
            )
        create_deck(
            dic["fol"],
            dic["explicit"],
            dic["zones"],
            dic["freq"],
            dic["nonregular"],
            dic["acoeff"],
            dic["boundaries"],
            dic["reg"],
            dic["freg"],
            dic["sit"],
            dic["fsit"],
        )
        expreccs_success("generated files written to ", dic["fol"], [""])
        return

    process_input(dic, file[0])

    dic["fpos"] = (
        f"{dic['fol']}/postprocessing/" if dic["subfolders"] else f"{dic['fol']}/"
    )

    for iteration in range(dic["iterations"] + 1):
        fil = f"_{iteration-1}" if iteration > 1 else ""
        for name in ["reference", "regional", f"site_{dic['site_bctype'][0]}"]:
            if dic["subfolders"]:
                dic[f"fpre{name}{fil}"] = f"{dic['fol']}/preprocessing/{name}{fil}/"
                dic[f"fsim{name}{fil}"] = f"{dic['fol']}/simulations/{name}{fil}/"
            else:
                dic[f"fpre{name}{fil}"], dic[f"fsim{name}{fil}"] = (
                    f"{dic['fol']}/",
                    f"{dic['fol']}/",
                )

    write_folders(dic)

    os.chdir(dic["fol"])
    try:
        mapping_properties(dic)
        write_properties(dic)
        init_multipliers(dic)

        run_models(dic)

        if dic["iterations"] > 0 and dic["mode"] != "none":
            if not dic["subfolders"]:
                expreccs_error(
                    "invalid combination, backcoupling requires "
                    f"{cli_correct_value('-s 1')} and cannot be used with "
                    f"{cli_error_value('-s 0')}."
                )
            backcoupling(dic)

        if dic["plot"] != "no":
            latex_available = shutil.which("latex") is not None
            if not latex_available:
                expreccs_tip(
                    "LaTeX is recommended for figures to use the intended fonts and "
                    "formats. Follow the installation instructions in the expreccs "
                    "documentation."
                )
            plotting(dic)

        expreccs_success("generated files written to ", dic["fol"], [""])
    finally:
        os.chdir(cwd)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Create the CLI parser and parse expreccs arguments.

    Parameters
    ----------
    argv : list[str] | None, optional
        Arguments to parse instead of ``sys.argv[1:]``.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Main method to simulate regional and site reservoirs for CO2 storage. "
        "The valid flags for toml configuration files are -i, -o, -m, -c, -p, -u, -r, -t, "
        "-w, -l. The valid flags for paths to the regional and site folders are -i, -o, -b, "
        "-f, -a, -w, -e, -z, -n",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str.strip,
        default="input.toml",
        help="The base name of the configuration file; or paths (space between them and "
        "quotation marks) to the regional and site models",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str.strip,
        default="output",
        help="The base name of the output folder",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str.strip,
        choices=["reference", "site", "regional", "regional_site", "all", "none"],
        default="all",
        help="Parts of expreccs to run",
    )
    parser.add_argument(
        "-c",
        "--compare",
        type=str.strip,
        choices=["", "compare"],
        help="Generate a common plot for the current folders",
    )
    parser.add_argument(
        "-p",
        "--plot",
        type=str.strip,
        choices=["reference", "site", "regional", "all", "no"],
        default="no",
        help="Plots to generate",
    )
    parser.add_argument(
        "-t",
        "--transform",
        type=str.strip,
        default="0",
        help="Grades to rotate the site geological model",
    )
    parser.add_argument(
        "-b",
        "--boundaries",
        type=str.strip,
        default="[0,0,0,0]",
        help="Set the number of entries to skip the bc projections on "
        "the site, where 'j=0,i=nx-1,j=ny-1,i=0', e.g., '[0,2,0,0]' would skip all cells "
        "with i=nx-1 and i=nx-2; this becomes handly for models where all cells in a "
        "given site are inactive along a side. Set an entry to -1 to skip the whole "
        "boundary",
    )
    parser.add_argument(
        "-f",
        "--frequency",
        type=str.strip,
        default="1",
        help="Frequency to evaluate the boundary pressures on the site between "
        "report steps in the site. Write an array, e.g., '2,7,3', to set the "
        "frequency in each site report step",
    )
    parser.add_argument(
        "-a",
        "--acoeff",
        type=str.strip,
        default="3.2",
        help="Exponential 'a' coefficient for the telescopic time-discretization "
        "for the given frequency '-f'. Write an array, e.g., '2.2,0,3.1', to set "
        "the coefficient in each site report step ('3.2' by default, use 0 for an "
        "equidistance partition).",
    )
    parser.add_argument(
        "-e",
        "--explicit",
        type=str.strip,
        choices=["0", "1"],
        default="1",
        help="Set to '0' to write the pressure increase on the site bc from "
        "the regional values ('1': the pressure values on the "
        "boundaries correspond to the explicit values on the regional simulations).",
    )
    parser.add_argument(
        "-z",
        "--zones",
        type=str.strip,
        choices=["0", "1"],
        default="0",
        help="Set to '1' to project the regional pressures per fipnum zones, i.e., "
        "the pressure maps to the site bcs are written for equal fipnum numbers in "
        "the whole xy layer ('0': the projections include the z "
        "location offset between regional and site models).",
    )
    parser.add_argument(
        "-s",
        "--subfolders",
        type=str.strip,
        choices=["0", "1"],
        default="1",
        help="Set to '0' to not create the subfolders preprocessing, output, and "
        "postprocessing, i.e., to write all generated files in the output directory",
    )
    parser.add_argument(
        "-n",
        "--nonregular",
        type=str.strip,
        choices=["0", "1"],
        default="0",
        help="Set to '1' for a site with irregular contour, i.e., not defined in a "
        "rectangle",
    )
    return parser.parse_args(argv)


def check_cmdargs(cmdargs: argparse.Namespace) -> None:
    """Validate command-line values and incompatible operations.

    Parameters
    ----------
    cmdargs : argparse.Namespace
        Parsed command-line arguments.

    Raises
    ------
    SystemExit
        If an input value is invalid or required input cannot be used.
    """
    input_value = cmdargs.input
    if not input_value:
        expreccs_error(
            f"invalid value {cli_error_value('-i')}, the input cannot be empty."
        )

    if not cmdargs.output:
        expreccs_error(
            f"invalid value {cli_error_value('-o')}, the output folder cannot be empty."
        )

    input_paths = input_value.split()
    if len(input_paths) not in [1, 2]:
        expreccs_error(
            f"invalid value {cli_error_value(f'-i {input_value}')}, expected one "
            "configuration file or two model-folder paths separated by a space."
        )

    configuration_input = len(input_paths) == 1
    folder_input = len(input_paths) == 2

    if configuration_input and not input_paths[0].lower().endswith(".toml"):
        expreccs_error(
            f"invalid extension {cli_error_value(f'-i {input_value}')}, the valid "
            f"extension is {cli_correct_value('.toml')}, or provide paths to the "
            "regional and site model folders."
        )

    transform = cmdargs.transform
    try:
        transform_value = float(transform)
    except ValueError:
        transform_value = float("nan")

    if not math.isfinite(transform_value):
        expreccs_error(
            f"invalid value {cli_error_value(f'-t {transform}')}, expected a finite "
            "number of degrees."
        )

    boundaries = cmdargs.boundaries
    boundary_pattern = re.fullmatch(
        r"\[\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*\]",
        boundaries,
    )
    if not boundary_pattern:
        expreccs_error(
            f"invalid value {cli_error_value(f'-b {boundaries}')}, expected four "
            "integers inside brackets, "
            f"{cli_correct_value('e.g., -b [0,2,0,0]')}."
        )

    boundary_values = [int(value.strip()) for value in boundaries[1:-1].split(",")]
    if any(value < -1 for value in boundary_values):
        expreccs_error(
            f"invalid value {cli_error_value(f'-b {boundaries}')}, boundary entries "
            "must be -1 or non-negative integers."
        )

    frequency = cmdargs.frequency
    if not re.fullmatch(
        r"[1-9]\d*(?:\s*,\s*[1-9]\d*)*",
        frequency,
    ):
        expreccs_error(
            f"invalid value {cli_error_value(f'-f {frequency}')}, expected positive "
            "integers separated by commas."
        )

    frequency_values = [int(value.strip()) for value in frequency.split(",")]

    acoeff = cmdargs.acoeff
    try:
        acoeff_values = [float(value.strip()) for value in acoeff.split(",")]
    except ValueError:
        acoeff_values = []

    if not acoeff_values or any(
        value < 0 or not math.isfinite(value) for value in acoeff_values
    ):
        expreccs_error(
            f"invalid value {cli_error_value(f'-a {acoeff}')}, expected non-negative "
            "finite numbers separated by commas."
        )

    if len(acoeff_values) not in [1, len(frequency_values)]:
        expreccs_error(
            f"invalid value {cli_error_value(f'-a {acoeff}')}, expected one "
            "coefficient or one coefficient for each value provided with "
            f"{cli_correct_value('-f')}."
        )

    compare = cmdargs.compare
    if compare:
        compare_options = {
            "-i": ("input", "input.toml"),
            "-m": ("mode", "all"),
            "-p": ("plot", "no"),
            "-t": ("transform", "0"),
            "-b": ("boundaries", "[0,0,0,0]"),
            "-f": ("frequency", "1"),
            "-a": ("acoeff", "3.2"),
            "-e": ("explicit", "1"),
            "-z": ("zones", "0"),
            "-n": ("nonregular", "0"),
        }
        invalid_options = [
            option
            for option, (name, default) in compare_options.items()
            if getattr(cmdargs, name) != default
        ]
        if invalid_options:
            expreccs_error(
                f"invalid combination, {cli_error_value('-c compare')} runs the "
                "standalone comparison workflow and cannot be combined with "
                f"{cli_error_value(', '.join(invalid_options))}."
            )

        if cmdargs.subfolders != "1":
            expreccs_error(
                f"invalid combination, {cli_error_value('-c compare')} requires the "
                "subfolder structure and cannot be used with "
                f"{cli_error_value('-s 0')}."
            )

        return

    if folder_input:
        configuration_options = {
            "-m": ("mode", "all"),
            "-p": ("plot", "no"),
            "-t": ("transform", "0"),
            "-s": ("subfolders", "1"),
        }
        invalid_options = [
            option
            for option, (name, default) in configuration_options.items()
            if getattr(cmdargs, name) != default
        ]
        if invalid_options:
            expreccs_error(
                "invalid option when providing regional and site model folders; this "
                "workflow cannot be combined with "
                f"{cli_error_value(', '.join(invalid_options))}."
            )

    if configuration_input:
        folder_options = {
            "-b": ("boundaries", "[0,0,0,0]"),
            "-f": ("frequency", "1"),
            "-a": ("acoeff", "3.2"),
            "-e": ("explicit", "1"),
            "-z": ("zones", "0"),
            "-n": ("nonregular", "0"),
        }
        invalid_options = [
            option
            for option, (name, default) in folder_options.items()
            if getattr(cmdargs, name) != default
        ]
        if invalid_options:
            expreccs_error(
                "invalid option for a TOML configuration file; options "
                f"{cli_error_value(', '.join(invalid_options))} can only be used when "
                "providing regional and site model folders."
            )

    if cmdargs.plot != "no" and cmdargs.subfolders != "1":
        expreccs_error(
            "invalid combination, plot generation requires the subfolder structure "
            "and cannot be used with "
            f"{cli_error_value('-s 0')}."
        )
