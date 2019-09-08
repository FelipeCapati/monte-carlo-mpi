#!/usr/bin/env python
from datetime import datetime
from mpi4py import MPI
from math import floor
import numpy as np
import sys

# Setup MPI
MAXPROCS = 4
comm = MPI.COMM_SELF.Spawn(sys.executable,
                           args=['worker_monte_carlo.py'],
                           maxprocs=MAXPROCS)
rank = comm.Get_rank()

# Configure total number of integration
n_total = np.array(8000000, 'i')

# Init Monte Carlo Work
now = datetime.now()

# Configure Limit of Integration
lim_x_min = 1
lim_x_max = 4
lim_y_min = -3
lim_y_max = 4
lim_z_min = -2
lim_z_max = 2

# Send MPI Broadcast requisition
requesition = np.array(floor(n_total/MAXPROCS), 'i')
comm.Bcast([requesition, MPI.INT], root=MPI.ROOT)

# Get Reduce MPI
n_fig = np.array(0.0, 'i')
comm.Reduce(None, [n_fig, MPI.INT],
            op=MPI.SUM, root=MPI.ROOT)

# Calculate volume of figure
v_total = (lim_x_max - lim_x_min) * (lim_y_max - lim_y_min) * (lim_z_max - lim_z_min)
v_figura = round(v_total * (n_fig / float(requesition*MAXPROCS)), 2)

# End Monte Carlo Work
time_process = round((datetime.now() - now).total_seconds(), 2)

print("> rank(%s) :: Iterations: %s Volume: %s :: TimeToProcess: %s" %(rank, requesition*MAXPROCS, v_figura, time_process))

comm.Disconnect()