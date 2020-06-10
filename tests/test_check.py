# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for the checks."""

from liferay_inbound_checker.check import ScoreCheck, LicenseWhitelistedCheck


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
        assert check.success
        assert result

    for i in range(0, 83):
        result = check.process(ScoreMock(i))
        assert not check.success
        assert check.reasons
        assert not result


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
