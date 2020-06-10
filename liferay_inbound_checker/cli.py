# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Console script for liferay_inbound_checker."""
import sys
from pathlib import Path

import click
from requests import RequestException

from liferay_inbound_checker.clearlydefined import (
    ClearlyDefinedDefinitions,
    definitions_from_clearlydefined,
)
from liferay_inbound_checker.dependencies import (
    convert_to_tree,
    dependencies_from_tree,
    generate_pom,
)


@click.command()
def main(args=None):
    """Console script for liferay_inbound_checker."""
    pom_xml = generate_pom(Path.home() / "Projektoj/liferay-portal")
    root = convert_to_tree(pom_xml)
    dependencies = dependencies_from_tree(root)
    for dependency in dependencies:
        try:
            definitions = ClearlyDefinedDefinitions(
                definitions_from_clearlydefined(dependency)
            )
        except RequestException:
            print(f"error for {dependency}")
            continue

        if definitions.score >= 50:
            print(f"{dependency} good")
        else:
            print(f"{dependency} bad")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
