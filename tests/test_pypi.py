from doitpy import pypi


class TestPyPi(object):
    def test_git_manifest(self):
        task = pypi.PyPi('abc').git_manifest()
        assert task['basename'] == 'pypi'
        assert task['name'] == 'abc-manifest'
        assert 'git' in task['actions'][0]
        assert 'MANIFEST' in task['actions'][0]

    def test_sdist_upload(self):
        task = pypi.PyPi('abc').sdist_upload()
        assert task['basename'] == 'pypi'
        assert task['name'] == 'abc-sdist_upload'
        assert 'sdist upload' in task['actions'][0]
        assert task['task_dep'][0] == 'pypi:abc-manifest'
