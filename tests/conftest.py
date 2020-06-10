# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import json
from inspect import cleandoc

import pytest

from liferay_inbound_checker.clearlydefined import ClearlyDefinedResult
from liferay_inbound_checker.dependencies import convert_to_tree


@pytest.fixture()
def sample_pom():
    return cleandoc(
        """
        <?xml version="1.0" encoding="UTF-8"?>
        <project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd" xmlns="http://maven.apache.org/POM/4.0.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <modelVersion>4.0.0</modelVersion>
          <groupId>com.liferay.portal</groupId>
          <artifactId>release.portal.bom.third.party</artifactId>
          <version>unspecified</version>
          <packaging>pom</packaging>
          <licenses>
            <license>
              <name>LGPL 2.1</name>
              <url>http://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt</url>
            </license>
          </licenses>
          <developers>
            <developer>
              <name>Brian Wing Shun Chan</name>
              <organization>Liferay, Inc.</organization>
              <organizationUrl>http://www.liferay.com</organizationUrl>
            </developer>
          </developers>
          <scm>
            <connection>scm:git:git@github.com:liferay/liferay-portal.git</connection>
            <developerConnection>scm:git:git@github.com:liferay/liferay-portal.git</developerConnection>
            <tag>c4e9d36fe5cf8869788da31fe94c0fe2c9b729e7</tag>
            <url>https://github.com/liferay/liferay-portal</url>
          </scm>
          <repositories>
            <repository>
              <id>liferay-public-releases</id>
              <name>Liferay Public Releases</name>
              <url>https://repository-cdn.liferay.com/nexus/content/repositories/liferay-public-releases/</url>
            </repository>
          </repositories>
          <dependencyManagement>
            <dependencies>
              <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-context</artifactId>
                <version>5.2.2.RELEASE</version>
              </dependency>
              <dependency>
                <groupId>com.liferay</groupId>
                <artifactId>com.fasterxml.jackson.databind</artifactId>
                <version>2.10.3.LIFERAY-PATCHED-1</version>
              </dependency>
            </dependencies>
          </dependencyManagement>
        </project>
        """
    )


@pytest.fixture()
def sample_pom_root(sample_pom):
    return convert_to_tree(sample_pom)


