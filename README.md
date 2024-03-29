# parstud

A modular [Python 3](https://www.python.org/) project for generation and processing of run statistics for parallelized 3D Proper Orthogonal Decomposition.

## Background

The `parstud` project aims to create a flexible parametric study runner and subsequent text-to-image processing for applying 3D Proper Orthogonal Decomposition (POD). In particular, this code was developed to work in conjunction with our own open-source parallel C++ 3D POD code, [parallel-pod](https://github.com/mrovirasacie/parallel-pod). Nevertheless, the code is flexible enough that it can be adapted for other parametric studies with little effort.

In order to understand `parstud` an introduction to [parallel-pod](https://github.com/mrovirasacie/parallel-pod) is relevant. POD or modal analysis is a post-processing mathematical technique that intends to extract the most important energetical and dynamical features of a fluid flow. These spatial features of the flow are known as modes. Each of them is related to characteristic values which represent their relative energy levels and intrinsic frequencies of motion. A small subset of those modes can be then used to create a low-order reconstruction of the instantaneous flow field. A visual representation of this can be seen in the image below extracted from *Taira, et al. "Modal analysis of fluid flows: An overview." (2017)*:

![Taira, Kunihiko, et al. "Modal analysis of fluid flows: An overview." Aiaa Journal (2017): 4013-4041.​](https://i.imgur.com/5lBV1a1.png)


In our code, these modes are determined from computational fluid dynamic (CFD) data. In particular, we used cases run with the open-source C++ code [OpenFOAM](https://github.com/OpenFOAM). For a large number of time instants (N) a regularly-spaced cloud of point data is extracted from the simulation. Each of these clouds is known as a snapshot and usually contains a large number of points (M). The speed of the mathematical operations by which this data is converted into isolated modes scales with the size of the data set (M x N). Hence, serial code implementations in an interpreted programming language can be prohibitively slow for a very in-depth study of the flow physics. The implementation of [parallel-pod](https://github.com/mrovirasacie/parallel-pod) in C++ provides a fast compiled language framework to reduce this issue which is further mitigated by [OpenMP](https://www.openmp.org/) parallelization.

Although still work in progress, `parallel-pod` is in working condition and we were interested in studying the scalability and performance of the code. Hence, `parstud` represents our effort of interfacing `parallel-pod` with a python code that can not only run a parametric study over a large number of processors but also can post-process the logs produced by the runs and generate images to visualize the code performance.

## About

`parstud` is divided up into three different modules (`runner`, `reader` and `plotter`), each containing a series of worker and helper functions. Although they can be called and run separately, they can also be executed using the main script `parstud.py`. This function is implemented with subcommand argument parsing for ease of use of the modules. More information about how to correctly call the `parstud.py` script can be seen in [**Getting Started**](#Getting-Started). Here, we will cover each of the modules individually:

#### `runner`

The `runner` module contains one main script, `run_profile.py`. The functionality of this script is divided up sequentially as follows:

1. Check if the OS is compatible. Since almost the entirety of academic and high-performance computing (HPC) cluster environments are running Linux, other OSs are not supported by the current implementation.

2. Generate the system calls by applying the variation of an input parameter (i.e. the number of threads to be employed in the run) over a pre-defined command.

3. Create three `info` files in which to store relevant information for the case:
 - `meminfo`: stores the RAM information of the system.
 - `sysinfo`: stores general information about the hardware of the system (i.e. architecture, CPUs, cache...).
 - `runinfo`: stores the different calls and the number of current and total passes for that command call. Start/stop information is also recorded here.

#### `reader`

The output logs created by the different calls issued by the runner modules are then handled separately by the `reader` module and its main script `reader.py`. This module has two functions which handle the reading as follows:

- `read_log`: reads both the different functionalities executed by the `parallel-pod` code (i.e. reading, computing, and writing) as well as the time it took for each of these functions to finish.

- `build_database`: generates a pandas dataframe database based on the calls recorded into `runinfo` by the `runner` module. For each of the calls, it executes the `read_log` function to extract the relevant data from the logs. The function then returns a structured dataframe including all function and time data for all logs.

After the `build_database` function creates the database based on the logs from the runs, storing it in a `cvs` file is a typical use case.

#### `plotter`

The `plotter` module can be employed to read the database and create two types of plots. This is done through two different functions inside the module.

- `error_plot`: exports seven images, one for each functionality of the `parallel-pod` code. The data for all passes for each run at a fixed number of processors are used to create both mean and error values. Hence, trends in time spent against the number of processors as well as data variability can be observed quickly.

- `piechart_plot`: exports one single image containing the averaged proportion *reading*, *computing* and *writing* functions among all runs and all passes. For this, a reduction in variables from the seven initial functions available in the `parallel-pod` logs to only three has to be performed. This is done by using the helper function `reduce_df`. This allows to swiftly observe bottlenecks and distribution of the code's load. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for usage, development and testing purposes. **Please note** that only Linux environments are supported in the current implementation.

First clone this repository by:

```
git clone https://github.com/kriron/parstud
```

In order to use `parstud` several [Python 3](https://www.python.org/) packages are required. Creating a brand new [Conda](https://docs.conda.io/en/latest/) environment for this is recommended. This can be done easily with the provided `yml` file as follows:

```
conda env create -f parstud/conda/parstud.yml
conda activate parstud
```

After executing these commands a new Conda environment names `parstud` will be created with all necessary packages. The environment is self-contained so as to not influence other local python installations and avoid conflicts with previously installed packages. To deactivate this environment simply type:

```
conda deactivate
```

To check that everything is running smoothly you can attempt to prompt the help message from the `runner` module executing it through the main `parstud.py` script. This is done by:

```
python parstud/parstud.py run --help
```

You should see the following:

```
usage: parstud.py run [-h] [-fd] [-v [VARIATIONS [VARIATIONS ...]]]
 [-p PASSES]
 dir systemcall

positional arguments:
 dir Directory where to store the run output.
 systemcall Base system call to be varied.

optional arguments:
 -h, --help show this help message and exit
 -fd, --forcedirectory
 Force usage of output directory. WARNING: This will
 wipe the specified directory clean
 -v [VARIATIONS [VARIATIONS ...]], --variations [VARIATIONS [VARIATIONS ...]]
 Variations to be applied to base system call
 -p PASSES, --passes PASSES
 Number of passes per systemcall variation.
```

Similar help messages can be obtained for the `read` and `plot` subcommands.

## Testing

Testing of all modules within `parstud` can be done automatically by running:

```
python -m pytest --cov=parstud/
```

If you would like to see a more detailed description of the tests and coverage an HTML report can be produced as follows:

```
python -m pytest --cov=parstud/ --cov-report=html
```

This will create an `htmlcov/` folder in the root of your `parstud` folder. Inside it, a file named `index.html` can be viewed in most internet browsers. This can be done directly from the command line by:

```
firefox htmlcov/index.html 
```

Individual modules can also be tested similarly. For instance check the tests and coverage of the plotter module by:

```
python -m pytest tests/test_plotter/ --cov=parstud/plotter/
```

The implemented tests have the aim to check that the functions within the three modules `runner`, `reader` and `plotter` have the desired functionality as well as raising the correct error warnings.

## Authors

* [Kristian Rönnberg](https://github.com/kriron)
* [Marc Rovira](https://github.com/marrov)
