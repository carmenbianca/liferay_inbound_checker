# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Top-level package for Liferay Inbound Checker."""

__author__ = """Carmen Bianca Bakker"""
__email__ = "carmen@carmenbianca.eu"
__version__ = "0.1.0"

import os
from contextlib import contextmanager


@contextmanager
def cwd(path):
    old_pwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_pwd)


# This whitelist is manually copied from the Liferay Inbound Licensing Policy.
LICENSE_WHITELIST = [
    "0BSD",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "CC0-1.0",
    "ISC",
    "MIT",
    "Expat",
    "MIT-0",
    "MIT-CMU",
    "MIT-feh",
    "X11",
    # Not on the list, but should be
    "LGPL-2.1-or-later",
    "LGPL-3.0-or-later",
    # Edge case
    # "NOASSERTION",
]
