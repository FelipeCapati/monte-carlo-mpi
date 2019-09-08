#!/usr/bin/env python
from datetime import datetime
from random import uniform
import numpy as np

# Initialize
print("############################################################")
print("##################### Code without MPI #####################")
print("############################################################")

# Configure total number of integration
n_total = np.array(1000000, 'i')

# Init Monte Carlo Work
now = datetime.now()

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

# Calculate volume of figure
v_total = (lim_x_max - lim_x_min) * (lim_y_max - lim_y_min) * (lim_z_max - lim_z_min)
v_figura = round(v_total * (n_fig / float(n_total)), 2)

# End Monte Carlo Work
time_process = round((datetime.now() - now).total_seconds(), 2)

print("> Simple Monte Carlo :: Iterations:%s :: Volume: %s :: TimeToProcess: %s" %(n_total, v_figura, time_process))