from doitpy import pypi


class TestPyPi(object):
    def test_revision_git(self):
        pkg = pypi.PyPi()
        task = pkg.revision_git()
        assert task['basename'] == 'pypi'
        assert task['name'] == 'revision'
        assert 'git rev-list' in task['actions'][0]
        assert pkg.revision_file == 'revision.txt'
        assert pkg.revision_file in task['actions'][0]
        assert task['targets'] == [pkg.revision_file]

    def test_manifest_git(self):
        task = pypi.PyPi().manifest_git()
        assert task['basename'] == 'pypi'
        assert task['name'] == 'manifest'
        assert len(task['actions']) == 1
        assert task['file_dep'] == []
        assert 'git ls-tree' in task['actions'][0]
        assert 'MANIFEST' in task['actions'][0]

    def test_manifest_with_revision(self):
        pkg = pypi.PyPi()
        pkg.revision_git()
        task = pkg.manifest_git()
        assert task['basename'] == 'pypi'
        assert task['name'] == 'manifest'
        assert len(task['actions']) == 2
        assert task['file_dep'] == [pkg.revision_file]
        assert 'git ls-tree' in task['actions'][0]
        assert 'MANIFEST' in task['actions'][0]
        assert pkg.revision_file in task['actions'][1]

    def test_sdist(self):
        task = pypi.PyPi().sdist()
        assert task['basename'] == 'pypi'
        assert task['name'] == 'sdist'
        assert task['actions'][0].endswith('sdist')
        assert task['file_dep'][0] == 'MANIFEST'

    def test_sdist_upload(self):
        task = pypi.PyPi().sdist_upload()
        assert task['basename'] == 'pypi'
        assert task['name'] == 'sdist_upload'
        assert 'sdist upload' in task['actions'][0]
        assert task['file_dep'][0] == 'MANIFEST'
