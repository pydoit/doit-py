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

    :param files list-str: list of files to spell check
    :param dictionary str: path of dictionary with extra words
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
def sphinx(root_path, build_path, task_dep=None):
    """build sphinx docs"""
    cmd = "sphinx-build -b html -d %s_build/doctrees %s %s"
    action = cmd % (root_path, root_path, build_path)
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

    :param www_path str: path to folder containig www files
    :param task_dep list-str: name of task that build the docs
    """
    action = "python setup.py upload_docs --upload-dir %s"
    yield {
        'basename': 'pythonhosted_upload',
        'actions': [action % www_path],
        'task_dep': task_dep,
        'verbosity': 2,
        }
