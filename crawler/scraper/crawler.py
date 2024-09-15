import json

from crawler.scraper.article_crawler import start_crawl_articles
from crawler.scraper.articles_crawler import start_crawl_articles_from_categories
from crawler.scraper.category_crawler import start_crawler_categories
from crawler.scraper.saver import save_articles_dataset
from crawler.scraper.selenium import instantiate_crawler


def group_articles_by_categories(articles_list):
    articles_by_category = {}
    for article in articles_list:
        if article["category"] not in articles_by_category:
            articles_by_category[article["category"]] = [article]
        else:
            articles_by_category[article["category"]].append(article)

    return articles_by_category


def start_crawler():
    # Crawl articles from categories
    driver = instantiate_crawler("https://www.open.online/c/x/", headless=False, noSandbox=False)
    categories = start_crawler_categories(driver)
    # driver.close()

    # Restart driver to avoid stale element reference error
    driver = instantiate_crawler("https://www.open.online/c/x/", headless=False, noSandbox=False)
    articles_list = start_crawl_articles_from_categories(driver, categories)
    driver.close()

    with open("data/articles.json", "r") as f:
        articles_list = json.load(f)

        # Fetch every article page
        driver = instantiate_crawler("https://www.open.online/c/x/", headless=False, noSandbox=False)
        articles_list = start_crawl_articles(driver, articles_list)

    # Group articles by category
    articles_by_category = group_articles_by_categories(articles_list)

    # Print how many articles we have per category
    for category in articles_by_category:
        print(f"Category: {category} - Articles: {len(articles_by_category[category])}")

    # Close driver
    driver.close()

    # Write articles to file
    save_articles_dataset(articles_by_category)
