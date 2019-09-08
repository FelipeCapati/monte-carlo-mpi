from datetime import datetime
from random import uniform
from mpi4py import MPI
import numpy as np
import math

# Configure total number of integration
n_total = np.array(1000000, 'i')

# Init Monte Carlo Work
now = datetime.now()

# Initialize MPI Communication
comm = MPI.COMM_WORLD

# Setup Global Variables MPI
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()
TOTAL_NODE = 4

# Configure Limit of Integration
lim_x_min = 1
lim_x_max = 4
lim_y_min = -3
lim_y_max = 4
lim_z_min = -2
lim_z_max = 2

# If Master Rank
if rank == 0:
    # Initialize
    print("############################################################")
    print("####################### Code with MPI ######################")
    print("############################################################")

    # Send MPI Broadcast requisition
    requesition = np.array(math.floor(n_total / TOTAL_NODE), 'i')
    for node in range(1, TOTAL_NODE):
        comm.send(requesition, dest=node)
        print('From rank(%s): %s we sent: %s to node: %s' %(rank, name, requesition, node))

    # Calculate Part of MPI in Rank 0 too
    n_fig = 0
    for i in range(0, requesition):
        x_random = uniform(lim_x_min, lim_x_max)
        y_random = uniform(lim_y_min, lim_y_max)
        z_random = uniform(lim_z_min, lim_z_max)

        toroid = z_random ** 2 + ((x_random ** 2 + y_random ** 2) ** 0.5 - 3) ** 2
        if (x_random > 1) and (y_random >= -3) and (toroid <= 1):
            n_fig += 1

    # Get MPI Processed by nodes
    requesition_sum = n_fig
    for node in range(1, TOTAL_NODE):
        requesition_sum += comm.recv(source=node)
        print('On rank(%s): %s we received: %s' % (rank, name, requesition_sum))

    # Calculate volume of figure
    v_total = (lim_x_max - lim_x_min) * (lim_y_max - lim_y_min) * (lim_z_max - lim_z_min)
    v_figura = round(v_total * (requesition_sum / float(requesition * TOTAL_NODE)), 2)

    # End Monte Carlo Work
    time_process = round((datetime.now() - now).total_seconds(), 2)

    print("> MPI Monte Carlo :: rank(%s) :: Iterations: %s Volume: %s :: TimeToProcess: %s" %(rank, requesition * TOTAL_NODE, v_figura, time_process))


# If Slave Rank
else:
    requesition = comm.recv(source=0)
    print('On rank(%s): %s we received: %s' % (rank, name, requesition))

    # Calculate part of Monte Carlo
    n_fig = 0
    for i in range(0, requesition):
        x_random = uniform(lim_x_min, lim_x_max)
        y_random = uniform(lim_y_min, lim_y_max)
        z_random = uniform(lim_z_min, lim_z_max)

        toroid = z_random ** 2 + ((x_random ** 2 + y_random ** 2) ** 0.5 - 3) ** 2
        if (x_random > 1) and (y_random >= -3) and (toroid <= 1):
            n_fig += 1

    # Export calc to MPI Master
    requesition = n_fig
    comm.send(requesition, dest=0)
    print('From rank(%s): %s we sent: %s to node: 0' % (rank, name, requesition))