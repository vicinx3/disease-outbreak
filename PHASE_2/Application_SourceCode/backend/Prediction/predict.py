import json

with open('decision_tree_predictions.json', 'r') as dtfp:
    decision_tree = json.load(dtfp)

with open('random_forest_predictions.json', 'r') as rffp:
    random_forest = json.load(rffp)

predicted_outbreaks = {}

for country in decision_tree.keys():
    country_predictions = {}
    if country in random_forest.keys():
        for prediction in decision_tree[country].keys():
            if prediction in random_forest[country].keys():
                country_predictions[prediction] = decision_tree[country][prediction]
    
    predicted_outbreaks[country] = country_predictions

with open('predicted_outbreaks.json', 'w') as fp:
    json.dump(predicted_outbreaks, fp)
    
print("Common predictions written to predicted_outbreaks.json")