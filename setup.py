from setuptools import setup, find_packages

setup(
    name='cronicas_adaptativas',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy',
        'psycopg2-binary',
        'pymongo',
        'pytest'
    ],
    entry_points={
        'console_scripts': ['cronicas=main:main']
    }
)