"""create task to upload project to PyPi

Example:
 - create a `MANIFEST` file with all tracked files in a git repo
 - upload an `sdist` package

::

    def task_pypi():
        pkg = PyPi()
        yield pkg.manifest_git()
        yield pkg.sdist_upload()

"""

class PyPi(object):
    """helper to create tasks to upload a python package to PyPi"""

    def __init__(self):
        self.revision_file = None


    def revision_git(self, file_name='revision.txt'):
        """create file with repo rev number"""
        cmd = "git rev-list --branches=master --max-count=1 HEAD > {}"
        self.revision_file = file_name
        return {
            'basename': 'pypi',
            'name': 'revision',
            'actions': [cmd.format(file_name)],
            'targets': [file_name],
            }


    def manifest_git(self):
        """create manifest file for distutils

        Put all files being tracked by git into the manifest
        """

        cmds = ["git ls-tree --name-only -r HEAD > MANIFEST"]
        file_dep = []
        if self.revision_file:
            file_dep.append(self.revision_file)
            cmds.append("echo '{}' >> MANIFEST".format(self.revision_file))
        return {
            'basename': 'pypi',
            'name': 'manifest',
            'actions': cmds,
            'file_dep': file_dep,
            'targets': ['MANIFEST'],
            }

    def sdist(self):
        """create sdist package"""
        return {
            'basename': 'pypi',
            'name': 'sdist',
            'actions': ["python setup.py sdist"],
            'file_dep': ['MANIFEST'],
            'verbosity': 2,
            }

    def sdist_upload(self):
        """upload sdist package to pypi"""
        return {
            'basename': 'pypi',
            'name': 'sdist_upload',
            'actions': ["python setup.py sdist upload"],
            'file_dep': ['MANIFEST'],
            'verbosity': 2,
            }
