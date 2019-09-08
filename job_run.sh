#!/bin/bash
python simple_monte_carlo.py
mpirun -n 4 python mpi_monte_carlo.py