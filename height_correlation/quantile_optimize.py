# Import modules
import numpy
import pyswarms
from .objective_funtion import htcor_objfn

def quantile_optimize(z_soil, z_soil_size, z_canopy, z_canopy_size, manual_ht,
    c1 = 0.5, c2 = 0.3, w = 0.9):
    """
    Optimize quantiles

    Parameters
    ----------
    z_soil : numpy.ndarray
        A 1D array of z coordinates for the soil image.
        Example:
            z_soil = numpy.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
    z_soil_size :
        A 1D array of sizes for plot groupings.
        Example:
            z_soil = numpy.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
            z_soil_size = numpy.array([2,3,4])
            This represents the following groups:
                [1.0, 2.0]
                [3.0, 4.0, 5.0]
                [6.0, 7.0, 8.0, 9.0]
    z_canopy : numpy.ndarray
        A 1D array of z coordinates for the canopy image.
        Example:
            See z_soil example.
    z_canopy_size : numpy.ndarray
        A 1D array of sizes for plot groupings.
        Example:
            See z_soil_size example.
    manual_ht : numpy.ndarray
        A 1D array of "true"/"manual" heights.
    c1 : float
    c2 : float
    w : float
        Inertial weight.

    Returns
    -------
    cost, pos
        Cost value and position of the best found solution.

    """
    # Create bounds
    min_bound = numpy.array([0.0, 0.0])
    max_bound = numpy.array([1.0, 1.0])
    bounds = (min_bound, max_bound)

    # swarm parameters
    options = {     # swarm inertial coefficients
        'c1' : c1,
        'c2' : c2,
        'w' : w
    }
    kwargs = {      # arguments to pass to objective function
        "z_soil"        : z_soil,
        "z_soil_size"   : z_soil_size,
        "z_canopy"      : z_canopy,
        "z_canopy_size" : z_canopy_size,
        "manual_ht"     : manual_ht
    }

    # create optimizer object
    optimizer = pyswarms.single.GlobalBestPSO(
        n_particles = 10,
        dimensions = 2,
        options = options,
        bounds = bounds
    )

    # Perform optimization
    cost, pos = optimizer.optimize(
        htcor_objfn,
        iters=1000,
        **kwargs
    )

    return cost, pos
