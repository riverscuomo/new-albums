import inspect
import os
import logging
from typing import Optional
from pathlib import Path

# There's nothing special about `config` here. I simply needed a module from `new_albums`
# to use with `inspect` to get a full path.
import config


def accept_reject_path() -> Optional[Path]:
    logging.info(
        "[accept_reject]: Attempting to find accept.txt and/or reject.txt if they exist."
    )
    return config_home_check() or module_path_check()


def config_home_check() -> Optional[Path]:
    logging.info("[accept_reject]: Checking XDG_CONFIG_HOME or APPDATA for configs.")

    config_home: Optional[str] = os.environ.get("XDG_CONFIG_HOME") or os.environ.get(
        "APPDATA"
    )
    if config_home:
        logging.debug(f"[accept_reject]: Config directory => {config_home}")
        new_albums_conf: Path = Path(config_home).joinpath("new_albums")

        if new_albums_conf.exists() and check_accept_reject_exists(new_albums_conf):
            return new_albums_conf

    return None


def module_path_check() -> Optional[Path]:
    logging.info(
        "[accept_reject]: Checking the `new_albums` module path for accept.txt and/or reject.txt if they exist."
    )

    module_path: Path = Path(inspect.getfile(config)).parent
    logging.info(f"[accept_reject]: Module path => {module_path}")

    if check_accept_reject_exists(module_path):
        logging.info(f"[accept_reject]: Module path contains accept.txt or reject.txt")
        return module_path

    return None


def check_accept_reject_exists(path: Path) -> bool:
    """Check if a directory contains 'accept.txt' and/or 'reject.txt'.

    Parameters
    ----------
    path : pathlib.Path

    Returns
    -------
    bool
    """

    # The user may provide neither, one, or both files.
    # TODO: Use filter to return the paths instead of repeating work.
    return any(
        (
            entry.is_file() and entry.name in ["accept.txt", "reject.txt"]
            for entry in path.glob("*.txt")
        )
    )
