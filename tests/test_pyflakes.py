from pathlib import Path

from doitpy import pyflakes


TEST_PATH = Path(__file__).parent

class TestCheckPath(object):
    def test_success(self):
        assert pyflakes.check_path(str(TEST_PATH / 'sample/flake_ok.py'))
    def test_failure(self):
        assert not pyflakes.check_path(str(TEST_PATH / 'sample/flake_fail.py'))

class TestPyflakes(object):
    def test_init(self):
        obj = pyflakes.Pyflakes()
        assert obj.config['exclude_patterns'] == []
        obj = pyflakes.Pyflakes(exclude_patterns=['.#*'])
        assert obj.config['exclude_patterns'] == ['.#*']

    def test_call(self):
        obj = pyflakes.Pyflakes()
        task_dict = obj('my_module.py')
        assert task_dict['file_dep'] == ['my_module.py']

    def test_tasks(self):
        exclude_pattern = 'tests/*'
        check_pattern = '**/*.py'
        exclude_path = 'flake_fail.py'
        base_dir = TEST_PATH / 'sample'
        obj = pyflakes.Pyflakes(base_dir=base_dir,
                                exclude_patterns=[exclude_pattern])
        tasks = list(obj.tasks(check_pattern, exclude_paths=[exclude_path]))
        assert len(tasks) == 2
        names = [t['name'] for t in tasks]
        assert str(base_dir / 'flake_ok.py') in names
        assert str(base_dir / 'flake_compat.py') in names
