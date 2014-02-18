from __future__ import absolute_import

from pathlib import Path
from pyflakes.scripts.pyflakes import checkPath


def check_path(filename):
    """a doit action - execute pyflakes in a single file.
    @return (bool) check succeded
    """
    return not bool(checkPath(filename))


class Pyflakes(object):
    EXCLUDE_PATTERNS = ( )

    def __init__(self, exclude_patterns=None):
        """
        @param exclude_patterns: (list - str) pathlib patterns to be excluded
        """
        if exclude_patterns is None:
            self.exclude_patterns = self.EXCLUDE_PATTERNS
        else:
            self.exclude_patterns = exclude_patterns


    def __call__(self, py_file):
        """return task metada to jshint single file"""
        return {
            'name': py_file,
            'actions': [(check_path, [py_file])],
            'file_dep': [py_file],
            }

    def tasks(self, pattern, exclude_path=()):
        """yield tasks as given by pattern

        @param pattern: (list - str) list of path patterns of files to be linted
        @param exclude: (list - str) list of path of files to be removed
                        from selection
        """

        # yield a task for every py file in selection
        base = Path('.')
        excluded_path = set([base.joinpath(e) for e in exclude_path])
        for src in base.glob(pattern):
            if src in excluded_path:
                break
            for exclude_pattern in self.exclude_patterns:
                if src.match(exclude_pattern):
                    break
            else:
                yield self(str(src))
