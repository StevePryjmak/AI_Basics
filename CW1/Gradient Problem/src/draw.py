from constants import *
import matplotlib.pyplot as plt
import numpy as np


def setup_grid(function, dimensions=DIMENSIONALITY, dem_1=DEM_1, dem_2=DEM_2):
    x_arr = np.arange(-UPPER_BOUND, UPPER_BOUND, PLOT_STEP)
    y_arr = np.arange(-UPPER_BOUND, UPPER_BOUND, PLOT_STEP)
    dem_x, dem_y = np.meshgrid(x_arr, y_arr)
    dem_z = np.empty(dem_x.shape)
    #
    for i in range(dem_x.shape[0]):
        for j in range(dem_x.shape[1]):
            point = np.zeros(dimensions)
            point[dem_1] = dem_x[i, j]
            point[dem_2] = dem_y[i, j]
            dem_z[i, j] = function(np.array(point))
    plt.contour(dem_x, dem_y, dem_z, 20)

    plt.xlim(-UPPER_BOUND, UPPER_BOUND)
    plt.ylim(-UPPER_BOUND, UPPER_BOUND)
    plt.title("Gradient Problem Descent Steps")
