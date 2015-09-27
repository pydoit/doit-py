from pathlib import Path

from configclass import Config
from doitpy.coverage import PythonModule, PythonPackage, Coverage


TEST_PATH = Path(__file__).parent
SAMPLE = TEST_PATH / 'sample' # path to sample project

class TestPythonPackage(object):
    def test_init_tests_in_package(self):
        pkg = PythonPackage(SAMPLE)
        assert pkg.test_dir == str(SAMPLE / 'tests')
        assert len(pkg.src) == 3
        assert str(SAMPLE / 'flake_ok.py') in pkg.src
        assert str(SAMPLE / 'flake_fail.py') in pkg.src
        assert len(pkg.test) == 1
        assert str(SAMPLE / 'tests/test_flake_ok.py') in pkg.test

    def test_init_test_path(self):
        pkg = PythonPackage(SAMPLE,
                            test_path=str(TEST_PATH/'test2'))
        assert pkg.test_dir == str(TEST_PATH / 'test2')

    def test_all_modules(self):
        pkg = PythonPackage(SAMPLE)
        all_modules = list(pkg.all_modules())
        assert len(all_modules) == 4
        assert str(SAMPLE / 'flake_fail.py') in all_modules



class TestCoverage(object):
    def test_init_pkg_instance(self):
        cov = Coverage([PythonPackage(SAMPLE)])
        assert len(cov.pkgs) == 1
        assert cov.pkgs[0].src_dir == str(SAMPLE)

    def test_cover_all(self):
        pkg = PythonPackage(SAMPLE)
        cov = Coverage([pkg])
        task = list(cov.all('my_cov'))[0]
        assert task['verbosity'] == 2
        assert task['basename'] == 'my_cov'
        assert task['actions'] == [
            'coverage run --branch `which py.test`',
            'coverage report --show-missing {}'.format(
                ' '.join(pkg.all_modules()))
            ]

    def test_all_module(self):
        pkg = PythonModule(str(SAMPLE / 'flake_ok.py'),
                           str(SAMPLE / 'tests/test_flake_ok.py'))
        cov = Coverage([pkg])
        task = list(cov.all('my_cov'))[0]
        assert task['verbosity'] == 2
        assert task['basename'] == 'my_cov'
        assert task['actions'] == [
            'coverage run --branch `which py.test`',
            'coverage report --show-missing {}'.format(
                ' '.join(pkg.all_modules()))
            ]

    def test_cover_all_parallel(self):
        pkg = PythonPackage(SAMPLE)
        cov = Coverage([pkg], config=Config(parallel=True, branch=False,
                                            omit=['abc']))
        task = list(cov.all('my_cov'))[0]
        assert task['verbosity'] == 2
        assert task['basename'] == 'my_cov'
        assert task['actions'] == [
            'coverage run --parallel-mode `which py.test`',
            'coverage combine',
            'coverage report --show-missing --omit abc {}'.format(
                ' '.join(pkg.all_modules()))
            ]

    def test_cover_all_multiprocessing(self):
        pkg = PythonPackage(SAMPLE)
        cov = Coverage([pkg], config=Config(concurrency='multiprocessing'))
        task = list(cov.all('my_cov'))[0]
        assert task['verbosity'] == 2
        assert task['basename'] == 'my_cov'
        assert task['actions'] == [
            'coverage run --branch --concurrency multiprocessing `which py.test`',
            'coverage report --show-missing {}'.format(
                ' '.join(pkg.all_modules()))
            ]


    def test_cover_src(self):
        pkg = PythonPackage(SAMPLE)
        cov = Coverage([pkg])
        task = list(cov.src('my_cov'))[0]
        assert task['verbosity'] == 2
        assert task['basename'] == 'my_cov'
        assert task['actions'] == [
            'coverage run --branch `which py.test`',
            'coverage report --show-missing {}'.format(' '.join(pkg.src))
            ]


    def test_cover_module(self):
        pkg = PythonPackage(SAMPLE)
        cov = Coverage([pkg])
        tasks = list(cov.by_module('my_cov'))
        assert len(tasks) == 1
        task = tasks[0]
        assert task['verbosity'] == 2
        assert task['basename'] == 'my_cov'
        src = pkg.src_dir + '/flake_ok.py'
        test = pkg.src_dir + '/tests/test_flake_ok.py'
        assert task['actions'] == [
            'coverage run --branch `which py.test` {}'.format(test),
            'coverage report --show-missing {}'.format(' '.join([src, test]))
            ]
