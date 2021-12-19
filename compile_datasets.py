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


def find_nearest_ocean_element(oc_data_month, AIS_lat, AIS_lon, AIS_ts):
    """
    Find elements in dataset of oceanic variables closest to experimental values
    and return them.

    Input:

            oc_data_month
            AIS_lat
            AIS_lon
            AIS_ts

    Output:

            oceanic_lat
            oceanic_lon
            oceanic_ts

    """

    # find nearest elements in oceanic datasets
    oceanic_lat = find_nearest_element(oc_data_month["lat"].values, AIS_lat)
    oceanic_lon = find_nearest_element(oc_data_month["lon"].values, AIS_lon)
    oceanic_ts  = find_nearest_element(oc_data_month["ts"].values, AIS_ts)

    return oceanic_lat, oceanic_lon, oceanic_ts


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
