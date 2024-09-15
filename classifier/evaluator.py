import os

from sklearn import metrics
import numpy as np
from sklearn.model_selection import KFold, cross_val_score

from commons.serializer import Serializer

RESULTS_PATH = "./classifier/data/results"
ARTICLES_PATH = "./classifier/data/articles"
DATASET_PATH = "./classifier/data/dataset"
CLASSIFIER_PATH = "./classifier/data/classifiers"


class Evaluator:

    @staticmethod
    def evaluate(classifier, tfidf_test, test_set, file_name):
        predicted = classifier.predict(tfidf_test)  # prediction
        # Extracting statistics and metrics
        accuracy = np.mean(predicted == test_set.target)  # accuracy extraction
        file_text = "Accuracy on tests set:\n"
        file_text += str(accuracy)
        file_text += "\nMetrics per class on tests set:\n"

        file_text += metrics.classification_report(test_set.target,
                                                   predicted,
                                                   target_names=test_set.target_names)
        file_text += "\nConfusion matrix:\n"
        labels = ['amb ', 'att ', 'c&s ', 'eco ', 'mon ', 'pol ', 'sci ', 'spo ', 'tec ']
        file_text += "      amb  att  c&s  eco  mon  pol  sci  spo  tec \n"
        confusion_matrix = metrics.confusion_matrix(test_set.target, predicted)

        i = 0
        for row in confusion_matrix:
            file_text += labels[i] + " " + str(row) + '\n'
            i += 1
        print(file_text)

        f = open("./data/evaluations/" + file_name + ".txt", "w")
        f.write(file_text)
        f.close()

        print("End of tests " + file_text)

    @staticmethod
    def cross_validate(classifier, tfidf_train, train_set, file_name):
        # Perform k-fold cross-validation

        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        cv_scores = cross_val_score(classifier, tfidf_train, train_set, cv=kf)

        # Print cross-validation scores to file
        file_text = "Cross-Validation Scores:\n"
        file_text += str(cv_scores)
        file_text += "\nMean Accuracy:\n"
        file_text += str(cv_scores.mean())

        f = open(RESULTS_PATH + "/" + file_name + ".txt", "w")
        f.write(file_text)
        f.close()


def evaluate_models(tfidf_test, test_set):
    # Create evaluation folder if not exists
    if not os.path.exists("./data/evaluations"):
        os.makedirs("./data/evaluations")

    clf_mul = Serializer.load_object(CLASSIFIER_PATH + "/multinomialNB_classifier")
    Evaluator.evaluate(clf_mul, tfidf_test, test_set, "multinomialNB_classifier_result")

    clf_dt = Serializer.load_object(CLASSIFIER_PATH + "/decisionTree_classifier")
    Evaluator.evaluate(clf_dt, tfidf_test, test_set, "decisionTree_classifier_result")

    clf_rf = Serializer.load_object(CLASSIFIER_PATH + "/randomForest_classifier")
    Evaluator.evaluate(clf_rf, tfidf_test, test_set, "randomForest_classifier_result")

    clf_knn = Serializer.load_object(CLASSIFIER_PATH + "/kNeighbors_classifier")
    Evaluator.evaluate(clf_knn, tfidf_test, test_set, "knn_classifier_result")


def cross_validate_models(tfidf_train, train_set):
    # Perform k-fold cross-validation
    kf = KFold(n_splits=10, shuffle=True, random_state=42)

    # Cross-validation for decision tree
    clf_dt = Serializer.load_object(CLASSIFIER_PATH + "/decisionTree_classifier")
    cv_scores_dt = cross_val_score(clf_dt, tfidf_train, train_set.target, cv=kf)
    print(f'Decision Tree Cross-Validation Scores: {cv_scores_dt}')
    print(f'Decision Tree Cross-Validation Mean Accuracy: {cv_scores_dt.mean()}')

    # Cross-validation for random forest
    clf_rf = Serializer.load_object(CLASSIFIER_PATH + "/randomForest_classifier")
    cv_scores_rf = cross_val_score(clf_rf, tfidf_train, train_set.target, cv=kf)
    print(f'Random Forest Cross-Validation Scores: {cv_scores_rf}')
    print(f'Random Forest Cross-Validation Mean Accuracy: {cv_scores_rf.mean()}')

    # Cross-validation for kNN
    clf_knn = Serializer.load_object(CLASSIFIER_PATH + "/kNeighbors_classifier")
    cv_scores_knn = cross_val_score(clf_knn, tfidf_train, train_set.target, cv=kf)
    print(f'kNN Cross-Validation Scores: {cv_scores_knn}')
    print(f'kNN Cross-Validation Mean Accuracy: {cv_scores_knn.mean()}')

    # Cross-validation for Naive Bayes
    clf_mul = Serializer.load_object(CLASSIFIER_PATH + "/multinomialNB_classifier")
    cv_scores_nb = cross_val_score(clf_mul, tfidf_train, train_set.target, cv=kf)
    print(f'Naive Bayes Cross-Validation Scores: {cv_scores_nb}')
    print(f'Naive Bayes Cross-Validation Mean Accuracy: {cv_scores_nb.mean()}')
