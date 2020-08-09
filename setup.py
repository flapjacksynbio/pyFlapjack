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
        'requests_jwt'
        ],
    setup_requires=[
        'numpy', 
        'scipy', 
        'pandas',
        'requests', 
        'tqdm', 
        'plotly', 
        'asyncio', 
        'requests_jwt'
        ],
    packages=['flapjack'],
    python_requires='>=3',
    version='v0.0'
)
