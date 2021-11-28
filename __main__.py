"""
__main__.py

The main executable file to used in the processing of all files related to the
maritime_decarbonisation repository.


Databases used in the study include..

        static vessel information           Ray et al (2017)
        dynamic vessel AIS dataset          Ray et al (2017)
        oceanic condition data              Boudiere et al (2013)


A full description of the research and references used can be found in README.md

"""


### Import libraries and data processing files ###

import sys
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import data_cleaning
import weather_merge
import ETR_scenarios




def usage_check():
    """
    0. Check terminal call usage and return dataset directory if ok.

    Outputs:

            data_dir        directory of datasets used.
    """

    # usage check
    if len(sys.argv) != 2:
        print("Usage: python3 __main__.py datasets")
        sys.exit(1)

    else:
        data_dir = sys.argv[1]

    return data_dir




def load_AIS_data(data_dir):
    """
    0. Check terminal call usage and load dataset into pandas dataframe using
    arguments given from command line.

    Inputs:

            data_dir        directory of datasets used.

    Outputs:

            static_df       static vessel dataset
            dynamic_df      dynamic AIS vessel dataset

    """

    # form full directories
    static_filename = data_dir + r'/nari_static.csv'
    dynamic_filename = data_dir + r'/nari_dynamic.csv'


    # read datasets into dataframes
    static_dataset = pd.read_csv(static_filename)
    dynamic_dataset = pd.read_csv(dynamic_filename)

    return static_dataset, dynamic_dataset,




def load_oceanic_data(data_dir):
    """
    0. Check terminal call usage and load dataset into pandas dataframe using
    arguments given from command line.

    Inputs:

            data_dir        directory of datasets used.

    Outputs:

            static_df       static vessel dataset
            dynamic_df      dynamic AIS vessel dataset

    """

    # form full directories
    oc_oct_filename = data_dir + r'/oc_october.csv'
    oc_nov_filename = data_dir + r'/oc_november.csv'
    oc_dec_filename = data_dir + r'/oc_december.csv'
    oc_jan_filename = data_dir + r'/oc_january.csv'
    oc_feb_filename = data_dir + r'/oc_february.csv'
    oc_mar_filename = data_dir + r'/oc_march.csv'

    # read datasets into dataframes
    oc_oct = pd.read_csv(oc_oct_filename).drop(['dpt', 'wlv'], axis=1)
    oc_nov = pd.read_csv(oc_nov_filename).drop(['dpt', 'wlv'], axis=1)
    oc_dec = pd.read_csv(oc_dec_filename).drop(['dpt', 'wlv'], axis=1)
    oc_jan = pd.read_csv(oc_jan_filename).drop(['dpt', 'wlv'], axis=1)
    oc_feb = pd.read_csv(oc_feb_filename).drop(['dpt', 'wlv'], axis=1)
    oc_mar = pd.read_csv(oc_mar_filename).drop(['dpt', 'wlv'], axis=1)

    return oc_oct, oc_nov, oc_dec, oc_jan, oc_feb, oc_mar




def load_weather_data(data_dir):
    """
    0. Check terminal call usage and load dataset into pandas dataframe using
    arguments given from command line.

    Inputs:

            data_dir        directory of datasets used.

    Outputs:

            static_df       static vessel dataset
            dynamic_df      dynamic AIS vessel dataset

    """

    # form full directories
    weather_observation_filename = data_dir + r'/table_weather_observation.csv'
    weather_stations_filename = data_dir + r'/table_weatherStation.csv'
    weather_wind_direction_filename = data_dir + r'/table_windDirection.csv'

    # read datasets into dataframes
    weather_observation = pd.read_csv(weather_observation_filename)
    weather_stations = pd.read_csv(weather_stations_filename)
    weather_wind_direction = pd.read_csv(weather_wind_direction_filename)

    return weather_observation, weather_stations, weather_wind_direction



if __name__ == '__main__':

    # 0. Import datasets
    static_dataset, dynamic_dataset = load_AIS_data()
    oc_oct, oc_nov, oc_dec, oc_jan, oc_feb, oc_mar = load_oceanic_data()
    weather_observation, weather_stations, weather_wind_direction = load_weather_data()

    # 1. Data cleaning and generation of sample
    dynamic_sample = data_cleaning(static_dataset, dynamic_dataset)

    # 2. Addition of volume and draught features
    dynamic_sample_full = feature_generation(dynamic_sample)

    # 3. Manipulation of oceanic dataset


    # data data_merging
    data_merging()


    # ETR_scenarios
    ETR_scenarios()
