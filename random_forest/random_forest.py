#!/usr/bind/env python3

"""
Create a random forest to predict robot height values from hand-measured height
values.
"""
# Scott, I thought we agreed it was the other way around?
# (predicting hand-measured height from robot height)

__author__ = "Scott Teresi, Anna Haber"

import pandas as pd
import numpy as np
import argparse
import logging
import coloredlogs

# TODO Scott, do we need the extract_dsm and extract_canopy_ht
# functions that Robert wrote? I'd think we would if we want to
# run our machine learning on height values.
from ..load_data.import_obs_data import obs_data, geno_plot_dict
from ..load_data.import_image_data import image_data, extract_dsm
from ..load_data.import_ground_data import ground_data, extract_canopy_ht
from ..load_data.replace_names import replace_names


def validate_args(args, logger):
    """Raise if an input argument is invalid."""

    if not os.path.isfile(args.human_data):
        logger.critical("Argument 'human_data' is not file")
        raise ValueError("%s is not a directory" % (args.human_data))
    if not os.path.isfile(args.drone_data):
        logger.critical("Argument 'drone_data' is not file")
        raise ValueError("%s is not a directory" % (args.drone_data)) 
    if not os.path.isfile(args.obs_data):
        logger.critical("Argument 'obs_data' is not file")
        raise ValueError("%s is not a directory" % (args.obs_data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load input data')
    path_main = os.path.abspath(__file__)

    parser.add_argument('human_data', type=str, help='parent path of human
                        measured height data file')
    parser.add_argument('drone_data', type=str, help='parent path of drone
                        measured height data file')
    parser.add_argument('obs_data', type=str, help='parent path of observation
                        key file')
    parser.add_argument('--path_to_data', '-p', type=str, default=os.path.join(
                        path_main, '..', 'data'), help='path to data files within 
                        git repository directory')
    args = parser.parse_args()
    args.human_data = os.path.abspath(args.human_data)
    args.drone_data = os.path.abspath(args.drone_data)
    args.obs_data = os.path.abspath(args.obs_data)
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = logging.getLogger(__name__)
    coloredlogs.install(level=log_level)

    logger.info("Validating command line arguments")
    for argname, argval in vars(args).items():
        logger.debug("%-12s: %s" % (argname, argval))
    validate_args(args, logger)

    logger.info("Ready to import")

    # Importing the data
    human_data = parser.get('human_data')
    drone_data = parser.get('drone_data')
    obs_key = parser.get('obs_data')
    logger.info('Config file objects have been set...')

    logger.info('Load and clean the drone data...')
    drone_data = image_data(drone_data)

    logger.info('Load and clean the ground truth data...')
    human_data = ground_data(human_data)

    logger.info('Load the observation key...')
    obs_key = obs_data(obs_key)

    logger.info('Constructing dictionary of genotype vs. plot ID...')
    GenoPlotDict = geno_plot_dict(obs_key)

    logger.info('Replace plot ID with genotype for drone data...')
    DroneData_Replaced = replace_names(drone_data, GenoPlotDict, 'plot_id')

    logger.info('Replace plot ID with genotype for ground truth data...')
    HumanData_Replaced = replace_names(human_data, GenoPlotDict, 'plot')
