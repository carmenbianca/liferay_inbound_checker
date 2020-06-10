# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for generating dependencies."""

import os
import subprocess
from pathlib import Path
from unittest.mock import create_autospec

from liferay_inbound_checker import cwd
from liferay_inbound_checker.dependencies import convert_to_tree, generate_pom


def test_generate_pom(mocker):
    mocker.patch("subprocess.run", spec=True)
    mocker.patch("os.chdir", spec=True)
    mocker.patch("pathlib.Path.read_text", return_value="Hello, world!")

    result = generate_pom(Path.home())
    os.chdir.assert_any_call(f"{Path.home()}/modules")
    os.chdir.assert_called_with(f"{Path.cwd()}")
    subprocess.run.assert_called_with(
        ["../gradlew", "-b", "releng.gradle", "generatePomThirdParty"]
    )
    Path.read_text.assert_called()
    assert result == "Hello, world!"


def test_convert_to_tree(sample_pom):
    root = convert_to_tree(sample_pom)
    assert root.tag == "project"
    dependencies = root.find("dependencyManagement").find("dependencies")
    assert len(dependencies) == 2
