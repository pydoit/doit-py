"""
Helper to create tasks that execute pyflakes.


Example to create a task for every python module (found recursively from current
path), excluding test modules and also `doc/conf.py`.

::

    from doitpy.pyflakes import Pyflakes

    def task_pyflakes():
        flaker = Pyflakes(exclude_patterns=['test_*'])
        yield flaker.tasks('**/*.py', exclude_paths=['doc/conf.py'])


"""

from __future__ import absolute_import

from pathlib import Path
from pyflakes.api import checkPath
from pyflakes.checker import Checker

from configclass import Config


def check_path(filename):
    """a doit action - execute pyflakes in a single file.
    :return bool: check succeded
    """
    return not bool(checkPath(filename))


class Pyflakes(object):
    """generate tasks for pyflakes
    """

    #: :class:`confclass.Config`
    #:
    #: :var str base_dir: list of path patterns of files to be linted
    #: :var list-str exclude_patterns: list of pattern of files to be removed
    #:                                from selection
    #: :var list-str exclude_paths: list of path of files to be removed
    #:                             from selection
    config = Config(
        base_dir='.',
        exclude_patterns=[],
        exclude_paths=[],
        )


    def __init__(self, **kwargs):
        """:param kwargs: config params
        """
        self.config = self.config.make(kwargs)


    def __call__(self, py_file):
        """Return a task for single file.

        :param str pyfile: path to file
        :return: task metadata to run pyflakes on a single module
        """
        # 'unicode' is a builtin in py2 but not on py3.
        # Make sure pyflakes consider 'unicode' as a builtin so
        # it does not fail on py3.
        Checker.builtIns.add('unicode')
        return {
            'name': py_file,
            'actions': [(check_path, [py_file])],
            'file_dep': [py_file],
            }

    def tasks(self, pattern, **kwargs):
        """run pyflakes on python module

        yield one task for each file as given by pattern

        :param str pattern: path pattern of files to be linted
        """

        config = self.config.make(**kwargs)
        # yield a task for every py file in selection
        base = Path(config['base_dir'])
        excluded = set([base.joinpath(e) for e in config['exclude_paths']])
        for src in base.glob(pattern):
            if src in excluded:
                continue
            for exclude_pattern in config['exclude_patterns']:
                if src.match(exclude_pattern):
                    break
            else:
                yield self(str(src))
