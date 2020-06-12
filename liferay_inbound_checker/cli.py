# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-FileAttributionText: Stefan Bakker <s.bakker777@gmail.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Console script for liferay_inbound_checker."""
import subprocess
import sys
from inspect import cleandoc
from multiprocessing.pool import ThreadPool

import click
from requests import RequestException

from liferay_inbound_checker import cwd
from liferay_inbound_checker.check import check, is_whitelisted, load_whitelist
from liferay_inbound_checker.clearlydefined import (
    ClearlyDefinedDefinitions,
    definitions_from_clearlydefined,
)
from liferay_inbound_checker.dependencies import (
    convert_to_tree,
    dependencies_from_tree,
    generate_pom,
    get_current_revision,
)


def generate_dependencies(portal_path):
    click.echo("Generating list of dependencies.")
    pom_xml = generate_pom(portal_path)
    root = convert_to_tree(pom_xml)
    dependencies = dependencies_from_tree(root)
    click.echo("Success!")
    return dependencies


def load_whitelist_cli(portal_path):
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


def check_dependencies(dependencies, whitelist):
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
        click.echo()
        click.echo(result.dependency)
        if not result.success:
            success = False
            for reason in result.reasons:
                click.echo(reason)
        else:
            click.echo("TODO advice for good results goes here.")

    failures = sum(1 for result in calculated_results if not result.success)
    successes = len(calculated_results) - failures

    click.echo()
    click.echo(f"Successful dependencies: {successes}")
    click.echo(f"Failed dependencies: {failures}")

    if not success:
        click.echo()
        click.echo(
            "Did not succeed. Please review the above advice. If necessary, open an Inbound Licensing ticket in the FOSS project at <https://issues.liferay.com/projects/FOSS/issues/>. For more information see: <https://grow.liferay.com/excellence/Liferay+Inbound+Licensing+Policy#what-happens-when-i-open-an-inbound-licensing-ticket>."
        )
    else:
        click.echo()
        click.echo("No failures. Success!")

    return success


@click.group()
def main():
    pass


@main.command()
@click.argument("portal_path")
def all_dependencies(portal_path):
    dependencies = generate_dependencies(portal_path)

    whitelist = load_whitelist_cli(portal_path)

    return check_dependencies(dependencies, whitelist)


@main.command()
@click.argument("portal_path")
def delta_dependencies(portal_path):
    new_dependencies = set(generate_dependencies(portal_path))

    # TODO: get old_dependencies
    current_revision = get_current_revision(portal_path)
    with cwd(portal_path):
        subprocess.run(["git", "checkout", "master"])
    old_dependencies = set(generate_dependencies(portal_path))
    with cwd(portal_path):
        subprocess.run(["git", "checkout", current_revision])

    dependencies = new_dependencies - old_dependencies

    whitelist = load_whitelist_cli(portal_path)

    return check_dependencies(dependencies, whitelist)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
