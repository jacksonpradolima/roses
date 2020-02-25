# ROSES 
ROSES (**R** pyth**O**n **S**tatistical t**E**st**S**) is a package to use statistical tests from R to Python for multiple algorithms in multiple problems.

[![PyPI License](https://img.shields.io/pypi/l/jMetalPy.svg?style=flat-square)]()
[![PyPI Python version](https://img.shields.io/pypi/pyversions/jMetalPy.svg?style=flat-square)]()
[![DOI](https://zenodo.org/badge/209055396.svg)](https://zenodo.org/badge/latestdoi/209055396)

This package was created due to differences in the precision from other Python packages for statistical tests. As R is a programming language with excellent libraries for statistical, **ROSES** was created as a bridge (parses) to use them.  

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)
- [Citation](#citation)

## Requirements

Install Python:

```console
sudo apt install python3-dev python3-setuptools python3-tk python-dev
```

Install R:
```console 
sudo apt install r-base
```

To compile the R libraries:
```console 
sudo apt install gfortran libcurl4-openssl-dev
```

To install the following R libraries, otherwhise a warning will be handled:
```console
install.packages('devtools')
devtools::install_github("b0rxa/scmamp")
install.packages('PMCMR')
install.packages("https://cran.r-project.org/src/contrib/Archive/mvtnorm/mvtnorm_1.0-8.tar.gz", repos=NULL)
install.packages('PMCMRplus')
install.packages('sp')
install.packages("https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.3-6.tar.gz", repos=NULL)
install.packages('pgirmess')
```

If you received warnings to install the R libraries, try some the commands as follow:

```console
sudo apt install libevent-dev libreadline-dev libudunits2-dev libgdal-dev libgeos-dev libproj-dev libgmp3-dev libmpfr-dev
```

## Installation
To download ROSE just clone the Git repository hosted in GitHub:

```console
git clone https://github.com/jacksonpradolima/ROSE.git
python setup.py install
```

Alternatively, you can install it with `pip`:

```console
pip install roses
```

## Usage
Examples of configuring and running all the included algorithms are located in the *test* folders [roses folder](roses).

## Features
The current release of **ROSES** (v0.3) contains the following tests:

* Kruskal-Wallis with Post-hoc when necessary (comparing p-value)
* Friedman  with Critical Distance plot and Post-hoc when necessary (comparing p-value)
* Varghas and Delaney (effect size)

## License
This project is licensed under the terms of the MIT - see the [LICENSE](LICENSE) file for details.

## Citation

If this package contributes to a project which leads to a scientific publication, I would appreciate a citation.

```
@misc{roses,
  author       = {Prado Lima, Jackson Antonio do},
  title        = {{ROSES (R pythOn Statistical tEstS)}},
  month        = sep,
  year         = 2019,
  doi          = {10.5281/zenodo.3444187},
  url          = {https://doi.org/10.5281/zenodo.3444187}
}
```
