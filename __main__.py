"""
__main__.py

The main executable file to used in the processing of all files related to the
maritime_decarbonisation repository.


Databases used in the study include..

        static vessel information           Ray et al (2017)
        dynamic vessel AIS dataset          Ray et al (2017)
        oceanic condition data              Boudiere et al (2013)


A full description of the research and references used can be found in README.md

To-do/improvements...

    - add comments in
    - combine monthly oceanic datasets in one

"""


### Import libraries ###
import sys
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

### Import external functions ###
import AIS_data_cleaning
import ts_by_month
import weather_data_cleaning
import oceanic_matching
import weather_matching


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

            static_df       static vessel dataset.
            dynamic_df      dynamic AIS vessel dataset.

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
    weather_observation, weather_stations, weather_wind_direction = load_weather_data() # weather_wind_direction not used

    # 1. Data cleaning and generation of sample
    dynamic_sample = AIS_data_cleaning(static_dataset, dynamic_dataset)

    # 2. Addition of volume and draught features
    dynamic_sample_full = feature_generation(dynamic_sample)

    # 3. Obtain timestamps for beginning and end of each month
    month_ts_array = ts_by_month(oc_oct, oc_nov, oc_dec, oc_jan, oc_feb, oc_mar)

    # 4. Combine dynamic and static weather datasets (weather_obervation and weather_stations)
    weather_final = add_weather_coordinates(weather_observation, weather_stations)

    # 5. data_merging
    ocean_lat, ocean_lon, ocean_ts = nearest_ocean_station(month_ts_array)

    # 6. Genereate oceanic and weather parameter fields
    ocean_hs = np.zeros(len(dynamic_sample_full))
    ocean_dir = np.zeros(len(dynamic_sample_full))
    ocean_lm = np.zeros(len(dynamic_sample_full))

    weather_wind_ID = np.zeros(len(dynamic_sample_full))
    weather_Ff = np.zeros(len(dynamic_sample_full))
    weather_P = np.zeros(len(dynamic_sample_full))
    weather_T = np.zeros(len(dynamic_sample_full))

    for dyn_idx in range(len(dynamic_sample_full)):

        # get AIS coordintes and timestamp
        AIS_lat = dynamic_sample_full["lat"].values[dyn_idx]
        AIS_lon = dynamic_sample_full["lon"].values[dyn_idx]
        AIS_ts  = dynamic_sample_full["t"].values[dyn_idx]

        # obtain closest match of oceanic parameters (hs, dir, lm)
        ocean_hs_idx, ocean_dir_idx, ocean_lm_idx = ocean_parameter_matching(AIS_lat, AIS_lon, AIS_ts)

        # assign to arrays
        ocean_hs[dyn_idx] = ocean_hs_idx
        ocean_dir[dyn_idx] = ocean_dir_idx
        ocean_lm[dyn_idx] = ocean_lm_idx


        # obtain closest match of weather paramters (wind_ID, Ff, P, T)
        weather_wind_ID_idx, weather_Ff_idx, weather_P_idx, weather_T_idx = weather_parameter_matching(AIS_lat, AIS_lon, AIS_ts)

        # assign to arrays
        weather_wind_ID[dyn_idx] = weather_wind_ID_idx
        weather_Ff[dyn_idx] = weather_Ff_idx
        weather_P[dyn_idx] = weather_P_idx
        weather_T[dyn_idx] = weather_T_idx


    # Add these additional oceanic variables to dynamic AIS dataset
    dynamic_sample_full["ocean_hs"] = ocean_hs
    dynamic_sample_full["ocean_dir"] = ocean_dir
    dynamic_sample_full["ocean_lm"] = ocean_lm

    dynamic_sample_full["weather_wind_ID"] = weather_wind_ID
    dynamic_sample_full["weather_Ff"] = weather_Ff
    dynamic_sample_full["weather_P"] = weather_P
    dynamic_sample_full["weather_T"] = weather_T


    # clean and give option to save
    full_dynamic_set = dynamic_sample_full
    full_dynamic_set.drop(["sourcemmsi"], axis=1)

    # save to local directory
    full_dynamic_set.to_csv("datasets/full_dynamic_set.csv")
