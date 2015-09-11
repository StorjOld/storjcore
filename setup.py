#!/usr/bin/env python
# coding: utf-8


import os
import sys
from setuptools import setup, find_packages


exec(open('storjcore/version.py').read())  # load __version__
DOWNLOAD_URL = "%(baseurl)s/%(name)s/%(name)s-%(version)s.tar.gz" % {
    'baseurl': "https://pypi.python.org/packages/source/a",
    'name': 'storjcore',
    'version': __version__  # NOQA
}


setup(
    name='storjcore',
    description="Client for storing and auditing data. http://storj.io",
    long_description=open("README.rst").read(),
    keywords="",
    url='http://storj.io',
    author='Shawn Wilkinson',
    author_email='shawn+storjcore@storj.io',
    license="MIT",
    version=__version__,  # NOQA
    test_suite="tests",
    dependency_links=[],
    install_requires=open("requirements.txt").readlines(),
    tests_require=open("test_requirements.txt").readlines(),
    download_url=DOWNLOAD_URL,
    packages=find_packages(),
    classifiers=[
        # "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
