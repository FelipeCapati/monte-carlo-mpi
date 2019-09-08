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



https://mpi4py.readthedocs.io/en/stable/tutorial.html#running-python-scripts-with-mpi

Dynamic Process Management

    Compute Pi - Master (or parent, or client) side:

    #!/usr/bin/env python
    from mpi4py import MPI
    import numpy
    import sys

    comm = MPI.COMM_SELF.Spawn(sys.executable,
                               args=['cpi.py'],
                               maxprocs=5)

    N = numpy.array(100, 'i')
    comm.Bcast([N, MPI.INT], root=MPI.ROOT)
    PI = numpy.array(0.0, 'd')
    comm.Reduce(None, [PI, MPI.DOUBLE],
                op=MPI.SUM, root=MPI.ROOT)
    print(PI)

    comm.Disconnect()

    Compute Pi - Worker (or child, or server) side:

    #!/usr/bin/env python
    from mpi4py import MPI
    import numpy

    comm = MPI.Comm.Get_parent()
    size = comm.Get_size()
    rank = comm.Get_rank()

    N = numpy.array(0, dtype='i')
    comm.Bcast([N, MPI.INT], root=0)
    h = 1.0 / N; s = 0.0
    for i in range(rank, N, size):
        x = h * (i + 0.5)
        s += 4.0 / (1.0 + x**2)
    PI = numpy.array(s * h, dtype='d')
    comm.Reduce([PI, MPI.DOUBLE], None,
                op=MPI.SUM, root=0)

    comm.Disconnect()


