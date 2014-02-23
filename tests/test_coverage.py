from pathlib import Path

from doitpy.coverage import PythonPackage, Coverage

TEST_PATH = Path(__file__).parent


class TestPythonPackage(object):
    def test_init_tests_in_package(self):
        pkg = PythonPackage(TEST_PATH / 'sample')
        assert pkg.test_base == str(TEST_PATH / 'sample/tests')
        assert len(pkg.src) == 2
        assert str(TEST_PATH / 'sample/flake_ok.py') in pkg.src
        assert str(TEST_PATH / 'sample/flake_fail.py') in pkg.src
        assert len(pkg.test) == 1
        assert str(TEST_PATH / 'sample/tests/test_flake_ok.py') in pkg.test
        assert pkg.test == pkg.test_files

    def test_init_test_path(self):
        pkg = PythonPackage(TEST_PATH / 'sample',
                            test_path=str(TEST_PATH/'test2'))
        assert pkg.test_base == str(TEST_PATH / 'test2')

    def test_all_modules(self):
        pkg = PythonPackage(TEST_PATH / 'sample')
        all_modules = list(pkg.all_modules())
        assert len(all_modules) == 3
        assert str(TEST_PATH / 'sample/flake_fail.py') in all_modules
