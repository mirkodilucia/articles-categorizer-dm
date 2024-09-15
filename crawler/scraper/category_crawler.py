import json
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from crawler.scraper.cookie_manager import accept_cookie


def craw_categories(driver):
    categories = []

    sleep(2)

    # find element with classname class="menu-burger" and click it
    driver.find_element(By.CLASS_NAME, "menu-burger").click()

    # wait for element with class name "cat-item" to be present
    WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CLASS_NAME, "cat-item"))
    sleep(2)

    categories_tags = driver.find_elements(By.CLASS_NAME, "cat-item")

    # remove last element from list
    for category in categories_tags:

        # get li > a href and content
        element = category.find_element(By.TAG_NAME, "a")
        if element is None:
            break

        # check for stale element reference for element
        if element.get_attribute("href") is None:
            continue

        category_url = element.get_attribute("href")
        category_name = element.text

        print(f"Category: {category_name} - {category_url}")

        # crawl articles
        categories.append({
            "name": category_name,
            "url": category_url,
        })

    return categories


def start_crawler_categories(
        driver
):
    driver.get("https://www.open.online/")
    accept_cookie(driver)

    categories = craw_categories(driver)
    # save categories json to file
    with open("data/categories.json", "w") as f:
        json.dump(categories, f)

    # close browser
    driver.quit()
