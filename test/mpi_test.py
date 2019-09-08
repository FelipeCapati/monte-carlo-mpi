from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD

rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

shared = (1+rank)*5

if rank == 0:
    data = shared
    comm.send(data, dest=1)
    comm.send(data, dest=2)
    print('From rank', name, 'and rank', rank, 'we sent', data)
    data = comm.recv(source=1)
    print('on node', name, 'and rank', rank, 'we received:', data)
    data = comm.recv(source=2)
    print('on node', name, 'and rank', rank, 'we received:', data)

elif rank == 1:
    data = comm.recv(source=0)
    print('on node',name, 'and rank', rank, 'we received:', data)
    data += 10
    comm.send(data, dest=0)
    print('From rank', name, 'and rank', rank, 'we sent', data)

elif rank == 2:
    data = comm.recv(source=0)
    print('on node', name, 'and rank', rank, 'we received:', data)
    data += 10
    comm.send(data, dest=0)
    print('From rank', name, 'and rank', rank, 'we sent', data)