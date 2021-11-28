"""
feature_generation.py

Function used to derive draught and volume features for regressor model.


A full description of the research and references used can be found in README.md
"""


def feature_generation(dynamic_sample):
    """
    2.1 Derive features for volume (where area used as a proxy) and draught.

    Input:

            dynamic_sample      sample of dynamic dataset with 40
                                containerships.

    Output:

            dynamic_sample_full dynamic dataset sample with addtion of volume
                                and draught as features.

    """

    # take bow, stern, starboard and port values to derive volume feature (area)
    to_bow = dynamic_sample["tobow"].values
    to_stern = dynamic_sample["tostern"].values
    to_starboard = dynamic_sample["tostarboard"].values
    to_port = dynamic_sample["toport"].values

    # get volume (area) and draught features
    areas = (to_bow + to_stern) * (to_starboard + to_port)
    draught = dynamic_sample["draught"].values

    # add volume (area) and draught
    dynamic_sample_full = dynamic_sample
    dynamic_sample_full["volume"] = areas
    dynamic_sample_full["draught"] = draught

    # remove automatically generated fields
    dynamic_sample_full.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1)

    # option to save sampled dynamic dataset
    # dynamic_sample_full.to_csv("datasets/dynamic_sample_full.csv")

    return dynamic_sample_full
