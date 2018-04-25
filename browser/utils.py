import os
import re
from random import choices, randint

from django.test import TestCase, LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriverWait(self.browser, 60).until(EC.title_contains("Welcome"))

def fast_multiselect(driver, element_id, labels=[]):
    """https://sqa.stackexchange.com/questions/1355/what-is-
    the-correct-way-to-select-an-option-using-seleniums-python-webdriver"""
    select = Select(driver.find_element_by_id(element_id))

    if labels == []:
        texts = [opt.text for opt in select.options]
        labels = choices(texts, k=randint(1, len(texts)//2))

    for label in labels:
        select.select_by_visible_text(label)

def get_web_element_attribute_names(web_element):
    """Get all attribute names of a web element

    Possible to define this function in a custom
    webElement class that inherits from the original
    """
    # get element html
    html = web_element.get_attribute("outerHTML")
    # find all attributes with regex
    pattern = """([a-z]+-?[a-z]+_?)='?"?"""
    return re.findall(pattern, html)

def launch_search():
    """Launch a search engine"""

    os.system('cls')
    try:
        driver = webdriver.Firefox()
    except WebDriverException:
        driver = webdriver.Chrome()

    engine = input("Choose your search engine of choice\n 1. Google.\n2. DuckDuckGo.")

    if engine == "1":
        _ = driver.get("http://www.google.com")
    elif engine == "2":
        _ = driver.get("http://www.duckduckgo.com")
    
    try:
        driver.find_element_by_link_text("English").click()
    except NoSuchElementException:
        print("Page is likely already in English. Continuing")

    search_element = driver.find_element_by_name("q")

    print("The following attribute names were found for the search box/n")
    print(get_web_element_attribute_names(search_element))

    search_element.send_keys("selenium browser automation")
    search_element.submit()
    WebDriverWait(driver, 10).until(EC.title_contains("selenium browser automation"))

    print("Browser title is ---- ", driver.title)
    driver.quit()

if __name__ == "__main__":
    launch_search()
    