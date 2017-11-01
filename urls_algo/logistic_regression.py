from sklearn.linear_model import LogisticRegression as lr
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.cross_validation import cross_val_score, cross_val_predict
from sklearn import metrics
from sklearn import model_selection
from decision_tree import load_data


train_inputs, test_inputs, train_outputs, test_outputs = load_data()

model = lr()

model.fit(train_inputs, train_outputs)
predictions = model.predict(test_inputs)

accuracy = metrics.accuracy_score(test_outputs, predictions)
print "Accuracy on testing data: " + str(accuracy)

score = model_selection.cross_val_score(model, train_inputs, train_outputs, cv=6)
print("Cross-validation Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))

print "--------------------"

test_data = np.genfromtxt('datasets/new_phish.csv', delimiter=',', dtype=np.int32)[1:, :]
test_X = test_data[:, :-1]
test_y = test_data[:, -1]

predictions = model.predict(test_X)
accuracy = metrics.accuracy_score(test_y, predictions)
print "Final accuracy: ", accuracy
