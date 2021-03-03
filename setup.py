from setuptools import setup, find_packages

setup(
    name='shelly_API',
    version='0.1',
    description=(
        'Implementation of the Shelly API project'
    ),
    author='Hamid Malik',
    license='APL 2.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'bson',
        'flask',
        'flask_cors',
        'sqlite3'
    ],
    zip_safe=False
)