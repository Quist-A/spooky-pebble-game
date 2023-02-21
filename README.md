# Spooky pebble game

This repository belongs to the paper 'Optimizing Quantum Space using Spooky Pebble Games' (2023) by Arend-Jan Quist and Alfons Laarman. 


## How to use and import z3 (Linux)?

1. Clone the repository
2. Run the following in terminal (root folder):

#create a virtual environment\
virtualenv venv\
source venv/bin/activate

#clone submodules
git submodule init\
git submodule update

#install z3 (compile + python bindings)\
cd external\
python scripts/mk_make.py --python\
cd build\
make\
make install


## Overview of files

The file spooky_solver.py is the file to run the spooky solver to find fronts as shown in the paper. \
The file plotResults.py plots the results of the solver.

The file Convert_bench_file_to_DAG.py is used to convert a .bench file from the benchmark folder to a DAG. This DAG can then be used as benchmark input for the spooky pebble game simulators.

The file bmc2.py is the actual bmc solver of the spooky pebble game. This solver tries to find a solution timestep by timestep. The current performance is pretty good when many pebbles are used.

The file pebble_bmc2.py provide setups for the bmc solver for the spooky pebble game problem. 


