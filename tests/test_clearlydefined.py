# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for interaction with ClearlyDefined."""


import pytest
from requests import RequestException

from liferay_inbound_checker.clearlydefined import (
    ClearlyDefinedResult,
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


def test_score(clearlydefined_result):
    assert clearlydefined_result.score == 80


def test_score_different(clearlydefined_dict):
    clearlydefined_dict["scores"]["effective"] = 5
    result = ClearlyDefinedResult(clearlydefined_dict)
    assert result.score == 5
