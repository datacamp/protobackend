#!/usr/bin/env python

from os import path
from setuptools import setup

PACKAGE_NAME = "protobackend"
VERSION = "0.2.3"

HERE = path.abspath(path.dirname(__file__))
README_FILE = path.join(HERE, "README.md")

with open(README_FILE, encoding="utf-8") as fp:
    README = fp.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=[PACKAGE_NAME],
    description="Generic backend",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Michael Chow",
    author_email="michael@datacamp.com",
    maintainer="Jeroen Hermans",
    maintainer_email="content-engineering@datacamp.com",
    url="https://github.com/datacamp/protobackend",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
