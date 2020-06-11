# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for the whitelisting of dependencies."""

from liferay_inbound_checker.dependencies import Dependency
from liferay_inbound_checker.check import is_whitelisted

import pytest


@pytest.fixture()
def simple_whitelist():
    return [
        {
            "name": "org.springframework/spring-context",
            "version": "5.2.2.RELEASE",
            "issue": "https://issues.example.com/123",
            "comment": "N/A",
        }
    ]


def test_is_whitelisted(simple_whitelist):
    dependency = Dependency(
        "org.springframework", "spring-context", "5.2.2.RELEASE"
    )
    assert is_whitelisted(dependency, simple_whitelist)


def test_is_not_whitelisted(simple_whitelist):
    dependencies = [
        Dependency("red", "spring-context", "5.2.2.RELEASE"),
        Dependency("org.springframework", "red", "5.2.2.RELEASE"),
        Dependency("org.springframework", "spring-context", "red"),
    ]
    for dependency in dependencies:
        assert not is_whitelisted(dependency, simple_whitelist)


def test_is_whitelisted_bad_whitelist():
    whitelist = [{"not_a_name": "foo", "not_a_version": "bar"}]
    assert not is_whitelisted(Dependency("a", "b", "c"), whitelist)
