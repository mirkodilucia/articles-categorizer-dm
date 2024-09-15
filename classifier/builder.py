import os
import shutil

import numpy as np
from sklearn.datasets import load_files
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import timeit

from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from classifier.preprocessor import preprocess, download_stopword
from commons.logger import Logger
from commons.serializer import Serializer

ARTICLES_PATH = "./classifier/data/articles"
DATASET_PATH = "./classifier/data/dataset"
CLASSIFIER_PATH = "./classifier/data/classifiers"

DATASET_DISTRIBUTION_RATIO = 0.8

categories = ['AMBIENTE',
              'ATTUALITÀ',
              'CULTURA & SPETTACOLO',
              'ECONOMIA & LAVORO',
              'MONDO', 'POLITICA',
              'SCIENZE', 'SPORT',
              'TECNOLOGIA']


def find_perfect_k(tfidf_train, tfidf_test, target_train, target_test):
    """"find the best parameter k for the K-NN classifier, testing the classifier on the training set and returning the k with the best accuracy

    :param tfidf_train: scipy.sparse.csr.csr_matrix. Tfidf of the training set.
    :param tfidf_test: scipy.sparse.csr.csr_matrix. Tfidf of the tests set.
    :param target_train: numpy.ndarray. Target array of the training set
    :param target_test: numpy.ndarray. Target array of the tests set
    :return: perfectK: int. The k with the higher accuracy
    """
    perfect_k = 1
    max_accuracy = 0
    for i in range(2, 100):
        classifier = KNeighborsClassifier(n_neighbors=i).fit(tfidf_train, target_train)

        predicted = classifier.predict(tfidf_test)  # prediction
        accuracy = np.mean(predicted == target_test)  # accuracy extraction
        print("With " + str(i) + " neighbors accuracy of " + str(accuracy))
        if accuracy > max_accuracy:
            max_accuracy = accuracy
            perfect_k = i

    print("Best k is " + str(perfect_k) + " with an accuracy of " + str(max_accuracy))
    return perfect_k


def load_articles():
    train_set = load_files(DATASET_PATH + "/train",
                           encoding="latin1",
                           description=None,
                           categories=categories,
                           load_content=True,
                           shuffle=False,
                           random_state=42)

    test_set = load_files(DATASET_PATH + "/tests",
                          encoding="latin1",
                          description=None,
                          categories=categories,
                          load_content=True,
                          shuffle=False,
                          random_state=42)

    Logger.info("Downloading stopword...")
    # download_stopword()

    Logger.info("Preprocessing data...")
    count_vect = CountVectorizer(analyzer=preprocess, min_df=2, max_df=100000000)
    train_counts = count_vect.fit_transform(train_set.data)

    Logger.info("Computing tfidf...")
    tfidf_transformer = TfidfTransformer()
    train_tfidf = tfidf_transformer.fit_transform(train_counts)

    Logger.info("Transforming tests set...")
    test_counts = count_vect.transform(test_set.data)
    test_tfidf = tfidf_transformer.transform(test_counts)

    return train_set, test_set, train_tfidf, test_tfidf


def save_dataset(train_set, test_set, train_tfidf, test_tfidf):
    # create dataset folder if not extist
    if not os.path.exists(DATASET_PATH):
        os.makedirs(DATASET_PATH)

    Serializer.save_object(train_set, DATASET_PATH + "/train_set")
    Serializer.save_object(test_set, DATASET_PATH + "/test_set")
    Serializer.save_object(train_tfidf, DATASET_PATH + "/train_tfidf")
    Serializer.save_object(test_tfidf, DATASET_PATH + "/test_tfidf")
    return


def load_dataset():
    train_set = Serializer.load_object(DATASET_PATH + "/train_set")
    test_set = Serializer.load_object(DATASET_PATH + "/test_set")
    train_tfidf = Serializer.load_object(DATASET_PATH + "/train_tfidf")
    test_tfidf = Serializer.load_object(DATASET_PATH + "/test_tfidf")

    return train_set, test_set, train_tfidf, test_tfidf


