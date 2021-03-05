# SENG3011_code-onavirus
=========================================
Code-onavirus Outbreak Prediction Backend
=========================================
Designed and developed by:
* Kenvin Yu (z5207857)
* Evan Lee (z5207846)
* Eric Tan (z5205997)
* Victor Liu (z5207848)
* Ezra Eyaru (z5215204)

=========================================
Files and their functions
=========================================
.json files
* country_list.json:
    A list of all ISO Alpha-2 country codes.
* countries_dict.json:
    A dictionary assigning a separate numeric value to each country code.
* disease_list.json:
    A list of all known diseases appearing in the WHO articles so far.
* disease_dict.json:
    A dictionary assigning a separate numeric value to each unique disease.
* results.json:
    A list of json objects storing the fetched article data from WHO.
* last_outbreaks.json:
    A dictionary storing the date of the last outbreak of a disease in each country.
* decision_tree_predictions.json:
    A dictionary containing the results predicted by the decision tree model.
* random_forest_predictions.json:
    A dictionary containing the results predicted by the random forest model.
* predicted_outbreaks.json:
    A dictionary containing the final results used for the web app predictions table.
    Contains the common predictions of both decision tree and random forest models.

.py files
* convert.py:
    Creates dictionary of unique values for each unique country and disease in
    country_list.json and disease_list.json.
* data_api.py:
    Fetches WHO data from database and stores it in results.json.
* preprocess.py:
    Takes results.json and processes it to create last_outbreaks.json and disease_data.csv.
    Processes each article fetched to find the following parameters for model training:
        * disease: unique disease value from disease_dict.json.
        * days since last outbreak: the number of days since the last outbreak of a particular disease in a particular country.
        * year started: the year a disease occurred.
        * event_days: duration of a disease event.
        * country: unique country value from countries_dict.json.
        * n_reports: the number of locations in a particular country reporting a particular disease.
        * outbreak: whether a particular instance of a disease was classified as an outbreak by WHO.
* model.py:
    Applies several models to an 80/20 split of preprocessed data in disease_data.csv.
    Trains each model on the 80% of samples and predicts the classification of the remaining 20%.
    Calculates precision, and f1 scores for each model and ranks the models in order of accuracy.
    Currently, Decision Tree and Random Forest are the most accurate, both with a range of 87% to 90% accuracy.
* best_estimator_tree.py and best_estimator_forest.py:
    Performs GridSearchCV hyperparameter tuning on its model and prints best hyperparameters
    best_estimator_forest.py has manually binary search narrowed down to a list of 3 parameters since it is too time consuming.
* decision_tree.py:
    Calculates new values for each paramater (days since last outbreak, year started, event_days, n_reports)
    for each disease case in each country, using averages of values unique to each instance of each disease in each country. 
    Then transforms those values to fit the training set scaling and predicts whether the occurrence is an outbreak or not 
    using Sklearn's Decision Tree Classifier. Outputs all predicted outbreaks with disease, country, date and duration to 
    decision_tree_predictions.json.
* random_forest.py:
    Performs the same function as decision_tree.py, but by using Sklearn's Random Forest Classifier instead and writes
    the predicted outbreaks to random_forest_predictions.json.
* predict.py:
    Reads both decision_tree_predictions.json and random_forest_predictions.json and writes all common predictions to
    predicted_outbreaks.json.
* run.py:
    A script file created to generate predictions without needing to read through each file.
    It runs:
        * data_api.py if there is no results.json
        * preprocess.py
        * model.py
        * decision_tree.py
        * random_forest.py
        * predict.py
    in order.

.csv files
* disease_data.csv:
    Numerical data created by preprocess.py from the article data from WHO, 
    used for model training.