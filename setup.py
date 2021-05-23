#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name="derp",
    version="0.1.0",
    author="Brendan Folie",
    author_email="bfolie@citrine.io",
    url="https://github.com/bfolie/derp",
    license="MIT",
    packages=find_packages(exclude=['tests']),
    description="command line tool to ensure that deprecated code is removed in a timely manner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'derp = derp.main:main',
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
    ]
)