# Command to build MPI in Linux
sudo apt-get install libcr-dev 
sudo apt-get install mpich 
sudo apt-get install mpich-doc

# Command to install dependencies
pip install requirements.txt

# Save requirements.txt
pip freeze > requirements.txt

# Comandos Random
Install with Anaconda: 
$ conda create -n mpi mpi4py numpy scipy 
Exemplo: 
from mpi4py import MPI 
comm = MPI.COMM_WORLD 
print("%d of %d" % (comm.Get_rank(), comm.Get_size())) 
Use mpirun and python to execute:
$ mpirun -n 4 python script.py 
