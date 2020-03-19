#!/usr/bind/env python3

"""
Create a random forest to predict hand-measured height from robot height
values.
"""

__author__ = "Scott Teresi, Anna Haber"

import pandas as pd
import numpy as np
import argparse
import logging
import coloredlogs
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# TODO Scott, do we need the extract_dsm and extract_canopy_ht
# functions that Robert wrote? I'd think we would if we want to
# run our machine learning on height values.
from load_data.import_obs_data import obs_data, geno_plot_dict
from load_data.import_image_data import image_data, extract_dsm
from load_data.import_ground_data import ground_data, extract_canopy_ht
from load_data.replace_names import replace_names


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

    parser.add_argument('human_data', type=str, default=os.path.join(
                        path_main, '../../', 'data'),
                        help='parent path of human data file')
    parser.add_argument('drone_data', type=str, default=os.path.join(
                        path_main, '../../', 'data'),
                        help='parent path of drone data file')
    parser.add_argument('obs_data', type=str,  default=os.path.join(
                        path_main, '../../', 'data'),
                        help='parent path of observation key file')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='set debugging level to DEBUG')
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

    logger.info('Load and clean the ground truth data...')
    human_data = ground_data(args.human_data)

    logger.info('Load and clean the drone data...')
    drone_data = image_data(args.drone_data)

    logger.info('Load the observation key...')
    obs_key = obs_data(args.obs_data)

    logger.info('Constructing dictionary of genotype vs. plot ID...')
    GenoPlotDict = geno_plot_dict(obs_key)

    logger.info('Replace plot ID with genotype for drone data...')
    DroneData_Replaced = replace_names(drone_data, GenoPlotDict, 'plot_id')

    logger.info('Replace plot ID with genotype for ground truth data...')
    HumanData_Replaced = replace_names(human_data, GenoPlotDict, 'plot')
