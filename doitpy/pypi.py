

class PyPi(object):
    """helper to create tasks to upload a python package to PyPi"""

    def __init__(self, name=None):
        self.name = name + '-' if name else ''

    def git_manifest(self):
        """create manifest file for distutils

        Put all files being tracked by git into the manifest
        """

        cmd = "git ls-tree --name-only -r HEAD > MANIFEST"
        return {
            'basename': 'pypi',
            'name': self.name + 'manifest',
            'actions': [cmd],
            }


    def sdist_upload(self):
        """upload sdist package to pypi"""
        return {
            'basename': 'pypi',
            'name': self.name + 'sdist_upload',
            'actions': ["python setup.py sdist upload"],
            'task_dep': [ 'pypi:' + self.name + 'manifest'],
            'verbosity': 2,
            }
