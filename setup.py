#!/usr/bin/env python

import os
#from distutils.core import setup
from setuptools import setup
import subprocess

setup(name='flapjack',
    install_requires=[
        'numpy==1.21.2',
        'scipy==1.7.1',
        'pandas==1.3.3',
        'requests==2.26.0',
        'tqdm==4.62.3',
        'plotly==5.3.1',
        'asyncio==5.3.1',
        'nest_asyncio==1.5.1',
        'requests_jwt==0.5.3',
        'websockets==10.0',
        'matplotlib==3.4.3',
        ],
    setup_requires=[
        'numpy==1.21.2',
        'scipy==1.7.1',
        'pandas==1.3.3',
        'requests==2.26.0',
        'tqdm==4.62.3',
        'plotly==5.3.1',
        'asyncio==5.3.1',
        'nest_asyncio==1.5.1',
        'requests_jwt==0.5.3',
        'websockets==10.0',
        'matplotlib==3.4.3',
        ],
    packages=['flapjack'],
    python_requires='>=3',
    version='v0.0'
)

# add packages via conda:
# conda install -c plotly plotly-orca
