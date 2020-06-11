# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-FileAttributionText: Stefan Bakker <s.bakker777@gmail.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Console script for liferay_inbound_checker."""
import sys
from multiprocessing.pool import ThreadPool

import click
from requests import RequestException

from liferay_inbound_checker.check import check, is_whitelisted, load_whitelist
from liferay_inbound_checker.clearlydefined import (
    ClearlyDefinedDefinitions,
    definitions_from_clearlydefined,
)
from liferay_inbound_checker.dependencies import (
    convert_to_tree,
    dependencies_from_tree,
    generate_pom,
)
from inspect import cleandoc


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

    click.echo("Loading whitelist.")
    try:
        whitelist = load_whitelist(
            f"{portal_path}/inbound_licensing_whitelist.yml"
        )
    except FileNotFoundError:
        whitelist = []
        click.echo("Could not find whitelist.")
    else:
        click.echo("Success!")

    click.echo()
    click.echo("Evaluating dependencies for their licensing.")

    success = True

    pool = ThreadPool(4)
    multiple_results = [
        pool.apply_async(check, (dependency, whitelist))
        for dependency in dependencies
    ]

    calculated_results = []

    for result in multiple_results:
        result = result.get()
        calculated_results.append(result)
        if not result.success:
            success = False
            click.echo()
            click.echo(result.dependency)
            for reason in result.reasons:
                click.echo(reason)

    failures = sum(1 for result in calculated_results if not result.success)
    successes = len(calculated_results) - failures

    click.echo()
    click.echo(f"Successful dependencies: {successes}")
    click.echo(f"Failed dependencies: {failures}")

    if not success:
        click.echo()
        click.echo(
            cleandoc(
                """
                Some of the declared dependencies did not meet the requirements for automated licensing compliance.

                If there were errors in retrieving internet results, investigate the problem or simply try running the test again.

                For other errors, please open an issue at <https://issues.liferay.com/projects/FOSS/issues/>. Please include the name and version of the component.

                The full details of the licensing requirements can be found in the Liferay Inbound Licensing Policy at <https://grow.liferay.com/excellence/Liferay+Inbound+Licensing+Policy>.
                """
            )
        )
    else:
        click.echo()
        click.echo("No failures. Success!")

    return success


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
