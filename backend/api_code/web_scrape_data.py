from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import json
import shutil
import os


def get_url_to_scrape(search_text):
    return "https://ndb.nal.usda.gov/ndb/search/list?&qt=&qlookup=" + search_text + "&ds=&manu="


def get_source_using_selenium(url):
    options_firefox = webdriver.FirefoxOptions()
    options_firefox.add_argument('--headless')
    options_firefox.add_argument('--proxy-type=http')
    options_firefox.add_argument('--load-images=false')
    options_firefox.add_argument('--ssl-protocol=any')
    options_firefox.add_argument('--ignore-ssl-errors=true')
    driver = webdriver.Firefox(executable_path='E:\selenium_webdriver\geckodriver-v0.23.0-win64\geckodriver.exe',
                               options=options_firefox)
    driver.get(url)
    return driver


def write_link_scrape_to_file(driver):
    body = driver.find_element_by_tag_name('body')
    # table = body.find_element_by_css_selector('.table')
    t_body = body.find_element_by_css_selector('.table > tbody:nth-child(2)')
    list_row = t_body.find_elements_by_tag_name("tr")
    for row in list_row:
        list_data = row.find_elements_by_tag_name("td")
        url = list_data[1].find_element_by_tag_name('a').get_attribute('href')
        with open(os.path.join(os.getcwd(), "link_scrape.txt"), 'a') as out_file:
            out_file.write(url+'\n')


def click_next_page(driver, num_click):
    body = driver.find_element_by_tag_name('body')
    next_button = body.find_element_by_class_name('nextLink')
    next_button.click()
    time.sleep(1)
    for i in range(num_click):
        write_link_scrape_to_file(driver)


def remove_duplicate_lines():
    lines_seen = set()  # holds lines already seen

    outfile = open(os.path.join(os.getcwd(), "link_scrape_without_duplicate.txt"), "a")
    for line in open(os.path.join(os.getcwd(), "link_scrape.txt"), "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()


if __name__ == "__main__":
    url = get_url_to_scrape("raw")
    driver = get_source_using_selenium(url)
    write_link_scrape_to_file(driver)
    '''
    After scrape the first page, call to scrape other pages
    '''
    click_next_page(driver, 3)
    driver.quit()
    '''
    After that remove duplicate lines
    '''
    remove_duplicate_lines()
