from __future__ import absolute_import

from pathlib import Path
from pyflakes.scripts.pyflakes import checkPath

from .config import Config


def check_path(filename):
    """a doit action - execute pyflakes in a single file.
    @return (bool) check succeded
    """
    return not bool(checkPath(filename))


class Pyflakes(object):
    config = Config(exclude_patterns=[])

    def __init__(self, **kwargs):
        """
        @param exclude_patterns: (list - str) pathlib patterns to be excluded
        """
        self.config = self.config.make(kwargs)

    def __call__(self, py_file):
        """return task metadata to run pyflakes on a single module"""
        return {
            'name': py_file,
            'actions': [(check_path, [py_file])],
            'file_dep': [py_file],
            }

    def tasks(self, pattern, base_dir='.', exclude_path=()):
        """yield tasks as given by pattern

        @param pattern: (list - str) list of path patterns of files to be linted
        @param exclude: (list - str) list of path of files to be removed
                        from selection
        """

        # yield a task for every py file in selection
        base = Path(base_dir)
        excluded_path = set([base.joinpath(e) for e in exclude_path])
        for src in base.glob(pattern):
            if src in excluded_path:
                continue
            for exclude_pattern in self.config['exclude_patterns']:
                if src.match(exclude_pattern):
                    break
            else:
                yield self(str(src))
