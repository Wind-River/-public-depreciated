# Copyright 2017 Intel Corporation
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
# ------------------------------------------------------------------------------

from __future__ import print_function

import os
import subprocess

from setuptools import setup, find_packages


def bump_version(version):
    (major, minor, patch) = version.split('.')
    patch = str(int(patch) + 1)
    return ".".join([major, minor, patch])


def auto_version(default, strict):
    output = subprocess.check_output(['git', 'describe', '--dirty'])
    parts = output.decode('utf-8').strip().split('-', 1)
    parts[0] = parts[0][1:]  # strip the leading 'v'
    if len(parts) == 2:
        parts[0] = bump_version(parts[0])
    if default != parts[0]:
        msg = "setup.py and (bumped?) git describe versions differ: {} != {}"\
            .format(default, parts[0])
        if strict:
            print("ERROR: " + msg, file=sys.stderr)
            sys.exit(1)
        else:
            print("WARNING: " + msg, file=sys.stderr)
            print("WARNING: using setup.py version {}".format(
                default), file=sys.stderr)
            parts[0] = default

    if len(parts) == 2:
        return ".git".join([parts[0], parts[1].replace("-", ".")])
    else:
        return parts[0]


def version(default):
    if 'VERSION' in os.environ:
        if os.environ['VERSION'] == 'AUTO_STRICT':
            version = auto_version(default, strict=True)
        elif os.environ['VERSION'] == 'AUTO':
            version = auto_version(default, strict=False)
        else:
            version = os.environ['VERSION']
    else:
        version = default + ".dev1"
    return version



setup(name='sawtooth-part',
      version=version('1.1.0'),
      description='Sparts Part Example',
      author='Wind River',
      url='https://github.com/Wind-River/software-parts-ledger',
      packages=find_packages(),
      install_requires=[
          'aiohttp',
          'colorlog',
          'protobuf',
          'sawtooth-sdk',
          'sawtooth-signing',
          'PyYAML',
          ],
      entry_points={
          'console_scripts': [
              'pt = sawtooth_part.part_cli:main_wrapper',
              'part_tp_python = sawtooth_part.processor.main:main',
          ]
      })
