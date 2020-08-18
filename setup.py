#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#  This file is part of the synctextranslator package.
#
#  Copyright (C) 2020  Benedikt Otto <s6beotto@uni-bonn.de>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synctextranslator",
    version="0.0.1",
    author="Benedikt Otto",
    author_email="benedikt_o@web.de",
    description="translator of synctex linenumbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenediktO/synctextranslator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'synctextranslator=translator.translator:main'
        ],
	}
)