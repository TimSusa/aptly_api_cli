try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name='Aptly-Api-Cli',
    version='0.1',
    url='https://github.com/TimSusa/aptly_api_cli',
    license='MIT',
    keywords = "aptly aptly-server debian",
    author='Tim Susa',
    author_email='timsusa@gmx.de',
    description='This python command line interface, executes remote calls to the Aptly server, without blocking the Aptly database.',
    long_description=__doc__,
    packages=find_packages(),
    py_modules=['aptly_api_cli', 'aptly_cli'],
    entry_points={
        'console_scripts': [
            'aptly-cli=aptly_cli.cli.cli:main'
        ]
    },
    # data_files=[
    #     ('supervisor', ['contrib/rest-api.sv.conf']),
    # ],
    # package_data={
    #     'configs': [
    #         'cluster/cloudinit/aws/*.conf',
    #     ],
    # },
    platforms='any'
)
