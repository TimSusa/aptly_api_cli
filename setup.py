try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name='Aptly-Api-Cli',
    version='0.1',
    url='https://github.com/TimSusa/aptly_api_cli',
    license='MIT',
    keywords="aptly aptly-server debian",
    author='Tim Susa',
    author_email='timsusa@gmx.de',
    description='This cli executes remote calls to the Aptly server, without blocking the Aptly database.',
    long_description=__doc__,
    # packages=find_packages(),
    package_dir={'aptly_cli': 'aptly_cli'},
    packages=['aptly_cli', 'aptly_cli.api', 'aptly_cli.cli', 'aptly_cli.util'],
    # py_modules=['aptly_cli.api.api', 'cli'],
    entry_points={
        'console_scripts': [
            'aptly-cli=aptly_cli.cli.cli:main'
        ]
    },
    # data_files=[
    #     ('supervisor', ['contrib/rest-api.sv.conf']),
    # ],
    package_data={
        'configs': [
            'aptly-cli.conf',
        ],
    },
    platforms='any'
)
