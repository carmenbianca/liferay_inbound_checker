# SPDX-FileCopyrightText: © 2020 Liferay, Inc. <https://liferay.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from inspect import cleandoc

import pytest

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
