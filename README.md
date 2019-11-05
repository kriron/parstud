# parstud

A modular [Python 3](https://www.python.org/) project for generation and processing of run statistics for parallelized 3D Proper Orthogonal Decomposition.

## Background

The `parstud` project aims to create a flexible parametric study runner and subsequent text-to-image processing for applying 3D Proper Orthogonal Decomposition  (POD). In particular this code was developed to work in conjunction with our own open-source parallel C++ 3D POD code, [parallel-pod](https://github.com/mrovirasacie/parallel-pod). Nevertheless, the code is flexible enough that it can be adapted for other parametric studies with little effort.

In order to understand `parstud` an introduction to [parallel-pod](https://github.com/mrovirasacie/parallel-pod) is relevant. POD or modal analysis is a post-processing mathematical technique that intends to extract the most important energetical and dynamical features of a fluid flow. These spatial features of the flow are known as modes. Each of them is related to characteristic values which represent their relative energy levels and instrinsic frequencies of motion. In our code, these modes are determined from compuational fluid dynamic (CFD). In particular, we used cases runned with the open-source C++ code [OpenFOAM](https://github.com/OpenFOAM). For a large number of time instants (N) a regularly-spaced cloud of point data is extracted from the simulation. Each of these clouds is known as a snapshot and usually contains a large ammount of points (M). The speed of the mathematical operations by which this data is converted to isolated modes scales with the size of the data set (M x N). Hence, the code can be prohibitively slow for a very in depth study. The implementation of [parallel-pod](https://github.com/mrovirasacie/parallel-pod) in C++ provides a fast language framework to reduce this issue which is further mitigated by paralellisation. 

## About

Go through each module as well as the main parstud function and explain all relevant functionalities.

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

After executing these commands a new Conda environment names `parstud` will be created with all necessary packages. The environment is self-contained so as to not influence other local python installations and avoid conflicts with previously installed packages. In order to deactivate this environment simply type:

```
conda deactivate
```

## Testing

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

Indiviudual modules can also be tested in a similar manner. For instance check the tests and coverage of the plotter module by:

```
python -m pytest tests/test_plotter/ --cov=parstud/plotter/
```

The implemented tests have the aim to check that the functions within the three modules `runner`, `reader` and `plotter` have the desired functionality as well as raising the correct error warnings.

## Authors

* [Kristian Rönnberg](https://github.com/kriron)
* [Marc Rovira](https://github.com/mrovirasacie)