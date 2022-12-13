# Spooky pebble game




# How to use and import z3?
This has been partially copied from Sebastiaan Brand (clifford-circ-pdr project).

1. Download the repository
2. Run the following in terminal (root folder):

#create a virtual environment\
virtualenv .venv\
source venv/bin/activate

#install z3 (compile + python bindings)\
cd z3\
python scripts/mk_make.py --python\
cd build\
make\
make install


# Overview of files

The SAT_encoding_spooky_pg_....py files are simulators of the spooky pebble game using a SAT solver. The different files use different methods or additional features, e.g. numpy, or at most one pebble placed per timestep.

The FixedPoint.py file is also a simulator of the spooky pebble game, but uses a FixedPoint solver. 

The file Convert_bench_file_to_DAG.py is used to convert a .bench file from the benchmark folder to a DAG. This DAG can then be used as benchmark input for the spooky pebble game simulators.
