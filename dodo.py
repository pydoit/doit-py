import glob
import subprocess

from doitpy.pyflakes import Pyflakes
from doitpy.coverage import PythonPackage, Coverage
from doitpy.package import Package
from doitpy import docs


DOIT_CONFIG = {'default_tasks': ['pyflakes', 'test']}


def task_pyflakes():
    flakes = Pyflakes()
    yield flakes.tasks('*.py')
    yield flakes.tasks('doitpy/*.py')
    yield flakes.tasks('tests/**/*.py',
                       exclude_paths=['tests/sample/flake_fail.py',])


def task_test():
    """run unit-tests"""
    # XXX
    return {'actions': ['py.test tests']}

def task_coverage():
    cov = Coverage([PythonPackage('doitpy', test_path='tests')],
                   config={'branch':False})
    yield cov.all()
    yield cov.src()
    yield cov.by_module()


def task_package():
    """upload package to pypi"""
    pkg = Package()
    yield pkg.manifest_git()
    yield pkg.sdist()
    yield pkg.sdist_upload()


def task_docs():
    doc_files = glob.glob('doc/*.rst') + ['README.rst']
    yield docs.spell(doc_files, 'doc/dictionary.txt')
    yield docs.sphinx('doc/', 'doc/_build/html/', task_dep=['spell'])
    yield docs.pythonhosted_upload('doc/_build/html/', task_dep=['sphinx'])



##########################
from doit.tools import result_dep

init_file = 'doitpy/__init__.py'

def task_version():
    """update version on <pkg-name>/__init__.py and doc/conf.py"""
    # get package version from setup.py
    # version must be set with a string literal using single/double quotes
    # but not triple-quotes.
    def version_str2tuple(string):
        parts = []
        for part in string.split('.'):
            parts.append(part if not part.isdigit() else int(part))
        return tuple(repr(x) for x in parts)
    def get_version():
        #cmd = ("""awk 'match($0, /version[[:space:]]*=[[:space:]]*"""
        #       r"""['\''"](.*)['\''"].*/, ary) {print ary[1]}' setup.py""")
        cmd = 'python setup.py --version'
        version_str = subprocess.check_output(cmd, shell=True,
                                              universal_newlines=True)
        version_str = version_str.strip()
        version_tuple = version_str2tuple(version_str)
        return {
            'version': '.'.join(version_tuple[:2]),
            'release': version_str,
            'tuple': version_tuple,
            }

    yield {
        'name': 'get_from_setup',
        'file_dep': ['setup.py'],
        'actions': [get_version],
        }

    sed = "sed --in-place --regexp-extended "
    yield {
        'name': 'set_pkg',
        'uptodate': [result_dep('version:get_from_setup')],
        'getargs': {'version': ('version:get_from_setup', 'tuple')},
        'actions': [
            sed + r"'s/(__version__ = )(.*)/\1%(version)s/' " + init_file],
        'targets': [init_file]
        }

    doc_file = 'doc/conf.py'
    yield {
        'name': 'set_doc',
        'uptodate': [result_dep('version:get_from_setup')],
        'getargs': {
            'version': ('version:get_from_setup', 'version'),
            'release': ('version:get_from_setup', 'release')},
        'actions': [
            sed + r""" "s/(version = )(.*)/\1'%(version)s'/" """ + doc_file,
            sed + r""" "s/(release = )(.*)/\1'%(release)s'/" """ + doc_file,
            ]
        }
