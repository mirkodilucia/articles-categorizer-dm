from classifier.preprocessor import stem_words, preprocess, clean_text, URL_MATCHER, HTML_TAG_MATCHER, \
    NON_DIGIT_MATCHER, process


def test_clean_text():
    article = ("Il cane correva velocemente. <b>Il cane correva velocemente.</b> a 30km/h. "
               "https://www.open.online/2021/07/01/ambiente/1")

    cleaned_test = process(article)

    print(cleaned_test)
    assert cleaned_test is not None


def test_stopwords():
    stopwords = stem_words("Il cane correva velocemente a 30km/h. Come un fulmine. Spettacolo!")
    stopwords = list(stopwords)

    assert stopwords is not None
    assert len(stopwords) > 0

    control_list = ["can", "corr", "veloc", "30km", "fulmin", "spettacol"]
    for word in stopwords:
        assert word in control_list


def test_stem_words():
    doc = "Il cane correva velocemente"
    stemmed_doc = stem_words(doc)

    # Make stemmed_doc a list
    stemmed_doc = list(stemmed_doc)

    print(stemmed_doc)
    assert stemmed_doc is not None
    assert len(stemmed_doc) > 0
    assert stemmed_doc[0] == "can" or stemmed_doc[0] == "corr" or stemmed_doc[0] == "veloc"


def test_clean_url():
    url = "Ciao https://www.google.com/"

    cleaned_url = clean_text(url, URL_MATCHER)
    print(cleaned_url)
    assert cleaned_url is not None
    assert len(cleaned_url) > 0
    assert cleaned_url == "Ciao "


def test_clean_html():
    html = "Ciao <b>mondo</b>!"

    cleaned_html = clean_text(html, HTML_TAG_MATCHER)
    print(cleaned_html)
    assert cleaned_html is not None
    assert len(cleaned_html) > 0
    assert cleaned_html == "Ciao mondo!"


def test_clean_non_digit():
    text = "Replace this pattern: ABC 123 with XYZ 789."

    cleaned_text = clean_text(text, NON_DIGIT_MATCHER)
    print(cleaned_text)
    assert cleaned_text is not None
    assert len(cleaned_text) > 0
    assert cleaned_text == "Replace this pattern ABC  with XYZ "
