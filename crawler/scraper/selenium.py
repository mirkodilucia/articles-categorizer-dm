from selenium import webdriver


def instantiate_crawler(
        url,
        noSandbox=True,
        headless=True,
):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1920,1080')

    if noSandbox:
        chrome_options.add_argument('--no-sandbox')

    if headless:
        chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    return driver
