import json

from crawler.scraper.crawler import start_crawler, group_articles_by_categories
from commons.logger import Logger
from crawler.scraper.saver import save_articles_dataset

if __name__ == '__main__':
    Logger.setup_logger()
    Logger.info("Starting crawler")

    start_crawler()

    # with open("data/articles.json", "r") as f:
    #    articles_list = json.load(f)

        # Group articles by category
    #    articles_by_category = group_articles_by_categories(articles_list)

        # Create global.articles.json if not exist
    #    save_articles_dataset(articles_by_category)



