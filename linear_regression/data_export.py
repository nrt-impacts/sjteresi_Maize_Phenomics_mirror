
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

from load_data.import_image_data import image_data, extract_dsm
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
    config['Filenames'] = {'HumanData': 'ground_data_2019.csv',
                           'DroneData': 'point_data_6in_2019obs.csv',
                           'ObservationKey': 'obs_2019_key.csv'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    logger.info("Reading config file...")
    parser = ConfigParser()
    parser.read('config.ini')
    # Set the objects from the parser
    HumanData = parser.get('Filenames', 'HumanData')
    DroneData = parser.get('Filenames', 'DroneData')
    ObservationKey = parser.get('Filenames', 'ObservationKey')
    logger.info("Config file objects have been set...")

    logger.info("Load and clean the data...")
    DroneData = image_data(DroneData)

    logger.info('Importing the ground data...')
    HumanData = ground_data(HumanData)

    # extract data from columns for soil
    soil, soil_size = extract_dsm(
        DroneData,
        colname = "DSM_7_2_19",
        groupcol = "plot_id",
        grouprow = HumanData["plot"].values
    )


    # extract data from columns for canopy
    canopy, canopy_size = extract_dsm(
        DroneData,
        colname = "DSM_9_2_19", # this is the last date (caution: dead plants?)
        groupcol = "plot_id",
        grouprow = HumanData["plot"].values
    )

    # extract canopy manually taken heights from pandas.DataFrame
    manual_ht = extract_canopy_ht(
        HumanData
    )

    # manually determnine quantile settings
    q = np.linspace(0.0, 1.0, 11)
    
    soil_q = get_quantile(q, soil, soil_size)
    canopy_q = get_quantile(q, canopy, canopy_size)
    soil_col = ["s" + str(e) for e in q]
    canopy_col = ["c" + str(e) for e in q]
    soil_df = pd.DataFrame(soil_q, columns = soil_col)
    canopy_df = pd.DataFrame(canopy_q, columns = canopy_col)
    manual_df = pd.DataFrame({"manual": manual_ht})
    export_data = pd.concat([soil_df, canopy_df, manual_df], axis = 1)
    
    export_data.to_csv("quantiles.csv", index = False)

