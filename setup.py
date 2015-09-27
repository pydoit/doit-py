# -*- coding: utf-8 -*-

import sys
from setuptools import setup

install_requires = [
    'doit',
    'configclass',
    ]

if sys.version_info[0] < 3 or sys.version_info[1] < 4:
    install_requires.append('pathlib')

setup (
    name = 'doit-py',
    version = '0.4.0',
    author = 'Eduardo Naufel Schettino',
    author_email = 'schettino72@gmail.com',
    description = 'doit tasks for python stuff',
    url = 'http://pythonhosted.org/doit-py',
    keywords = ['doit',],
    platforms = ['any'],
    license = 'MIT',
    packages = ['doitpy'],
    install_requires = install_requires,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ]
)
