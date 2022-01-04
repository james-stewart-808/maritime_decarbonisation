"""
oceanic_matching.py

Script to match dynamic AIS samples with closest matching oceanic variables.
Steps include...

        X.1


A full description of the research and references used can be found in README.md
"""

def ocean_parameter_matching(AIS_lat, AIS_lon, AIS_ts):
    """
    X. Use coordinates and timestamp from an AIS entry and return closest
    matching variables.

    Inputs:

            AIS_lat        latitude of AIS entry.
            AIS_lon        longitude of AIS entry.
            AIS_ts         timestamp of AIS entry.

    Outputs:

            ocean_hs       wave height.
            ocean_dir      wave direction.
            ocean_lm       mean wave length.

    """

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

    return ocean_hs, ocean_dir, ocean_lm





"""
###############################
### FUTURE IMPROVED VERSION ###
###############################

def find_nearest_ocean_element(oc_data_month, AIS_lat, AIS_lon, AIS_ts):

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



    # find nearest elements in oceanic datasets
    oceanic_lat = find_nearest_element(oc_data_month["lat"].values, AIS_lat)
    oceanic_lon = find_nearest_element(oc_data_month["lon"].values, AIS_lon)
    oceanic_ts  = find_nearest_element(oc_data_month["ts"].values, AIS_ts)

    return oceanic_lat, oceanic_lon, oceanic_ts

"""
