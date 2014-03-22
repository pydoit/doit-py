import glob
import subprocess

from doitpy.pyflakes import Pyflakes
from doitpy.coverage import PythonPackage, Coverage


DOIT_CONFIG = {'default_tasks': ['pyflakes']}


def task_pyflakes():
    exclude = ['tests/sample/flake_fail.py', 'doc/conf.py']
    yield Pyflakes().tasks('**/*.py', exclude_paths=exclude)


def task_coverage():
    cov = Coverage([PythonPackage('doitpy', test_path='tests')])
    yield cov.all()
    yield cov.src()
    yield cov.by_module()




#### docs


def task_spell():
    """spell checker for doc files"""
    # spell always return successful code (0)
    # so this checks if the output is empty
    def check_no_output(doc_file):
        # -l list misspelled words
        # -p set path of personal dictionary
        cmd = 'hunspell -l -d en_US -p doc/dictionary.txt %s'
        output = subprocess.check_output(cmd % doc_file, shell=True,
                                         universal_newlines=True)
        if len(output) != 0:
            print(output)
            return False

    for doc_file in glob.glob('doc/*.rst') + ['README.rst']:
        yield {
            'name': doc_file,
            'actions': [(check_no_output, (doc_file,))],
            'file_dep': ['doc/dictionary.txt', doc_file],
            'verbosity': 2,
            }


DOC_ROOT = 'doc/'
DOC_BUILD_PATH = DOC_ROOT + '_build/html/'
def task_sphinx():
    """generate docs"""
    action = "sphinx-build -b html -d %s_build/doctrees %s %s"
    return {
        'actions': [action % (DOC_ROOT, DOC_ROOT, DOC_BUILD_PATH)],
        'verbosity': 2,
        'task_dep': ['spell'],
        }

