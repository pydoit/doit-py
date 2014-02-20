import glob

class Coverage(object):
    """python code coverage"""
    TEST_MOD_PREFIX = 'test_' # FIXME use this
    # TODO handle more than one package
    # TODO handle package with sub-packages

    def __init__(self, source, test):
        self.source_dir = source
        self.test_dir = test

    def all(self):
        """show coverage for all modules including tests"""
        all_modules = []
        sources = glob.glob(self.source_dir + "/*.py")
        tests = glob.glob(self.test_dir + "/test_*.py")

        for module in sources + tests:
            all_modules.append(module)

        yield {
            'basename': 'coverage',
            'actions':[
                "coverage run --branch `which py.test`",
                "coverage report --show-missing %s" % " ".join(all_modules),
                ],
            'verbosity': 2}


    def src(self):
        """show coverage for all modules (exclude tests)"""
        all_modules = []
        sources = glob.glob(self.source_dir + "/*.py")

        for module in sources:
            all_modules.append(module)

        yield {
            'basename': 'cov_code',
            'actions':[
                "coverage run --branch `which py.test`",
                "coverage report --show-missing %s" % " ".join(all_modules),
                ],
            'verbosity': 2}


    def by_module(self):
        """show coverage for individual modules"""
        to_strip = len(self.test_dir + '/test_')
        tests = glob.glob(self.test_dir + "/test_*.py")
        for test in tests:
            source = self.source_dir + '/' + test[to_strip:]
            yield {
                'basename': 'cov_module',
                'name': test,
                'actions':
                    ["coverage run --branch `which py.test` -v %s" % test,
                     "coverage report --show-missing %s %s" % (source, test)],
                'verbosity': 2}

