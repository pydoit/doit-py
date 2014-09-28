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



Project Details
==================

 - Source code & Project management on github - https://github.com/pydoit/doit-py
 - Website & docs - http://pythonhosted.org/doit-py
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

.. autoclass:: doitpy.coverage.PythonModule
   :members: __init__
   :member-order: bysource


.. autoclass:: doitpy.coverage.PythonPackage
   :members: __init__, all_modules
   :member-order: bysource

   .. autoattribute:: doitpy.coverage.PythonPackage.config


.. autoclass:: doitpy.coverage.Coverage
   :members: __init__, all, src, by_module
   :member-order: bysource

   .. autoattribute:: doitpy.coverage.Coverage.config



module: docs
==================

.. automodule:: doitpy.docs

.. autofunction:: doitpy.docs.spell

.. autofunction:: doitpy.docs.sphinx

.. autofunction:: doitpy.docs.pythonhosted_upload


module: package
==================

.. automodule:: doitpy.package

.. autoclass:: doitpy.package.Package
   :members: __init__, revision_git, manifest_git, sdist, sdist_upload
   :member-order: bysource
