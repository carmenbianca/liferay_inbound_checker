# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Console script for liferay_inbound_checker."""
import sys
from pathlib import Path

import click
from requests import RequestException

from liferay_inbound_checker.check import LicenseWhitelistedCheck, ScoreCheck
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
    success = True

    pom_xml = generate_pom(Path.home() / "Projektoj/liferay-portal")
    root = convert_to_tree(pom_xml)
    dependencies = dependencies_from_tree(root)

    for dependency in dependencies:
        dependency_success = True
        click.echo()
        click.echo(
            f"{dependency.groupid}/{dependency.artifactid}@{dependency.version}"
        )
        try:
            definitions = ClearlyDefinedDefinitions(
                definitions_from_clearlydefined(dependency)
            )
        except RequestException:
            click.echo(f"Could not download definitions.")
            continue

        if definitions.score == 0:
            pass

        score_check = ScoreCheck()
        if not score_check.process(definitions):
            success = dependency_success = False
            click.echo(score_check.reasons[0])

        license_whitelisted_check = LicenseWhitelistedCheck()
        if not license_whitelisted_check.process(definitions):
            success = dependency_success = False
            for reason in license_whitelisted_check.reasons:
                click.echo(reason)

        if dependency_success:
            click.echo("Good.")

    return success


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