@pytest.fixture()
def clearlydefined_json():
    return cleandoc(
        """
        {
            "described": {
                "releaseDate": "2019-12-03",
                "sourceLocation": {
                    "type": "sourcearchive",
                    "provider": "mavencentral",
                    "namespace": "org.springframework",
                    "name": "spring-context",
                    "revision": "5.2.2.RELEASE",
                    "url": "http://central.maven.org/maven2/org/springframework/spring-context/5.2.2.RELEASE/spring-context-5.2.2.RELEASE-sources.jar"
                },
                "urls": {
                    "registry": "http://central.maven.org/maven2/org/springframework/spring-context",
                    "version": "http://central.maven.org/maven2/org/springframework/spring-context/5.2.2.RELEASE",
                    "download": "http://central.maven.org/maven2/org/springframework/spring-context/5.2.2.RELEASE/spring-context-5.2.2.RELEASE.jar"
                },
                "hashes": {
                    "sha1": "a77a18fa425eba9c55447fa0711e2dbfbf71907b",
                    "sha256": "bb9ed510c61e44b4d39b4e27eb6dfa1737914ee10e4d915a9d757114dbd01fd0"
                },
                "files": 893,
                "tools": [
                    "clearlydefined/1.5.0",
                    "licensee/9.13.0",
                    "scancode/3.2.2"
                ],
                "toolScore": {
                    "total": 100,
                    "date": 30,
                    "source": 70
                },
                "score": {
                    "total": 100,
                    "date": 30,
                    "source": 70
                }
            },
            "files": [
                {
                    "path": "META-INF/license.txt",
                    "license": "Apache-2.0 AND BSD-3-Clause",
                    "natures": [
                        "license"
                    ],
                    "attributions": [
                        "Copyright (c) 2000-2011 INRIA, France Telecom",
                        "Copyright (c) 1999-2009, OW2 Consortium <https://www.ow2.org/>"
                    ],
                    "hashes": {
                        "sha1": "e642b683c2403816bd0e23b196a0116ba88a7331",
                        "sha256": "576b97db98ed31831110d7083605e4b62e09769f877f90051750adc89b6cfd7c"
                    },
                    "token": "576b97db98ed31831110d7083605e4b62e09769f877f90051750adc89b6cfd7c"
                },
                {
                    "path": "META-INF/MANIFEST.MF",
                    "hashes": {
                        "sha1": "4502529cbf251d40b4e4d88e6bd072e59a914222",
                        "sha256": "d94a867f80e5b2ad4399cb09938cbd252aeff74b85a260ce29530309daa781d8"
                    }
                },
                {
                    "path": "META-INF/notice.txt",
                    "attributions": [
                        "Copyright (c) 2002-2019 Pivotal, Inc."
                    ],
                    "hashes": {
                        "sha1": "61b45cf406310233ce8abd39d8bcae98634ece1b",
                        "sha256": "6e1409bc0b4cc23e541c8a44ce15ebcf0cff225b7019e6b4f301783a3b9e55ea"
                    },
                    "token": "6e1409bc0b4cc23e541c8a44ce15ebcf0cff225b7019e6b4f301783a3b9e55ea"
                },
                {
                    "path": "META-INF/spring-context.kotlin_module",
                    "hashes": {
                        "sha1": "bb823d40b2f47900956960093049fd2304f097ad",
                        "sha256": "de361b718a64acca78f11098d683f8a5a9b89313a49a03133fab4e6bc25dd968"
                    }
                },
                {
                    "path": "META-INF/spring.handlers",
                    "hashes": {
                        "sha1": "7190b5021dd44febc2c6dda3220371dcbbf1016b",
                        "sha256": "8f0dc64049c22a3f3096404a3fe676e7d1655f227d6a6eb32ad0faea62f48ed7"
                    }
                },
                {
                    "path": "META-INF/spring.schemas",
                    "hashes": {
                        "sha1": "d91ded8af73d4f36bc98ccecb095cc3c1d401f7b",
                        "sha256": "88472fe3f4b3aaa1a1d0d5f7e3b775474ba1aa3f41d4abf617a8e6abdcaf7141"
                    }
                }
            ],
            "licensed": {
                "declared": "Apache-2.0",
                "toolScore": {
                    "total": 60,
                    "declared": 30,
                    "discovered": 0,
                    "consistency": 0,
                    "spdx": 15,
                    "texts": 15
                },
                "facets": {
                    "core": {
                        "attribution": {
                            "unknown": 891,
                            "parties": [
                                "Copyright (c) 2002-2019 Pivotal, Inc.",
                                "Copyright (c) 2000-2011 INRIA, France Telecom",
                                "Copyright (c) 1999-2009, OW2 Consortium <https://www.ow2.org/>"
                            ]
                        },
                        "discovered": {
                            "unknown": 892,
                            "expressions": [
                                "Apache-2.0 AND BSD-3-Clause"
                            ]
                        },
                        "files": 893
                    }
                },
                "score": {
                    "total": 60,
                    "declared": 30,
                    "discovered": 0,
                    "consistency": 0,
                    "spdx": 15,
                    "texts": 15
                }
            },
            "coordinates": {
                "type": "maven",
                "provider": "mavencentral",
                "namespace": "org.springframework",
                "name": "spring-context",
                "revision": "5.2.2.RELEASE"
            },
            "_meta": {
                "schemaVersion": "1.6.1",
                "updated": "2019-12-07T02:20:44.481Z"
            },
            "scores": {
                "effective": 80,
                "tool": 80
            }
        }
        """
    )


@pytest.fixture()
def clearlydefined_dict(clearlydefined_json):
    return json.loads(clearlydefined_json)


@pytest.fixture()
def clearlydefined_result(clearlydefined_dict):
    return ClearlyDefinedResult(clearlydefined_dict)
