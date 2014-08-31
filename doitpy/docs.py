"""create tasks related to documentation generation

Example to create tasks to:
 - spell check all restructured text files (including README)
 - build sphinx docs in `doc` folder
 - upload built sphinx docs to `pythonhosted` using `setuptools`

::

    def task_docs():
        doc_files = glob.glob('doc/*.rst') + ['README.rst']
        yield docs.spell(doc_files, 'doc/dictionary.txt')
        yield docs.sphinx('doc/', 'doc/_build/html/', task_dep=['spell'])
        yield docs.pythonhosted_upload('doc/_build/html/', task_dep=['sphinx'])


"""

import subprocess

def check_no_output(doc_file, dictionary):
    """run spell checker on file

    spell always return successful code (0)
    so this checks if the output is empty
    """
    # -l list misspelled words
    # -p set path of personal dictionary
    cmd = 'hunspell -l -d en_US -p {} {}'.format(dictionary, doc_file)
    output = subprocess.check_output(cmd, shell=True,
                                     universal_newlines=True)

    if len(output) != 0:
        print(output)
        return False
    else:
        return True

# task creator
def spell(files, dictionary):
    """spell checker for doc files

    :param list-str files: list of files to spell check
    :param str dictionary: path of dictionary with extra words
    """
    for doc_file in files:
        yield {
            'basename': 'spell',
            'name': doc_file,
            'actions': [(check_no_output, (doc_file, dictionary))],
            'file_dep': [dictionary, doc_file],
            'verbosity': 2,
            }


# task creator
def sphinx(root_path, build_path, sphinx_opts='', task_dep=None):
    """build sphinx docs

    :param str root_path: root path of sphinx docs
    :param str build_path: path generated sphinx docs will be saved in
    :param str sphinx_opts: `sphinx-build` command line options
    :param list-str task_dep: list of tasks this task will depend on
    """
    cmd = "sphinx-build -b html {opts} -d {root}_build/doctrees {root} {build}"
    action = cmd.format(root=root_path, build=build_path, opts=sphinx_opts)
    # sphinx has its own check it up-to-date so we dont care
    # about always re-executing the task.
    task = {
        'basename': 'sphinx',
        'actions': [action],
        'verbosity': 2,
        }
    if task_dep:
        task['task_dep'] = task_dep
    yield task


# task creator
def pythonhosted_upload(www_path, task_dep):
    """deploy website (sphinx docs)

    :param str www_path: path to folder containig www files
    :param list-str task_dep: list of tasks this task will depend on
    """
    action = "python setup.py upload_docs --upload-dir %s"
    yield {
        'basename': 'pythonhosted_upload',
        'actions': [action % www_path],
        'task_dep': task_dep,
        'verbosity': 2,
        }
