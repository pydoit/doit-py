from doitpy.pyflakes import Pyflakes
from doitpy.coverage import PythonPackage, Coverage


DOIT_CONFIG = {'default_tasks': ['pyflakes']}


def task_pyflakes():
    exclude = ['tests/sample/flake_fail.py', 'doc/conf.py']
    yield Pyflakes().tasks('**/*.py', exclude_path=exclude)


def task_coverage():
    cov = Coverage([PythonPackage('doitpy', test_path='tests')])
    yield cov.all()
    yield cov.src()
    yield cov.by_module()
