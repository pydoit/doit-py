from pathlib import Path

from doitpy import docs


SAMPLE_PATH = Path(__file__).parent / 'sample'

class TestSpell(object):

    def test_check_ok(self):
        assert docs.check_no_output(str(SAMPLE_PATH / 'flake_fail.py'),
                                    str(SAMPLE_PATH / 'dict.txt'))

    def test_check_fail(self):
        assert not docs.check_no_output(str(SAMPLE_PATH / 'flake_ok.py'),
                                        str(SAMPLE_PATH / 'dict.txt'))

    def test_spell_task(self):
        tasks = list(docs.spell(['a.txt', 'b.txt'], 'dict.txt'))
        assert len(tasks) == 2
        assert tasks[0]['name'] == 'a.txt'
        assert tasks[0]['file_dep'] == ['dict.txt', 'a.txt']

class TestSphinx(object):
    def test_sphinx(self):
        task = list(docs.sphinx('root', 'build', task_dep=['prep']))[0]
        assert task['basename'] == 'sphinx'
        assert task['task_dep'] == ['prep']

class TestPythonHosted(object):
    def test_upload(self):
        task = list(docs.pythonhosted_upload('www', task_dep=['build']))[0]
        assert task['basename'] == 'pythonhosted_upload'
        assert task['task_dep'] == ['build']
