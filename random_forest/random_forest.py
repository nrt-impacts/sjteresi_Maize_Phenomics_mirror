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


def verify_human_replaced_files(nonreplaced_human_path, replaced_human_path,
                                replacement_dict):
    if os.path.exists(replaced_human_path):
        logger.info('Importing previously name replaced human data from disk...')
        replaced_human = pd.read_csv(replaced_human_path, header='infer',
                                     sep='\t')
    else:
        logger.info('Previously replaced human data does not exist...')
        logger.info('Importing unfiltered human data from raw...')
        human = ground_data(nonreplaced_human_path)
        replaced_human = replace_names(human,replacement_dict, 'plot')
        replaced_human.to_csv(replaced_human_path, sep='\t', header=True)
    return replaced_human

def verify_drone_replaced_files(nonreplaced_drone_path, replaced_drone_path,
                                replacement_dict):
    # TODO clean and possibly merge with the other verify function to clear
    # confusion
    if os.path.exists(replaced_drone_path):
        logger.info('Importing previously name replaced drone data from disk...')
        replaced_drone = pd.read_csv(replaced_drone_path, header='infer',
                                     sep='\t')
    else:
        logger.info('Previously replaced drone data does not exist...')
        logger.info('Importing unfiltered drone data from raw...')
        drone = image_data(nonreplaced_drone_path)
        replaced_drone = replace_names(drone,replacement_dict, 'plot_id')
        replaced_drone.to_csv(replaced_drone_path, sep='\t', header=True)
    return replaced_drone

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load input data')
    path_main = os.path.abspath(__file__)

    parser.add_argument('--human_data', '-g', type=str, default=os.path.join(
                        path_main, '../../', 'data/ground_data_2019.csv'),
                        help='parent path of human data file')
    parser.add_argument('--drone_data', '-d', type=str, default=os.path.join(
                        path_main, '../../', 'data/point_data_6in_2019obs.csv'),
                        help='parent path of drone data file')
    parser.add_argument('--obs_data', '-o', type=str,  default=os.path.join(
                        path_main, '../../', 'data/obs_2019_key.csv'),
                        help='parent path of observation key file')

    parser.add_argument('--replaced_human', '-x', type=str,  default=os.path.join(
                        path_main, '../../', 'data/replaced/replaced_human.tsv'),
                        help='parent path of replaced human data')
    parser.add_argument('--replaced_drone', '-z', type=str,  default=os.path.join(
                        path_main, '../../', 'data/replaced/replaced_drone.tsv'),
                        help='parent path of genotype replaced drone data')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='set debugging level to DEBUG')
    args = parser.parse_args()
    args.human_data = os.path.abspath(args.human_data)
    args.drone_data = os.path.abspath(args.drone_data)
    args.obs_data = os.path.abspath(args.obs_data)
    args.replaced_human = os.path.abspath(args.replaced_human)
    args.replaced_drone = os.path.abspath(args.replaced_drone)
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = logging.getLogger(__name__)
    coloredlogs.install(level=log_level)

    logger.info("Validating command line arguments")
    for argname, argval in vars(args).items():
        logger.debug("%-12s: %s" % (argname, argval))
    validate_args(args, logger)
    logger.info("Importing")

    logger.info('Load the observation key...')
    obs_key = obs_data(args.obs_data)

    logger.info('Constructing dictionary of genotype vs. plot ID...')
    GenoPlotDict = geno_plot_dict(obs_key)

    logger.info('Checking for replaced/filtered data')

    logger.info('Load and clean the ground truth data...')
    human_data = verify_human_replaced_files(args.human_data, args.replaced_human,
                                GenoPlotDict)
    drone_data = verify_drone_replaced_files(args.drone_data, args.replaced_drone,
                                GenoPlotDict)

