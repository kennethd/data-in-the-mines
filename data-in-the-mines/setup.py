#!/usr/bin/env python2.7

# distutils does not support 'python setup.py develop'
#from distutils.core import setup
from setuptools import setup

setup(
    name = 'data-in-the-mines',
    version = '0.1',
    description = 'Automate reports generation, and provide a web interface to look at them',
    author = 'Kenneth Dombrowski',
    author_email = 'kenneth@ylayali.net',
    url = 'http://git.ylayali.net/data-in-the-mines.git',
    packages = ['ditm', 'ditm.examples', 'ditm.flask', 'ditm.test'],
    license = 'MIT',
)
