"""
__main__.py

The main executable file to used in the processing of all files related to the
maritime_decarbonisation repository.


Databases used in the study include..

        static vessel information           Ray et al (2017)
        dynamic vessel AIS dataset          Ray et al (2017)
        oceanic condition data              Boudiere et al (2013)


A full description of the research and references used can be found in README.md

Things to-do...

    - add comments in

"""


### Import libraries and data processing files ###

import sys
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import AIS_data_cleaning
import ts_by_month
import weather_data_cleaning
import compile_datasets



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


    # 6. Iterate through AIS dynamic data
    for dyn_idx in range(len(dynamic_sample_full)):

        # get AIS coordintes and timestamp
        AIS_lat = dynamic_sample_full["lat"].values[dyn_idx]
        AIS_lon = dynamic_sample_full["lon"].values[dyn_idx]
        AIS_ts  = dynamic_sample_full["t"].values[dyn_idx]


        # obtain oceanic parameters at closest point and time
        try:

            # if in October
            if AIS_ts > month_ts_array[0] & AIS < month_ts_array[1]:

                # find closest measuring point and time
                oceanic_lat, oceanic_lon, oceanic_ts = find_nearest_ocean_element(oc_oct, AIS_lat, AIS_lon, AIS_ts)

                # obtain oceanic data from this point and time
                ocean_lat_df = oc_october_final[oc_october_final["lat"] == ocean_lat]
                ocean_lon_df = ocean_lat_df[ocean_lat_df["lon"] == ocean_lon]
                ocean_t_df = ocean_lon_df[ocean_lon_df["ts"] == ocean_ts]


            # if in November
            elif AIS_ts > month_ts_array[2] & AIS < month_ts_array[3]:

                # find closest measuring point and time
                oceanic_lat, oceanic_lon, oceanic_ts = find_nearest_ocean_element(oc_nov, AIS_lat, AIS_lon, AIS_ts)

                # obtain oceanic data from this point and time
                ocean_lat_df = oc_november_final[oc_october_final["lat"] == ocean_lat]
                ocean_lon_df = ocean_lat_df[ocean_lat_df["lon"] == ocean_lon]
                ocean_t_df = ocean_lon_df[ocean_lon_df["ts"] == ocean_ts]


            # if in December
            elif AIS_ts > month_ts_array[4] & AIS < month_ts_array[5]:

                # find closest measuring point and time
                oceanic_lat, oceanic_lon, oceanic_ts = find_nearest_ocean_element(oc_dec, AIS_lat, AIS_lon, AIS_ts)

                # obtain oceanic data from this point and time
                ocean_lat_df = oc_december_final[oc_october_final["lat"] == ocean_lat]
                ocean_lon_df = ocean_lat_df[ocean_lat_df["lon"] == ocean_lon]
                ocean_t_df = ocean_lon_df[ocean_lon_df["ts"] == ocean_ts]


            # if in January
            elif AIS_ts > month_ts_array[6] & AIS < month_ts_array[7]:

                # find closest measuring point and time
                oceanic_lat, oceanic_lon, oceanic_ts = find_nearest_ocean_element(oc_jan, AIS_lat, AIS_lon, AIS_ts)

                # obtain oceanic data from this point and time
                ocean_lat_df = oc_january_final[oc_october_final["lat"] == ocean_lat]
                ocean_lon_df = ocean_lat_df[ocean_lat_df["lon"] == ocean_lon]
                ocean_t_df = ocean_lon_df[ocean_lon_df["ts"] == ocean_ts]


            # if in February
            elif AIS_ts > month_ts_array[8] & AIS < month_ts_array[9]:

                # find closest measuring point and time
                oceanic_lat, oceanic_lon, oceanic_ts = find_nearest_ocean_element(oc_feb, AIS_lat, AIS_lon, AIS_ts)

                # obtain oceanic data from this point and time
                ocean_lat_df = oc_february_final[oc_october_final["lat"] == ocean_lat]
                ocean_lon_df = ocean_lat_df[ocean_lat_df["lon"] == ocean_lon]
                ocean_t_df = ocean_lon_df[ocean_lon_df["ts"] == ocean_ts]


            # if in March
            else:

                # find closest measuring point and time
                oceanic_lat, oceanic_lon, oceanic_ts = find_nearest_ocean_element(oc_mar, AIS_lat, AIS_lon, AIS_ts)

                # obtain oceanic data from this point and time
                ocean_lat_df = oc_march_final[oc_october_final["lat"] == ocean_lat]
                ocean_lon_df = ocean_lat_df[ocean_lat_df["lon"] == ocean_lon]
                ocean_t_df = ocean_lon_df[ocean_lon_df["ts"] == ocean_ts]


            # obtain significant height (hs), mean direction (dir) and mean
            # wave length (lm) from that data point
            ocean_hs[row] = ocean_t_df["hs"].values[0]
            ocean_dir[row] = ocean_t_df["dir"].values[0]
            ocean_lm[row] = ocean_t_df["lm"].values[0]


        # if unknown
        except:

            ocean_hs[row] = None
            ocean_dir[row] = None
            ocean_lm[row] = None


        # find closest measuring point and time in historic weather database
        weather_lat, weather_lon, weather_ts = find_nearest_weather_element(mmsi_lat, mmsi_lon, mmsi_ts)


        # obtain weather data from this point and time
        weather_lat_df = weather_final[weather_final["latitude"] == weather_lat]
        weather_lon_df = weather_lat_df[weather_lat_df["longitude"] == weather_lon]
        weather_t_df = weather_lon_df[weather_lon_df["local_time"] == weather_ts]


        # obtain wind direction (wind_ID), mean wind speed (Ff), atmospheric
        # pressure (P) and air temperature at 2 meter elevation from that datapoint

        try:

            weather_wind_ID[row] = weather_t_df["id_windDirection"].values[0]
            weather_Ff[row] = weather_t_df["Ff"].values[0]
            weather_P[row]  = weather_t_df["P"].values[0]
            weather_T[row]  = weather_t_df["T"].values[0]


        # account for missing data
        except:

            weather_wind_ID[row] = None
            weather_Ff[row] = None
            weather_P[row]  = None
            weather_T[row]  = None


    # Add these additional oceanic variables to dynamic AIS dataset
    dynamic_sample_full["ocean_hs"] = ocean_hs
    dynamic_sample_full["ocean_dir"] = ocean_dir
    dynamic_sample_full["ocean_lm"] = ocean_lm


    # Add these additional weather variables to dynamic AIS dataset
    dynamic_sample_full["weather_wind_ID"] = weather_wind_ID
    dynamic_sample_full["weather_Ff"] = weather_Ff
    dynamic_sample_full["weather_P"] = weather_P
    dynamic_sample_full["weather_T"] = weather_T

    # clean and give option to save
    full_dynamic_set =dynamic_sample_full
    full_dynamic_set.drop(["sourcemmsi"], axis=1)
    # full_dynamic_set.to_csv("datasets/full_dynamic_set.csv")
