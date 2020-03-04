#!/usr/bin/env python3

# TODO implement a description for the entire file

__author__ = "Scott Teresi"

import logging
import coloredlogs
from configparser import ConfigParser

from load_data.import_image_data import image_data
from load_data.import_ground_data import ground_data
from load_data.import_obs_data import obs_data
from load_data.import_obs_data import geno_plot_dict
from replace_names import replace_names

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

    logger.info('Importing the ground data...')
    ObsData = obs_data(ObservationKey)

    logger.info('Creating plotID vs. genotype dictionary...')
    GenoPlotDict = geno_plot_dict(ObsData)

    logger.info('Replacing plotID with genotype for HumanData...')
    ReplacedHumanData = replace_names(HumanData, GenoPlotDict, 'plot')

    logger.info('Replacing plotID with genotype for DroneData...')
    ReplacedDroneData = replace_names(DroneData, GenoPlotDict, 'plot_id')
