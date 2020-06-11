# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from abc import ABC, abstractmethod
from inspect import cleandoc
from os import PathLike
from typing import Dict, Iterator, List

import yaml
from requests import RequestException

from liferay_inbound_checker import LICENSE_WHITELIST
from liferay_inbound_checker.clearlydefined import (
    ClearlyDefinedDefinitions,
    clearlydefined_url,
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

    TARGET_NUMBER = 87

    def process(self, definitions: ClearlyDefinedDefinitions) -> bool:

        self.success = definitions.score >= self.TARGET_NUMBER
        if not self.success:
            self.reasons = [ScoreTooLowReason(definitions.score)]
        return self.success


class LicenseWhitelistedCheck(BaseCheck):
    def process(self, definitions: ClearlyDefinedDefinitions) -> bool:
        success = True
        reasons = []
        licenses = definitions.discovered_licenses
        if not licenses:
            success = False
            reasons.append(NoDiscoveredLicensesReason())
        for lic in licenses:
            if lic == "NOASSERTION":
                success = False
                reasons.append(NoassertionDetectedReason())
            elif lic not in LICENSE_WHITELIST:
                success = False
                reasons.append(NotWhitelistedLicenseReason(lic))
        # if licenses == {"NOASSERTION"}:
        #     success = False
        #     reasons.append(
        #         OnlyNoassertionReason(
        #             "Component only has 'NOASSERTION' as discovered license."
        #         )
        #     )

        self.success = success
        self.reasons = reasons
        return self.success


class Reason:
    """Base class for reasons for a check failing."""

    ADVICE = ""

    def __str__(self):
        return str(self.ADVICE)


class RequestExceptionReason(Reason):
    """Couldn't connect to the URL."""

    ADVICE = cleandoc(
        """
        {url}: {err}
        There was an error in retrieving a result from an internet API. This error should be investigated. Alternatively, simply try running the test again, and hope it works.
        """
    )

    def __init__(self, url, err):
        self.url = url
        self.err = err

    def __str__(self):
        return self.ADVICE.format(url=self.url, err=self.err)


class NoDiscoveredLicensesReason(Reason):
    ADVICE = cleandoc(
        """
        The dependency has no declared or detected licenses. Please search the dependency for any licensing information, and open an Inbound Licensing ticket with your findings.
        """
    )


class NotWhitelistedLicenseReason(Reason):
    ADVICE = cleandoc(
        """
        '{lic}' was detected as a license of the package. This license is not pre-approved, so it needs Legal approval. Please open an Inbound Licensing ticket.
        """
    )

    def __init__(self, lic):
        self.lic = lic

    def __str__(self):
        return self.ADVICE.format(lic=self.lic)


class NoassertionDetectedReason(Reason):
    ADVICE = cleandoc(
        """
        'NOASSERTION' was detected as a license of the package. This may be indicative of problems. Please open an Inbound Licensing ticket.
        """
    )


class ScoreTooLowReason(Reason):
    ADVICE = cleandoc(
        """
        This package scored {score} on ClearlyDefined. This is below the threshold of {target_score}. This needn't be a problem, but may be indicative of problems. Please open an Inbound Licensing ticket.
        """
    )

    def __init__(self, score):
        self.score = score

    def __str__(self):
        return self.ADVICE.format(
            score=self.score, target_score=ScoreCheck.TARGET_NUMBER
        )


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
        return result

    try:
        definitions = ClearlyDefinedDefinitions(
            definitions_from_clearlydefined(dependency)
        )
    except RequestException as err:
        result.success = False
        result.reasons = [
            RequestExceptionReason(
                clearlydefined_url(result.dependency), str(err),
            )
        ]
        return result

    for check_cls in (ScoreCheck, LicenseWhitelistedCheck):
        check = check_cls()
        if not check.process(definitions):
            result.success = False
            result.reasons.extend(check.reasons)

    return result
