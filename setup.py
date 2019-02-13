#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from owslib_esgfwps import __version__, __author__, __email__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as changes_file:
    changes = changes_file.read()

requirements = [line.strip() for line in open('requirements.txt')]


setup(
    name='owslib-esgfwps',
    version=__version__,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="OWSLib extension for the ESGF compute WPS profile",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + changes,
    url='https://github.com/bird-house/OWSLib-esgfwps',
    keywords='owslib extension wps esgf',
    author=__author__,
    author_email=__email__,
    packages=find_packages('owslib_esgfwps'),
    include_package_data=True,
    zip_safe=False,
)
