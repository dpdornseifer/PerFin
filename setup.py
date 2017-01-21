import os
from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='perfin',
    version='0.0.1dev',
    packages=['tests', 'perfin', 'examples'],
    install_requires=[
        'pandas',
        'numpy',
    ],
    url='https://github.com/dpdornseifer/PerFin',
    license='MIT',
    author='David_Dornseifer',
    author_email='dp.dornseifer@googlemail.com',
    description='PerFin a Personal Finance library.',
    long_description=read('README.md'),
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
    ],
)
