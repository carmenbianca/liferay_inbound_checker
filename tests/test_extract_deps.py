# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for extracting dependencies."""

from liferay_inbound_checker.dependencies import extract_from_pom, Dependency


def test_extract_dependencies(sample_pom):
    """Given a sample pom, extract the dependencies."""
    result = extract_from_pom(sample_pom)
    assert sorted(result) == [
        Dependency(
            "com.liferay",
            "com.fasterxml.jackson.databind",
            "2.10.3.LIFERAY-PATCHED-1",
        ),
        Dependency("org.springframework", "spring-context", "5.2.2.RELEASE"),
    ]
