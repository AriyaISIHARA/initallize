# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='Initallize',
    version=1.0,
    description="generate __all__ definition in __init__.py",
    packages=find_packages(exclude=['test']),
    package_dir={'': 'src'},
    test_suite='test'
)
