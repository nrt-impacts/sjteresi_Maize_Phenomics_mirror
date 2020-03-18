import numpy


def get_quantile(q, height, height_size):
    """
    Retrieve a height vector.

    Parameters
    ----------
    q : numpy.ndarray, list-like, float
        An array, list, or float of quantiles to grab.
    height : numpy.ndarray
        A vector of heights. This vector is mixed for each plot. The number of
        data points per plot is not equal across all plots (due to NAs). The
        'height_size' vector denoting the sizes of these chunks.
    height_size : numpy.ndarray
        A vector of sizes of data chunks in 'height'.

    Returns
    -------
    ht : numpy.ndarray
        An array of heights at the specified quantiles.
    """
    # allocate empty array
    ht = numpy.empty((len(height_size), len(q)), dtype='float64')

    # get start, stop indices
    height_stop = height_size.cumsum()
    height_start = height_stop - height_size

    # for each group, get quantile
    for i, (st, sp) in enumerate(zip(height_start, height_stop)):
        ht[i, :] = numpy.quantile(height[st:sp], q)

    # return height
    return ht


def htcor_objfn(x, z_soil, z_soil_size, z_canopy, z_canopy_size, manual_ht):
    """
    Height correlation objective function. The goal is to minimize this
    function.

    Parameters
    ----------
    x : numpy.ndarray
        A matrix of two columns representing quantile positions.
        First column represents low (soil) quantile.
        Second column represents upper (canopy) quantile.
        Range of this x matrix must be 0-1!
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

    Returns
    -------
    The negative Pearson product-moment correlation coefficient between the
    image height and the manual height. -r.
    """
    # allocate empty arrays for soil height and canopy height.
    soil_ht = numpy.empty(
        shape=(len(x), len(manual_ht)),
        dtype='float64'
    )
    canopy_ht = numpy.empty(
        shape=(len(x), len(manual_ht)),
        dtype='float64'
    )

    # calculate stop indices for soil, canopy
    soil_stop = z_soil_size.cumsum()
    canopy_stop = z_canopy_size.cumsum()

    # calculate quantile values
    for i, (st, sp) in enumerate(zip(soil_stop - z_soil_size, soil_stop)):
        soil_ht[:, i] = numpy.quantile(z_soil[st:sp], x[:, 0])
    for i, (st, sp) in enumerate(zip(canopy_stop - z_canopy_size, canopy_stop)):
        canopy_ht[:, i] = numpy.quantile(z_canopy[st:sp], x[:, 1])

    # calculate estimated heights
    est_ht = canopy_ht - soil_ht

    # calculate Pearson correlation coefficient
    r = numpy.fromiter(
        (numpy.corrcoef(est_ht[r, :], manual_ht)[0, 1] for r in range(len(est_ht))),
        dtype='float64'
    )

    # return negative Pearson correlation coefficient, since we want to minimize
    return -1.0 * r
