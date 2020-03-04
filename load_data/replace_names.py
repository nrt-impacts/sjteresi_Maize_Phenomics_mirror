#!/usr/bin/env python3

__author__ = "Anna Haber"

"""
This code serves to replace plotID with genotype in a column of a pandas.DataFrame.
"""

import pandas


def replace_names(df, dictionary, colreplace):
    """ Replace the plotID with genotype and append as a column.

    Args:
        pandas.DataFrame (DroneData or HumanData)
        Dictionary with plotID as key and genotype as value
        Column to be replaced (str)
    """
    # Creates a new column 'Genotype' by replacing plotID with genotype.
    df['Genotype'] = df[colreplace].replace(to_replace=dictionary, value=None)
    # Drops the old plotID column.
    df = df.drop(colreplace, axis=1)

    return df
