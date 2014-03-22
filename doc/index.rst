.. doit-py documentation master file, created by
   sphinx-quickstart on Fri Mar 14 06:23:05 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
doit-py -  documentation
===================================


Intro
=========

`doit`_ tasks for python stuff

.. _doit: http://pydoit.org

Include tasks for:

- pyflakes
- coverage


Project Details
==================

 - Source code & Project management on github - https://github.com/pydoit/doit-py
 - Website & docs - http://packages.python.org/doit-py
 - Discussion group - https://groups.google.com/forum/#!forum/python-doit
 - `MIT license <http://opensource.org/licenses/mit-license.php>`_


module: pyflakes
==================

.. automodule:: doitpy.pyflakes

.. autoclass:: doitpy.pyflakes.Pyflakes
   :members: __init__, __call__, tasks
   :member-order: bysource

   .. autoattribute:: doitpy.pyflakes.Pyflakes.config


module: coverage
==================

.. automodule:: doitpy.coverage

.. autoclass:: doitpy.coverage.PythonPackage
   :members: __init__, all_modules
   :member-order: bysource

   .. autoattribute:: doitpy.coverage.PythonPackage.config


.. autoclass:: doitpy.coverage.Coverage
   :members: __init__, all, src, by_module
   :member-order: bysource

   .. autoattribute:: doitpy.coverage.Coverage.config


configuration
===============

.. autoclass:: confclass.Config
   :show-inheritance:
   :members: make




.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

