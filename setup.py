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
	    'websockets',
	    'matplotlib',
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
	    'websockets',
	    'matplotlib',
        ],
    packages=['flapjack'],
    python_requires='>=3',
    version='v0.0'
)

# add packages via conda:
# conda install -c plotly plotly-orca
