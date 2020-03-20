#!/usr/bin/env python3

__author__ = "Anna Haber"

import pandas as pd


def ground_data(file_name, sortcol="plot"):
    """ Import the ground_data_2019.csv data

    Args:
        path_to_file (str)

    """
    # read data into pandas.DataFrame
    ground_data = pd.read_csv(
        file_name,
        sep=',',
        header='infer'
    )

    # Keep the plot, PlantHeightP1, and PlantHeightP2 columns only.
    ground_data = ground_data[['plot', 'PlantHeightP1', 'PlantHeightP2']]
    ground_data['MeanPHeight'] = ground_data[
        ['PlantHeightP1','PlantHeightP2']
    ].mean(axis=1)

    # remove NaN values
    ground_data = ground_data.loc[~ground_data['MeanPHeight'].isna(), :]
    ground_data = ground_data.loc[~ground_data['PlantHeightP1'].isna(), :]
    ground_data = ground_data.loc[~ground_data['PlantHeightP2'].isna(), :]

    # sort by plot_id
    ground_data = ground_data.sort_values(by=sortcol)

    return ground_data


def extract_canopy_ht(df, colname='MeanPHeight'):
    """
    extract canopy heights
    Assumes a pandas.DataFrame sorted by "plot"
    """
    # extract numpy.ndarray copy
    canopy_ht = df.loc[:, colname].values.copy()

    names = df['plot'].values

    # return numpy.ndarray
    return canopy_ht, names
