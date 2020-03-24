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
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pydot
from sklearn.tree import export_graphviz
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from load_data.import_obs_data import obs_data, geno_plot_dict
from load_data.import_image_data import image_data
from load_data.import_ground_data import ground_data
from load_data.replace_names import replace_names

def read_quantile_data(quantile_data_location, replace_names, GenoPlotDict):
    """
    TODO add args
    """
    quantile_data = pd.read_csv(quantile_data_location, header='infer')
    quantile_data.drop(columns=['manual_ht'], inplace=True)
    quantile_data = replace_names(quantile_data, GenoPlotDict, 'plot')
    quantile_data = quantile_data.loc[:,
                                      ~quantile_data.columns.str.contains('name')]

    return quantile_data

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

def test_code():
    # Test Code that does not necessarily work
    # logger.info('Visualizing a single decision tree...')
    # tree = rf.estimators_[5]
    # Export image to a .dot file
    # export_graphviz(tree, out_file = args.tree_dot, feature_names = 
                    # feature_list, rounded = True, precision = 1)
    # Use dot file to create a graph
    # (graph, ) = pydot.graph_from_dot_file(args.tree_dot)
    # Write graph to a png file
    # graph.write_png('tree.png')



    # Get numerical feature importances
    importances = list(rf.feature_importances_)
    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature,
                           importance in zip(feature_list, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1],
                                 reverse = True)
    # Print out the feature and importances
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in
     feature_importances];


    # New random forest with only the two most important variables
    rf_most_important = RandomForestRegressor(n_estimators= 250,
                                              random_state=42)
    # Extract the two most important features
    important_indices = [feature_list.index('data_10_07.0.9946622335380833'),
                         feature_list.index('data_10_07.1.0')]
    train_important = train_features[:, important_indices]
    test_important = test_features[:, important_indices]
    # Train the random forest
    rf_most_important.fit(train_important, train_labels)
    # Make predictions and determine the error
    predictions = rf_most_important.predict(test_important)
    errors = abs(predictions - test_labels)
    # Display the performance metrics
    print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
    mape = np.mean(100 * (errors / test_labels))
    accuracy = 100 - mape
    print('Accuracy:', round(accuracy, 2), '%.')

    # Notebooks
    # Set the style
    plt.style.use('fivethirtyeight')
    # list of x locations for plotting
    x_values = list(range(len(importances)))
    # Make a bar chart
    plt.bar(x_values, importances, orientation = 'vertical')
    # Tick labels for x axis
    plt.xticks(x_values, feature_list, rotation='vertical')
    # Axis labels and title
    plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable Importances')
    plt.show()

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
    parser.add_argument('--quantile_data', '-q', type=str,  default=os.path.join(
                        path_main, '../../', 'data/quantiles.csv'),
                        help='parent path of quantiles file')
    parser.add_argument('--replaced_human', '-x', type=str,  default=os.path.join(
                        path_main, '../../', 'data/replaced/replaced_human.tsv'),
                        help='parent path of replaced human data')
    parser.add_argument('--replaced_drone', '-z', type=str,  default=os.path.join(
                        path_main, '../../', 'data/replaced/replaced_drone.tsv'),
                        help='parent path of genotype replaced drone data')
    parser.add_argument('--tree_dot', '-r', type=str, default=os.path.join(
                        path_main, '../../', 'random_forest/tree.dot'),
                        help='parent path of single tree visualization')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='set debugging level to DEBUG')
    args = parser.parse_args()
    args.human_data = os.path.abspath(args.human_data)
    args.drone_data = os.path.abspath(args.drone_data)
    args.obs_data = os.path.abspath(args.obs_data)
    args.quantile_data = os.path.abspath(args.quantile_data)
    args.replaced_human = os.path.abspath(args.replaced_human)
    args.replaced_drone = os.path.abspath(args.replaced_drone)
    args.tree_dot = os.path.abspath(args.tree_dot)
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
    
    logger.info('Get quantile data')
    quantile_data = read_quantile_data(args.quantile_data, replace_names,
                                       GenoPlotDict)
    print(quantile_data.head())
    print(quantile_data.shape)

    # One-hot encoding to make genotype binary so it can be input
    # to the machine learning model.
    logger.info('Convert Genotype of drone data to numerical...')
    QuantNumeric = pd.get_dummies(quantile_data)

    # Setting up the features and labels
    logger.info('Formatting labels...')
    labels = np.array(human_data['MeanPHeight'])

    logger.info('Saving feature names...')
    feature_list = list(QuantNumeric.columns)

    logger.info('Formatting features...')
    features = np.array(QuantNumeric)
    print(features.shape)

    logger.info('Partitioning training and testing data...')
    train_features, test_features, train_labels, test_labels = train_test_split(
            features, labels, test_size=0.25, random_state=42)
    # print('Training features shape: ', train_features.shape)
    # print('Training labels shape: ', train_labels.shape)
    # print('Testing features shape: ', test_features.shape)
    # print('Testing labels shape: ', test_labels.shape)

    # Run the random forest model
    logger.info('Instantiating model...')
    rf = RandomForestRegressor(n_estimators=200, random_state=42)

    logger.info('Train the model on training data...')
    rf.fit(train_features, train_labels);

    logger.info('Making predictions on testing data...')
    predictions = rf.predict(test_features)

    logger.info('Calculating absolute errors...')
    errors = abs(predictions - test_labels)
    print('Mean absolute error: ', round(np.mean(errors), 2))

    logger.info('Calculating mean absolute percentage error...')
    mape = 100 * (errors/test_labels)
    accuracy = 100 - np.mean(mape)
    print('Accuracy: ', round(accuracy, 2), '%.')





