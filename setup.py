# -*- coding: utf-8 -*-

from setuptools import setup

install_requires = [
    'doit',
    'configclass',
    ]

setup (
    name = 'doit-py',
    version = '0.5.0',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ]
)
