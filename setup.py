from os.path import abspath, dirname, join

from setuptools import find_packages, setup

basedir = abspath(dirname(__file__))

with open(join(basedir, 'README.md')) as f:
    README = f.read()

setup(
    name='roses',
    version='0.3.7',
    description='ROSES (R pythOn Statistical tEstS) is a package to use statistical tests from R to Python',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Jackson Antonio do Prado Lima',
    author_email='jacksonpradolima@gmail.com',
    maintainer='Jackson Antonio do Prado Lima',
    maintainer_email='jacksonpradolima@gmail.com',
    license='MIT',
    url='https://github.com/jacksonpradolima/roses',
    packages=find_packages(exclude=['test_']),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
    ],
    install_requires=[
        'pandas>=0.23.4',
        'scipy>=1.1.0',
        'numpy>=1.15.2',
        'seaborn>=0.9.0',
        'pingouin>=0.2.2',
        'matplotlib>=3.0.2',
        'tzlocal==1.5.1',
        'rpy2==2.9.5'
    ],
)
