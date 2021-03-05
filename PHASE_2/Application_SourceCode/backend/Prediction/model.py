# Run 5 different models on disease data and rank them

from os import path
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Check results.json exists
# if not path.exists('results.json'):
#    print("Run python3 data_api.py first")
#    exit()

# Check disease_data.csv exists
if not path.exists('disease_data.csv'):
    print("Run python3 preprocess.py first")
    exit()
    
data = pd.read_csv('disease_data.csv').to_numpy()

data = preprocessing.minmax_scale(data)

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

names = ["K Nearest Neighbours", "Bernoulli Naive Bayes", "Linear SVM",
"Decision Tree Classifier", "Random Forest Classifier"
]

classifiers = [
    KNeighborsClassifier(),
    BernoulliNB(),
    SGDClassifier(),
    DecisionTreeClassifier(),
    RandomForestClassifier()
]

model_scores = {}

for name, clf in zip(names, classifiers):
    print("--" + name)
    model = clf.fit(X_train, y_train)
    predicted_y = model.predict(X_test)

    acc = accuracy_score(y_test, predicted_y)
    prec = precision_score(y_test, predicted_y, average=None, zero_division=0)
    recall = recall_score(y_test, predicted_y, average=None, zero_division=0)

    print('Accuracy score:', acc)
    print('Precision score:', prec)
    print('Recall score:', recall)

    print(classification_report(y_test, predicted_y))
    model_scores[name] = acc

model_view = [(v,k) for k,v in model_scores.items()]
model_view.sort(reverse=True)
print("--Model accuracy based on pre-existing data--")
for v,k in model_view:
    print("%(model)s: %(acc).1f" %{'model': k, 'acc': v * 100.0})
print()