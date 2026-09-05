# SPDX-FileCopyrightText: 2023-2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0
# pylint: disable=R0912,R0913,R0914,R0915

"""Load, validate, and normalize TOML configuration for expreccs.

The module combines validated simulation input with command-line and runtime
settings, derives grid and saturation-table dimensions, and preprocesses OPM
Flow TUNING records. Validation reports unknown values, missing variables, and
incompatible shapes through the shared terminal-formatting helpers.
"""

import math
import subprocess
import tomllib
from typing import Any

import numpy as np

from expreccs.utils.terminal import (
    cli_correct_value,
    cli_error_value,
    cli_warning_value,
    expreccs_error,
    expreccs_warning,
)

_REQUIRED = {
    "flow",
    "regional_dims",
    "regional_x_n",
    "regional_y_n",
    "regional_z_n",
    "reference_x_n",
    "reference_y_n",
    "reference_z_n",
    "site_location",
    "fault_regional",
    "fault_site",
    "thickness",
    "pressure",
    "temperature",
    "sensor_coords",
    "regional_bctype",
    "site_bctype",
    "krw",
    "krn",
    "pcap",
    "safu",
    "rock",
    "well_coords",
    "inj",
}
_OPTIONAL = {"hysteresis", "salinity", "rock_comp", "iterations", "z_xy"}
_CONFIGURABLE = _REQUIRED | _OPTIONAL


def process_input(dic: dict[str, Any], in_file: str) -> None:
    """Load TOML input and add validated values to the runtime configuration.

    Parameters
    ----------
    dic : dict[str, Any]
        Shared mutable expreccs configuration and runtime data.
    in_file : str
        Path to the TOML configuration file.
    """
    defaults = {
        "hysteresis": False,
        "salinity": 0.0,
        "rock_comp": 0.0,
        "iterations": 0,
        "z_xy": 0.0,
    }
    with open(in_file, "rb") as file:
        cfg_file = tomllib.load(file)

    # Validate only the TOML dictionary. ``dic`` also contains command-line and
    # runtime values such as fol and subfolders, which must never be removed.
    cfg_file = {**defaults, **cfg_file}
    dic.update(check_entries(cfg_file))

    dic["satnum"] = len(dic["thickness"])
    dic["reference_dims"] = dic["regional_dims"]
    for res in ["regional", "reference"]:
        dic[f"{res}_num_cells"] = [
            np.sum(dic[f"{res}_x_n"]),
            np.sum(dic[f"{res}_y_n"]),
            np.sum(dic[f"{res}_z_n"]),
        ]
    dic["ntabs"] = dic["satnum"]
    if dic["hysteresis"]:
        dic["ntabs"] *= 2
    process_tuning(dic)


def process_tuning(dic: dict[str, Any]) -> None:
    """Detect and normalize OPM TUNING schedule records.

    Parameters
    ----------
    dic : dict[str, Any]
        Shared mutable expreccs configuration and runtime data.
    """
    dic["tuning"] = False
    for value in dic["flow"].split():
        if "--enable-tuning" in value and value[16:] in ["true", "True", "1"]:
            dic["tuning"] = True
            break
    if len(dic["inj"][0][0]) == 4:
        expreccs_error(
            "after the 2025.04 release, column 4 in the first entry for the maximum "
            "solver time step in the injection has been moved as a new entry, including "
            "the items for the TUNING keyword, which gives more control when setting "
            "the simulations. Please see the configuration files in the examples and "
            "online documentation (Configuration file->Well-related parameters), and "
            "update your configuration file accordingly."
        )
    size = 3 if dic["site_bctype"][0] == "wells" else 2
    for i, inj in enumerate(dic["inj"]):
        if len(inj) > size:
            tmp = inj[-1].split("/")
            dic["inj"][i][-1] = tmp[0].strip()
            if len(tmp) > 1:
                for val in tmp[1:]:
                    dic["inj"][i].append(val.strip())


def _finite_number(value: Any) -> bool:
    """Check whether a value is a finite, non-Boolean number.

    Parameters
    ----------
    value : Any
        Value to inspect.

    Returns
    -------
    bool
        Whether the value is a finite non-Boolean number.
    """
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def _add_error(errors: list[str], message: str) -> None:
    """Append one configuration-validation error.

    Parameters
    ----------
    errors : list[str]
        Accumulated validation messages.
    message : str
        Message to append or display.
    """
    errors.append(message)


