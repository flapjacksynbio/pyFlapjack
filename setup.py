from setuptools import setup, find_packages


with open('README.md', 'r') as ld:
    long_description = ld.read()

setup(name='flapjack',
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
        'numpy==1.21.2',
        'scipy==1.7.1',
        'pandas==1.3.3',
        'requests==2.26.0',
        'tqdm==4.62.3',
        'plotly==5.3.1',
        'asyncio==3.4.3',
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
        'asyncio==3.4.3',
        'nest_asyncio==1.5.1',
        'requests_jwt==0.5.3',
        'websockets==10.0',
        'matplotlib==3.4.3',
        ],
    packages=find_packages(),
    python_requires='>=3',
)
