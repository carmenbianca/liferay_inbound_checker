# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Console script for liferay_inbound_checker."""
import sys

import click
from requests import RequestException

from liferay_inbound_checker.check import check_all
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
@click.argument("portal_path")
def main(portal_path):
    """Console script for liferay_inbound_checker."""
    success = True

    click.echo("Generating list of dependencies.")
    pom_xml = generate_pom(portal_path)
    root = convert_to_tree(pom_xml)
    dependencies = dependencies_from_tree(root)
    click.echo("Success!")

    success = True
    for result in check_all(dependencies):
        if not result.success:
            success = False
            click.echo()
            click.echo(
                f"{result.dependency.groupid}/{result.dependency.artifactid}@{result.dependency.version}"
            )
            for reason in result.reasons:
                click.echo(reason)
        else:
            click.echo()
            click.echo(
                f"{result.dependency.groupid}/{result.dependency.artifactid}@{result.dependency.version}"
            )
            click.echo("Good")

    return success


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
