from doitpy.pyflakes import Pyflakes
from doitpy.coverage import Coverage


DOIT_CONFIG = {'default_tasks': ['pyflakes']}


def task_pyflakes():
    yield Pyflakes().tasks('**/*.py', exclude_path=['sample_fail.py'])


def task_coverage():
    cov = Coverage(source='doitpy', test='test')
    yield cov.all()
    yield cov.src()
    yield cov.by_module()

