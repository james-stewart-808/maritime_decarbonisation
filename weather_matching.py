"""
compile_datasets.py

Script to compile xxx. Steps include...

        X.1


A full description of the research and references used can be found in README.md
"""


def find_nearest_element(array, value):
    """
    Function to find nearest element in an array.

    Input:

            array                   set values in existing array
            value                   experimental value.

    Output:

            nearest_element         element in existing array closest to
                                    experimental value.

    """

    # convert to numpy array and find closest array element as an index
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()

    # convert index to element value
    nearest_element = array[index]

    return nearest_element



def find_nearest_weather_element(weather_final, AIS_lat, AIS_lon, AIS_ts):
    """
    Find elements in dataset of weather variables closest to experimental values
    and return them.

    Input:

            AIS_lat
            AIS_lon
            AIS_ts

    Output:

            weather_lat
            weather_lon
            weather_ts

    """

    # find nearest elements in weather datasets
    weather_lat = find_nearest_element(weather_final["latitude"].values, AIS_lat)
    weather_lon = find_nearest_element(weather_final["longitude"].values, AIS_lon)
    weather_ts = find_nearest_element(weather_final["latitude"].values, AIS_ts)

    return weather_lat, weather_lon, weather_ts




def weather_parameter_matching(AIS_lat, AIS_lon, AIS_ts, weather_final):

    # obtain closest match of weather parameters (lat, lon)
    weather_lat, weather_lon, weather_ts = find_nearest_weather_element(weather_final, AIS_lat, AIS_lon, AIS_ts)


    # algorithm for getting data assoicated with these points
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


    return weather_wind_ID, weather_Ff, weather_P, weather_T
