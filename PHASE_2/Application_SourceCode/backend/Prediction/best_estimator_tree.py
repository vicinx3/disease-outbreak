import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline

data = pd.read_csv('disease_data.csv').to_numpy()

# Shuffle data rows for independence
np.random.shuffle(data)

# Train test split: 80-20
X_train = np.zeros((6, int(0.8 * len(data))))
X_train = data[:int(0.8 * len(data)), :-1]
y_train = np.zeros((1, int(0.8 * len(data))))
y_train = data[:int(0.8 * len(data)), -1]

X_test = np.zeros((6, len(data) - int(0.8 * len(data))))
X_test = data[int(0.8 * len(data)):, :-1]
y_test = np.zeros((1, len(data) - int(0.8 * len(data))))
y_test = data[int(0.8 * len(data)):, -1]

pipeline = make_pipeline(
    MinMaxScaler(),
    DecisionTreeClassifier()
)

hyperparameters = {
    'decisiontreeclassifier__max_depth': list(range(1, 20))
    # 'decisiontreeclassifier__min_samples_leaf': list(range(1, 10))       
}


clf = GridSearchCV(pipeline, hyperparameters, cv=10)

# Train
clf.fit(X_train, y_train)

# Predict
y_pred = clf.predict(X_test)

print("Best parameters for Decision Tree:")
print(clf.best_params_)

print('Accuracy score:', accuracy_score(y_test, y_pred))
print('Precision score:', precision_score(y_test, y_pred, average=None, zero_division=0))
print('Recall score:', recall_score(y_test, y_pred, average=None, zero_division=0))

print(classification_report(y_test, y_pred))