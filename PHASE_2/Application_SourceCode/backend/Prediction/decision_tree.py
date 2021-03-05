# Predict next outbreak for each disease in each country in current year using Decision Tree Classifier

from datetime import date, timedelta
import json
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('disease_data.csv').to_numpy()

with open('countries_dict.json', 'r') as cfp:
    countries_dict = json.load(cfp)

with open('disease_dict.json', 'r') as dfp:
    disease_dict = json.load(dfp)

with open('last_outbreaks.json', 'r') as ofp:
    last_outbreaks = json.load(ofp)

#--------------------------------------------------------------------------------------------------#
# Functions

# Given a disease and a country, calculate average days between outbreaks (rounded)
def average_days_between(disease, country):
    days = []
    for row in data:
        if row[0] == disease and row[4] == country and row[-1] == 1:
            days.append(row[1])

    if len(days) == 0:
        return 0
    return round(np.average(days))

# Date of last outbreak for a given disease key
def last_outbreak_date(disease_key, country_key):
    if country_key not in last_outbreaks[disease_key].keys():
        return date(1, 1, 1)
    date_string = last_outbreaks[disease_key][country_key]
    date_y = int(date_string.split('-')[0])
    date_m = int(date_string.split('-')[1])
    date_d = int(date_string.split('-')[2])
    return date(date_y, date_m, date_d)

# Given a disease and a country, calculate average length of an outbreak (rounded)
def average_length(disease, country):
    lengths = []
    for row in data:
        if row[0] == disease and row[4] == country and row[-1] == 1:
            lengths.append(row[3])
    
    if len(lengths) == 0:
        return 0
    return round(np.average(lengths))

# Given a disease and a country, calculate average n_reports (rounded)
def average_reports(disease, country):
    reports = []
    for row in data:
        if row[0] == disease and row[4] == country:
            reports.append(row[-2])
    
    if len(reports) == 0:
        return 0
    return round(np.average(reports))

#--------------------------------------------------------------------------------------------------#
print("Predicting using Decision Tree model...")

# To prevent overlap for countries
seen_countries = []

# Paramaters in order: disease, days_since_last_outbreak, year, event_days, country, n_reports
country = 0

curr_date = date.today()

# Dictionary for disease and it's predicted outbreak date per country 
predicted_outbreaks = {}

# Shuffle training data
np.random.shuffle(data)

X_train = np.zeros((len(data), 7))
X_train = data[:, :-1]
y_train = np.zeros((len(data), 1))
y_train = data[:, -1]

# Fit and train model
clf = DecisionTreeClassifier(max_depth=20)
scaler = preprocessing.MinMaxScaler().fit(X_train)
X_train = scaler.transform(X_train)
model = clf.fit(X_train, y_train)

for country_key in countries_dict.keys():
    if countries_dict[country_key] in seen_countries or country_key == "other":
        continue
    
    country = countries_dict[country_key]
    disease = 0

    # Prevent overlap for diseases already done in countries
    seen_diseases = []

    # Dictionary for disease in particular country
    disease_outbreak = {}

    for disease_key in disease_dict.keys():
        if disease_dict[disease_key] in seen_diseases or disease_key == "other" or disease_key == "unknown":
            continue
        
        disease = disease_dict[disease_key]
        days_since_last_outbreak = 0
        prediction_length = 0
        prediction_n_reports = 0

        # Check if disease has had an outbreak
        if disease_key not in last_outbreaks.keys():
            continue

        # Calculate next date, only predict if in future
        prediction_date = last_outbreak_date(disease_key, country_key) + timedelta(average_days_between(disease, country))
        if prediction_date < curr_date:
            continue
        prediction_year = prediction_date.year
        days_since_last_outbreak = abs(prediction_date - last_outbreak_date(disease_key, country_key)).days

        # Average of event_days
        prediction_length = average_length(disease, country)

        # Average of n_reports
        prediction_n_reports = average_reports(disease, country)

        # Array for appending to end of data to min max
        X_test = np.array([
            [
                disease, days_since_last_outbreak, 
                prediction_year, prediction_length, 
                country, prediction_n_reports
            ]
        ])

        # Transform test
        X_test = scaler.transform(X_test)

        # Predict
        predicted_y = model.predict(X_test)

        # Dictionary for date and duration of a case
        outbreak_details = {}
        
        # If outbreak, add to dictionary
        if predicted_y[0] == 1:
            outbreak_details["date"] = prediction_date.strftime('%Y-%m-%d')
            outbreak_details["duration"] = int(prediction_length)
            disease_outbreak[disease_key] = outbreak_details
            
        seen_diseases.append(disease_dict[disease_key])
    
    if len(disease_outbreak) != 0:
        predicted_outbreaks[country_key] = disease_outbreak

    seen_countries.append(countries_dict[country_key])
        
with open('decision_tree_predictions.json', 'w') as fp:
    json.dump(predicted_outbreaks, fp)

print("Predicted results written to decision_tree_predictions.json")