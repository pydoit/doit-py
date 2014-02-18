from doitpy.pyflakes import Pyflakes

def task_pyflakes():
    yield Pyflakes().tasks('**/*.py')
