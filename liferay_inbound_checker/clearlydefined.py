# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import json
from contextlib import suppress
from typing import Dict, Set

import requests
from license_expression import Licensing
from requests.compat import urljoin

from .dependencies import Dependency

_LICENSING = Licensing()


def definitions_from_clearlydefined(dependency: Dependency) -> Dict:
    """
    :raises requests.RequestException: if the request could not be made.
    """
    url = urljoin(
        "https://api.clearlydefined.io/definitions/maven/mavencentral/",
        f"{dependency.groupid}/{dependency.artifactid}/{dependency.version}",
    )
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    raise requests.RequestException(
        f"Status code of '{url}' was {response.status_code}"
    )


class ClearlyDefinedDefinitions:
    def __init__(self, json_dict: Dict):
        self._json_dict = json_dict

    def is_empty(self) -> bool:
        """ClearlyDefined sometimes returns empty definitions. This method
        does a naive check to verify for that.
        """
        try:
            self._json_dict["described"]["hashes"]["sha1"]
            return False
        except KeyError:
            return True

    @property
    def discovered_license_expressions(self) -> Set[str]:
        result = set()

        with suppress(KeyError):
            result = result.union({self._json_dict["licensed"]["declared"]})

        try:
            facets = self._json_dict["licensed"]["facets"].values()
        except KeyError:
            return result

        for facet in facets:
            with suppress(KeyError):
                result = result.union(set(facet["discovered"]["expressions"]))

        return result

    @property
    def discovered_licenses(self) -> Set[str]:
        """
        :raises ExpressionError: if expression could not be parsed.
        """
        result = set()
        expressions = self.discovered_license_expressions
        for expression in expressions:
            parsed = _LICENSING.parse(expression)
            licenses = _LICENSING.license_keys(parsed)
            for lic in licenses:
                result.add(lic)
        return result

    @property
    def score(self) -> int:
        return self._json_dict["scores"]["effective"]