def prepare_dataset():
    # read all files in classifier/data/**/* and separe them in train and tests
    files = os.listdir(ARTICLES_PATH)

    # Ignore hidden files
    files = [f for f in files if not f.startswith('.')]

    # for each folder in the data folder, split the files in train and tests
    for folder in files:
        base_folder = ARTICLES_PATH + "/" + folder

        # Create new folder in /data/articles/train and /data/articles/tests with the same name of the folder in /data
        article_train_folder = DATASET_PATH + "/train/" + folder
        if not os.path.exists(article_train_folder):
            os.makedirs(article_train_folder)

        article_test_folder = DATASET_PATH + "/tests/" + folder
        if not os.path.exists(article_test_folder):
            os.makedirs(article_test_folder)

        # Copy the files in the new folders
        articles = os.listdir(base_folder)
        for file in articles:
            # Read file clean the text and copy it in the new folder
            with open(base_folder + "/" + file, "r") as f:
                text = f.read()
                text = preprocess(text)

            train_destination = article_train_folder + "/" + file
            test_destination = article_test_folder + "/" + file

            if np.random.rand() < DATASET_DISTRIBUTION_RATIO:
                with open(train_destination, "w") as f:
                    f.write(" ".join(text))
                    f.close()
            else:
                with open(test_destination, "w") as f:
                    f.write(" ".join(text))
                    f.close()

    return


def rebuild_dataset():
    prepare_dataset()
    train_set, test_set, train_tfidf, test_tfidf = load_articles()
    save_dataset(train_set, test_set, train_tfidf, test_tfidf)
    return train_set, test_set, train_tfidf, test_tfidf


def rebuild_dataset_if_needed():
    # Need to rebuild the dataset?
    if not os.path.exists(DATASET_PATH + "/test") and not os.path.exists(DATASET_PATH + "/train"):
        return rebuild_dataset()

    return load_dataset()


def train_classifiers(train_set, test_set, train_tfidf, test_tfidf):
    # create classifiers folder if not extist
    if not os.path.exists(CLASSIFIER_PATH):
        os.makedirs(CLASSIFIER_PATH)

    clf_mul = MultinomialNB().fit(train_tfidf, train_set.target)
    Serializer.save_object(clf_mul, CLASSIFIER_PATH + "/multinomialNB_classifier")

    clf_dt = DecisionTreeClassifier().fit(train_tfidf, train_set.target)
    Serializer.save_object(clf_dt, CLASSIFIER_PATH + "/decisionTree_classifier")

    clf_rf = RandomForestClassifier().fit(train_tfidf, train_set.target)
    Serializer.save_object(clf_rf, CLASSIFIER_PATH + "/randomForest_classifier")

    k = find_perfect_k(train_tfidf, test_tfidf, train_set.target, test_set.target)
    clf_kn = KNeighborsClassifier(n_neighbors=k).fit(train_tfidf, train_set.target)
    Serializer.save_object(clf_kn, CLASSIFIER_PATH + "/kNeighbors_classifier")

    return


def train_classifiers_if_needed(train_set, test_set, train_tfidf, test_tfidf):
    # Create classifiers folder if not extist
    if not os.path.exists(CLASSIFIER_PATH):
        os.makedirs(CLASSIFIER_PATH)

    # Need to train the classifiers?
    if not os.path.exists(CLASSIFIER_PATH + "/multinomialNB_classifier.pkl"):
        clf_mul = MultinomialNB().fit(train_tfidf, train_set.target)
        Serializer.save_object(clf_mul, CLASSIFIER_PATH + "/multinomialNB_classifier")

    if not os.path.exists(CLASSIFIER_PATH + "/decisionTree_classifier.pkl"):
        clf_dt = DecisionTreeClassifier().fit(train_tfidf, train_set.target)
        Serializer.save_object(clf_dt, CLASSIFIER_PATH + "/decisionTree_classifier")

    if not os.path.exists(CLASSIFIER_PATH + "/randomForest_classifier.pkl"):
        clf_rf = RandomForestClassifier().fit(train_tfidf, train_set.target)
        Serializer.save_object(clf_rf, CLASSIFIER_PATH + "/randomForest_classifier")

    if not os.path.exists(CLASSIFIER_PATH + "/kNeighbors_classifier.pkl"):
        k = find_perfect_k(train_tfidf, test_tfidf, train_set.target, test_set.target)
        clf_kn = KNeighborsClassifier(n_neighbors=k).fit(train_tfidf, train_set.target)
        Serializer.save_object(clf_kn, CLASSIFIER_PATH + "/kNeighbors_classifier")


def build_classifiers(
        force_rebuild=False,
        force_train=False
):
    start = timeit.default_timer()

    if force_rebuild:
        train_set, test_set, train_tfidf, test_tfidf = rebuild_dataset()
    else:
        train_set, test_set, train_tfidf, test_tfidf = rebuild_dataset_if_needed()

    if force_train:
        train_classifiers_if_needed(train_set, test_set, train_tfidf, test_tfidf)
    else:
        train_classifiers_if_needed(train_set, test_set, train_tfidf, test_tfidf)

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Program Executed in " + str(execution_time))

    return train_set, test_set, train_tfidf, test_tfidf
