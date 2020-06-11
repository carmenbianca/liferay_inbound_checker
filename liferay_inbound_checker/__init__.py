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

# This blacklist is manually copied from the Liferay Inbound Licensing Policy.
LICENSE_BLACKLIST = [
    # # Can't be used in Portal
    # "AGPL-1.0-only",
    # "AGPL-1.0-or-later",
    # "AGPL-1.0",
    # "AGPL-3.0-only",
    # "AGPL-3.0-or-later",
    # "AGPL-3.0",
    # "GPL-1.0-only",
    # "GPL-1.0-or-later",
    # "GPL-1.0",
    # "GPL-2.0-only",
    # "GPL-2.0-or-later",
    # "GPL-2.0",
    # "GPL-3.0-only",
    # "GPL-3.0-or-later",
    # "GPL-3.0",
    # # Requires Legal approval
    # "BSD-3-Clause-Attribution",
    # "BSD-3-Clause-Clear",
    # "BSD-4-Clause",
    # "MIT-advertising",
    # "MPL-1.1",
    # "SSPL-1.0",
    # # Don't even bother
    "BSD-3-Clause-No-Nuclear-License",
    "BSD-3-Clause-No-Nuclear-License-2014",
    "BSD-3-Clause-No-Nuclear-Warranty",
    "JSON",
    "CC-BY-NC-1.0",
    "CC-BY-NC-2.0",
    "CC-BY-NC-2.5",
    "CC-BY-NC-3.0",
    "CC-BY-NC-4.0",
    "CC-BY-NC-ND-1.0",
    "CC-BY-NC-ND-2.0",
    "CC-BY-NC-ND-2.5",
    "CC-BY-NC-ND-3.0",
    "CC-BY-NC-ND-4.0",
    "CC-BY-NC-SA-1.0",
    "CC-BY-NC-SA-2.0",
    "CC-BY-NC-SA-2.5",
    "CC-BY-NC-SA-3.0",
    "CC-BY-NC-SA-4.0",
]
