#!/usr/bin/env python

from distutils.core import setup


with open('requirements.txt') as f:
    requirements = f.readlines()
requirements = [element.strip() for element in requirements]


setup(name='pythonsupermarket',
      version='0.0.1',  # TODO: get it from version.py directly (create it first).
      description='Code Challenge.',
      author='emilybache',
      maintainer='berliinist',
      platforms='any',
      install_requires=requirements,
      classifiers=['Operating System :: OS Independent',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.8'])
