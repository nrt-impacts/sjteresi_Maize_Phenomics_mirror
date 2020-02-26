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

    # Drop the RGB columns
    image_data = image_data.loc[:, ~image_data.columns.str.contains('RGB')]

    # Drop the X and Y columns
    image_data = image_data.drop(columns=['X','Y'], axis=1)

    # Drop rows with plot_id containing the word fill
    image_data = image_data[~image_data.plot_id.str.contains('fill')]

    # Drop the last two sequences of numbers from the plot_id column
    image_data.plot_id = image_data.plot_id.str[:9]  # TODO Confirm with robert
    # one more time that we can indeed cut the first 9 out and we won't mess up
    # any names.

    return image_data
