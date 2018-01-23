#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-distributed-collage-filter.
# https://github.com/globocom/thumbor-distributed-collage-filter

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, Globo.com <thumbor@corp.globo.com>

from setuptools import setup, find_packages
from thumbor_distributed_collage_filter import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
    'pyssim>=0.4.0',
]

setup(
    name='thumbor-distributed-collage-filter',
    version=__version__,
    description='Distributed collage is a filter for creating side-by-side images.',
    long_description='''
Distributed collage is a filter for creating side-by-side images.
''',
    keywords='thumbor filter',
    author='Globo.com',
    author_email='thumbor@corp.globo.com',
    url='https://github.com/globocom/thumbor-distributed-collage-filter',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'thumbor>=6.4.1',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'thumbor-distributed-collage-filter=thumbor_distributed_collage_filter.cli:main',
        ],
    },
)
