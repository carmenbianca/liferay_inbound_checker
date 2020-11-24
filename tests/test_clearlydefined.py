# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for interaction with ClearlyDefined."""


import pytest
from requests import RequestException

from liferay_inbound_checker.clearlydefined import (
    ClearlyDefinedDefinitions,
    definitions_from_clearlydefined,
)
from liferay_inbound_checker.dependencies import Dependency


class MockResponse:
    """Super simple mocked version of Response."""

    def __init__(self, text=None, status_code=None):
        self.text = text
        self.status_code = status_code


def test_definitions_simple(mocker, clearlydefined_json, clearlydefined_dict):
    mocker.patch(
        "requests.get", return_value=MockResponse(clearlydefined_json, 200)
    )

    assert (
        definitions_from_clearlydefined(Dependency("a", "b", "c"))
        == clearlydefined_dict
    )


def test_definitions_exception(mocker):
    mocker.patch("requests.get", side_effect=RequestException())

    with pytest.raises(RequestException):
        definitions_from_clearlydefined(Dependency("a", "b", "c"))


def test_definitions_bad_status_code(mocker):
    mocker.patch("requests.get", return_value=MockResponse("Error", 404))

    with pytest.raises(RequestException):
        definitions_from_clearlydefined(Dependency("a", "b", "c"))


def test_score(clearlydefined_definitions):
    assert clearlydefined_definitions.score == 80


def test_score_different(clearlydefined_dict):
    clearlydefined_dict["scores"]["effective"] = 5
    result = ClearlyDefinedDefinitions(clearlydefined_dict)
    assert result.score == 5


def test_discovered_license_expressions(clearlydefined_definitions):
    assert clearlydefined_definitions.discovered_license_expressions == {
        "Apache-2.0",
        "Apache-2.0 AND BSD-3-Clause",
    }


def test_discovered_license_expressions_different():
    json_dict = {
        "licensed": {
            "declared": "GPL-3.0-or-later",
            "facets": {
                "core": {
                    "discovered": {"expressions": ["MIT", "GPL-3.0-or-later"],}
                },
                "test": {
                    "discovered": {"expressions": ["CC0-1.0", "NOASSERTION"]}
                },
            },
        }
    }
    result = ClearlyDefinedDefinitions(json_dict)
    assert result.discovered_license_expressions == {
        "MIT",
        "GPL-3.0-or-later",
        "CC0-1.0",
        "NOASSERTION",
    }


def test_discovered_licenses(clearlydefined_definitions):
    clearlydefined_definitions.discovered_licenses == {
        "Apache-2.0",
        "BSD-3-Clause",
    }

def test_discovered_licenses_parse_error():
    """Special case for mysql/mysql-connector-java."""
    json_dict = {
        "licensed": {
            "declared": "GPL-2.0-only WITH (OTHER AND Universal-FOSS-exception-1.0)",
        }
    }
    result = ClearlyDefinedDefinitions(json_dict)
    assert result.discovered_licenses == {
        "GPL-2.0-only",
        "OTHER",
        "Universal-FOSS-exception-1.0",
    }


def test_is_empty():
    definitions = ClearlyDefinedDefinitions(dict())
    assert definitions.is_empty()


def test_is_not_empty(clearlydefined_definitions):
    assert not clearlydefined_definitions.is_empty()
