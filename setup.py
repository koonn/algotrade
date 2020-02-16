# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    lic = f.read()

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name='algotrade',
    version='0.0.1',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='konnot',
    author_email='konnie211@gmail.com',
    install_requires=requires,
    url='https://github.com/konnot/algotrade',
    license=lic,
    packages=find_packages(exclude=('tests', 'docs'))
)

