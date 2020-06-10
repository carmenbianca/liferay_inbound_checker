# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Interactions with dependencies."""

import subprocess
from copy import copy
from os import PathLike
from pathlib import Path
from typing import List, NamedTuple
from xml.etree.ElementTree import Element, fromstring

from . import cwd


class Dependency(NamedTuple):
    """Struct for dependencies."""

    groupid: str
    artifactid: str
    version: str


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


def _remove_namespace_from_xml(root: Element) -> Element:
    """ElementTree very annoyingly puts the XML namespace in tall tags like
    '{namespace}tag'. This function removes that.
    """
    root = copy(root)

    for element in root.iter():
        _, has_namespace, postfix = element.tag.partition("}")
        if has_namespace:
            element.tag = postfix

    return root


def convert_to_tree(xml: str) -> Element:
    """Convert an XML string to an XML tree object."""
    root = fromstring(xml)
    return _remove_namespace_from_xml(root)


def dependencies_from_tree(root: Element) -> List[Dependency]:
    """Turn an XML tree into a flat list of dependencies.

    :raises AttributeError: if the tree does not contain dependencies.
    """
    dependencies = root.find("dependencyManagement").find("dependencies")
    result = []
    for dependency in dependencies:
        result.append(
            Dependency(
                dependency.find("groupId").text,
                dependency.find("artifactId").text,
                dependency.find("version").text,
            )
        )
    return result
