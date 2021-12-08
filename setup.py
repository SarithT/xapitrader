from setuptools import setup, find_packages
from os.path import basename
from glob import glob
from os.path import dirname
from os.path import join
from os.path import splitext

setup(
    name='xapitrader',
    version='0.0.15',
    license='MIT',
    description='Wrapper over XTB xAPI communication protocol',
    author='Dawid Tan',
    author_email='tan.dawid@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    python_requires='>=3.8',
)