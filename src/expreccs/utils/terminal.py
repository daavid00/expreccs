# SPDX-FileCopyrightText: 2026 NORCE Research AS
# SPDX-License-Identifier: GPL-3.0

"""Format command-line messages for expreccs.

The module applies ANSI colors when supported by the selected output stream and
provides consistent formatting for values, errors, warnings, tips, progress
messages, and generated-file reports.
"""

import os
import sys
from typing import NoReturn

ANSI_BOLD_RED = "1;31"
ANSI_BOLD_YELLOW = "1;33"
ANSI_BOLD_GREEN = "1;32"
ANSI_BOLD_BLUE = "1;34"
ANSI_BOLD_MAGENTA = "1;35"
ANSI_YELLOW = "1;33"
ANSI_GREEN = "1;32"
ANSI_CYAN = "36"
ANSI_RED = "31"
ANSI_BLUE = "1;34"


def _supports_color(stream: object = sys.stderr) -> bool:
    """Check whether an output stream supports ANSI colors.

    Parameters
    ----------
    stream : object, optional
        Output stream used for color detection.

    Returns
    -------
    bool
        Whether the stream supports ANSI color output.
    """
    return (
        hasattr(stream, "isatty")
        and stream.isatty()
        and os.environ.get("NO_COLOR") is None
        and os.environ.get("TERM") != "dumb"
    )


def _colorize(
    text: str,
    code: str,
    stream: object = sys.stderr,
) -> str:
    """Wrap text in an ANSI color sequence when supported.

    Parameters
    ----------
    text : str
        Text to format.
    code : str
        ANSI color code.
    stream : object, optional
        Output stream used for color detection.

    Returns
    -------
    str
        Original or ANSI-colored text.
    """
    if not _supports_color(stream):
        return text
    return f"\033[{code}m{text}\033[0m"


def cli_warning_value(value: str) -> str:
    """Format a warning-related CLI option or value.

    Parameters
    ----------
    value : str
        Value to inspect.

    Returns
    -------
    str
        Formatted value.
    """
    return _colorize(repr(value), ANSI_YELLOW)


def cli_correct_value(value: str) -> str:
    """Format a valid CLI option or value.

    Parameters
    ----------
    value : str
        Value to inspect.

    Returns
    -------
    str
        Formatted value.
    """
    return _colorize(repr(value), ANSI_GREEN)


def cli_error_value(value: str) -> str:
    """Format an invalid CLI option or value.

    Parameters
    ----------
    value : str
        Value to inspect.

    Returns
    -------
    str
        Formatted value.
    """
    return _colorize(repr(value), ANSI_RED)


def cli_info_value(value: str) -> str:
    """Format an informational CLI option or value.

    Parameters
    ----------
    value : str
        Value to inspect.

    Returns
    -------
    str
        Formatted value.
    """
    return _colorize(repr(value), ANSI_BLUE)


def expreccs_error(message: str) -> NoReturn:
    """Raise a fatal command-line error.

    Parameters
    ----------
    message : str
        Message to append or display.

    Raises
    ------
    SystemExit
        Always raised with the formatted message.
    """
    label = _colorize("error", ANSI_BOLD_RED)
    raise SystemExit(f"{expreccs_name()}: {label}: {message}")


def expreccs_warning(message: str) -> None:
    """Display a non-fatal command-line warning.

    Parameters
    ----------
    message : str
        Message to append or display.
    """
    label = _colorize("warning", ANSI_BOLD_YELLOW)
    print(f"{expreccs_name()}: {label}: {message}", file=sys.stderr)


def expreccs_info(message: str) -> None:
    """Display an informational command-line message.

    Parameters
    ----------
    message : str
        Message to append or display.
    """
    label = _colorize("info", ANSI_BOLD_BLUE, sys.stdout)
    print(f"{expreccs_name()}: {label}: {message}")


def expreccs_tip(message: str) -> None:
    """Display a command-line suggestion.

    Parameters
    ----------
    message : str
        Message to append or display.
    """
    label = _colorize("tip", ANSI_BOLD_MAGENTA, sys.stdout)
    print(f"{expreccs_name(sys.stdout)}: {label}: {message}")


def expreccs_success(msg: str, output_dir: str, filenames: list[str]) -> None:
    """Display generated output locations and filenames.

    Parameters
    ----------
    msg : str
        Text written before the output path.
    output_dir : str
        Output directory.
    filenames : list[str]
        Generated filenames.
    """
    label = _colorize("success", ANSI_BOLD_GREEN, sys.stdout)
    if not filenames:
        print(f"{expreccs_name()}: {label}: {msg}{output_dir}")
    elif len(filenames) == 1:
        print(f"{expreccs_name()}: {label}: {msg}{output_dir}/{filenames[0]}")
    elif len(filenames) <= 5:
        print(f"{expreccs_name()}: {label}{msg}")
        print(f"            Output directory: {output_dir}")
        print(f"            Files ({len(filenames)}): {', '.join(filenames)}")
    else:
        print(f"{expreccs_name()}: {label}{msg}")
        print(f"            Output directory: {output_dir}")
        print(f"            Files ({len(filenames)}):")
        for filename in filenames:
            print(f"              - {filename}")


def expreccs_name(stream: object = sys.stderr) -> str:
    """Format the expreccs program name.

    Parameters
    ----------
    stream : object, optional
        Output stream used for color detection.

    Returns
    -------
    str
        Formatted program name.
    """
    characters = [("expreccs", "1")]
    return "".join(
        _colorize(character, color, stream) for character, color in characters
    )
