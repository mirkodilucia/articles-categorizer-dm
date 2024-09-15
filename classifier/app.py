from sklearn.feature_extraction.text import TfidfVectorizer

from classifier.builder import build_classifiers

from classifier.evaluator import evaluate_models, cross_validate_models
from commons.logger import Logger
from crawler.cleanup import cleanup


def dataset_cleanup():
    cleanup("./classifier/data/articles")
    cleanup("./classifier/data/dataset")
    cleanup("./classifier/data/dataset/tests")
    cleanup("./classifier/data/dataset/train")


if __name__ == '__main__':
    # Read args from launch args and set up build_classifiers
    # dataset_cleanup()

    Logger.setup_logger()
    Logger.info("Starting classifier")

    # Build classifiers
    train_set, test_set, train_tfidf, test_tfidf = build_classifiers(force_train=False, force_rebuild=False)

    # Evaluate classifiers
    evaluate_models(test_tfidf, test_set)

    # Cross validate classifiers
    cross_validate_models(train_tfidf, train_set)

    # Evaluate models
    evaluate_models(test_tfidf, test_set)

    vectorizer = TfidfVectorizer()
    vectorizer.fit(train_set.data)