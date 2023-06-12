#!/usr/bin/env python
from Centromics.__version__ import version

from setuptools import setup, find_packages
from distutils.extension import Extension
#from Cython.Build import cythonize

with open('README.md') as f:
    long_description = f.read()


setup(
    name='Centromics',
    version=version,
    description='Centromics: visualing centromeres with omics data',
    url='https://github.com/zhangrengang/Centromics/',
    author='Zhang, Ren-Gang and Wang, Zhao-Xuan',
    license='GPL-3.0',

    python_requires='>=3.6:',
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    entry_points={
        'console_scripts': ['centromics = Centromics.pipe:main',
        ],
    },
)
