
# Web Scraper and Machine Learning Classifiers for https://open.online News Data

This project consists of two main modules:

- **Crawler**: A web scraper for a news website.
- **Classifiers**: An application for evaluating four machine learning classifiers: k-Nearest Neighbors (kNN), Decision Tree, Random Forest, and Naive Bayes.

## Project Structure

The main structure of the project is as follows:

```
/project-root
│
├── /crawler
│   └── app.py             # Entry point for the web scraper
│
├── /classifiers
│   └── app.py             # Entry point for the classifier evaluation
│
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Crawler Module

![Alt Text](docs/demo.gif)

To run the web scraper:

```bash
python crawler/app.py
```

This script will scrape the specified news website and store the data in a format that can be further processed or used for machine learning tasks.

### Classifiers Module

To run the classifier evaluation:

```bash
python classifiers/app.py
```

This script will load a dataset (ensure you have the data prepared) and evaluate the performance of the four classifiers: kNN, Decision Tree, Random Forest, and Naive Bayes. The results will be displayed on the terminal.

## Dependencies

The project uses Python and the following main libraries (listed in `requirements.txt`):

- `scikit-learn` for machine learning classifiers
- `beautifulsoup4` and `requests` for web scraping

You can install all the dependencies using the `requirements.txt` file as described in the Installation section.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
