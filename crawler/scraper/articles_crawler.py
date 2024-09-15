import json
from time import sleep

from selenium.webdriver.common.by import By

from crawler.scraper.cookie_manager import accept_cookie

MAX_PAGES = 45
MAX_ARTICLES_PER_CATEGORY = 360


def crawl_articles(driver, url, category):
    articles = []

    if url == "https://www.open.online/c/x/":
        return articles

    driver.get(url)

    # find all articles
    current_page = 0
    current_articles = 0

    while current_page < MAX_PAGES and current_articles < MAX_ARTICLES_PER_CATEGORY:
        articles_tags = driver.find_elements(By.CLASS_NAME, "news__inner")
        for article in articles_tags:
            if current_articles >= MAX_ARTICLES_PER_CATEGORY:
                break

            article_title_tag = article.find_element(By.CLASS_NAME, "news__title").find_element(By.TAG_NAME, "a")

            if article_title_tag is None:
                continue

            article_title = article_title_tag.text
            article_url = article_title_tag.get_attribute("href")

            print(f"Article: {category} - {article_title} - {article_url}")

            articles.append({
                "category": category,
                "title": article_title,
                "url": article_url,
                "date": "",
                "time": "",
                "author": ""
            })
            current_articles += 1

        current_page = next_page(driver, current_page)
        if current_page is None:
            break

    return articles


def next_page(driver, current_page):
    next_page_buttons = driver.find_elements(By.CLASS_NAME, "pagination-item")

    for i in range(len(next_page_buttons)):
        if next_page_buttons[i].text == str(current_page + 1):
            next_page_button = next_page_buttons[i]
            next_page_button.click()

            # wait until page is loaded
            driver.implicitly_wait(3)
            sleep(2)

            break

    return current_page + 1


def start_crawl_articles_from_categories(
        driver,
        categories
):
    accept_cookie(driver)

    # read from data/categories.json
    with open("data/categories.json", "r") as f:
        categories = json.load(f)

    articles = []

    i = 0
    for category in categories:
        # print("Fetching... ", i, category["url"])

        new_articles_list = crawl_articles(driver, category["url"], category["name"])

        # flatten list of articles
        articles += new_articles_list
        i += 1

    # save articles json to file
    with open("data/articles.json", "w") as f:
        json.dump(articles, f)

    # close browser
    driver.quit()

    return articles
