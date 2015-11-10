try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name='Aptly-Api-Cli',
    version='0.1',
    url='http://masterhoschi.dyndns.org/git',
    license='MIT',
    author='Tim Susa',
    author_email='timsusa@gmx.de',
    description='This python command line interface, executes calls to the Aptly server remotely, without blocking the Aptly database.',
    long_description=__doc__,
    packages=find_packages(),
    # py_modules=['run', 'staging', 'client', 'manage'],
    # entry_points={
    #     'console_scripts': [
    #         'rest-api=cluster_manager:run',
    #         'rest-cli=cli.cli:run',
    #         'rest-manage=manage:__main__'
    #     ]
    # },
    # data_files=[
    #     ('supervisor', ['contrib/rest-api.sv.conf']),
    #     ('supervisor', ['contrib/worker.sv.conf']),
    #     ('nginx', ['contrib/api-staging.conf']),
    # ],
    # package_data={
    #     'configs': [
    #         'cluster/cloudinit/aws/*.conf',
    #         'cluster/cloudinit/openstack/*.conf',
    #         'cluster/config_templates/core/*.json',
    #         'cluster/config_templates/hadoop/*.json',
    #         'cluster/config_templates/kafka/*.json',
    #         'cluster/config_templates/samza/*.json',
    #         'cluster/config_templates/dataapi/*.json',
    #         'keys/public_key',
    #         'keys/private_key',
    #         'templates/cluster/*.rb',
    #         'templates/cluster/kafka/server.properties',
    #         'templates/cluster/camus/camus.properties',
    #         'templates/cluster/cdhfive/*.ini',
    #         'templates/cluster/cdhfive/*.xml',
    #         'templates/cluster/cdhfive/*.conf',
    #         'templates/email/generic/*.tmpl',
    #         'templates/email/tlabs/*.tmpl',
    #         'web/*.conf'
    #     ],
    #     'db_migrate': [
    #         'alembic.ini',
    #         'alembic_production.ini',
    #         'script.py.mako',
    #         'README',
    #         'versions/*.py',
    #     ],
    # },
    platforms='any'
)
