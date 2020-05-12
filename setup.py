import os

NAME = 'nc'
OWNER = 'rec'

VERSION_FILE = os.path.join(os.path.dirname(__file__), NAME, 'VERSION')
VERSION = open(VERSION_FILE).read().strip()

URL = 'http://github.com/{OWNER}/{NAME}'.format(**locals())
DOWNLOAD_URL = '{URL}/archive/{VERSION}.tar.gz'.format(**locals())

INSTALL_REQUIRES = open('requirements.txt').read().splitlines()
TESTS_REQUIRE = open('test_requirements.txt').read().splitlines()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
]

if __name__ == '__main__':
    import setuptools

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
        packages=['nc'],
        classifiers=CLASSIFIERS,
        tests_require=TESTS_REQUIRE,
        install_requires=INSTALL_REQUIRES,
        include_package_data=True,
        scripts=['scripts/pync'],
    )
