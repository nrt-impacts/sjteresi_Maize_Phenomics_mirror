#!/usr/bin/env python3

__author__ = "Anna Haber"

import pandas as pd

def ground_data(file_name):
    """ Import the ground_data_2019.csv data

    Args:
        path_to_file (str)

    """

    ground_data = pd.read_csv(
            file_name,
            sep=',',
            header='infer')

    # Keep the plot, PlantHeightP1, and PlantHeightP2 columns only.
    ground_data = ground_data.loc['plot','PlantHeightP1','PlantHeightP2',axis=1]
    #ground_data.head()

    return ground_data
