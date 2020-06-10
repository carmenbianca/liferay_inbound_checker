# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for extracting dependencies."""

from liferay_inbound_checker.dependencies import (
    Dependency,
    dependencies_from_tree,
)


def test_extract_dependencies(sample_pom_root):
    """Given a sample pom, extract the dependencies."""
    result = dependencies_from_tree(sample_pom_root)
    assert sorted(result) == [
        Dependency(
            "com.liferay",
            "com.fasterxml.jackson.databind",
            "2.10.3.LIFERAY-PATCHED-1",
        ),
        Dependency("org.springframework", "spring-context", "5.2.2.RELEASE"),
    ]
