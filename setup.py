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
	    'statsmodels',
	    'jupyter',
	    'websockets',
	    'matplotlib',
	    'seaborn'
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
	    'statsmodels',
	    'jupyter',
	    'websockets',
	    'matplotlib',
	    'seaborn'
        ],
    packages=['flapjack'],
    python_requires='>=3.8',
    version='v0.0'
)
