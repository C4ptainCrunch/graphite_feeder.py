from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description = ""

setup(
    name='graphite_feeder',
    version='0.1',

    description='Feed metrics into Graphite easily from Python',
    long_description=long_description,

    url='https://github.com/C4ptainCrunch/graphite_feeder.py',
    author='Nikita Marchant',
    author_email='nikita.marchant@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='graphite metrics feeder',

    packages=['graphite_feeder'],
    install_requires=[],
)
