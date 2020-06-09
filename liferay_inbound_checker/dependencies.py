# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Interactions with dependencies."""

import subprocess
from os import PathLike
from pathlib import Path
from typing import NamedTuple

from . import cwd


class Dependency(NamedTuple):
    """Struct for dependencies."""

    groupid: str
    artifactid: str
    version: str

    @property
    def name(self):
        return f"{self.groupid}.{self.artifactid}"


def generate_pom(portal_directory: PathLike) -> str:
    """Generate the POM of dependencies of *portal_directory* and return the POM
    as a string.
    """

    with cwd(f"{portal_directory}/modules"):
        subprocess.run(
            ["../gradlew", "-b", "releng.gradle", "generatePomThirdParty"]
        )
    return (
        Path(portal_directory)
        / "modules/build/release.portal.bom.third.party-unspecified.pom"
    ).read_text()
