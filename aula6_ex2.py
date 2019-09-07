def volume_object(N:int):
    now = datetime.now()
    xdata = np.array([])
    ydata = np.array([])
    zdata = np.array([])
    lim_x_min = 1
    lim_x_max = 4
    lim_y_min = -3
    lim_y_max = 4
    lim_z_min = -2
    lim_z_max = 2

    n_total = N
    n_fig = 0
    for i in range(0, n_total):
        x_random = uniform(lim_x_min, lim_x_max)
        y_random = uniform(lim_y_min, lim_y_max)
        z_random = uniform(lim_z_min, lim_z_max)

        toroid = z_random**2 + ((x_random**2+y_random**2)**0.5-3)**2
        if(x_random > 1) and (y_random >= -3) and (toroid <= 1):
            n_fig += 1
            xdata = np.concatenate((xdata, np.array([x_random])), axis=0)
            ydata = np.concatenate((ydata, np.array([y_random])), axis=0)
            zdata = np.concatenate((zdata, np.array([z_random])), axis=0)
    v_total = (lim_x_max-lim_x_min)*(lim_y_max-lim_y_min)*(lim_z_max-lim_z_min)
    v_figura = v_total*(n_fig/n_total)
    time_process = round((datetime.now() - now).total_seconds(), 2)
    
    return [v_figura, time_process, xdata, ydata, zdata]

[v_figura, time_process, xdata, ydata, zdata] = volume_object(N=100000)
print("The total volume is: %s" %v_figura)