from setuptools import setup, find_packages


with open('README.md', 'r') as ld:
    long_description = ld.read()

setup(name='pyflapjack',
    version='1.0.0',
    author='Tim Rudge',
    author_email='Tim.Rudge@newcastle.ac.uk ',
    description='Python package that interfaces the Flapjack API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RudgeLab/pyFlapjack',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
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
        'kaleido'
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
        'kaleido'
        ],
    packages=find_packages(),
    python_requires='>=3',
)
