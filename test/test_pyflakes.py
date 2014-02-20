import os

from doitpy import pyflakes


TEST_PATH = os.path.dirname(__file__)

class TestCheckPath(object):
    def test_success(self):
        assert pyflakes.check_path('{}/sample_ok.py'.format(TEST_PATH))
    def test_failure(self):
        assert not pyflakes.check_path('{}/sample_fail.py'.format(TEST_PATH))

class TestPyflakes(object):
    def test_init(self):
        obj = pyflakes.Pyflakes()
        assert obj.exclude_patterns == ()
        obj = pyflakes.Pyflakes(['.#*'])
        assert obj.exclude_patterns == ['.#*']

    def test_call(self):
        obj = pyflakes.Pyflakes()
        task_dict = obj('my_module.py')
        assert task_dict['file_dep'] == ['my_module.py']

    def test_tasks(self):
        exclude_pattern = 'test_*'
        check_pattern = '*.py'
        exclude_path = 'sample_fail.py'
        obj = pyflakes.Pyflakes([exclude_pattern])
        tasks = list(obj.tasks(check_pattern, TEST_PATH, [exclude_path]))
        assert len(tasks) == 1
        assert tasks[0]['name'] == '{}/sample_ok.py'.format(TEST_PATH)
