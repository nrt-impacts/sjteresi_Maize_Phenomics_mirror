# Import modules
import numpy
import pyswarms
from .objective_funtion import htcor_objfn

# Create bounds
min_bound = numpy.array([0.0, 0.0])
max_bound = numpy.array([1.0, 1.0])
bounds = (min_bound, max_bound)

# swarm parameters
options = {     # swarm inertial coefficients
    'c1': 0.5,
    'c2': 0.3,
    'w':0.9
}
kwargs = {  # arguments to pass to objective function
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
