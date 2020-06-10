# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for the checks."""

from requests import RequestException

from liferay_inbound_checker.check import (
    LicenseWhitelistedCheck,
    ScoreCheck,
    check,
)
from liferay_inbound_checker.dependencies import Dependency


class ScoreMock:
    def __init__(self, score):
        self.score = score


class DiscoveredMock:
    def __init__(self, discovered_licenses):
        self.discovered_licenses = discovered_licenses


def test_score_check():
    check = ScoreCheck()
    for i in range(83, 101):
        result = check.process(ScoreMock(i))
        assert result
        assert check.success

    for i in range(0, 83):
        result = check.process(ScoreMock(i))
        assert not result
        assert not check.success
        assert check.reasons


def test_whitelisted_check(clearlydefined_definitions):
    check = LicenseWhitelistedCheck()
    result = check.process(clearlydefined_definitions)
    assert result
    assert check.success


def test_whitelisted_check_not_whitelisted():
    check = LicenseWhitelistedCheck()
    result = check.process(DiscoveredMock({"CC0-1.0", "WTFPL"}))
    assert not result
    assert not check.success
    assert len(check.reasons) == 1


def test_whitelisted_check_no_licenses():
    check = LicenseWhitelistedCheck()
    result = check.process(DiscoveredMock(set()))
    assert not result
    assert not check.success
    assert len(check.reasons) == 1


def test_whitelisted_check_only_noassertion():
    check = LicenseWhitelistedCheck()
    result = check.process(DiscoveredMock({"NOASSERTION"}))
    assert not result
    assert not check.success
    assert len(check.reasons) == 1


def test_check_could_not_download(mocker):
    mocker.patch(
        "liferay_inbound_checker.check.definitions_from_clearlydefined",
        side_effect=RequestException(),
    )

    result = check(Dependency("a", "b", "c"))
    assert not result.success
    assert result.reasons


def test_check_simple(mocker, clearlydefined_dict):
    clearlydefined_dict["scores"]["effective"] = 83
    mocker.patch(
        "liferay_inbound_checker.check.definitions_from_clearlydefined",
        return_value=clearlydefined_dict,
    )

    result = check(Dependency("a", "b", "c"))
    assert result.success
