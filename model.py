###############################
### DECISION TREE REGRESSOR ###
###############################
# associated literature
# L. Breiman, J. Friedman, R. Olshen, and C. Stone, “Classification and Regression Trees”, Wadsworth, Belmont, CA, 1984.
# T. Hastie, R. Tibshirani and J. Friedman. “Elements of Statistical Learning”, Springer, 2009.
# L. Breiman, and A. Cutler, “Random Forests”, https://www.stat.berkeley.edu/~breiman/RandomForests/cc_home.htm


# import machine learning libraries
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score


# load in sampled dynamic dataset
full_dynamic_set = pd.read_csv("datasets/full_dynamic_set.csv")


# explore range of SOGs
SOG_plot = final_mmsi_short_clean["speedoverground"].values
np.average(SOG_plot)
max(SOG_plot)


# historgram
n, bins, patches = plt.hist(x=SOG_plot, bins='auto', color='#0504aa', alpha=1.0, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Speed over Ground')
plt.ylabel('Counts')
maxfreq = n.max()
plt.savefig("Shipping/SOG_histogram.png")




### MODEL TRAINING ###
# get training and testing datasets using 80:20 ratio
training_df, testing_df = train_test_split(final_mmsi_short_clean, test_size=0.2, train_size=0.8, random_state=1)


# split training and testing sets into independent and dependent variables
training_df_x = training_df.drop(["speedoverground"], axis=1)
training_df_y = training_df["speedoverground"]

testing_df_x = testing_df.drop(["speedoverground"], axis=1)
testing_df_y = testing_df["speedoverground"]


# training the decision tree regressor (DTR)
DTR = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR.fit(training_df_x, training_df_y)


# explore the DTR just built
DTR.get_depth()
DTR.get_n_leaves()


# Baseline predicition performance
baseline_predictions = DTR.predict(x_testing)
DTR.score(baseline_predictions, y_testing)




### FORECASTING & SCENARIOS ###
# Scenario 2030
scenario_2030 = test.drop(["speedoverground"], axis=1)
wave_height_2030 = x_testing["ocean_hs"] + 0.035
wind_speed_2030 = x_testing["weather_Ff"] + 0.28
air_temp_2030 = x_testing["weather_T"] + 0.364

scenario_2030["ocean_hs"] = wave_height_2030
scenario_2030["weather_Ff"] = wind_speed_2030
scenario_2030["weather_T"] = air_temp_2030
scenario_2030_predictions = DTR.predict(scenario_2030)


# Scenario 2050
scenario_2050 = test.drop(["speedoverground"], axis=1)
wave_height_2050 = x_testing["ocean_hs"] + 0.085
wind_speed_2050 = x_testing["weather_Ff"] + 0.68
air_temp_2050 = x_testing["weather_T"] + 0.884

scenario_2050["ocean_hs"] = wave_height_2050
scenario_2050["weather_Ff"] = wind_speed_2050
scenario_2050["weather_T"] = air_temp_2050
scenario_2050_predictions = DTR.predict(scenario_2050)


# Comparison of Scenarios
np.average(baseline_predictions)
np.average(scenario_2030_predictions)
np.average(scenario_2050_predictions)

# change in SOG to 2030 & 2050
(np.average(baseline_predictions) - np.average(scenario_2030_predictions)) / np.average(baseline_predictions)
(np.average(baseline_predictions) - np.average(scenario_2050_predictions)) / np.average(baseline_predictions)

# CO2 third-power relation
((np.average(baseline_predictions) - np.average(scenario_2030_predictions)) / np.average(baseline_predictions)) ** (3)
((np.average(baseline_predictions) - np.average(scenario_2050_predictions)) / np.average(baseline_predictions)) ** (3)




### Comparison of R2 coefficients ###
# COG R2
x_train_COG = np.array(train["courseoverground"]).reshape(-1, 1)
x_test_COG = np.array(test["courseoverground"]).reshape(-1, 1)

DTR_COG = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_COG.fit(x_train_COG, y_training)

y_test_COG = DTR_COG.predict(x_test_COG).reshape(-1, 1)
r2_score(y_testing, y_test_COG)



# Volume
x_train_vol = np.array(train["volume"]).reshape(-1, 1)
x_test_vol = np.array(test["volume"]).reshape(-1, 1)

DTR_vol = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_vol.fit(x_train_vol, y_training)

y_test_vol = DTR_vol.predict(x_test_vol).reshape(-1, 1)
r2_score(y_testing, y_test_vol)



# draught
x_train_dra = np.array(train["draught"]).reshape(-1, 1)
x_test_dra = np.array(test["draught"]).reshape(-1, 1)

DTR_dra = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_dra.fit(x_train_dra, y_training)

y_test_dra = DTR_dra.predict(x_test_dra).reshape(-1, 1)
r2_score(y_testing, y_test_dra)



# ocean_hs
x_train_hs = np.array(train["ocean_hs"]).reshape(-1, 1)
x_test_hs = np.array(test["ocean_hs"]).reshape(-1, 1)

DTR_hs = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_hs.fit(x_train_hs, y_training)

y_test_hs = DTR_hs.predict(x_test_hs).reshape(-1, 1)
r2_score(y_testing, y_test_hs)



# ocean_dir
x_train_ocean_dir = np.array(train["ocean_dir"]).reshape(-1, 1)
x_test_ocean_dir = np.array(test["ocean_dir"]).reshape(-1, 1)

DTR_ocean_dir = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_ocean_dir.fit(x_train_ocean_dir, y_training)

y_test_ocean_dir = DTR_ocean_dir.predict(x_test_ocean_dir).reshape(-1, 1)
r2_score(y_testing, y_test_ocean_dir)



# ocean_lm
x_train_lm = np.array(train["ocean_lm"]).reshape(-1, 1)
x_test_lm = np.array(test["ocean_lm"]).reshape(-1, 1)

DTR_lm = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_lm.fit(x_train_lm, y_training)

y_test_lm = DTR_lm.predict(x_test_lm).reshape(-1, 1)
r2_score(y_testing, y_test_lm)



# weather_wind_ID
x_train_wind_id = np.array(train["weather_wind_ID"]).reshape(-1, 1)
x_test_wind_id = np.array(test["weather_wind_ID"]).reshape(-1, 1)

DTR_wind_id = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_wind_id.fit(x_train_wind_id, y_training)

y_test_wind_id = DTR_wind_id.predict(x_test_wind_id).reshape(-1, 1)
r2_score(y_testing, y_test_wind_id)



# weather_Ff
x_train_Ff = np.array(train["weather_Ff"]).reshape(-1, 1)
x_test_Ff = np.array(test["weather_Ff"]).reshape(-1, 1)

DTR_Ff = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_Ff.fit(x_train_Ff, y_training)

y_test_Ff = DTR_Ff.predict(x_test_Ff).reshape(-1, 1)
r2_score(y_testing, y_test_Ff)



# weather_P
x_train_P = np.array(train["weather_P"]).reshape(-1, 1)
x_test_P = np.array(test["weather_P"]).reshape(-1, 1)

DTR_P = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_P.fit(x_train_P, y_training)

y_test_P = DTR_P.predict(x_test_P).reshape(-1, 1)
r2_score(y_testing, y_test_P)



# weather_T
x_train_T = np.array(train["weather_T"]).reshape(-1, 1)
x_test_T = np.array(test["weather_T"]).reshape(-1, 1)

DTR_T = DecisionTreeRegressor(random_state=0, max_depth=None, min_samples_split=4, min_samples_leaf=3)
DTR_T.fit(x_train_T, y_training)

y_test_T = DTR_T.predict(x_test_T).reshape(-1, 1)
r2_score(y_testing, y_test_T)



# R2 visualisation
r2s = [0.6104, 0.5006, 0.4588, 0.3698, 0.3537, 0.2281, 0.0925, 0.0719, 0.0429, 0.0238]
features = ["Wave \nHeight", "Wave \nDirection", "Course over \nGround", "Wave \nPeriod", "Air \nPressure", "Temperature", "Wind\nDirection", "Wind\nSpeed", "Tonnage", "Draught"]
bottoms = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

plt.bar(features, r2s, align='center')
plt.xlabel('Feature')
plt.ylabel('Determination Coefficient')
plt.xticks(fontsize=8, rotation=90)
plt.grid(axis='y', alpha=0.75)
plt.savefig("Shipping/DoC Bar.png")

n, bins, patches = plt.hist(x=SOG_plot, bins='auto', color='#0504aa', alpha=1.0, rwidth=0.85)
maxfreq = n.max()
plt.savefig("Shipping/SOG_histogram.png")
