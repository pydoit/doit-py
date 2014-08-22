import glob
import subprocess

from doitpy.pyflakes import Pyflakes
from doitpy.coverage import PythonPackage, Coverage
from doitpy.pypi import PyPi


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



def task_pypi():
    """upload package to pypi"""
    yield PyPi().git_manifest()
    yield PyPi().sdist_upload()


def task_website():
    """deploy website (sphinx docs)"""
    action = "python setup.py upload_docs --upload-dir %s"
    return {'actions': [action % DOC_BUILD_PATH],
            'task_dep': ['sphinx'],
            'verbosity': 2,
            }


##########################
from doit.tools import result_dep

init_file = 'doitpy/__init__.py'

def task_version():
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
