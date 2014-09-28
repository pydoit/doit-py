"""tasks to create python distribution packages (distutils/setuptools)

Example:
 - create a `MANIFEST.in` file with all tracked files in a git repo
 - upload an `sdist` package

::

    from doitpy.package import Package

    def task_package():
        pkg = Package()
        yield pkg.manifest_git()  # package:manifest
        yield pkg.sdist()         # package:sdist
        yield pkg.sdist_upload()  # pypi:sdist_upload

"""

import subprocess


class Package(object):
    """helper to create tasks to upload a python package to PyPi"""

    def __init__(self):
        self.revision_file = None


    def revision_git(self, file_name='revision.txt'):
        """create file with repo rev number"""
        cmd = "git rev-list --branches=master --max-count=1 HEAD > {}"
        self.revision_file = file_name
        return {
            'basename': 'package',
            'name': 'revision',
            'actions': [cmd.format(file_name)],
            'targets': [file_name],
            }

    def _create_manifest_git(self):
        cmd = "git ls-tree --name-only -r HEAD"
        file_list = subprocess.check_output(cmd, shell=True, )
        with open('MANIFEST.in', 'w') as manifest:
            for filename in file_list.decode('utf-8').splitlines():
                manifest.write('include {}\n'.format(filename))


    def manifest_git(self):
        """create MANIFEST.in file for distutils/setuptools

        Put all files being tracked by git into the manifest
        """
        actions = [self._create_manifest_git]
        file_dep = []
        if self.revision_file:
            file_dep.append(self.revision_file)
            cmd = "echo 'include {}' >> MANIFEST.in"
            actions.append(cmd.format(self.revision_file))
        return {
            'basename': 'package',
            'name': 'manifest',
            'actions': actions,
            'file_dep': file_dep,
            'targets': ['MANIFEST.in'],
            'uptodate': [False],
            }

    def sdist(self):
        """create sdist package"""
        return {
            'basename': 'package',
            'name': 'sdist',
            'actions': ["python setup.py sdist"],
            'file_dep': ['MANIFEST.in'],
            'uptodate': [False],
            'verbosity': 2,
            }

    def sdist_upload(self):
        """upload sdist package to pypi"""
        return {
            'basename': 'pypi',
            'name': 'sdist_upload',
            'actions': ["python setup.py sdist upload"],
            'file_dep': ['MANIFEST.in', 'setup.py'],
            'verbosity': 2,
            }
