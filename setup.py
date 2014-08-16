# -*- coding: utf-8 -*-

from setuptools import setup

setup (
    name = 'doit-py',
    version = '0.2.dev1',
    author = 'Eduardo Naufel Schettino',
    author_email = 'schettino72@gmail.com',
    description = 'doit tasks for python stuff',
    url = 'http://pythonhosted.org/doit-py',
    keywords = ['doit',],
    platforms = ['any'],
    license = 'MIT',
    packages = ['doitpy'],
    install_requires = [
        'pathlib',
        'doit',
        'configclass',
        ],
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
        'Topic :: Software Development :: Libraries',
    ]
)
