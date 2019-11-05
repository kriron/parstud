# parstud

A modular [Python 3](https://www.python.org/) project for generation and processing of run statistics for parallelized 3D Proper Orthogonal Decomposition.

## Background

Describe aim of the project with more detail. Include mentions to C++ 3DPOD code and briefly hot it works.

## About

Go through each module as well as the main function and explain their functionalities.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for usage, development and testing purposes.

First clone this repository by:

```
git clone https://github.com/kriron/parstud
```

In order to use  `parstud` several [Python 3](https://www.python.org/) packages are required. Creating a brand new [Conda](https://docs.conda.io/en/latest/) environment for this is recomended. This can be done easily with the provided yml file as follows:

```
conda env create -f parstud/conda/parstud.yml
conda activate parstud
```

## Running the tests

Testing of all modules within `parstud` can be done automatically by running:

```
python -m pytest --cov=parstud/
```

If you would like to see a more detailed description of the tests and converage an html report can be produced as follows:

```
python -m pytest --cov=parstud/ --cov-report=html
```

This will create an `htmlcov/` folder in the root of your `parstud` folder. Inside it a file named `index.html` can be viewed in most internet browsers. This can be done directly from the command line by:

```
firefox htmlcov/index.html 
```

## Authors

* [Kristian Rönnberg](https://github.com/kriron)
* [Marc Rovira](https://github.com/mrovirasacie)