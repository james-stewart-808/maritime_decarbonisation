"""
weather_data_cleaning.py

Function to join dynamic and static weather datasets. Steps include...

        X.1     combine station latitude and longitude from static dataset with
                dynamic dataset.


A full description of the research and references used can be found in README.md

"""


def add_weather_coordinates(weather_observation, weather_stations):
    """
    X.1 Add latitude and longitude coordinates to dynamic weather observations
    from static weather_stations dataset.

    Input:

            weather_observation         ...
            weather_stations            ...

    Output:

            weather_final               ...

    """

    # define empty latitude and longitude arrays
    latitude = np.zeros(len(weather_observation))
    longitude = np.zeros(len(weather_observation))

    # iterate through weather observations and assign coordinates
    for row in range(len(weather_observation)):

        # use id_station as key between datasets
        temp_weather_df = weather_stations[weather_stations["id_station"] == weather_observation["id_station"][row]]
        # assign coordinate values to empty lat and lon arrays
        latitude[row] = temp_weather_df["latitude"].values[0]
        longitude[row] = temp_weather_df["longitude"].values[0]

    # add derived data series to weather_observation dataframe
    weather_observation["latitude"] = weather_latitude
    weather_observation["longitude"] = weather_longitude

    # drop unnecessary fields
    weather_final = weather_observation.drop(["id_station", "Tn", "Tx", "U", "ff10", "ff3", "VV", "Td", "RRR", "tR"], axis=1)

    # option to save final joined weather dataset
    # weather_final.to_csv("datasets/weather_final.csv")

    return weather_final
