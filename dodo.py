from doitpy.pyflakes import Pyflakes
from doitpy.coverage import PythonPackage, Coverage


DOIT_CONFIG = {'default_tasks': ['pyflakes']}


def task_pyflakes():
    yield Pyflakes().tasks('**/*.py', exclude_path=['tests/sample_fail.py'])


def task_coverage():
    cov = Coverage([PythonPackage('doitpy', test_path='tests')],
                   omit=['"tests/sample_*"'])
    yield cov.all()
    yield cov.src()
    yield cov.by_module()
