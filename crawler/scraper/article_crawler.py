import json
import os
from time import sleep

from selenium.webdriver.common.by import By
from crawler.scraper.cookie_manager import accept_cookie


def crawl_article(driver, url):
    driver.get(url)

    # wait until page is loaded
    driver.implicitly_wait(4)

    # find element with class name "news__content article"
    article_content = driver.find_element(By.CLASS_NAME, "news__content")

    # get all <p> from article_content
    article_content_p = article_content.find_elements(By.TAG_NAME, "p")

    article = ""
    # get text from all the elements inside the article_content
    for p in article_content_p:
        article += p.text

    return article


def crawl_articles_by_category(driver, articles_list, category, i):
    articles = []
    for article in reversed(articles_list[i:]):
        # skip if article already crawled
        # if os.path.exists(f"data/{article['category']}/{i}.txt"):
        #    i += 1
        #    continue

        print("Fetching... ", i, article["url"])

        new_articles_list = crawl_article(driver, article["url"])

        if category != article["category"]:
            category = article["category"]
            i = 1

        # flatten list of articles
        articles.append({
            "title": article["title"],
            "url": article["url"],
            "date": article["date"],
            "time": article["time"],
            "author": article["author"],
            "content": new_articles_list
        })

        # Save article in /data/category/[article_number].txt
        # create folder for each category
        category_folder = f"data/" + category
        # create the folder if it doesn't exist
        try:
            os.makedirs(category_folder, exist_ok=True)
        except FileExistsError:
            pass

        # create file for each article
        with open(f"data/{category}/{i}.txt", "w") as f:
            f.write(f"Content: {new_articles_list}\n")

        i += 1

    # save articles json to file
    with open("data/global.articles.json", "w") as f:
        json.dump(articles, f)

    return articles


def start_crawl_articles(driver, articles_list):
    accept_cookie(driver)

    i = 1
    category = ""
    articles = []

    # Separate article by category using { category: [articles] }
    articles_by_category = {}
    for article in articles_list:
        if article["category"] not in articles_by_category:
            articles_by_category[article["category"]] = [article]
        articles_by_category[article["category"]].append(article)

    # Print dataset size
    for category, articles_list in articles_by_category.items():
        print(f"Category {category} has {len(articles_list)} articles")

    # For each articles_by_category count crawled articles saved in data/{category} and start crawling from the last one
    for category, articles_list in articles_by_category.items():

        # Create folder for each category
        if not os.path.exists(f"data/{category}"):
            os.makedirs(f"data/{category}", exist_ok=True)

        # Count articles already crawled
        i = len(os.listdir(f"data/{category}"))

        if i >= 360:
            print(f"Category {category} already crawled")
            continue

        print(f"Starting crawling articles from category {category} from article {i}")
        articles = crawl_articles_by_category(driver, articles_list, category, i)

        i = 1
    driver.quit()
