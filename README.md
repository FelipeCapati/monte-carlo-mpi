# Command to build MPI in Linux
sudo apt-get install libcr-dev 
sudo apt-get install mpich 
sudo apt-get install mpich-doc

# Command to install dependencies
pip install requirements.txt

# Command to test MPI installation
mpirun -n 4 python test/mpi_test.py
ou
chmod +x job_mpi_test.sh
./job_mpi_test.sh

# Save requirements.txt
pip freeze > requirements.txt

# Command to Run Monte Carlo MPI Project
mpirun -n 4 python main.py
ou
chmod +x job_run.sh
./job_run.sh

# Comandos Random
Install with Anaconda: 
$ conda create -n mpi mpi4py numpy scipy 
Exemplo: 
from mpi4py import MPI 
comm = MPI.COMM_WORLD 
print("%d of %d" % (comm.Get_rank(), comm.Get_size())) 
Use mpirun and python to execute:
$ mpirun -n 4 python script.py 
