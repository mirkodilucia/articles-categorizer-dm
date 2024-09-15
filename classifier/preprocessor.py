from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.stem.snowball import ItalianStemmer
from nltk.corpus import stopwords

URL_MATCHER = r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
HTML_TAG_MATCHER = r'<[^>]*>'
NON_DIGIT_MATCHER = r'[^a-zA-Z ]'
PUNCTUATION_MATCHER = r'[^\w\s]'
MULTIPLE_SPACE_MATCHER = r' +'
CONSECUTIVE_LETTERS_MATCHER = r'(.)\1{2,}'
CAMEL_CASE_MATCHER = r'(?<=[a-z])(?=[A-Z])'


def download_stopword():
    stopwords.words(stopwords.words('italian'))


# Remove first occurence of the word Content: in the text
def remove_content(text):
    return text.replace('Content:', '')


def preprocess(text):
    cleaned_text = process(remove_content(text))
    return stem_words(cleaned_text)


def stem_words(doc):
    analyzer = CountVectorizer().build_analyzer()
    return (ItalianStemmer().stem(w) for w in analyzer(doc) if w not in stopwords.words('italian'))


def process(doc):
    # Remove URLs
    doc = clean_text(doc, URL_MATCHER)

    # Remove HTML tags
    doc = clean_text(doc, HTML_TAG_MATCHER)

    # Remove non-alphanumeric characters
    doc = clean_text(doc, NON_DIGIT_MATCHER)

    # Remove punctuation
    doc = clean_text(doc, PUNCTUATION_MATCHER)

    # Remove multiple spaces
    doc = clean_text(doc, MULTIPLE_SPACE_MATCHER)

    # Remove consecutive letters
    doc = clean_text(doc, CONSECUTIVE_LETTERS_MATCHER)

    # Remove camel case
    doc = clean_text(doc, CAMEL_CASE_MATCHER)

    return doc.lower().strip()


def clean_text(text, pattern):
    return re.sub(pattern, ' ', text)
