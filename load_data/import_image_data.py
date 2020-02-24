#!/usr/bin/env python3

__author__ = "Scott Teresi"

"""
This code serves to import the image data and perform filtering operations on
that data.
"""

import pandas as pd


def image_data(file_name):
    """ Import the point_data_6in_2019.obs.csv data

    Args:
        path_to_file (str)

    """

    image_data = pd.read_csv(
        file_name,
        sep=',',
        header='infer')
