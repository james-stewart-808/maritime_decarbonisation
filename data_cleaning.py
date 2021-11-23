"""
data_cleaning.py

Script to clean datasets. Steps in the cleaning process include...

        1.1     Removing unnecessary fields.
        1.2     Filtering for containerhips only.
        1.3     Filtering for only navigation codes related to the mission - 0, 3, 4, 8.
        1.4     Only entries with Speed over Ground greater than 5.


A full description of the research and references used can be found in README.md
"""


def remove_fields(static_df):
    """
    1.1 Removing unnecessary fields from the static dataset to reduce computation

    Input:

            static_df       static vessel dataset
            dynamic_df      dynamic AIS vessel dataset

    Output:

            static_df_rm    static vessel dataset with unused fields removed

    """

    static_df_rm = static_df.drop(['imonumber', 'callsign', 'shipname', 'eta', 'destination', 'mothershipmmsi', 't'], axis=1)

    return static_df_rm




def containership_filter(static_df_rm):
    """
    1.2 Filter to leave containership vessels only.

    Input:

            static_df_rm    static vessel dataset with unused fields removed

    Output:

            df

    """

    mmsi_bank, type_bank = np.zeros(len(static_df_rm)), np.zeros(len(static_df_rm))
    bank_counter = 0

    # for loop to find containerships only
    for ship_row in range(len(static_df_rm)):
        # use try to account for invalid ship type entries
        try:
            # if ship type is a containership (type 7)
            if str(int(static_df_rm["shiptype"][ship_row]))[0] == '7':

                mmsi_bank[bank_counter] = static_df_rm["sourcemmsi"][ship_row]
                type_bank[bank_counter] = int(static_df_rm["shiptype"][ship_row])

                bank_counter += 1

        except ValueError:
            pass





    return 0






### DATA CLEANING 2 - ONLY CONTAINERSHIPS ###

## Get Type Dataframe ##
# create pandas dataframe of them, without duplicates, and get indexes
type_dataframe = pd.DataFrame(data=[mmsi_bank, type_bank])
type_dataframe = type_dataframe.T
type_dataframe = type_dataframe.drop_duplicates(subset=0)
type_dataframe = type_dataframe.drop([186295], axis=0)
type_dataframe

# get indexes
type_dataframe_indexes = list(type_dataframe.index)
type_dataframe_indexes

# make into a dictionary
type_dictionary = {}
for ship_index in type_dataframe_indexes:
    type_dictionary.update({int(type_dataframe[0][ship_index]): int(type_dataframe[1][ship_index])})





# Get what's already saved - container_ship_movements
to_delete_from_dynamic_df = np.zeros(len(dynamic_df))
keys = type_dictionary.keys()
time_check = np.arange(0, 19000000, 500000)
sourcemmsi = dynamic_df["sourcemmsi"]
type(dynamic_df["sourcemmsi"])
iterator_range = np.arange(len(dynamic_df))


for iterator in iterator_range:

    if sourcemmsi[iterator] not in keys:
        to_delete_from_dynamic_df[iterator] = 1

    if iterator in time_check:
        print(iterator)


to_delete_from_dynamic_df_list = []
for iterator in iterator_range:
    if to_delete_from_dynamic_df[iterator] == 1:
        to_delete_from_dynamic_df_list.append(iterator)

    if iterator in time_check:
        print(iterator)


cleaned_dynamic_df = dynamic_df.drop(to_delete_from_dynamic_df_list, axis=0)
#cleaned_dynamic_df.to_csv("/Users/apple/Desktop/transport/Shipping/datasets/Ray et al/[P1] AIS Data/cleaned.csv")

# inspection
len(cleaned_dynamic_df["sourcemmsi"].unique())
len(type_dictionary)
type_dictionary[cleaned_dynamic_df["sourcemmsi"][18084111]]
len(cleaned_dynamic_df["sourcemmsi"].unique())

cleaned_dynamic_df

cleaned_dynamic_df = pd.read_csv('/Users/apple/Desktop/transport/Shipping/container_ship_movements.csv')










# Read in dataset with only containerships
cleaned_dynamic_df = pd.read_csv('/Users/apple/Desktop/transport/Shipping/container_ship_movements.csv')


### DATA CLEANING 3 - ONLY SPECIFIC MISSION PROFILES ###
# codes contain... 0 underway, 1 at anchor, 2 not under command, 3 restricted maneuverability, 4 constrained by draught, 5 moored, 8 underway sailing, 15 undefined
cleaned_dynamic_df["navigationalstatus"].unique()


# Is every ship considered definitely a containership? Yes
shiptype_new = []
for i in cleaned_dynamic_df["sourcemmsi"].unique():
    shiptype_new.append(type_dictionary[i])

pd.Series(shiptype_new).unique()


# keep only status codes: 0, 3, 4, 8
cleaned_dynamic_df
cleaned_dynamic_df[cleaned_dynamic_df['navigationalstatus'].isin([0, 3, 4, 8])]
cleaned_data_navstat = cleaned_dynamic_df[cleaned_dynamic_df['navigationalstatus'].isin([0, 3, 4, 8])]
cleaned_data_navstat = cleaned_data_navstat.drop("Unnamed: 0", axis=1)
cleaned_data_navstat

def navigation_codes():
    """
    3. Filter for navigation codes of 0, 3, 4 and 8 only.

    Input:

    Output:

    """

    return 0




### DATA CLEANING 4 - Above 5 Speed over Ground (SOG) ###
cleaned_data_navstat
final_dataset = cleaned_data_navstat[cleaned_data_navstat["speedoverground"] > 5.0].reset_index().drop('index', axis=1)
final_dataset.to_csv("/Users/apple/Desktop/transport/Shipping/datasets/final_dataset.csv")
final_dataset




def SOG_above_5():
    """
    4. Filter for vessel speed over grounds of greater than 5.

    Input:

    Output:

    """

    return 0




def data_cleaning():
    """
    Compilation function

    Input:

        xyz     from __main__.py

    Output:

        yzx     using functions above

    """


    return 0
