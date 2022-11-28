# Spooky pebble game



How to use and import z3?
This has been partially copied from Sebastiaan Brand (clifford-circ-pdr project).

1. Download the repository
2. Run the following in terminal (root folder):

#create a virtual environment
virtualenv .venv
source venv/bin/activate

#install z3 (compile + python bindings)
cd z3
python scripts/mk_make.py --python
cd build
make
make install
