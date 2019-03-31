import os, setuptools, sys
from setuptools.command.test import test as TestCommand


# From here: http://pytest.org/2.2.4/goodpractises.html
class RunTests(TestCommand):
    DIRECTORY = 'test'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [self.DIRECTORY]
        self.test_suite = True

    def run_tests(self):
        # Import here, because outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        if errno:
            raise SystemExit(errno)


class RunCoverage(RunTests):
    def run_tests(self):
        import coverage
        cov = coverage.Coverage(config_file=True)

        cov.start()
        super().run_tests()
        cov.stop()

        cov.report(file=sys.stdout)
        coverage = cov.html_report(directory='htmlcov')
        fail_under = cov.get_option('report:fail_under')
        if coverage < fail_under:
            print('ERROR: coverage %.2f%% was less than fail_under=%s%%' % (
                  coverage, fail_under))
            raise SystemExit(1)


NAME = 'nc'
OWNER = 'timedata-org'

VERSION_FILE = os.path.join(os.path.dirname(__file__), NAME, 'VERSION')
VERSION = open(VERSION_FILE).read().strip()

URL = 'http://github.com/{OWNER}/{NAME}'.format(**locals())
DOWNLOAD_URL = '{URL}/archive/{VERSION}.tar.gz'.format(**locals())

INSTALL_REQUIRES = open('requirements.txt').read().splitlines()
TESTS_REQUIRE = open('test_requirements.txt').read().splitlines()

PACKAGES = setuptools.find_packages(exclude=['test'])
CMDCLASS = {
    'coverage': RunCoverage,
    'test': RunTests,
}

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

SETUPTOOLS_VERSION = '18.5'
SETUPTOOLS_ERROR = """

Your version of setuptools is %s but this needs version %s or greater.

Please type:

    pip install -U setuptools pip

and then try again.
"""

sversion = setuptools.version.__version__
if sversion < SETUPTOOLS_VERSION:
    raise ValueError(SETUPTOOLS_ERROR % (sversion, SETUPTOOLS_VERSION))

setuptools.setup(
    name=NAME,
    version=VERSION,
    description='Named colors in Python',
    long_description=open('README.rst').read(),
    author='Tom Ritchford',
    author_email='tom@swirly.com',
    url=URL,
    download_url=DOWNLOAD_URL,
    license='MIT',
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    tests_require=TESTS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    cmdclass=CMDCLASS,
    include_package_data=True,
)
