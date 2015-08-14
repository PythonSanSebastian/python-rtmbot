#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os.path as op
import io
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# long description
def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


# Get version without importing, which avoids dependency issues
module_name = find_packages(exclude=['tests'])[0]
__version__ = '0.0.1'


LICENSE = 'new BSD'

setup_dict = dict(
    name=module_name,
    version=__version__,
	url='',

    description="A bot for Slack.",

    license=LICENSE,

    author='',
    author_email='',
    maintainer='',
    maintainer_email='',

    packages=find_packages(),

    install_requires=read('requirements.txt'),

    #extra_files=['CHANGES.rst', 'LICENSE', 'README.rst'],

    long_description=read('README.md'),

    platforms='Linux/MacOSX',

    entry_points={
        'console_scripts': [
            'slackbot = rtmbot.main:main',
        ]
    },

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    extras_require={
        'testing': ['pytest', 'pytest-cov'],
    }
)


# Python3 support keywords
if sys.version_info >= (3,):
    setup_dict['use_2to3'] = False
    setup_dict['convert_2to3_doctests'] = ['']
    setup_dict['use_2to3_fixers'] = ['']


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup_dict.update(dict(tests_require=['pytest'],
                       cmdclass={'test': PyTest}))


if __name__ == '__main__':
    setup(**setup_dict)
