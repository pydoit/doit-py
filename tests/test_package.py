from doitpy import package


class TestPackage(object):
    def test_revision_git(self):
        pkg = package.Package()
        task = pkg.revision_git()
        assert task['basename'] == 'package'
        assert task['name'] == 'revision'
        assert 'git rev-list' in task['actions'][0]
        assert pkg.revision_file == 'revision.txt'
        assert pkg.revision_file in task['actions'][0]
        assert task['targets'] == [pkg.revision_file]

    def test_manifest_git(self):
        task = package.Package().manifest_git()
        assert task['basename'] == 'package'
        assert task['name'] == 'manifest'
        assert len(task['actions']) == 1
        assert task['file_dep'] == []
        assert 'MANIFEST.in' in task['targets']

    def test_manifest_with_revision(self):
        pkg = package.Package()
        pkg.revision_git()
        task = pkg.manifest_git()
        assert task['basename'] == 'package'
        assert task['name'] == 'manifest'
        assert len(task['actions']) == 2
        assert task['file_dep'] == [pkg.revision_file]
        assert 'MANIFEST.in' in task['targets']
        assert pkg.revision_file in task['actions'][1]

    def test_sdist(self):
        task = package.Package().sdist()
        assert task['basename'] == 'package'
        assert task['name'] == 'sdist'
        assert task['actions'][0].endswith('sdist')
        assert task['file_dep'][0] == 'MANIFEST.in'

    def test_sdist_upload(self):
        task = package.Package().sdist_upload()
        assert task['basename'] == 'pypi'
        assert task['name'] == 'sdist_upload'
        assert 'sdist upload' in task['actions'][0]
        assert task['file_dep'][0] == 'MANIFEST.in'
