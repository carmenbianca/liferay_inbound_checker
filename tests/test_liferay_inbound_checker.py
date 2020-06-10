# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for `liferay_inbound_checker` package."""

import pytest
from click.testing import CliRunner

from liferay_inbound_checker import cli, liferay_inbound_checker


def test_command_line_interface():
    """Test the CLI."""
