#!/usr/bin/env python3

__author__ = "Scott Teresi"

"""
This code serves to import the image data and perform filtering operations on
that data.
"""

import pandas as pd
import numpy


def image_data(file_name, sortcol="plot_id"):
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
    image_data = image_data.drop(columns=['X', 'Y'], axis=1)

    # Drop rows with plot_id containing the word fill
    image_data = image_data[~image_data.plot_id.str.contains('fill')]

    # Drop the last two sequences of numbers from the plot_id column
    image_data.plot_id = image_data.plot_id.str[:9]  # TODO Confirm with robert
    # one more time that we can indeed cut the first 9 out and we won't mess up
    # any names.

    image_data = image_data.sort_values(by=sortcol)

    return image_data


def extract_dsm(df, colname, groupcol="plot_id", grouprow=None):
    """
    Extract column from pandas.DataFrame. Spit out column values without NA
    and a groupings array. Assumes sorted pandas.DataFrame
    """
    # grab column values
    sub_df = None
    if grouprow is None:
        sub_df = df.loc[:, [groupcol, colname]]
    else:
        sub_df = df.loc[df[groupcol].isin(grouprow), [groupcol, colname]]

    # make NA mask
    mask_NA = sub_df[colname].isna()

    # remove masked things
    sub_df = sub_df.loc[~mask_NA, [groupcol, colname]]

    # group columns by 'groupby'
    groups = sub_df.groupby(groupcol)

    # get sizes of each group
    col_size = numpy.int64([len(group) for name, group in groups])

    # get values
    col = sub_df.loc[:, colname].values

    # get column names as object_ array
    col_name = numpy.object_([name for name, group in groups])

    # return tuple of values
    return col, col_size, col_name


def las_outlier_filter(g):
    q1 = g['z_position'].quantile(0.25)
    q3 = g['z_position'].quantile(0.75)
    iqr = q3 - q1
    llim = q1 - (1.5 * iqr)
    ulim = q3 + (1.5 * iqr)
    mask = (g['z_position'] > llim) & (g['z_position'] < ulim) # between llim and ulim
    return mask

def las_data(file_name, sortcol = "shpID"):
    """
    Load file data from LAS CSV.

    file_name : str
        File name.
    sortcol : str
        Name of column to sort by.
    """
    # load csv
    df = pd.read_csv(file_name)

    # sort by sortcol
    df.sort_values(by = sortcol, inplace = True)

    # Drop the last two sequences of numbers from the shpID column
    df['shpID'] = df['shpID'].str[:9]

    # filter for outliers : actually makes the prediction worse!
    # group_list = []
    # for name, group in df.groupby(sortcol):
    #     mask = las_outlier_filter(group)
    #     group_list.append(group[mask])
    #
    # out_df = pd.concat(group_list, axis=0)

    return df

def las_extract(df, colname, groupcol = "shpID", grouprow = None):
    """
    df : pandas.DataFrame
        This DataFrame *MUST* be pre-sorted!
    colname : str
        Column name to extract.
    groupcol : str
        Column name to group by.
    grouprow : list, array
        Rows to use (e.g. filtering NA plots)
    """
    # make NA mask
    mask = df[colname].isna()

    # if we are selected specific rows, add grouprow bitwise mask to mask
    if grouprow is not None:
        mask = (mask | (~df[groupcol].isin(grouprow)))

    # remove masked things
    sub_df = df.loc[~mask, [groupcol, colname]]

    # group columns by 'groupby'
    groups = sub_df.groupby(groupcol)

    # get sizes of each group
    col_size = numpy.int64([len(group) for name, group in groups])

    # get values
    col = sub_df.loc[:, colname].values

    # get column names as object_ array
    col_name = numpy.object_([name for name, group in groups])

    # return tuple of values
    return col, col_size, col_name
