#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='scraperapp',
    version='1.0.0',
    author="Hamid Poursepanj",
    author_email="hamidp555@gmail.com",
    long_description=long_description,
    packages=find_packages(),
    entry_points={'scrapy': ['settings = scraperapp.settings']},
)
