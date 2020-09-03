#!/usr/bin/env python

import os
#from distutils.core import setup
from setuptools import setup
import subprocess

setup(name='flapjack',
    install_requires=[        
        'numpy', 
        'scipy', 
        'pandas',
        'requests', 
        'tqdm', 
        'plotly', 
        'asyncio', 
        'nest_asyncio',
        'requests_jwt',
	'statsmodels'
        ],
    setup_requires=[
        'numpy', 
        'scipy', 
        'pandas',
        'requests', 
        'tqdm', 
        'plotly', 
        'asyncio', 
        'nest_asyncio',
        'requests_jwt',
	'statsmodels'
        ],
    packages=['flapjack'],
    python_requires='>=3',
    version='v0.0'
)