def _validate_numeric_array(
    cfg_file: dict[str, Any],
    key: str,
    errors: list[str],
    *,
    length: int | None = None,
    positive: bool = False,
    integer: bool = False,
) -> bool:
    """Validate a one-dimensional numeric configuration array.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML configuration values.
    key : str
        Configuration variable name.
    errors : list[str]
        Accumulated validation messages.

    Returns
    -------
    bool
        Whether the array is valid.
    """
    if key not in cfg_file:
        return False
    value = cfg_file[key]
    valid = isinstance(value, list) and bool(value)
    if valid and length is not None:
        valid = len(value) == length
    if valid:
        valid = all(
            _finite_number(item)
            and (not integer or isinstance(item, int))
            and (not positive or item > 0)
            for item in value
        )
    if not valid:
        expected = (
            f"an array of {length} finite numbers"
            if length is not None
            else "a non-empty numeric array"
        )
        if positive and integer:
            expected = "a non-empty array of positive integers"
        _add_error(
            errors,
            f"variable {cli_error_value(key)} has invalid value "
            f"{cli_error_value(str(value))}, expected {cli_correct_value(expected)}.",
        )
    return valid


def _validate_numeric_matrix(
    cfg_file: dict[str, Any], key: str, errors: list[str], columns: int
) -> bool:
    """Validate a numeric configuration matrix.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML configuration values.
    key : str
        Configuration variable name.
    errors : list[str]
        Accumulated validation messages.
    columns : int
        Required number of matrix columns.

    Returns
    -------
    bool
        Whether the matrix is valid.
    """
    if key not in cfg_file:
        return False
    value = cfg_file[key]
    valid = (
        isinstance(value, list)
        and bool(value)
        and all(
            isinstance(row, list)
            and len(row) == columns
            and all(_finite_number(item) for item in row)
            for row in value
        )
    )
    if not valid:
        _add_error(
            errors,
            f"variable {cli_error_value(key)} has invalid value "
            f"{cli_error_value(str(value))}, expected "
            f"{cli_correct_value(f'a non-empty numeric matrix with {columns} columns')}.",
        )
    return valid


