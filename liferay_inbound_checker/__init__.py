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
