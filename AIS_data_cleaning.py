"""
AIS_data_cleaning.py

Script to clean AIS data. Steps in the cleaning process include...

        1.1     Removing unnecessary fields.
        1.2     Generating database of unique mmsi and type values.
        1.3     Removing all non-containerships from dynamic database.
        1.4     Filtering for only navigation codes related to mission (0, 3, 4, 8).
        1.5     Filter out entries with Speed over Ground less than 5.


A full description of the research and references used can be found in README.md
"""


def remove_fields(static_dataset):
    """
    1.1 Removing unnecessary fields from the static dataset to reduce computation

    Input:

            static_dataset      static vessel dataset.
            dynamic_dataset     dynamic AIS vessel dataset.

    Output:

            static_data_rm      static vessel dataset with unused fields
                                removed.

    """

    static_data_rm = static_dataset.drop(['imonumber', 'callsign', 'shipname', 'eta', 'destination', 'mothershipmmsi', 't'], axis=1)

    return static_data_rm




def containerships_index(static_data_rm):
    """
    1.2 Generate dataframe of unique vessel mmsi numbers and their ship codes.

    Input:

            static_data_rm      static vessel dataset with unused fields
                                removed.

    Output:

            static_container    database of container vessel mmsi's and type
                                codes.

    """

    # establish empty dataframe
    columns = ['mmsi', 'shiptype']
    static_container = pd.DataFrame(columns=cols)


    # for loop to extract containerships only
    for ship_row in range(len(static_data_rm)):
        # use try to account for invalid ship type entries
        try:
            # if ship type is a containership (type 7)
            if str(int(static_data_rm["shiptype"][ship_row]))[0] == '7':

                static_container_temp = pd.DataFrame([[static_data_rm["sourcemmsi"][ship_row], int(static_data_rm["shiptype"][ship_row]])])
                static_container_temp.columns = columns
                static_container = pd.concat([static_container, static_container_temp], ignore_index=False)

        except ValueError:
            pass


    # reformat and clean as required
    static_container = static_container.T #??
    static_container = static_container.drop_duplicates(subset=0) #??
    static_container = static_container.drop([186295], axis=0) #??

    return static_container




def filter_for_containerships(dynamic_dataset, static_container):
    """
    1.3 Generate dataframe of unique vessel mmsi numbers and their ship codes.

    Input:

            dynamic_dataset     dynamic AIS vessel dataset.
            static_container    database of container vessel mmsi's and type
                                codes.

    Output:

            dynamic_container   dynamic AIS vessel dataset of containerhsip
                                movements only.

    """

    # convert to dictionary for processing speed
    containership_dictionary = {}
    for vessel_row in range(len(static_container)):
        containership_dictionary.update({int(static_container["mmsi"][vessel_row]): int(static_container["mmsi"][vessel_row])})


    # establish a list of rows in the dynamic dataset to be deleted
    dynamic_rows_to_delete = []

    # run through dynamic dataset
    for dynamic_row in range(len(dynamic_dataset)):
        if dynamic_dataset["sourcemmsi"][dynamic_row] not in containership_dictionary.keys():
            dynamic_rows_to_delete.append(dynamic_row)

    dynamic_container = dynamic_dataset.drop(dynamic_rows_to_delete, axis=0)

    return dynamic_container




def navigation_codes(dynamic_container):
    """
    1.4 Filter for navigation codes of 0, 3, 4 and 8 only.

    Input:

            dynamic_container   dynamic AIS vessel dataset of containerhsip
                                movements only.

    Output:

            dynamic_navstat     dynamic AIS vessel dataset of containership
                                movements with nav codes of 0, 3, 4, 8.

    """

    # select only entries with navigational status of 0, 3, 4, 8
    dynamic_navstat = dynamic_container[dynamic_container['navigationalstatus'].isin([0, 3, 4, 8])]

    # dropped automatically generated 'Unnamed: 0' field (could be improved)
    dynamic_navstat = dynamic_navstat.drop("Unnamed: 0", axis=1)

    return dynamic_navstat




def SOG_above_5(dynamic_navstat):
    """
    1.5 Filter for vessel speed over grounds of greater than 5.

    Input:

            dynamic_navstat     dynamic AIS vessel dataset of containership
                                movements with nav codes of 0, 3, 4, 8.

    Output:

            dynamic_cleaned     fully cleaned dynamic dataset.

    """

    # filter AIS data for vessel speeds above 5 only
    dynamic_cleaned = dynamic_navstat[dynamic_navstat["speedoverground"] > 5.0].reset_index().drop('index', axis=1)

    return dynamic_cleaned



def generate_sub_sample(dynamic_cleaned): # This should maybe be the first thing to do
    """
    1.6 Take a sample of N containerships.

    Input:

            dynamic_cleaned     fully cleaned dynamic dataset.

    Output:

            dynamic_sample      sample of dynamic dataset with 40 containerships.

    """

    # define sample size
    N = 40

    # get the chosen N containership mmsi numbers
    dynamic_mmsi_numbers = dynamic_cleaned["sourcemmsi"].unique()[:N]

    # sample the dataset for the N containerships
    dynamic_sample = dynamic_cleaned[dynamic_cleaned["sourcemmsi"].isin(dynamic_mmsi_numbers)].reset_index().drop("index", axis=1)

    # remove fields that won't be features into the model
    dynamic_sample = dynamic_sample.drop(["navigationalstatus", "rateofturn", "trueheading"], axis=1)

    # option to save
    # dynamic_sample.to_csv("datasets/dynamic_sample.csv")

    return dynamic_sample




def data_cleaning(static_dataset, dynamic_dataset):
    """
    Compilation function.

    Input:

            static_dataset      static vessel dataset.
            dynamic_dataset     dynamic AIS vessel dataset.

    Output:

            dynamic_cleaned     fully cleaned dynamic dataset.

    """

    # filter preparation
    static_data_rm = remove_fields(static_dataset)
    static_container = get_containerships_index(static_data_rm)

    # filtering
    dynamic_container = filter_for_containerships(dynamic_dataset, static_container)
    dynamic_navstat = filter_by_navigation_codes(dynamic_container)
    dynamic_cleaned = filter_by_SOG(dynamic_navstat)

    # generate sample dataset for model creation
    dynamic_sample = generate_sub_sample(dynamic_cleaned)

    # option to save cleaned dataset
    # dynamic_cleaned.to_csv("datasets/cleaned_dynamic.csv")

    return dynamic_sample
