==============
OWSLib-esgfwps
==============

.. image:: https://img.shields.io/travis/bird-house/OWSLib-esgfwps.svg
   :target: https://travis-ci.org/bird-house/OWSLib-esgfwps
   :alt: Travis Build

.. image:: https://img.shields.io/github/license/bird-house/OWSLib-esgfwps.svg
   :target: https://github.com/bird-house/OWSLib-esgfwps/blob/master/LICENSE.txt
   :alt: GitHub license

.. image:: https://badges.gitter.im/bird-house/birdhouse.svg
   :target: https://gitter.im/bird-house/birdhouse?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
   :alt: Join the chat at https://gitter.im/bird-house/birdhouse


The `OWSLib-esgfwps` package is an OWSLib_ extension for the ESGF_ compute WPS profile.


* Free software: Apache Software License 2.0
* Documentation: https://owslib-esgfwps.readthedocs.io.

Installation
============

Install from GitHub
-------------------

Check out code from the birdhouse GitHub repo and start the installation:

.. code-block:: sh

   $ git clone https://github.com/bird-house/OWSLib-esgfwps.git
   $ cd OWSLib-esgfwps
   $ conda env create -f environment.yml
   $ python setup.py install

Usage
=====

.. automodule:: owslib-esgfwps

Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _OWSLib: https://geopython.github.io/OWSLib/
.. _ESGF: https://github.com/ESGF/esgf-compute-api
