#!/usr/bind/env python3

"""
Create a random forest to predict robot height values from hand-measured height
values.
"""

__author__ = "Scott Teresi, Anna Haber"

import pandas as pd
import numpy as np
import argparse
import logging
import coloredlogs

# TODO Anna add the import commands for the functions from the other files, I
# think the .. notation is for going back two folders. Maybe think about this.
# Can be tricky, my ViM automatically tells me where I am when doing these .
# notations, so be careful.
from ..load_data.import_obs_data


def validate_args(args, logger):
    """Raise if an input argument in invalid."""

    if not os.path.isfile(args.human_data):
        logger.critical("Argument 'human_data' is not file")
        raise ValueError("%s is not a directory" % (args.human_data))
    if not os.path.isfile(args.drone_data):
        logger.critical("Argument 'drone_data' is not file")
        raise ValueError("%s is not a directory" % (args.drone_data))
    # TODO Anna add the check for the obs data, mimic the structure as above


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load input data')
    path_main = os.path.abspath(__file__)
    # TODO Add default command line argument to the python file for the data
    # sets, look up the bottom of my code in TE Density density.py if you are
    # truly stuck. Since this default parameter will probably require a common
    # path, we should tell everyone in the lab to make a common path, maybe
    # store the data in a /data folder in the main repository folder.
    parser.add_argument('human_data', type=str, help='parent path of human
                        measured height data file')
    parser.add_argument('drone_data', type=str, help='parent path of drone
                        measured height data file')
    parser.add_argument('obs_data', type=str, help='parent path of observation
                        key file')
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