def check_entries(cfg_file: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize TOML configuration entries.

    Parameters
    ----------
    cfg_file : dict[str, Any]
        TOML configuration values.

    Returns
    -------
    dict[str, Any]
        Validated TOML configuration.

    Raises
    ------
    SystemExit
        If an input value is invalid or required input cannot be used.
    """
    if not isinstance(cfg_file, dict):
        expreccs_error(
            f"invalid TOML content {cli_error_value(type(cfg_file).__name__)}, expected "
            f"{cli_correct_value('a dictionary of configuration variables')}."
        )

    cfg_file = cfg_file.copy()
    unknown = sorted(cfg_file.keys() - _CONFIGURABLE)
    if unknown:
        formatted = ", ".join(cli_warning_value(key) for key in unknown)
        plural = len(unknown) != 1
        expreccs_warning(
            f"unknown TOML variable{'s' if plural else ''} {formatted} "
            "will be ignored."
        )
        for key in unknown:
            cfg_file.pop(key)

    errors: list[str] = []
    for key in sorted(_REQUIRED - cfg_file.keys()):
        _add_error(errors, f"missing required TOML variable {cli_error_value(key)}.")

    flow = cfg_file.get("flow")
    if flow is not None:
        if not isinstance(flow, str) or not flow.strip():
            _add_error(
                errors,
                f"variable {cli_error_value('flow')} has invalid value "
                f"{cli_error_value(str(flow))}, expected "
                f"{cli_correct_value('a non-empty string')}.",
            )
        elif (
            subprocess.call(
                flow,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
            != 1
        ):
            _add_error(
                errors,
                f"the executable {cli_error_value(f'flow = {flow}')} is not found, "
                "see the information about installation in the documentation.",
            )

    _validate_numeric_array(cfg_file, "regional_dims", errors, length=3)
    for res in ("regional", "reference"):
        for axis in ("x", "y", "z"):
            _validate_numeric_array(
                cfg_file,
                f"{res}_{axis}_n",
                errors,
                positive=True,
                integer=True,
            )
    _validate_numeric_array(cfg_file, "site_location", errors, length=6)
    _validate_numeric_array(cfg_file, "fault_regional", errors, length=5)
    _validate_numeric_matrix(cfg_file, "fault_site", errors, 2)
    _validate_numeric_array(cfg_file, "thickness", errors, positive=True)
    _validate_numeric_array(cfg_file, "temperature", errors, length=2)
    _validate_numeric_array(cfg_file, "sensor_coords", errors, length=3)
    _validate_numeric_matrix(cfg_file, "rock", errors, 3)
    _validate_numeric_matrix(cfg_file, "well_coords", errors, 4)

    pressure = cfg_file.get("pressure")
    if pressure is not None and (not _finite_number(pressure) or pressure <= 0):
        _add_error(
            errors,
            f"variable {cli_error_value('pressure')} has invalid value "
            f"{cli_error_value(str(pressure))}, expected "
            f"{cli_correct_value('a positive finite number')}.",
        )

    for key in ("krw", "krn", "pcap"):
        value = cfg_file.get(key)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            _add_error(
                errors,
                f"variable {cli_error_value(key)} has invalid value "
                f"{cli_error_value(str(value))}, expected "
                f"{cli_correct_value('a non-empty expression string')}.",
            )

    boundary_types = {
        "regional_bctype": {"open", "closed", "porv"},
        "site_bctype": {
            "open",
            "closed",
            "porv",
            "porvproj",
            "flux",
            "pres",
            "pres2p",
            "wells",
        },
    }
    for key, allowed in boundary_types.items():
        value = cfg_file.get(key)
        if value is None:
            continue
        valid = (
            isinstance(value, list)
            and bool(value)
            and isinstance(value[0], str)
            and value[0] in allowed
            and all(
                _finite_number(item) or (isinstance(item, str) and bool(item.strip()))
                for item in value[1:]
            )
        )
        if not valid:
            _add_error(
                errors,
                f"variable {cli_error_value(key)} has invalid value "
                f"{cli_error_value(str(value))}, expected a supported boundary type "
                f"followed by {cli_correct_value('string or finite numeric parameters')}.",
            )

    hysteresis = cfg_file.get("hysteresis", False)
    hysteresis_valid = isinstance(hysteresis, bool) or (
        isinstance(hysteresis, list)
        and bool(hysteresis)
        and all(isinstance(item, str) and bool(item.strip()) for item in hysteresis)
    )
    if not hysteresis_valid:
        _add_error(
            errors,
            f"variable {cli_error_value('hysteresis')} has invalid value "
            f"{cli_error_value(str(hysteresis))}, expected "
            f"{cli_correct_value('a Boolean or a non-empty array of strings')}.",
        )

    for key in ("salinity", "rock_comp"):
        value = cfg_file.get(key)
        if value is not None and (not _finite_number(value) or value < 0):
            _add_error(
                errors,
                f"variable {cli_error_value(key)} has invalid value "
                f"{cli_error_value(str(value))}, expected "
                f"{cli_correct_value('a non-negative finite number')}.",
            )

    iterations = cfg_file.get("iterations")
    if iterations is not None and (
        not isinstance(iterations, int)
        or isinstance(iterations, bool)
        or iterations < 0
    ):
        _add_error(
            errors,
            f"variable {cli_error_value('iterations')} has invalid value "
            f"{cli_error_value(str(iterations))}, expected "
            f"{cli_correct_value('a non-negative integer')}.",
        )

    z_xy = cfg_file.get("z_xy")
    if z_xy is not None and not (
        _finite_number(z_xy) or (isinstance(z_xy, str) and bool(z_xy.strip()))
    ):
        _add_error(
            errors,
            f"variable {cli_error_value('z_xy')} has invalid value "
            f"{cli_error_value(str(z_xy))}, expected "
            f"{cli_correct_value('a finite number or a non-empty expression string')}.",
        )

    thickness = cfg_file.get("thickness")
    if isinstance(thickness, list):
        layers = len(thickness)
        rock = cfg_file.get("rock")
        if isinstance(rock, list) and len(rock) != layers:
            _add_error(
                errors,
                f"variable {cli_error_value('rock')} has "
                f"{cli_error_value(str(len(rock)))} entries, expected "
                f"{cli_correct_value(f'{layers} entries, one per layer')}.",
            )

        safu = cfg_file.get("safu")
        if isinstance(safu, list):
            hysteresis_enabled = hysteresis is True or (
                isinstance(hysteresis, list) and bool(hysteresis)
            )
            expected = layers * (2 if hysteresis_enabled else 1)
            if len(safu) != expected:
                _add_error(
                    errors,
                    f"variable {cli_error_value('safu')} has "
                    f"{cli_error_value(str(len(safu)))} entries, expected "
                    f"{cli_correct_value(str(expected))}.",
                )
            elif not all(
                isinstance(row, list)
                and len(row) == 10
                and all(_finite_number(item) for item in row)
                for row in safu
            ):
                _add_error(
                    errors,
                    f"variable {cli_error_value('safu')} has invalid value, expected "
                    f"{cli_correct_value('10 finite numbers per saturation-function entry')}.",
                )

    inj = cfg_file.get("inj")
    if inj is not None and not (
        isinstance(inj, list)
        and bool(inj)
        and all(isinstance(entry, list) and len(entry) >= 2 for entry in inj)
    ):
        _add_error(
            errors,
            f"variable {cli_error_value('inj')} has invalid value, expected "
            f"{cli_correct_value('a non-empty schedule with at least two items per entry')}.",
        )

    if errors:
        details = "\n".join(f"  - {error}" for error in errors)
        expreccs_error(f"invalid TOML configuration:\n{details}")
    return cfg_file
