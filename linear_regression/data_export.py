
#Read data
#Get quantiles in pandas dataframe
#Take the data and use in r for linear model
#!/usr/bin/env python3

# TODO implement a description for the entire file

__author__ = "McKena Lipham"

import logging
import pandas as pd
import coloredlogs
import numpy as np
from configparser import ConfigParser

from matplotlib import pyplot

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from load_data.import_image_data import image_data, las_data, las_extract, extract_dsm
from load_data.import_ground_data import ground_data, extract_canopy_ht
from height_correlation.objective_function import htcor_objfn
from height_correlation.objective_function import get_quantile

if __name__ == '__main__':
    # TODO implement a main description
    """
    Test
    """
    log_level = logging.INFO
    logger = logging.getLogger(__name__)
    coloredlogs.install(level=log_level)
    logger.info("Setting config file...")
    config = ConfigParser()
    # Code in the parser objects, hard coded
    config['Filenames'] = {
        'HumanData': 'ground_data_2019.csv',
        'DroneData': 'point_data_6in_2019obs.csv',
        'ObservationKey': 'obs_2019_key.csv',
        'data_07_02': 'MSU_2019_07_02_NatCol_obs_plots.filter.csv',
        'data_07_15': 'MSU_2019_07_15_NatCol_obs_plots.filter.csv',
        'data_07_28': 'MSU_2019_07_28_NatCol_obs_plots.filter.csv',
        'data_08_12': 'MSU_2019_08_12_NatCol_obs_plots.filter.csv',
        'data_09_02': 'MSU_2019_09_02_NatCol_obs_plots.filter.csv',
        'data_09_11': 'MSU_2019_09_11_NatCol_obs_plots.filter.csv',
        'data_09_24': 'MSU_2019_09_24_NatCol_obs_plots.filter.csv',
        'data_10_07': 'MSU_2019_10_07_NatCol_obs_plots.filter.csv'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    logger.info("Reading config file...")
    parser = ConfigParser()
    parser.read('config.ini')

    # Set the objects from the parser
    HumanData = parser.get('Filenames', 'HumanData')
    data_list = [
        'data_07_02',
        'data_07_15',
        'data_07_28',
        'data_08_12',
        'data_09_02',
        'data_09_11',
        'data_09_24',
        'data_10_07'
    ]

    ObservationKey = parser.get('Filenames', 'ObservationKey')
    logger.info("Config file objects have been set...")

    # logger.info("Load and clean the data...")
    # soil_data = las_data(data_07_02)
    # canopy_data = las_data(data_09_02)

    logger.info('Importing the ground data...')
    HumanData = ground_data(HumanData)

    # make list of dataframes
    df_list = []

    # extract canopy manually taken heights from pandas.DataFrame
    manual_ht, plot = extract_canopy_ht(HumanData)

    df_list.append(pd.DataFrame({"manual_ht":manual_ht, "plot":plot}))

    # objfn = -0.8094930493649393
    q = np.array([0.1, 0.2, 0.21092202170754804, 0.3, 0.4, 0.5, 0.6, 0.7,
            0.8, 0.9, 0.9946622335380833, 1.0
        ]
    )

    for key in data_list:
        logger.info("Load %s" % key)
        fname = parser.get('Filenames', key)
        data = las_data(fname)

        logger.info("Clean %s" % key)
        points, size, name = las_extract(
            data,
            colname = 'z_position',
            groupcol = 'shpID',
            grouprow = HumanData['plot'].values
        )

        # extract quantiles
        logger.info("Calculate quantiles")
        data_q = get_quantile(q, points, size)

        # make header
        header = [key + "." + str(e) for e in q]

        # make DataFrame
        df = pd.DataFrame(data_q, columns = header)

        # add another column
        df[key + ".name"] = name

        df_list.append(df)


    export_data = pd.concat(df_list, axis = 1)

    export_data.to_csv("quantiles.csv", index = False)
