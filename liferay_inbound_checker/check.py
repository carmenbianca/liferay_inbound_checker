# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from abc import ABC, abstractmethod

from liferay_inbound_checker import LICENSE_WHITELIST
from liferay_inbound_checker.clearlydefined import ClearlyDefinedDefinitions


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
