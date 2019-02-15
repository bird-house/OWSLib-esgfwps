#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

version = __import__('owslib_esgfwps').__version__
author = __import__('owslib_esgfwps').__author__
email = __import__('owslib_esgfwps').__email__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as changes_file:
    changes = changes_file.read()

requirements = [line.strip() for line in open('requirements.txt')]


setup(
    name='owslib-esgfwps',
    version=version,
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
    author=author,
    author_email=email,
    py_modules=['owslib_esgfwps'],
)
