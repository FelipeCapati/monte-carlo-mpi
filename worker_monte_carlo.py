#!/usr/bin/env python
from random import uniform
from mpi4py import MPI
import numpy as np

# Setup MPI Worker
comm = MPI.Comm.Get_parent()
size = comm.Get_size()
rank = comm.Get_rank()

# Get data from root
n_total = np.array(0, dtype='i')
comm.Bcast([n_total, MPI.INT], root=0)

# Configure Limit of Integration
lim_x_min = 1
lim_x_max = 4
lim_y_min = -3
lim_y_max = 4
lim_z_min = -2
lim_z_max = 2

# Calculate part of Monte Carlo
n_fig = 0
for i in range(0, n_total):
    x_random = uniform(lim_x_min, lim_x_max)
    y_random = uniform(lim_y_min, lim_y_max)
    z_random = uniform(lim_z_min, lim_z_max)

    toroid = z_random ** 2 + ((x_random ** 2 + y_random ** 2) ** 0.5 - 3) ** 2
    if (x_random > 1) and (y_random >= -3) and (toroid <= 1):
        n_fig += 1

# Export count information using Reduce by sum
np_n_fig = np.array(n_fig, dtype='i')
comm.Reduce([np_n_fig, MPI.INT], None, op=MPI.SUM, root=0)

# Diconnect
comm.Disconnect()
