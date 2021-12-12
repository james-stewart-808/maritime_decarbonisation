"""
oc_data_cleaning.py

Script to clean oceanic data. Steps include...

        X.1     Get timestamp values corresponding to beginning and end of each
                month.
        X.2     Combine into array of timestamps.


A full description of the research and references used can be found in README.md
"""

def oc_data_cleaning(oc_oct, oc_nov, oc_dec, oc_jan, oc_feb, oc_mar):
    """
    Get timestamp values corresponding to beginning and end of each month.

    """

    # take min and max timestamps for monthly oceanic datasets
    ts_oct_min, ts_oct_max = min(oc_oct["ts"]), max(oc_oct["ts"]) # 1443654000 to 1446321600
    ts_nov_min, ts_nov_max = min(oc_nov["ts"]), max(oc_nov["ts"]) # 1446332400 to 1448913600
    ts_dec_min, ts_dec_max = min(oc_dec["ts"]), max(oc_dec["ts"]) # 1448924400 to 1451592000
    ts_jan_min, ts_jan_max = min(oc_jan["ts"]), max(oc_jan["ts"]) # 1446332400 to 1448913600
    ts_feb_min, ts_feb_max = min(oc_feb["ts"]), max(oc_feb["ts"]) # 1454281200 to 1456776000
    ts_mar_min, ts_mar_max = min(oc_mar["ts"]), max(oc_mar["ts"]) # 1456786800 to 1459454400

    # combine into timestamp object
    month_ts_array = np.array(ts_oct_min, ts_oct_max, ts_nov_min, ts_nov_max, ts_dec_min, ts_dec_max, ts_jan_min, ts_jan_max, ts_feb_min, ts_feb_max, ts_mar_min, ts_mar_max)

    return month_ts_array
