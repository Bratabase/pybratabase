#!/usr/bin/env python3

from setuptools import setup

setup(
    name='pybratabase',
    description='Bratabase API python client',
    url='https://github.com/bratabase/pybratabase',
    author='Jj Del Carpio',
    license='LGPL',
    packages=['pybratabase'],
    install_requires=[
        'requests>=2.3.0'
    ]
)
