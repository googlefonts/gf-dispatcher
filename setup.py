# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from setuptools import setup, find_packages, Command
from distutils import log

setup(
    name='dispatcher',
    version='0.0.1',
    author="Marc Foley",
    author_email="marc@mfoley.uk",
    description="Dispatch upstream fonts to Google Fonts repo",
    url="www.soon.co",
    license="Apache Software License 2.0",
    package_dir={"": "Lib"},
    packages=find_packages("Lib"),
    entry_points={
        "console_scripts": [
            "dispatcher = dispatcher.__main__:main"
        ],
    })
