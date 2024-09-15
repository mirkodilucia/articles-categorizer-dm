from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import ItalianStemmer


class Preprocess:

    @staticmethod
    def preprocess_text(doc):
        doc = re.sub(r'\d+', '', doc)
        analyzer = CountVectorizer().build_analyzer()
        return (ItalianStemmer().stem(w) for w in analyzer(doc) if w not in stopwords.words('english'))

    @staticmethod
    def decode_data(list):
        """"Decodes a list of texts extracted from files if necessary

        :param: list: list of str. List of text to decode
        :return: decodedData:list of str. List of text decoded
        """
        decoded_data = []
        for item in list:
            try:
                decoded_data.append(item.encode('latin1').decode('utf8'))
            except UnicodeDecodeError as e:
                decoded_data.append(item)

        return decoded_data
