# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from abc import ABC, abstractmethod
from os import PathLike
from typing import Dict, Iterator, List

import yaml
from requests import RequestException

from liferay_inbound_checker import LICENSE_WHITELIST
from liferay_inbound_checker.clearlydefined import (
    ClearlyDefinedDefinitions,
    definitions_from_clearlydefined,
)
from liferay_inbound_checker.dependencies import Dependency


def load_whitelist(path: PathLike) -> List[Dict]:
    """Given a path, parse the yaml inside."""
    with open(path) as fp:
        return yaml.safe_load(fp)


def is_whitelisted(dependency: Dependency, whitelist: List[Dict]) -> bool:
    name = f"{dependency.groupid}/{dependency.artifactid}"
    for item in whitelist:
        try:
            if item["name"] == name and item["version"] == dependency.version:
                return True
        except (KeyError, TypeError):
            continue
    return False


class BaseCheck(ABC):
    """Base class for checks."""

    def __init__(self):
        self.success = None
        self.reasons = []

    @abstractmethod
    def process(self, definitions: ClearlyDefinedDefinitions) -> bool:
        """Run the check on *definitions* either successfully or not."""


class ScoreCheck(BaseCheck):

    TARGET_NUMBER = 83

    def process(self, definitions: ClearlyDefinedDefinitions) -> bool:

        self.success = definitions.score >= self.TARGET_NUMBER
        if not self.success:
            self.reasons = [
                f"Score is {definitions.score}, lower than"
                f" {self.TARGET_NUMBER}."
            ]
        return self.success


class LicenseWhitelistedCheck(BaseCheck):
    def process(self, definitions: ClearlyDefinedDefinitions) -> bool:
        success = True
        reasons = []
        licenses = definitions.discovered_licenses
        if not licenses:
            success = False
            reasons.append("Component has no discovered licenses.")
        for lic in licenses:
            if lic not in LICENSE_WHITELIST:
                success = False
                reasons.append(
                    f"Component has discovered license '{lic}', which is not"
                    f" whitelisted."
                )
        if licenses == {"NOASSERTION"}:
            success = False
            reasons.append(
                "Component only has 'NOASSERTION' as discovered license."
            )

        self.success = success
        self.reasons = reasons
        return self.success


class Result:
    def __init__(self, dependency=None):
        self.dependency = dependency
        self.success = None
        self.reasons = []


def check(dependency: Dependency, whitelist: List[Dict] = None) -> Result:
    if whitelist is None:
        whitelist = []

    result = Result(dependency)
    result.success = True

    if is_whitelisted(dependency, whitelist):
        result.reasons = ["Whitelisted."]
        return result

    try:
        definitions = ClearlyDefinedDefinitions(
            definitions_from_clearlydefined(dependency)
        )
    except RequestException as err:
        result.success = False
        result.reasons = [str(err)]
        return result

    for check_cls in (ScoreCheck, LicenseWhitelistedCheck):
        check = check_cls()
        if not check.process(definitions):
            result.success = False
            result.reasons.extend(check.reasons)

    return result
