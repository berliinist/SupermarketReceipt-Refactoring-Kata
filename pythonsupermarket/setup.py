#!/usr/bin/env python

from distutils.core import setup

exec(open('pythonsupermarket/__init__.py').read())

with open('requirements.txt') as f:
    requirements = f.readlines()
requirements = [element.strip() for element in requirements]


setup(name='pythonsupermarket',
      version=__version__,
      description='Code Challenge.',
      author='emilybache',
      maintainer='berliinist',
      platforms='any',
      install_requires=requirements,
      classifiers=['Operating System :: OS Independent',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.8'])
