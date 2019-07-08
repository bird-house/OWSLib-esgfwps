#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

about = {}
with open(os.path.join(here, 'owslib_esgfwps', '__version__.py'), 'r') as f:
    exec(f.read(), about)

reqs = [line.strip() for line in open('requirements.txt')]
extra_reqs = [line.strip() for line in open('requirements_dev.txt')]


setup(
    name='owslib-esgfwps',
    version=about['__version__'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="OWSLib extension for the ESGF compute WPS profile",
    license="Apache Software License 2.0",
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/bird-house/OWSLib-esgfwps',
    keywords='owslib extension wps esgf cwt',
    author=about['__author__'],
    author_email=about['__email__'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    extra_requires=extra_reqs,
)
