#!/usr/bin/env python

# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "license-expression>=1.0", "PyYAML>=3.08"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Carmen Bianca Bakker",
    author_email="carmen@carmenbianca.eu",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Liferay Inbound Checker verifies the licensing of inbound packages to Liferay Portal",
    entry_points={
        "console_scripts": [
            "liferay_inbound_checker=liferay_inbound_checker.cli:main"
        ]
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="liferay_inbound_checker",
    name="liferay_inbound_checker",
    packages=find_packages(
        include=["liferay_inbound_checker", "liferay_inbound_checker.*"]
    ),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/carmenbianca/liferay_inbound_checker",
    version="0.1.0",
    zip_safe=False,
)
