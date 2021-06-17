"""
__main__.py

The main executable file to used in the processing of all files related to the
maritime_decarbonisation repository.


Databases used in the study include...

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


### Function execution ###

def load_data():
    """
    Check terminal call usage and load dataset into pandas dataframe.

    No inputs.

    Outputs:

            df          pandas dataframe of stock price history.

    """

    if len(sys.argv) != 3:
        print("Usage: python3 exe.py nari_static.csv nari_dynamic.csv")
        sys.exit(1)

    else:
        static_filename = sys.argv[1]
        dynamic_filename = sys.argv[2]

    # Read dataset into pandas dataframe and print head of dataframe
    static_df = pd.read_csv(static_filename)
    dynamic_df = pd.read_csv(dynamic_filename)

    return static_df, dynamic_df



def data_cleaning():
    """
    Run cleaning processes found in data_cleaning.py

    Input:



    Output:


    """


    return 0



def data_merging():
    """
    Run merging found in data_merging.py

    Input:



    Output:


    """


    return 0



def ETR_scenarios():
    """
    Train the extra trees regressor and generate scenarios based on climatic
    forecasts (references in README.md). Code available in ETR_scenarios.py

    Input:



    Output:


    """


    return 0



if __name__ == '__main__':

    # print data and show that
    static_df, dynamic_df = load_data()


    # data cleaning step
    data_cleaning()


    # data data_merging
    data_merging()


    # ETR_scenarios
    ETR_scenarios()
