#!/usr/bin/env python3

__author__ = "Scott Teresi"

"""
This code serves to import the observation key/plotID data and return a
dictionary and a dataframe
"""

import pandas as pd


def obs_data(file_name):
    """ Import the obs_2019_key.csv

    Args:
        path_to_file (str)

    """
    # TODO Anna:
        # Switch to the genotype_dictionary branch to perform all of these
        # tasks.
        # Task 1:
            # Verify that the obs_data() function is appropriate and
            # functional. You may or may not need to add additional code.
            # Return the dataframe and make sure phenomics.py can receive it
            # correctly.

    obs_data = pd.read_csv(
        file_name,
        sep=',',
        header='infer')

    return obs_data

# TODO Anna:
    # Task 2:
        # Create a separate function in this file to return a dictionary of
        # plotID vs genotypes
        # A dictionary will need to be constructed to perform the replace
        # function in Task 3 (we need to replace plotIDs with genotypes).
        # I suggest reading up on the zip() function in Python
        # and supplying the two appropriate columns from obs_2019_key.csv.
        # You can place this zip() command inside a dict() command
        # to construct a dictionary. Return the dictionary from the
        # function. Then make that function accessible from phenomics.py. And test
        # it inside of phenomics.py

# TODO Anna:
    # Task 3:
        # Create a separate file (replace_names.py) and function to replace the
        # plotID of a dataframe with the genotypes from your dictionary. Then run
        # that function inside of phenomics.py and verify that you can accurately
        # replace the plotID of ground_data.csv and point_data_6in_2019.csv with
        # the genotype.

        # Use pandas.DataFrame.replace (look up the documentation) utilizing a
        # your previously constructed dictionary to replace the plot_id in
        # ground_data_2019.csv and point_data_6in_2019.csv with the Genotype value from
        # obs_2019_key.csv.

# FINAL
# Run flake8 on all of your code before you submit a commit. The commit your
# changes and let me know and I will review the pull request and merge to
# master.
