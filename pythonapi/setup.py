from setuptools import setup, Extension
import sys
from pathlib import Path
import pybind11

ext_modules = [
    Extension(
        'montecpp',
        sources=['src/monte.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++'
    )
]

setup(
    name='montecpp',
    version='0.0.1',
    author='auto',
    ext_modules=ext_modules,
)
