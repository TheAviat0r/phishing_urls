from sklearn import tree
from sklearn.cross_validation import cross_val_score, cross_val_predict
from sklearn import metrics
from sklearn import model_selection
import numpy as np
import _pickle as pickle


def load_data():

    training_data = np.genfromtxt('scraper/scrapyres/_NEW.csv', delimiter=',', dtype=np.int32)
    training_data = training_data[1:, :]
    inputs = training_data[:,:-1]
    outputs = training_data[:, -1]

    return model_selection.train_test_split(inputs, outputs, test_size=0.33)

    # Return the four arrays
    #return training_inputs, training_outputs, testing_inputs, testing_outputs


if __name__ == '__main__':

    train_inputs, test_inputs, train_outputs, test_outputs = load_data()

    model = tree.DecisionTreeClassifier(max_depth = 3)
    model.fit(train_inputs, train_outputs)

    predictions = model.predict(test_inputs)

    accuracy = metrics.accuracy_score(test_outputs, predictions)
    print("Accuracy on testing data: " + str(accuracy))

    score = model_selection.cross_val_score(model, train_inputs, train_outputs, cv=6)
    print("Cross-validation Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))

    print("--------------------")

    with open("visual_tree.txt", "w") as f:
        f = tree.export_graphviz(model, out_file=f)

    filename = 'tree_model.bin'
    pickle.dump(model, open(filename, 'wb'))

    loaded_model = pickle.load(open(filename, 'rb'))

    test_data = np.genfromtxt('scraper/scrapyres/_TEST.csv', delimiter=',', dtype=np.int32)[1:, :]
    test_X = test_data[:, :-1]
    test_y = test_data[:, -1]

    predictions = model.predict(test_X)

    accuracy = metrics.accuracy_score(test_y, predictions)
    print("Final accuracy: ", accuracy)

    precision = metrics.precision_score(test_y, predictions)
    print("Precision:",precision)

    print("Recall:",metrics.recall_score(test_y, predictions))

    with open("visual_tree.txt", "w") as f:
        f = tree.export_graphviz(model, out_file=f)

    #y_true = np.array([0, 0, 1, 0])
    #y_scores = np.array([0, 0, 0, 1])
    #print average_precision_score(y_true, y_scores)
    """
    sum_accuracy = 0
    for i in range(100):
        model = tree.DecisionTreeClassifier(max_depth=1)
        model.fit(train_inputs, train_outputs)
        predictions = model.predict(test_X)
        accuracy = metrics.accuracy_score(test_y, predictions)
        sum_accuracy += accuracy
    print "Final accuracy: " + str(sum_accuracy/100)
    """
