"""
create tasks for coverage.py

 * test files must be named in format 'test_xxx.py'
 * packages does not contain sub-packages
"""
import glob

from .config import Config


class PythonPackage(object):
    # TODO should track sub-packages
    TEST_PREFIX = 'test_'

    def __init__(self, name, test_path=None):
        """if test_path is not given assume it is 'tests' inside source package"""
        self.name = name
        self.src_base = name if name else ''
        if test_path is None:
            self.test_base = '{}/tests'.format(self.src_base)
        else:
            self.test_base = test_path
        self.src = glob.glob("{}/*.py".format(self.src_base))
        self.test = glob.glob("{}/*.py".format(self.test_base))
        self.test_files = glob.glob("{}/{}*.py".format(
                self.test_base, self.TEST_PREFIX))

    def all_modules(self):
        for mod in self.src + self.test:
            yield mod


class Coverage(object):
    """python code coverage"""
    config = Config(
        cmd_run_test = "`which py.test`",
        branch=True,
        parallel=False,
        omit=[])

    def __init__(self, pkgs, config=None):
        self.config = self.config.make(config)
        self.pkgs = []
        for pkg in pkgs:
            if isinstance(pkg, PythonPackage):
                self.pkgs.append(pkg)
            else:
                self.pkgs.append(PythonPackage(pkg))


    def _action_list(self, modules, test=''):
        run_options = ''
        if self.config['branch']:
            run_options += '--branch '
        if self.config['parallel']:
            run_options += '--parallel-mode '

        report_options = ''
        if self.config['omit']:
            report_options += '--omit {}'.format(','.join(self.config['omit']))

        actions = ["coverage run {} {} {}".format(
                run_options, self.config['cmd_run_test'], test)]
        if self.config['parallel']:
            actions.append('coverage combine')
        actions.append("coverage report --show-missing {} {}".format(
                report_options, " ".join(modules)))
        return actions


    def all(self):
        """show coverage for all modules including tests"""
        all_modules = []

        for pkg in self.pkgs:
            for module in pkg.all_modules():
                all_modules.append(module)

        yield {
            'basename': 'coverage',
            'actions': self._action_list(all_modules),
            'verbosity': 2}


    def src(self):
        """show coverage for all modules (exclude tests)"""
        all_modules = []

        for pkg in self.pkgs:
            for module in pkg.src:
                all_modules.append(module)

        yield {
            'basename': 'coverage_src',
            'actions': self._action_list(all_modules),
            'verbosity': 2,
            }


    def by_module(self):
        """show coverage for individual modules"""
        for pkg in self.pkgs:
            to_strip = len('{}/{}'.format(pkg.test_base, pkg.TEST_PREFIX))
            tests = glob.glob('{}/{}*.py'.format(pkg.test_base, pkg.TEST_PREFIX))
            for test in tests:
                source = pkg.src_base + '/' + test[to_strip:]
                yield {
                    'basename': 'coverage_module',
                    'name': test,
                    'actions': self._action_list([source, test], test),
                    'verbosity': 2,
                    }

