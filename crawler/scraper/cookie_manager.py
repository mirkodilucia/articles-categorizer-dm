
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def accept_cookie(driver):
    # wait for element to be present on the page
    # the element is inside an iframe with id _cpmt-iframe
    WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "_cpmt-iframe"))

    # switch to iframe
    driver.switch_to.frame(driver.find_element(By.ID, "_cpmt-iframe"))

    # wait for element to be present on the iframe
    WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "_cpmt-accept"))

    # accept cookies
    driver.find_element(By.ID, "_cpmt-accept").click()

    # switch back to main page
    driver.switch_to.default_content()

    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
